# L06 Matplotlib 折线与散点入门

阶段：A · DSBA/Python/可视化/复杂度。
范围：折线、散点、英文标签、标题、网格、基础线型与双系列比较。图例和保存只掌握本课必需操作，柱状图、直方图及系统保存参数留到 L07；不讲 seaborn、模型训练、计算机系统原理。

仓库路径：L06/。

## 今日目标

读完后你应能：依据问题选 plot 或 scatter；从同一批观测中提取等长 x/y；画出标注完整的图；区分颜色、线型、标记；封装满足长度校验、保存、关闭、返回值约定的函数。

## 一、是什么：图是数据含义的编码

Matplotlib 是 Python 的绘图库，pyplot 是常见的入门接口，惯例写成 import matplotlib.pyplot as plt。Figure 是整张画布，Axes 是画布上的一个坐标系；注意 Axes 不是单指某一根 x 轴或 y 轴。

plot(x, y) 把第 i 个横坐标和第 i 个纵坐标配成点，再按输入顺序连接。scatter(x, y) 表达同样的点对，但不主动连接，因而不暗示前后顺序。它们都不是“把两列数字随便扔进去”：同一位置上的 x/y 必须描述同一个观测。

例如 day=[1,2,3]、sales=[20,22,19] 表示三天销量。折线强调随天数先升后降；若 x 表示不同顾客的广告曝光次数、y 表示各自消费额，顾客行号通常没有需要连接的意义，应优先散点。

## 二、为什么：先明确问题，再决定画法

表格适合查精确数值，图适合发现整体趋势、异常观测和两变量关系。图不是表格的替代品，更不能凭漂亮的走势直接下统计结论。

“这十天销量如何变化？”关注有序变化，选折线；“广告费较高的样本是否通常销量也高？”关注关系，选散点。散点向右上延伸只能提示样本中存在正向关联，不能证明提高广告费必然导致销量上升；季节、价格、样本选择都可能影响结果。

同图双折线适合比较同横轴、同单位的两组观测，如 A/B 店销量。若把销量与温度直接放在同一纵轴，量纲不同会混淆读者，本课先分别画图。

标签要交代变量和单位，标题要交代对象或问题；网格帮助估读，但不能补救错误坐标。颜色用于区分系列，线型和标记还能让黑白打印下的系列可辨认。

## 三、怎么写：准备数据 → 新建图 → 绘制 → 标注 → 输出 → 关闭

下面是完整的交互式例题：一周销量走势与广告费—销量关系。两张图各自创建，避免内容叠加；它不要求写入任何磁盘文件。

```python
import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5, 6, 7]
sales = [20, 22, 19, 25, 24, 28, 27]
ad = [1, 2, 3, 4, 5, 6]
ad_sales = [10, 12, 15, 14, 18, 20]

if len(days) != len(sales):
    raise ValueError("days and sales must have equal length")
fig = plt.figure()
plt.plot(days, sales, color="steelblue", linestyle="-", marker="o")
plt.xlabel("Day")
plt.ylabel("Sales (units)")
plt.title("Weekly sales")
plt.grid(True)
plt.show()
plt.close(fig)

if len(ad) != len(ad_sales):
    raise ValueError("ad and sales must have equal length")
fig = plt.figure()
plt.scatter(ad, ad_sales, color="darkorange")
plt.xlabel("Ad spend")
plt.ylabel("Sales (units)")
plt.title("Ad spend vs Sales")
plt.grid(True)
plt.show()
plt.close(fig)
```

第一张图第 3 天回落，但第 7 天销量比第 1 天高，不能据此声称“每天都增长”。第二张图整体向右上延伸，第 4 个样本却低于第 3 个：关联不等于每一点严格单调，更不等于因果。

plot 的 color 控制颜色，linestyle="-" 表示实线、"--" 表示虚线，marker="o" 为圆点、"s" 为方点。plot(x,y,"b-o") 是蓝色实线圆点的简写，初学封装函数时用关键字更清楚。只写 plot(y) 时横轴默认 0 到 n-1；若业务横轴是第 1 到第 7 天，不应省略 x。

双系列示例：

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
a = [10, 11, 13, 12]
b = [9, 10, 10, 12]
if not (len(x) == len(a) == len(b)):
    raise ValueError("length mismatch")
fig = plt.figure()
plt.plot(x, a, color="blue", linestyle="-", marker="o", label="A")
plt.plot(x, b, color="red", linestyle="--", marker="s", label="B")
plt.xlabel("Day")
plt.ylabel("Sales")
plt.title("A vs B")
plt.grid(True)
plt.legend()
plt.show()
plt.close(fig)
```

label 是系列名称；legend() 才把系列名称展示出来。不要只依赖红蓝颜色区分，线型和标记也不同更稳妥。

已有 Pandas 表时，先对成对列共同清洗，再按业务顺序画：

```python
sub = df[["day", "sales"]].dropna().sort_values("day")
plt.plot(sub["day"], sub["sales"], marker="o")
```

这里 df 应是已读入的 DataFrame。若日期是字符串，应先按真实日期含义转换，不要让字符串排序造成“1,10,2”的顺序。也不要为让图好看按 sales 排序，那会破坏时间顺序。

作业函数按题面保存 PNG：在无显示器脚本中先 import matplotlib，再 matplotlib.use("Agg")，最后导入 pyplot；绘制后 savefig(out_path)，然后 close 当前函数创建的 Figure，返回原样路径字符串。Agg 不会弹窗，适合批量渲染；交互学习可以 show。savefig 必须在 close 之前。保存目录须存在；样例脚本会准备自己的 out/。这里说明的是供你运行的代码契约，本次课件交付本身不在本地生成图。

## 四、易错点：会出图不等于图正确

1. 长度相同却配错观测。分别对 x/y dropna 后，长度甚至可能碰巧相同，但行对应已错。正确做法是对两列共同筛选，再同时取列。长度校验只能发现数量错误，不能发现语义错配。
2. 误以为 plot 自动按 x 排序。x=[3,1,2] 时它按 3→1→2 连线。时间趋势应把整对观测一起按时间排序；无序样本关系应换 scatter，不能只排序 x 而不调整 y。
3. 用 plot(df) 期待自动挑 day 当横轴。直接传二维数值表时通常按索引为多列画线。应显式写 plot(df["day"],df["sales"])。
4. 图越画越多、曲线叠加。pyplot 操作当前图；每张独立图先 figure，完成后 close(fig)。函数只关闭自己创建的图，不要随意 close("all") 干扰调用者。
5. 保存空图或找不到目录。先绘图和标注，再保存，最后关闭；父目录不存在时应由调用约定明确创建。本课只要求长度不匹配抛 ValueError，不要把所有异常都吞掉并假装成功。
6. 中文显示方框。常见原因是环境缺合适字体，并非绘图数据坏了；本课验收统一英文标签。透明度 alpha 影响重叠点可见性，scatter 的 s 表示标记面积而不是半径，切勿把面积增加误读成半径同比增加。

## 五、何时用：用问题检验选择

有序横轴下看变化，用 plot；无必须连接顺序的二维观测看关系，用 scatter。时间序列也可用散点强调离散采样，因此选择是表达目的，不是“时间数据绝不能 scatter”的硬规则。若连线会暗示不存在的连续过程，宁可只标出观测点并说明采样方式。

读图时依次问：横纵轴变量与单位是什么？每个点对应哪个观测？连线顺序是否有业务意义？坐标范围是否夸大波动？是否有异常或重叠点？是否把样本关联误说成因果？这些检查比换配色更重要。

机试封装顺序：先看函数签名和固定字符串，再校验长度、创建独立图、调用正确图元、补齐标签/标题/网格、按需 legend、保存并关闭、返回题定路径。除检查输出文件，还要检查图元、样式和异常行为；一张非空 PNG 不能证明题目做对。

## 三道练习摘要与硬验收

题目完整版本以 L06/homework.md 为准，本次保留原三道题的接口与评分要求。

1. plot_series(x,y,out_path)：实线圆点折线，标签 x/y、标题 series、网格；保存并关闭，返回原路径。长度不等必须 ValueError。
2. plot_scatter(x,y,out_path)：必须调用 scatter，标签 x/y、标题 scatter、网格；保存并关闭、返回路径，长度不等必须 ValueError。
3. plot_two_series(x,y1,y2,out_path)：蓝实线圆点 A、红虚线方点 B，标签 x/y、标题 A vs B、网格、图例；保存关闭并返回路径，三者长度不全等必须 ValueError。

共同验收：PNG 可解码且尺寸为正；正常/单点/等长空序列按题面契约完成，输入不被修改；异常长度不创建输出文件、不泄漏新 Figure；既有 Figure 不受影响；图元数量、数据、指定样式与固定文字逐项核对。输入限定为有限数值的一维列表或数组，输出为 .png 字符串路径且父目录已存在；不要求处理生成器、非数值输入或自动创建任意父目录。

标准答案：homework/answers.ipynb 当前为占位，约 9:30 写标准答案。

## 下节预告

L07 Matplotlib 柱状·直方图·图例与保存。今天先分清趋势和关系，下次学习类别比较、数值分布以及更规范的图例与保存。
