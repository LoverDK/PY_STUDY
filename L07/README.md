# L07 Matplotlib 柱状·直方图·图例与保存

阶段 A；交付日期 2026-10-17。前课 L06 Matplotlib 折线与散点入门；下课 L08 Pandas 描述统计与 value_counts 深练。

| 文件 | 用途 |
|---|---|
| notes.md | 五段详讲、例题、分箱手算及官方文档 |
| chat_delivery.md | 完整课堂稿 |
| examples.py | 三组可运行演示，默认仅内存渲染 |
| data/category_totals.csv | 类别统计样例 |
| data/durations.csv | 耗时原始观测 |
| homework.md | 三道机试题、固定接口与硬验收 |
| homework/answers.ipynb | 占位：约 9:30 写标准答案 |

依赖 Python 3 与 Matplotlib。供使用者运行：python L07/examples.py；默认输出 PNG 字节数和示例断言结果，不写图片。只有显式传 --out-dir out 才启用文件输出。Matplotlib 在使用者环境中可能维护字体缓存。本次课件交付不在本地执行绘图，也不写本地磁盘。

答案文件以 homework/answers.ipynb 为准，开课时仅占位。三题的真实路径输出行为按 homework.md 约定；图片保存参数固定 PNG/150 dpi/tight。
