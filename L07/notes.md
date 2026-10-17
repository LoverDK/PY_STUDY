# L07 Matplotlib 柱状·直方图·图例与保存

阶段：A · DSBA/Python/可视化/复杂度。
仓库路径：L07/。
范围：bar、hist、基础分组柱、legend、Figure/Axes 的基础使用、savefig 的 format/dpi/bbox_inches，以及保存后的关闭。
不讲：seaborn、交互仪表盘、统计推断、模型训练、计算机系统原理。

## 学习目标
1. 区分类别比较与数值分布，知道何时选 bar 或 hist。
2. 解释柱高、箱边界和计数，并手算一个小样本直方图。
3. 用数值横坐标与偏移量画不重叠的分组柱，正确显示图例。
4. 以明确的格式和分辨率保存图；不依赖弹窗，不误关调用者的画布。
5. 完成三道带固定接口、边界样例和图元验收的机试题。

## 一、是什么：两种“长得像柱子”的图，含义不同

柱状图 bar 的横轴表示类别，柱高是你提供的数值。比如课程 Python/SQL/C 的练习数为 12/8/10，三根柱分别表示三个类别。bar 不会自动替你按类别计数或求和；若原始表里同一课程有多行，应先汇总再画。

直方图 hist 的输入通常是一组原始数值观测。它先把连续数轴分成区间，再统计每个区间中落入多少观测。因此横轴是数值区间，不是任意类别；相邻区间的顺序与宽度有实际意义。

比较：
- “各门课完成多少题？”——类别与已有汇总值，bar。
- “同学完成作业的耗时集中在哪个范围？”——一组耗时观测，hist。
- “完成量随天数变化？”——回到 L06，优先考虑折线。

图例是图形样式与系列含义的对照，不是坐标轴标签。标题回答画了什么，轴标签回答变量和单位，图例回答颜色分别代表谁。

Figure 是整张画布，Axes 是其中的坐标系。本课用 fig, ax = plt.subplots() 显式保留它们；这不是复杂子图专题，只是避免“当前图”混淆。ax.bar 与 plt.bar 的核心用途相同。

## 二、为什么：画法会影响读者得到的结论

bar 比较的是类别间大小，类别顺序可以按业务规定，也可以按值排序，但排序时类别和值必须成对移动。柱高依赖相对共同基线的长度，本课保持纵轴从 0 起，避免截断纵轴夸大差异。

hist 展示集中程度、偏态、多峰或极端值的线索，但箱数会影响外观：箱太少掩盖细节，箱太多使图零碎。比较两个群体时，要使用共同的箱边界，否则同样颜色的柱可能并不对应同一数值范围。

频数和密度不是同一回事。density=False 时柱高是每箱计数；density=True 时归一化的是柱面积之和，不是高度之和。本课作业统一频数，不让“图看起来差不多”代替数值核对。

图例要在设置系列 label 后创建。文件输出要显式控制格式和分辨率，否则“交互窗口里好看”并不代表导出的文件清晰或完整。交付图片还应检查能否解码、标签是否被裁掉。

## 三、怎么写：类别、分箱、系列、输出四步练习

### 例题 1：三门课练习数

```python
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

names = ["Python", "SQL", "C"]
counts = [12, 8, 10]
fig, ax = plt.subplots(figsize=(6, 4))
try:
    ax.bar(names, counts, color="steelblue", edgecolor="black")
    ax.set_xlabel("Course")
    ax.set_ylabel("Exercises")
    ax.set_title("Exercises by course")
    ax.set_ylim(bottom=0)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.3)
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    print("PNG bytes:", buffer.getbuffer().nbytes)
finally:
    plt.close(fig)
```

这里用 BytesIO 在内存中输出，避免为了演示先写文件。真实文件输出只需把 buffer 换成已准备好父目录的路径，比如 out/course_counts.png。examples.py 默认只在内存中渲染；仅使用者显式传 --out-dir 才会写图。

bar(names,counts) 的每个柱高就是 counts 中对应的值。重复的字符串类别可能映射到同一个位置而互相覆盖，并不会自动累加。应该在绘图前处理重复类别；本课作业要求类别互异。

### 例题 2：耗时分布与边界手算

```python
durations = [10, 15, 20, 25, 30, 35, 40, 40]
edges = [10, 20, 30, 40]
fig, ax = plt.subplots(figsize=(6, 4))
try:
    n, bins, patches = ax.hist(
        durations, bins=edges, density=False, edgecolor="black"
    )
    ax.set_xlabel("Minutes")
    ax.set_ylabel("Count")
    ax.set_title("Completion time")
    print(n.tolist())        # [2.0, 2.0, 4.0]
    print(bins.tolist())     # [10.0, 20.0, 30.0, 40.0]
finally:
    plt.close(fig)
```

本例沿用上例的导入。边界数组长度为 4，因此形成 3 个箱：
[10,20) 有 10、15；[20,30) 有 20、25；最后一个 [30,40] 有 30、35、40、40，右端 40 也被计入。

通常除最后一箱外都是左闭右开，最后一箱两端都包含。20 只属于第二箱，不能在相邻两箱重复计数。本例 8 个观测全在范围内，计数和为 8；如果数据在指定边界以外，直方图会忽略这些观测，所以不能不加条件地认为计数和总等于原始样本数。

hist 返回三部分：n 是各箱计数或密度，bins 是实际边界，patches 是绘制对象。作业用 n 核对计数，不能把边界误当计数。

### 例题 3：两组并列柱与图例

```python
categories = ["Week1", "Week2", "Week3"]
a = [6, 8, 10]
b = [5, 9, 7]
positions = list(range(len(categories)))
width = 0.36
fig, ax = plt.subplots(figsize=(6, 4))
try:
    ax.bar([p-width/2 for p in positions], a,
           width=width, color="blue", label="A")
    ax.bar([p+width/2 for p in positions], b,
           width=width, color="orange", label="B")
    ax.set_xticks(positions)
    ax.set_xticklabels(categories)
    ax.set_xlabel("Week")
    ax.set_ylabel("Exercises")
    ax.set_title("A vs B practice")
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left", title="Group")
finally:
    plt.close(fig)
```

两次 bar 如果使用相同的位置，就会覆盖，而不是自动并列。这里类别中心为 0/1/2，A 向左移半个柱宽，B 向右移半个柱宽；轴刻度仍标在类别中心。label 为每一组命名，legend 才把名字显示出来。

### 保存规范

```python
fig.savefig(target, format="png", dpi=150, bbox_inches="tight")
```

target 可以是文件路径或二进制文件对象。format 显式指定 PNG 时，文件名应也用 .png；不要把 PNG 数据误叫成 .jpg。dpi 决定栅格输出分辨率；figsize 单位是英寸，未裁剪时 6×4 英寸、150 dpi 对应约 900×600 像素，但 tight 裁剪会改变最终像素尺寸，因此不能再断言精确为该尺寸。

bbox_inches="tight" 尝试按图形内容裁剪，帮助减少空白或标签被切的问题，但仍应检查结果。它不能自动解决重叠的长标签；必要时旋转刻度、增加画布或调整布局。

保存必须在关闭前。函数用 try/finally 关闭自己创建的 fig，保存失败时应抛出原异常，而不是声称成功；不要 close("all") 关闭别人已有的图。

## 四、易错点：逐个解释原因和修正

1. 把已汇总的 [12,8,10] 传给 hist，想得到 Python/SQL/C 三根柱。hist 会统计这三个数的分布，而不是保留类别含义；应该 bar(names,counts)。
2. 把边界个数当成箱数。三个箱需要四个边界；整数 bins=3 表示箱数，列表 bins=[...] 表示边界。两种传法不要混淆。
3. 把每个箱都当成闭区间。那会让 20/30 重复计入；遵循前述边界规则手算验证。
4. 两组柱在同一 x 位置直接重画。后画的可能盖住前面的；用数值位置加偏移，不要靠透明度掩饰布局错误。
5. label 写了却没有图例。需显式 legend；反过来先 legend 再加带 label 的图，也可能漏掉系列。
6. 只改 dpi 就认为图一定清楚。dpi 不能改善错误坐标、缺失单位、重叠文字或误导分箱；先修图形语义和布局。
7. 保存图片存在且非空就通过。文件也可能不是题定格式、内容是空轴或少一组数据；还需解码、图元、文字和返回值验收。

## 五、何时用：把问题翻译成输入契约

类别比较用 bar，原始数值分布用 hist，有序趋势用 plot，两数值变量关系用 scatter。同一组业务数据可以回答不同问题，所以图型不是由“数据来自 CSV”决定的。

当只有一个系列且标题已说明含义时，图例未必必要；有两个颜色系列时，图例应明确映射。比较多个群体分布应共用边界，并标清频数还是密度。本课不从图直接作显著性或因果结论。

机试时先拆出输入是什么、要返回什么、错误输入怎么处理、图上固定文字是什么，再写代码。不要把自动排序、创建目录、过滤越界样本等行为悄悄加入函数；以题面契约为准。

## 三道作业摘要
完整题面与固定字符串见 homework.md。
1. plot_category_bars：类别柱状图，保留输入顺序，返回原路径。
2. plot_duration_hist：给定边界画频数直方图，返回各箱计数列表及原路径；重点核对边界点与越界样本。
3. plot_grouped_bars：两组并列柱，指定偏移、颜色与图例，再按 PNG/150 dpi/tight 保存。

共同验收：正确图元、数值、固定文字、PNG 可解码；参数检查在创建图前；不修改输入、不泄漏画布、不关闭调用者图。答案约 9:30 写入 homework/answers.ipynb。

## 下节预告
L08 Pandas 描述统计与 value_counts 深练。将用统计量与频数表补充今天的图形观察。

## 官方参考
- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
