# L03 练习（考研/期末机试风格 · pandas）

使用本课目录下的 `sales.csv` 与 `students.json`（UTF-8）。  
允许：`import pandas as pd`。不要用 numpy/seaborn；不要手写逐行 `split` 代替 `read_csv`（除非题目明确禁止库）。

工作目录请设为 `L03/`，或在代码里用相对路径指向这两个文件。

---

## 练习 1：销售表摸底

写函数：

```python
def sales_overview(csv_path: str) -> tuple[int, int, int]:
    ...
```

要求：用 `pandas.read_csv` 读入；返回三元组 `(nrows, ncols, revenue_max)`，其中 `revenue_max` 为 `revenue` 列最大值（整数即可）。

**调用约定**（自测）：

```python
print(sales_overview("sales.csv"))
```

**样例输出**：

```text
(10, 5, 35988)
```

**验收**：

- 必须使用 `pandas.read_csv`
- 返回值类型为长度为 3 的 tuple/list，数值与样例一致
- 不得写死返回 `(10, 5, 35988)` 而不读文件

---

## 练习 2：学生及格名单

写函数：

```python
def passed_names(json_path: str) -> list[str]:
    ...
```

要求：读 `students.json`；选出 `score >= 60` 的行；按 `score` **降序**；返回这些人的 `name` 列表（从高到低）。

**调用约定**：

```python
print(passed_names("students.json"))
```

**样例输出**：

```text
['周八', '张三', '陈一', '孙七', '李四', '赵五']
```

**验收**：

- 必须用 `read_json` + 布尔过滤
- 列表长度 6；顺序必须与样例一致（先按分数降序）
- 不含「王二」「钱六」

---

## 练习 3：区域高销产品

写函数：

```python
def high_revenue_products(csv_path: str, region: str, threshold: int) -> list[str]:
    ...
```

要求：读销售 CSV；筛 `region == region` 且 `revenue >= threshold` 的行；返回这些行的 `product` 列表（**保持原表行序**，不要去重、不要排序）。

**调用约定**：

```python
print(high_revenue_products("sales.csv", "华东", 5000))
```

**样例输出**：

```text
['笔记本', '键盘']
```

**验收**：

- 条件必须同时用区域与阈值阈值
- 对样例调用结果必须完全一致
- 再自测：`high_revenue_products("sales.csv", "华北", 10000)` → `['笔记本']`

---

## 思路提示

1. `df.shape[0]`、`df.shape[1]`、`int(df["revenue"].max())`
2. `df[df["score"] >= 60].sort_values("score", ascending=False)["name"].tolist()`
3. `df[(df["region"] == region) & (df["revenue"] >= threshold)]["product"].tolist()`

布尔组合记得：`&` / `|` + 括号，不要用 `and` / `or`。
