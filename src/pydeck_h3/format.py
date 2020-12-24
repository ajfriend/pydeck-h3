import pandas as pd

def format(x):
    funcs = [
        from_list,
        from_set,
        from_dict,
        from_df,
        from_series,
    ]

    for f in funcs:
        out = f(x)
        if out is not None:
            return out

    # fallback if no matches
    return x, {}

def from_list(x):
    if isinstance(x, (list, tuple)) and isinstance(x[0], str):
        return from_set(set(x))
    else:
        return None


def from_set(x):
    if isinstance(x, set):
        x = [
            {'h3cell': h}
            for h in x
        ]

        info = {'col_hex': 'h3cell'}

        return x, info
    else:
        return None


def from_dict(x):
    if isinstance(x, dict):
        x = [
            {'h3cell': h, 'value': val}
            for h, val in x.items()
        ]

        info = {
            'col_hex': 'h3cell',
            'color': 'value',
        }

        return x, info
    else:
        return None


def from_df(x):
    if isinstance(x, pd.DataFrame):
        x = x.to_dict('records')

        return x, {}
    else:
        return None

def from_series(x):
    if isinstance(x, pd.Series):
        x = x.to_dict()
        return from_dict(x)
    else:
        return None
