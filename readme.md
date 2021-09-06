# pydeck-h3

Helper functions to viz H3 data with https://pydeck.gl/

- https://github.com/ajfriend/pydeck-h3
- WIP website: https://ajfriend.github.io/pydeck-h3/

install from github:

```
pip install git+https://github.com/ajfriend/pydeck-h3
```


## hexcluster class

what about support for the hexcluster class?


## Notes

- watch out for the `numpy.int64` issue with converting to json
    + it happens late; when converting the deck to a view

- can we build up the data and the options dictionary from the start?
    + is that a more-obvious way to describe the branching/dispatch to different plotting types?
