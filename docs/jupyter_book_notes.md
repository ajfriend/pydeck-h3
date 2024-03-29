# Jupyter Book Notes

Some personal notes on playing around with Jupyter Book.

## Orphan pages

Add the following to the top of a file to avoid getting a warning
if the page isn't included in the main TOC:

````md
```{eval-rst}
:orphan:
```
````

## RHS or Secondary Sidebar expansion

https://github.com/uber/h3-py/issues/198


## Admonition Options

```{note}
note
```

```{attention}
attention
```

```{caution}
caution
```

```{warning}
warning
```

```{danger}
danger
```


```{error}
error
```


```{hint}
hint
```


```{important}
important
```

```{tip}
tip
```


### Custom admonitions

```{admonition} Custom!
admonition
```

```{admonition} TODO
todo
```

More customization: https://github.com/executablebooks/jupyter-book/issues/1345
