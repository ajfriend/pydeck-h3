todo: list of map tiles that people can use
todo: explain colormaps
todo: what if we set `col_height=None` to get a 2d map (and works with DF!)

todo: how to get color and height scaling that works across multiple data sets. need to stay constant for comparison

```python
#plot2d(rows, default_color='yellow', col_hex=None, col_color=None, color_map='blah')


# maybe this is just a transform function (doesn't call the map)
# it just transforms a row form to the row form with _pdk
# just a transform will be easier to test
def plot2d(
    rows,
    col_hex,

    # bah, need a record type. importing a function should automatically import its record type constructor (in something like ML, or C even!)
    color = (245, 206, 66),  # dispatch on string vs tuple. or give the user a utility function u.color('yellow'). if string given, assumed that's the name of a column
    cmap = 'YlOrRd',  # let this thing take in a function (if we want global coloring, the function has to do the pre-normalization itself; the function will only look at one element at a time)

    line_width = 1, # dispatch on numeric vs string vs function
    opacity = .7,
):
    """
    line_width: int, float, or str to denote column name

    can have hte color be rgb or rgba tuples

    opacity is multiplicative
    """
```
