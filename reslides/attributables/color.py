#encoding=utf-8

class Color:
    pass

class RGB:
    def __init__(self, rgb):
        if isinstance(rgb, str):
            if rgb.startswith('#'):
                rgb = rgb[1:]
            if len(rgb) == 3:
                t = tuple(d / 15 for d in map(lambda c: int(c, base=16), rgb))
            if len(rgb) == 6:
                t = tuple(d / 255 for d in map(lambda xs: int(xs[0] + xs[1], base=16),
                                         zip(rgb[0::2], rgb[1::2])))
            self.rgb = t
        elif isinstance(rgb, tuple):
            self.rgb = tuple(float(d) for d in rgb)
        else:
            raise AttributeError()

    def __str__(self):
        return "{:0.2f} {:0.2f} {:0.2f} rg".format(*self.rgb)

