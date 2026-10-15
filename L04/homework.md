# L04 作业（考研 / 机试风）

要求：尽量用 **NumPy** 向量化写法；不要用纯 Python 双重循环硬算（练习 3 除外可混用，但仍须出现 `np.array`）。

---

## 练习 1 · reshape 与按行求和

**函数签名**

```python
def row_sums(n_rows: int, n_cols: int) -> list[int]:
    """
    构造 0 .. n_rows*n_cols-1，reshape 成 (n_rows, n_cols)，
    返回每一行的和，类型为 Python list[int]。
    """
```

**样例**

- `row_sums(3, 4)` → `[6, 22, 38]`
- `row_sums(2, 3)` → `[3, 12]`

**验收**

1. 必须使用 `np.arange(...).reshape(...)`（或等价创建后再 `reshape`）  
2. 行和必须用 `axis=1`（或明确按行聚合），不得手写三重循环累加  
3. 返回值为 `list`，元素为 `int`

---

## 练习 2 · 布尔筛选后求均值

**函数签名**

```python
def passed_mean(scores: list[float], threshold: float = 60.0) -> str:
    """
    将 scores 转为 ndarray，筛出 >= threshold 的元素。
    若存在：返回保留两位小数的均值字符串，如 "74.33"
    若不存在：返回 "NA"
    """
```

**样例**

- `passed_mean([55, 72, 91, 60, 48])` → `"74.33"`  
  （及格：72, 91, 60；均值 74.333… → `74.33`）
- `passed_mean([40, 50, 59], 60)` → `"NA"`
- `passed_mean([60, 60], 60)` → `"60.00"`

**验收**

1. 必须出现布尔索引（如 `arr[arr >= threshold]`）  
2. 禁止用 Python `and`/`or` 连接数组条件  
3. 有及格时格式必须是恰好两位小数的字符串；无人及格必须是 `"NA"`

---

## 练习 3 · 广播：每列减均值

**函数签名**

```python
def center_columns(data: list[list[float]]) -> list[list[float]]:
    """
    data 是矩形数值表（至少 1 行 1 列）。
    转为 ndarray 后，每列减去该列均值（广播），
    返回嵌套 list（外层行、内层列），元素为 float。
    """
```

**样例**

```text
输入: [[1, 2, 3], [4, 5, 6]]
列均值: [2.5, 3.5, 4.5]
输出: [[-1.5, -1.5, -1.5], [1.5, 1.5, 1.5]]
```

**验收**

1. 必须用 `mean(axis=0)`（或等价按列均值）再与原矩阵做减法广播  
2. 不得对每个元素单独查表减「手写列均值 list」而不经过数组运算（允许最后 `.tolist()`）  
3. 结果与样例数值误差绝对值 ≤ 1e-9

---

完成三题后，对照约 15:30 写入的 `homework/answers.ipynb`。
