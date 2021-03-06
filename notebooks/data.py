import pandas as pd

rows = [
    {'h3cell': '89283082807ffff', 'cats': 6, 'dogs': 15},
    {'h3cell': '89283082833ffff', 'cats': 0, 'dogs': 5},
    {'h3cell': '8928308283bffff', 'cats': 18, 'dogs': 1},
    {'h3cell': '892830828bbffff', 'cats': 19, 'dogs': 26},
    {'h3cell': '8928308280fffff', 'cats': 12, 'dogs': 2},
    {'h3cell': '8928308281bffff', 'cats': 1, 'dogs': 24},
    {'h3cell': '89283082813ffff', 'cats': 4, 'dogs': 14},
    {'h3cell': '89283082803ffff', 'cats': 2, 'dogs': 3},
    {'h3cell': '89283082817ffff', 'cats': 7, 'dogs': 6},
    {'h3cell': '892830828cfffff', 'cats': 17, 'dogs': 6},
    {'h3cell': '8928308280bffff', 'cats': 15, 'dogs': 18},
    {'h3cell': '89283082873ffff', 'cats': 6, 'dogs': 19},
    {'h3cell': '8928308288fffff', 'cats': 6, 'dogs': 14},
    {'h3cell': '89283082877ffff', 'cats': 10, 'dogs': 15},
    {'h3cell': '892830828c7ffff', 'cats': 19, 'dogs': 18},
    {'h3cell': '89283082857ffff', 'cats': 10, 'dogs': 8},
    {'h3cell': '89283082847ffff', 'cats': 4, 'dogs': 13},
    {'h3cell': '892830828abffff', 'cats': 4, 'dogs': 11},
    {'h3cell': '8928308288bffff', 'cats': 1, 'dogs': 8}
]


df = pd.DataFrame(rows)
hexset = set(df['h3cell'])
series = df.set_index('h3cell')['cats']

#hexdict = dict(df.set_index('h3cell')['cats']) # this one doesn't work because it gives numpy.int64s
hexdict = series.to_dict()

data = {
    'rows': rows,
    'df': df,
    'hexset': hexset,
    'series': series,
    'hexdict': hexdict,
}
