

def get_layer_params2d(*, opacity=.7, **kwargs):
    params = {
        'pickable': True,
        'extruded': False,
        'opacity': opacity,
        'get_hexagon':    '_pdk_h3cell',
        'get_fill_color': '_pdk_fill_color',
        'get_line_width': '_pdk_line_width',
    }

    return params


def get_layer_params3d(*, opacity=.7, wireframe=False, elevation_scale=20, **kwargs):
    params = {
        'pickable': True,
        'extruded': True,
        'opacity': opacity,
        'wireframe': wireframe,
        'elevation_scale': elevation_scale,
        'get_hexagon':    '_pdk_h3cell',
        'get_fill_color': '_pdk_fill_color',
        'get_elevation':  '_pdk_elevation',
    }

    return params

def get_layer_params(rows, **kwargs):
    if '_pdk_elevation' in rows[0]:
        return get_layer_params3d(**kwargs)
    else:
        return get_layer_params2d(**kwargs)
