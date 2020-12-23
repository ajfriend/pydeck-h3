from .util3d import make_pdk_rows

# import toolz

# from .util import transpose
# from .helpers import color_helper, line_width_helper, hex_helper


# def make_pdk_rows(
#     rows,
#     col_hex,

#     color = (245, 206, 66), # tuple or string
#     cmap = 'YlOrRd', #string or callable, but this function doesn't check

#     line_width = 1,
# ):

#     cols = toolz.merge(
#         # maybe an identity helper???
#         color_helper(rows, color, cmap=cmap),
#         line_width_helper(rows, line_width=line_width),
#         hex_helper(rows, col_hex),
#     )

#     _rows = transpose(cols)

#     pdk_rows = [
#         {
#             **row,
#             **_row
#         }
#         for row, _row in zip(rows, _rows)
#     ]

#     return pdk_rows




