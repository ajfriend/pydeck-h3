# pydeck-h3

Helper functions to viz H3 data with https://pydeck.gl/

- Gotta use [Nebula.gl](https://eng.uber.com/nebulagl/)!
- https://www.streamlit.io/
    + http://awesome-streamlit.org/
- dstack? https://news.ycombinator.com/item?id=24131723
    + https://dstack.ai/
- https://github.com/JetBrains/lets-plot
- https://medium.com/plotly/introducing-jupyterdash-811f1f57c02e


## Input formats

- `set`/`list` of hexes/iterable
- `dict`: hex -> float
- `dict`
    hex -> record keys/values
    
- "rows"
    - list of dicts, with one pair being `hexid`: '8928308288fffff'

    
- pandas.Series
    index is hexes, values give values

- pandas.DataFrame
    index or column is hexes?
    
    
record classes?

use pattern matching/dispatch. let user register new things dynamically, change things. make it easy to modify/inspect.

gotta work with string and int representations.


## what's the right, ultimate format?

prolly `dict`: hex -> {key: value} dict


# hexcluster class

what about support for the hexcluster class?


prolly `dict`: hexcluster -> {key: value} dict

how to idenfity hexcluster? just the set of hexes?

