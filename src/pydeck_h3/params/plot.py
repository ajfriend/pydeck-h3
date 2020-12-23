from .deck import get_deck_params
from .layer import get_layer_params

def get_plot_params(rows, opacity=.7, wireframe=False, elevation_scale=20, hide_underscored=True):
    """
    rows is a list of dictionaries, each with the keys

    _pdk_h3cell: str
    _pdk_line_width: int, float
    _pdk_fill_color: rgb or rgba tuples

    opacity is multiplicative

    all values in the dict not starting with `_` will be printed int he tooltip
    """


    # todo: doo all this processing in a helper function. this will be easier to test
    #
    # # todo: split these up into two different functions for layer and deck???

    layer_params = get_layer_params(
        rows,
        opacity=opacity,
        wireframe=wireframe,
        elevation_scale=elevation_scale,
    )

    deck_params = get_deck_params(rows, hide_underscored=hide_underscored)

    return layer_params, deck_params
