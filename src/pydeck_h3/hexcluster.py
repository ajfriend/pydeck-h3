import pydeck as pdk
import pandas as pd

MB_KEY = 'pk.eyJ1IjoiYWpmcmllbmQiLCJhIjoiY2pmbmRjczJmMTVkMzJxcW92Y2E4cHZjdCJ9.Jf-gFXU7FOIQxALzPajbdg'


# Define a layer to display on a map
layer = pdk.Layer(
    "H3ClusterLayer",
    rows,
    pickable=True,
   stroked=True,
    filled=True,
    extruded = False,
    get_hexagons = 'hexset',
    get_fill_color = 'color',
    get_line_color = [0, 0, 0],
    get_line_width = 100,
    get_elevation = 'value',
#    line_width_min_pixels=2,
    opacity=.7,
    elevation_scale = 5,
    wireframe=True,
)

# Set the viewport location
view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=9)


# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state,     mapbox_key = MB_KEY,
    map_style = 'mapbox://styles/mapbox/light-v10',)
r.to_html()



def plot(data, col_hex='hexset', col_color, cmap):
    pass
