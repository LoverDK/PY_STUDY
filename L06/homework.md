# L06 作业（考研 / 机试风）

要求：用 **matplotlib.pyplot** 完成（可用 numpy/pandas 准备数据）。轴标签与标题一律 **英文**，避免字体问题。脚本环境请自行 `matplotlib.use("Agg")`（若需要）。不要用 seaborn。

---

## 练习 1 · 折线图函数

**函数签名**

```python
def plot_series(x, y, out_path: str) -> str:
    """
    将等长序列 x, y 画成折线图（实线 + 圆形标记）。
    设置：
      xlabel = "x"
      ylabel = "y"
      title  = "series"
      grid(True)
    保存到 out_path（PNG），然后 close 图。
    返回 out_path（原样字符串）。
    若 len(x) != len(y)，抛出 ValueError。
    """
```

**样例**

```python
plot_series([1, 2, 3], [10, 20, 15], "out/hw1.png")
# → 返回 "out/hw1.png"，且该路径存在可读的 PNG 文件
```

**验收**

1. 必须调用 `plt.plot`（或等价 Axes.plot）；必须设置英文 `xlabel`/`ylabel`/`title` 为上述固定字符串  
2. 必须 `grid(True)`；必须把图保存到 `out_path` 后 `close`  
3. `len(x) != len(y)` 时必须 `raise ValueError`  
4. 返回值 `== out_path`；文件存在且大小 > 0

---

## 练习 2 · 散点图函数

**函数签名**

```python
def plot_scatter(x, y, out_path: str) -> str:
    """
    将等长序列 x, y 画成散点图。
    设置：
      xlabel = "x"
      ylabel = "y"
      title  = "scatter"
      grid(True)
    保存到 out_path，close，返回 out_path。
    若 len(x) != len(y)，抛出 ValueError。
    """
```

**样例**

```python
plot_scatter([1.0, 2.0, 3.0, 4.0], [2.1, 3.9, 6.2, 7.8], "out/hw2.png")
```

**验收**

1. 必须使用 `plt.scatter`（不得只用 `plot` 冒充实心点来交差）  
2. 标签/标题字符串必须分别为 `"x"` / `"y"` / `"scatter"`；必须 `grid(True)`  
3. 长度不一致 → `ValueError`  
4. 返回 `out_path`；文件存在且大小 > 0

---

## 练习 3 · 双折线对比

**函数签名**

```python
def plot_two_series(x, y1, y2, out_path: str) -> str:
    """
    在同一张图上画两条折线：
      y1: color="blue", linestyle="-", marker="o", label="A"
      y2: color="red",  linestyle="--", marker="s", label="B"
    设置：
      xlabel = "x"
      ylabel = "y"
      title  = "A vs B"
      grid(True)
      legend()   # 必须出现图例
    保存到 out_path，close，返回 out_path。
    若 len(x)、len(y1)、len(y2) 三者不全相等，抛出 ValueError。
    """
```

**样例**

```python
plot_two_series(
    [1, 2, 3, 4],
    [10, 11, 13, 12],
    [9, 10, 10, 12],
    "out/hw3.png",
)
```

**验收**

1. 必须两次 `plot`（或一次多系列但等价画出 A/B）；必须 `legend()`  
2. 标签/标题固定为 `"x"` / `"y"` / `"A vs B"`；必须 `grid(True)`  
3. 三者长度不全相等 → `ValueError`  
4. 返回 `out_path`；文件存在且大小 > 0  
5. 禁止使用 seaborn

---

完成三题后，对照约 15:30 写入的 `homework/answers.ipynb`。
