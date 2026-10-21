# L09 Pandas 多条件过滤与 loc/iloc 精熟

阶段 A，交付日期 2026-10-21。前课 L08；下课 L10 Pandas apply / map / 自定义列。

| 文件 | 内容 |
|---|---|
| notes.md | 五段详讲、四组例题和易错点 |
| chat_delivery.md | 完整课堂稿 |
| examples.py | 以内存 CSV 演示并带断言，不写文件 |
| data/candidates.csv | 课堂与练习数据 |
| homework.md | 三道题的接口、边界与硬验收 |
| homework/answers.ipynb | 占位：约 9:30 写标准答案 |

依赖 Python 3 与 pandas。学习者可运行 `python L09/examples.py`；脚本只读取内嵌字符串并输出终端结果，不写磁盘。

本课核心：布尔掩码与括号、`loc` 的标签语义、`iloc` 的位置语义、筛选后保留原索引。答案文件当前只是占位。
