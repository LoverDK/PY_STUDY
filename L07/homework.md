# L07 作业：柱状、直方图、分组柱与保存

仅使用 Python、Matplotlib，可用 NumPy 辅助。三题都是独立函数题；轴标签、标题、系列名严格按下文英文字符串。不能用 seaborn。

## 通用契约
- 数据为有限数值的一维列表；类别为非空、互异的英文字符串列表，按输入顺序画，不自动排序。空类别列表合法，但非空列表中的元素不得为空字符串。
- 三题 out_path 均为 .png 字符串，父目录事先存在。用 fig.savefig 或等价 savefig 保存，参数必须 format="png", dpi=150, bbox_inches="tight"。
- 返回的路径必须与传入字符串完全相同。先检查题定非法输入，再创建 Figure；非法输入必须抛 ValueError，不能保存输出。
- 每次创建独立 Figure，只关闭自己创建的图；正常与保存失败时都不能泄漏新画布，不得关闭调用者原有 Figure。保存异常原样向上传播。
- 不得原地修改数据或类别。非数值输入、NaN/无穷、生成器、非法路径等不在本课强制处理范围。
- 合法空输入仍须生成带正确轴、标题、必要图例的合法空图。
- 统一 figsize=(6,4)，纵轴下限 0；本课三题不要求网格。图中只应有题定的柱，不添加多余数据系列。

## 题一 · 类别柱状图
```python
def plot_category_bars(categories, values, out_path: str) -> str:
    ...
```
要求：
1. len(categories)==len(values)；类别互异且每个为非空字符串；values 每项 >=0。违反任一项抛 ValueError。
2. 一次 bar 或等价 Axes.bar，宽 0.6，color="steelblue"、edgecolor="black"，每柱高度对应 values，底部 0。
3. xlabel="Category"，ylabel="Value"，title="Category totals"；不要求图例。
4. 保存关闭后返回 out_path。
样例：
```python
plot_category_bars(["Python","SQL","C"], [12,8,10], "out/q1.png")
# 返回 "out/q1.png"，三个柱高依次 12/8/10
```
硬验收：柱数、中心顺序、刻度文本、高度、宽度、颜色、边线、固定标签逐项检查；空列表成功；单类别成功；长度不等、重复类别、空字符串类别、负高度分别 ValueError；PNG 可解码，不能只检查扩展名。

## 题二 · 指定边界的耗时频数直方图
```python
def plot_duration_hist(durations, bin_edges, out_path: str) -> tuple:
    ...
```
要求：
1. bin_edges 至少 2 项且严格递增，否则 ValueError；durations 允许空。
2. 必须调用 hist 或 Axes.hist，bins=bin_edges，density=False，color="darkorange"，edgecolor="black"，保持默认条形填充、rwidth=None，不做归一化、不加权。
3. xlabel="Minutes"，ylabel="Count"，title="Duration distribution"。
4. 返回 (counts, out_path)，counts 是普通 Python 列表，每项为整数，顺序按箱从小到大。
5. 边界规则：除最后箱左闭右开，最后箱两端包含；边界外观测不计入，不报错、不挪进首尾箱。
样例：
```python
plot_duration_hist([10,15,20,25,30,35,40,40], [10,20,30,40], "out/q2.png")
# ([2,2,4], "out/q2.png")
plot_duration_hist([-1,0,1,2,3,4], [0,1,3], "out/q2b.png")
# ([1,3], "out/q2b.png")，-1 与 4 在范围外
```
硬验收：箱数=边界数-1；每柱左边界、宽度和高度正确；固定文字、颜色和边线正确；空 durations 时 counts 为对应长度全零列表；单点落在最右边界应计入最后箱；重复/逆序/过少边界 ValueError；PNG 可解码。

## 题三 · 两组并列柱与规范图例
```python
def plot_grouped_bars(categories, a, b, out_path: str) -> str:
    ...
```
要求：
1. categories/a/b 三者等长，类别互异且非空字符串，a/b 高度非负；否则 ValueError。
2. 类别中心位置 0..n-1，width=0.36。A 每柱中心 i-0.18、color="blue"、label="A"；B 中心 i+0.18、color="orange"、label="B"；均从 0 起。
3. 必须有 A/B 两组 bar，x 刻度在整数中心，刻度文本为 categories。
4. xlabel="Category"，ylabel="Value"，title="A vs B totals"。
5. legend(loc="upper left", title="Group")，图例可见文本顺序 A、B；空数据也应有 A/B 图例。
6. 保存关闭后返回 out_path。
样例：
```python
plot_grouped_bars(["W1","W2"], [6,8], [5,9], "out/q3.png")
# 四根柱：A 中心 -0.18/0.82，高度 6/8；B 中心 0.18/1.18，高度 5/9
```
硬验收：2n 根柱、两个 BarContainer；中心/宽/高/颜色、刻度位置和文本、固定轴标签、标题及图例逐项检查；覆盖空数据与单类别；分别让 a/b 与类别长度不同，或负高度、重复/空类别，均应 ValueError。

## 共同输出验收清单
1. 可在保存前捕获 fig，检查图元数据及属性，浮点比较用容差。
2. 验证保存调用的 PNG、150 dpi、tight 参数；真实解码 PNG，宽高为正。tight 会改变图像尺寸，不强制 900×600。
3. 验证返回类型和值，输入完全不变；调用前后 Figure 编号集合一致。
4. 非法输入在建图和保存之前拒绝；模拟保存失败仍须关闭新 Figure，传播异常。
5. 不把文件存在/非空当作全部验收。

先独立作答，约 9:30 提交标准答案至 homework/answers.ipynb。
