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

完成三题后，对照约 9:30 写入的 `homework/answers.ipynb`。


## 验收边界与补充检查

- 输入为有限数值的一维列表或数组；允许单点与等长空序列。长度不匹配必须在创建图之前抛 ValueError。
- out_path 是 .png 字符串，父目录由调用者事先建好；不要求处理生成器、非数值输入或自动创建父目录。
- 正常调用返回原字符串，PNG 可解码、宽高为正。文件大小检查只是最低门槛，不能替代图元验收。
- 输入序列不得被原地排序或改写。函数结束后不得泄漏其新建 Figure，不得关闭调用者原有 Figure；非法长度不得新建输出文件。
- 图一核对一条 Line2D 的 x/y 数据、实线和圆点；图二核对散点 offsets 与输入点一一对应；图三核对两条线的 x/y 数据、颜色、线型、标记和 A/B 图例。
- 固定标签、标题、可见网格逐项检查。可在测试时拦截保存或关闭动作检查 Figure 对象，再验证真实 PNG。
