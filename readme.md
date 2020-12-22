# pydeck-h3

Helper functions to viz H3 data with https://pydeck.gl/

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

