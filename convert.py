import decimal
import re

COLORS = {'aliceblue': '#f0f8ff', 'antiquewhite': '#faebd7', 'aqua': '#00ffff', 'aquamarine': '#7fffd4', 'azure': '#f0ffff', 'beige': '#f5f5dc', 'bisque': '#ffe4c4', 'black': '#000000', 'blanchedalmond': '#ffebcd', 'blue': '#0000ff', 'blueviolet': '#8a2be2', 'brown': '#a52a2a', 'burlywood': '#deb887', 'cadetblue': '#5f9ea0', 'chartreuse': '#7fff00', 'chocolate': '#d2691e', 'coral': '#ff7f50', 'cornflowerblue': '#6495ed', 'cornsilk': '#fff8dc', 'crimson': '#dc143c', 'cyan': '#00ffff', 'darkblue': '#00008b', 'darkcyan': '#008b8b', 'darkgoldenrod': '#b8860b', 'darkgray': '#a9a9a9', 'darkgreen': '#006400', 'darkgrey': '#a9a9a9', 'darkkhaki': '#bdb76b', 'darkmagenta': '#8b008b', 'darkolivegreen': '#556b2f', 'darkorange': '#ff8c00', 'darkorchid': '#9932cc', 'darkred': '#8b0000', 'darksalmon': '#e9967a', 'darkseagreen': '#8fbc8f', 'darkslateblue': '#483d8b', 'darkslategray': '#2f4f4f', 'darkslategrey': '#2f4f4f', 'darkturquoise': '#00ced1', 'darkviolet': '#9400d3', 'deeppink': '#ff1493', 'deepskyblue': '#00bfff', 'dimgray': '#696969', 'dimgrey': '#696969', 'dodgerblue': '#1e90ff', 'firebrick': '#b22222', 'floralwhite': '#fffaf0', 'forestgreen': '#228b22', 'fuchsia': '#ff00ff', 'gainsboro': '#dcdcdc', 'ghostwhite': '#f8f8ff', 'gold': '#ffd700', 'goldenrod': '#daa520', 'gray': '#808080', 'green': '#008000', 'greenyellow': '#adff2f', 'grey': '#808080', 'honeydew': '#f0fff0', 'hotpink': '#ff69b4', 'indianred': '#cd5c5c', 'indigo': '#4b0082', 'ivory': '#fffff0', 'khaki': '#f0e68c', 'lavender': '#e6e6fa', 'lavenderblush': '#fff0f5', 'lawngreen': '#7cfc00', 'lemonchiffon': '#fffacd', 'lightblue': '#add8e6', 'lightcoral': '#f08080', 'lightcyan': '#e0ffff', 'lightgoldenrodyellow': '#fafad2', 'lightgray': '#d3d3d3', 'lightgreen': '#90ee90', 'lightgrey': '#d3d3d3', 'lightpink': '#ffb6c1', 'lightsalmon': '#ffa07a', 'lightseagreen': '#20b2aa', 'lightskyblue': '#87cefa', 'lightslategray': '#778899', 'lightslategrey': '#778899', 'lightsteelblue': '#b0c4de', 'lightyellow': '#ffffe0', 'lime': '#00ff00', 'limegreen': '#32cd32', 'linen': '#faf0e6', 'magenta': '#ff00ff', 'maroon': '#800000', 'mediumaquamarine': '#66cdaa', 'mediumblue': '#0000cd', 'mediumorchid': '#ba55d3', 'mediumpurple': '#9370db', 'mediumseagreen': '#3cb371', 'mediumslateblue': '#7b68ee', 'mediumspringgreen': '#00fa9a', 'mediumturquoise': '#48d1cc', 'mediumvioletred': '#c71585', 'midnightblue': '#191970', 'mintcream': '#f5fffa', 'mistyrose': '#ffe4e1', 'moccasin': '#ffe4b5', 'navajowhite': '#ffdead', 'navy': '#000080', 'oldlace': '#fdf5e6', 'olive': '#808000', 'olivedrab': '#6b8e23', 'orange': '#ffa500', 'orangered': '#ff4500', 'orchid': '#da70d6', 'palegoldenrod': '#eee8aa', 'palegreen': '#98fb98', 'paleturquoise': '#afeeee', 'palevioletred': '#db7093', 'papayawhip': '#ffefd5', 'peachpuff': '#ffdab9', 'peru': '#cd853f', 'pink': '#ffc0cb', 'plum': '#dda0dd', 'powderblue': '#b0e0e6', 'purple': '#800080', 'rebeccapurple': '#663399', 'red': '#ff0000', 'rosybrown': '#bc8f8f', 'royalblue': '#4169e1', 'saddlebrown': '#8b4513', 'salmon': '#fa8072', 'sandybrown': '#f4a460', 'seagreen': '#2e8b57', 'seashell': '#fff5ee', 'sienna': '#a0522d', 'silver': '#c0c0c0', 'skyblue': '#87ceeb', 'slateblue': '#6a5acd', 'slategray': '#708090', 'slategrey': '#708090', 'snow': '#fffafa', 'springgreen': '#00ff7f', 'steelblue': '#4682b4', 'tan': '#d2b48c', 'teal': '#008080', 'thistle': '#d8bfd8', 'tomato': '#ff6347', 'turquoise': '#40e0d0', 'violet': '#ee82ee', 'wheat': '#f5deb3', 'white': '#ffffff', 'whitesmoke': '#f5f5f5', 'yellow': '#ffff00', 'yellowgreen': '#9acd32'}

bc = decimal.Decimal('0.55228474983079339840225163227959')
pi = decimal.Decimal('3.14159265358979323846264338327950')
fi = pi / decimal.Decimal('180')
zero = decimal.Decimal('0')
one = decimal.Decimal('1')

circle = [['M', one, zero], ['C', one, bc, bc, one, zero, one], ['S', -one, bc, -one, zero], ['S', -bc, -one, zero, -one], ['S', one, -bc, one, zero], ['Z']]
square = [['M', zero, zero], ['H', one], ['V', one], ['H', zero], ['Z']]


def color(c):
    c = c.lower()
    if c.startswith('#'):
        if len(c) == 4:
            return ''.join(x * 2 for x in c)[1:]
        return c
    return '#' + COLORS.get(c, '000000')


def euler(x):
    u, v, d, i, s, c = x % (pi + pi), one, one, one, zero, zero
    for _ in range(100):
        c, v, d, i = c + v / d, v * u, d * i, i + one
        s, v, d, i = s + v / d, v * u, d * i, i + one
        c, v, d, i = c - v / d, v * u, d * i, i + one
        s, v, d, i = s - v / d, v * u, d * i, i + one
    return c, s


def parse(data):
    nargs = dict(zip('MmLlHhVvCcSsQqTtAaZz', [3, 3, 3, 3, 2, 2, 2, 2, 7, 7, 5, 5, 5, 5, 3, 3, 8, 8]))
    commands = []
    for token in re.findall(r'([MmLlHhVvCcSsQqTtAaZz]|(?:-?\d+(?:\.\d+)?|-?\.\d+))', data):
        if token in 'MmLlHhVvCcSsQqTtAaZz':
            commands.append([token])
        else:
            if len(commands[-1]) == nargs[commands[-1][0]]:
                commands.append([commands[-1][0]])
            commands[-1].append(decimal.Decimal(token))
    return commands


def simplify(commands):
    res = []
    first = None
    cursor = zero, zero
    control = zero, zero
    for args in commands:
        cx, cy = cursor
        match args[0]:
            case 'M':
                cmd = ['M', args[1], args[2]]
            case 'm':
                cmd = ['M', cx + args[1], cy + args[2]]
            case 'L':
                cmd = ['L', args[1], args[2]]
            case 'l':
                cmd = ['L', cx + args[1], cy + args[2]]
            case 'H':
                cmd = ['L', args[1], cy]
            case 'h':
                cmd = ['L', cx + args[1], cy]
            case 'V':
                cmd = ['L', cx, args[1]]
            case 'v':
                cmd = ['L', cx, cy + args[1]]
            case 'C':
                cmd = ['C', args[1], args[2], args[3], args[4], args[5], args[6]]
            case 'c':
                cmd = ['C', cx + args[1], cy + args[2], cx + args[3], cy + args[4], cx + args[5], cy + args[6]]
            case 'S':
                cmd = ['C', control[0], control[1], args[1], args[2], args[3], args[4]]
            case 's':
                cmd = ['C', control[0], control[1], cx + args[1], cy + args[2], cx + args[3], cy + args[4]]
            case 'Q':
                cmd = ['Q', args[1], args[2], args[3], args[4]]
            case 'q':
                cmd = ['Q', cx + args[1], cy + args[2], cx + args[3], cy + args[4]]
            case 'T':
                cmd = ['Q', control[0], control[1], args[1], args[2]]
            case 't':
                cmd = ['Q', control[0], control[1], cx + args[1], cy + args[2]]
            case 'A':
                cmd = ['L', args[6], args[7]]
            case 'a':
                cmd = ['L', cx + args[6], cy + args[7]]
            case 'Z':
                cmd = ['Z']
            case 'z':
                cmd = ['Z']

        if first is None and cmd[0] != 'M':
            first = cursor

        if cmd[0] == 'Z':
            cursor = first
        else:
            cursor = cmd[-2], cmd[-1]

        if cmd[0] == 'C' or cmd[0] == 'Q':
            control = cmd[-2] + cmd[-2] - cmd[-4], cmd[-1] + cmd[-1] - cmd[-3]
        else:
            control = cursor

        res.append(cmd)

    return res


def apply(commands, func):
    res = []
    for args in commands:
        match args[0]:
            case 'M':
                cmd = ['M', *func(args[1], args[2])]
            case 'L':
                cmd = ['L', *func(args[1], args[2])]
            case 'C':
                cmd = ['C', *func(args[1], args[2]), *func(args[3], args[4]), *func(args[5], args[6])]
            case 'Q':
                cmd = ['Q', *func(args[1], args[2]), *func(args[3], args[4])]
            case 'Z':
                cmd = ['Z']
        res.append(cmd)
    return res


def encode(commands):
    fmt = lambda x: x if type(x) is str else f'{round(x, 8):.8f}'.rstrip('0').rstrip('.')
    return ' '.join(' '.join(fmt(x) for x in args) for args in commands)


def transform(commands, trans):
    res = commands
    for op, args in re.findall(r'(translate|rotate|scale)\(([^\)]+)\)', trans)[::-1]:
        args = [decimal.Decimal(x) for x in args.split()]
        match op:
            case 'translate':
                tx, ty = args[0], args[-1]
                res = apply(res, lambda x, y: (x + tx, y + ty))
            case 'rotate':
                tx, ty = euler(args[0] * fi)
                res = apply(res, lambda x, y: (tx * x - ty * y, ty * x + tx * y))
            case 'scale':
                tx, ty = args[0], args[-1]
                res = apply(res, lambda x, y: (x * tx, y * ty))
    return res


def convert(svg):
    styles = dict(re.findall(r'\.(\S+)\s*\{(?:.|\n)*fill:\s*(\S+);(?:.|\n)*\}', svg))
    tags = re.findall(r'<(rect|polygon|circle|ellipse|path)([^/]+)/>', svg)
    viewbox = re.search(r'(viewBox="[^"]+")', svg).group(0)

    out = f'<svg {viewbox} xmlns="http://www.w3.org/2000/svg">\n'
    for tag, attribs in tags:
        attribs = dict(re.findall(r'(\w+)="([^"]+)"', attribs))
        fill = color(attribs.get('fill', styles.get(attribs.get('class'), '#000')))
        trans = attribs.get('transform', '')
        match tag:
            case 'path':
                commands = parse(attribs['d'])
            case 'polygon':
                x, y, *rest = attribs['points'].split()
                commands = parse(' '.join(['M', x, y, 'L'] + rest))
            case 'circle':
                tx, ty, r = attribs.get('cx', '0'), attribs.get('cy', '0'), attribs['r']
                trans += f'translate({tx} {ty}) scale({r} {r})'
                commands = circle
            case 'ellipse':
                tx, ty, rx, ry = attribs.get('cx', '0'), attribs.get('cy', '0'), attribs['rx'], attribs['ry']
                trans += f'translate({tx} {ty}) scale({rx} {ry})'
                commands = circle
            case 'rect':
                tx, ty, w, h = attribs.get('x', '0'), attribs.get('y', '0'), attribs['width'], attribs['height']
                trans += f'translate({tx} {ty}) scale({w} {h})'
                commands = square
        d = encode(transform(simplify(commands), trans))
        out += f'<path fill="{fill}" d="{d}"/>\n'
    out += '</svg>\n'
    return out


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()
    open(args.output, 'w').write(convert(open(args.input).read()))
