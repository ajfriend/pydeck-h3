"""
Basic 2D and 3D plotting; takes in a list of dictionaries
"""

import pydeck as pdk


def plot(rows, opts_layer, opts_deck):
    layer = pdk.Layer('H3HexagonLayer', rows, **opts_layer)
    deck = pdk.Deck([layer], **opts_deck)

    return deck
