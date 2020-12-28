import pydeck as pdk


MB_KEY = 'pk.eyJ1IjoiYWpmcmllbmQiLCJhIjoiY2pmbmRjczJmMTVkMzJxcW92Y2E4cHZjdCJ9.Jf-gFXU7FOIQxALzPajbdg'


import toolz

from .pdk_rows.util import transpose
from .pdk_rows.helpers import color_helper


def make_pdk_rows(
    rows,
    color,
    cmap = 'YlOrRd', #string or callable, but this function doesn't check
):
    cols = [
        color_helper(rows, color, cmap=cmap),
    ]


    cols = toolz.merge(*cols)
    _rows = transpose(cols)

    pdk_rows = [
        {
            **row,
            **_row
        }
        for row, _row in zip(rows, _rows)
    ]

    return pdk_rows



def plot(data, col_hex='hexset', col_color='color', cmap='YlOrRd', line_width=100, opacity=0.7):

    data = make_pdk_rows(data, col_color, cmap=cmap)

    layer = pdk.Layer(
        'H3ClusterLayer',
        data,
        pickable = True,
        stroked = True,
        filled = True,
        extruded = False,
        get_hexagons = col_hex,
        get_fill_color = '_pdk_fill_color',
        get_line_width = line_width,
        opacity = opacity,
    )


    view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=9)


    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
    )

    return deck
