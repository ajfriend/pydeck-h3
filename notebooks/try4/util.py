import matplotlib.pyplot as plt

"""
help with colors:

import matplotlib
matplotlib.colors.to_rgb('yellow')
matplotlib.colors.get_named_colors_mapping()['red']

"""


def get_scaled_cmap(cmap='YlOrRd', lower=0.0, upper=1.0):

    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)

    if lower == upper:
        pass # what to do!

    def foo(value):
        assert lower <= value <= upper

        if lower == upper:
            value = 1.0
        else:
            value = (value - lower)/float(upper - lower)

        out = cmap(value, bytes=True)
        out = map(int, out)

        r, g, b, a = out

        return r,g,b,a

    return foo
