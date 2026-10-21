# L09 作业 · 多条件过滤与 loc/iloc

使用 Python 与 Pandas。三题都不得修改输入 DataFrame；返回新的 DataFrame。输入表索引唯一，列名固定。除题面声明外，不自动排序、不重置索引、不填充缺失。空结果必须保留题定列及其顺序。

公共样例表：

```python
import pandas as pd

df = pd.DataFrame(
    {
        "track": ["Python", "SQL", "Python", "C", "SQL", "Python"],
        "score": [78.0, 88.0, 92.0, 85.0, None, 88.0],
        "minutes": [25, 32, 20, 28, 18, 30],
    },
    index=["s1", "s2", "s3", "s4", "s5", "s6"],
)
```

## 1. 多条件候选人筛选

```python
def filter_candidates(
    df: pd.DataFrame,
    min_score: float,
    tracks: list[str],
    min_minutes: float,
    max_minutes: float,
) -> pd.DataFrame:
    ...
```

要求：

- 若 `min_minutes > max_minutes`，先抛 `ValueError`。
- 保留成绩非缺失且 `score >= min_score` 的行。
- `track` 必须属于 `tracks`。
- `minutes` 必须在闭区间 `[min_minutes,max_minutes]`。
- 只返回 `["track","score","minutes"]`，保留原相对顺序与原索引。
- `tracks=[]` 或无命中时返回正确结构的空 DataFrame。

样例：

```python
filter_candidates(df, 80, ["Python", "SQL"], 20, 30)
# 只返回 s3、s6
```

硬验收：下界与上界均包含；缺失成绩排除；重复的 `tracks` 不产生重复行；空方向、空表、无命中正常；区间反向在任何筛选前抛错；输入内容、索引、列顺序不变。

## 2. 标签闭区间选择

```python
def select_label_block(
    df: pd.DataFrame,
    start_label,
    stop_label,
    columns: list[str],
) -> pd.DataFrame:
    ...
```

要求：

- 必须使用 `loc` 完成核心选择。
- `start_label`、`stop_label` 必须存在，否则抛 `KeyError`。
- `columns` 中每个列名必须存在；重复列名视为非法，抛 `ValueError`。
- 按当前索引顺序，从起始标签到终止标签闭区间选择。
- 若起始标签位置在终止标签之后，返回零行但保留指定列。
- `columns=[]` 合法，返回对应行数、零列的 DataFrame。
- 不排序、不重置索引。

样例：

```python
select_label_block(df, "s2", "s4", ["score", "minutes"])
# 索引 s2、s3、s4；两端都包含
```

硬验收：闭区间端点、单行区间、反向区间、零列、缺失标签、未知列、重复列；返回列顺序严格等于 `columns`；输入不变。

## 3. 位置列表选择

```python
def take_positions(
    df: pd.DataFrame,
    row_positions: list[int],
    column_positions: list[int],
) -> pd.DataFrame:
    ...
```

要求：

- 必须使用 `iloc` 完成核心选择。
- 位置必须是 Python `int` 且不是 `bool`；非法类型抛 `TypeError`。
- 支持合法负位置：行范围 `[-len(df), len(df)-1]`，列范围 `[-df.shape[1], df.shape[1]-1]`。
- 任一位置越界时，在选择前抛 `IndexError`。
- 位置列表的顺序和重复必须原样保留；例如 `[2,0,2]` 返回第三、第一、第三行。
- 任一位置列表为空都合法，返回对应形状的 DataFrame。
- 保留选中行原索引与列标签，不重置。

样例：

```python
take_positions(df, [2, 0, -1], [1, 2])
# 行 s3、s1、s6；列 score、minutes
```

硬验收：正位置、负位置、重复与乱序、空列表、空 DataFrame、越界、bool/float/string 位置；结果值、索引及列标签准确；输入不变。

## 共同验收

- 用 `pandas.testing.assert_frame_equal` 比较结果。
- 调用前后用 `assert_frame_equal(df, original)` 确认输入未改。
- 检查返回对象不是输入本身。
- 不接受通过 `reset_index`、排序或将缺失填零“凑出”样例。
- 解释：为什么 `loc` 标签切片包含终点，而 `iloc` 遵循位置左闭右开；为什么 Series 条件用 `& | ~` 而非 `and/or/not`。

标准答案文件：`homework/answers.ipynb`。开课先放占位：“约 9:30 写标准答案”。
