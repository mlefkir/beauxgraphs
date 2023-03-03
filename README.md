# beauxgraphs
Styles and examples for beautiful plots with matplotlib.

Command to use the matplotlib style file:
```python
plt.style.use("https://github.com/mlefkir/beauxgraphs/raw/main/beautifulgraphs_colblind.mplstyle")
```

```python
plt.style.use("https://github.com/mlefkir/beauxgraphs/raw/main/beautifulgraphs.mplstyle")
```
To use LaTeX equations in matplotlib:
```python
plt.style.use("https://github.com/mlefkir/beauxgraphs/raw/main/beautifulgraphs_latex.mplstyle")
```

To get the list of colors loaded:
```python
plt.rcParams["axes.prop_cycle"].by_key()["color"]
```