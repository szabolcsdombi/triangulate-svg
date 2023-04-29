import re
import struct

N = 16


class Draw:
    def __init__(self):
        self.curves = []
        self.points = []

    def point(self, x, y):
        if len(self.points):
            tx, ty = self.points[-1]
            if (tx - x) * (tx - x) + (ty - y) * (ty - y) < 1e-8:
                return
        self.points.append(x, y)


def build_curves(commands):
    draw = Draw()
    for args in commands:
        cx, cy = draw.cursor
        match args[0]:
            case 'M':
                draw.cursor = args[1], args[2]
            case 'L':
                draw.point(cx, cy)
                draw.point(args[1], args[2])
            case 'C':
                a = cx, cy
                b = args[1], args[2]
                c = args[3], args[4]
                d = args[5], args[6]
                for i in range(N):
                    draw.point(bez4(a[0], b[0], c[0], d[0], i / (N - 1)), bez4(a[1], b[1], c[1], d[1], i / (N - 1)))
            case 'Q':
                a = cx, cy
                b = args[1], args[2]
                c = args[3], args[4]
                for i in range(N):
                    draw.point(bez3(a[0], b[0], c[0], i / (N - 1)), bez3(a[1], b[1], c[1], i / (N - 1)))
            case 'Z':
                sx, sy = draw.points[0]
                draw.point(cx, cy)
                draw.point(sx, sy)
                draw.points.pop()
                draw.curves.append(draw.points)
                draw.points = []
    return draw.curves


def join_curves(curves):
    curves = curves.copy()
    for i in range(len(curves)):
        if winding(curves[i]) < 0.0:
            curves[i] = curves[i][::-1]

    curves[0] = curves[0][::-1]

    while len(curves) > 1:
        best = 1e9, 0, 0, 0
        for i in range(len(curves[0])):
            x1, y1 = curves[0][i]
            for c in range(1, len(curves)):
                for j in range(len(curves[c])):
                    x2, y2 = curves[c][j]
                    dist = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
                    if dist < best[0]:
                        best = dist, i, c, j

        i, c, j = best[1:]
        curves[0] = curves[0][:i] + [curves[0][i]] + curves[c][j:] + curves[c][:j] + [curves[c][j]] + curves[0][i:]
        curves = curves[:c] + curves[c + 1:]

    return curves[0]


def flip_crossings(points):
    while intersecting := crossing(points):
        a, b, i, j, t = intersecting
        points = points[:a + 1] + [t] + points[b:i + 1][::-1] + [t] + points[j:]
        if winding(points) > 0.0:
            points = points[::-1]
    return points


def intersect(a, b, c, d):
    eps = 1e-6
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d
    q = (bx - ax) * (cy - dy) - (by - ay) * (cx - dx)
    if q == 0.0:
        return False
    n = ((cx - ax) * (cy - dy) - (cy - ay) * (cx - dx)) / q
    m = ((bx - ax) * (cy - ay) - (by - ay) * (cx - ax)) / q
    if eps < n < 1.0 - eps and eps < m < 1.0 - eps:
        return ax + (bx - ax) * n, ay + (by - ay) * n


def area(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    return (bx - ax) * (cy - by) - (by - ay) * (cx - bx)


def winding(curve):
    s = 0.0
    x1, y1 = curve[-1]
    for x2, y2 in curve:
        s += (x2 - x1) * (y2 + y1)
        x1, y1 = x2, y2
    return s


def crossing(points):
    a = 0
    while a < len(points):
        b = (a + 1) % len(points)
        i = b + 1
        while i < len(points):
            j = (i + 1) % len(points)
            if a != i and b != i and a != j and b != j:
                if t := intersect(points[a], points[b], points[i], points[j]):
                    return a, b, i, j, t
            i += 1
        a += 1


def cut(points, a, b):
    outside = True
    for i in range(len(points)):
        j = (i + 1) % len(points)
        if area(points[a], points[b], points[i]) > 0.0:
            outside = False
        if a == i or b == i or a == j or b == j:
            continue
        if intersect(points[a], points[b], points[i], points[j]):
            return False
    return not outside


def bez3(a, b, c, t):
    e = a + (b - a) * t
    f = b + (c - b) * t
    g = e + (f - e) * t
    return g


def bez4(a, b, c, d, t):
    e = a + (b - a) * t
    f = b + (c - b) * t
    g = c + (d - c) * t
    h = e + (f - e) * t
    i = f + (g - f) * t
    j = h + (i - h) * t
    return j


def parse(data):
    nargs = dict(zip('MLCQZ', [3, 3, 7, 5, 1]))
    commands = []
    for token in re.findall(r'([MLCQZ]|(?:-?\d+(?:\.\d+)?|-?\.\d+))', data):
        if token in 'MLCQZ':
            commands.append([token])
        else:
            if len(commands[-1]) == nargs[commands[-1][0]]:
                commands.append([commands[-1][0]])
            commands[-1].append(float(token))
    return commands


def triangulate(points):
    points = points.copy()
    triangles = []

    a = 0
    while len(points) > 3:
        b = (a + 1) % len(points)
        c = (b + 1) % len(points)
        s = area(points[a], points[b], points[c])
        if s > 0.0 and cut(points, a, c):
            triangles.append((points[a], points[b], points[c]))
            points = points[:b] + points[b + 1:]
        elif s == 0.0:
            points = points[:b] + points[b + 1:]
        a = (a + 1) % len(points)

    triangles.append((points[0], points[1], points[2]))
    return triangles


def convert(svg):
    res = bytearray()
    tags = re.findall(r'<path fill="([^"]+)" d="([^"]+)"/>', svg)
    for fill, data in tags:
        r, g, b = int(fill[1:3], 16) / 255.0, int(fill[3:5], 16) / 255.0, int(fill[5:7], 16) / 255.0
        triangles = triangulate(flip_crossings(join_curves(build_curves(parse(data)))))
        for triangle in triangles:
            for x, y in triangle:
                res += struct.pack('2f3f', x, y, r, g, b)
    return res


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('-o', '--output', required=True)

    args = parser.parse_args()
    open(args.output, 'wb').write(convert(open(args.input).read()))
