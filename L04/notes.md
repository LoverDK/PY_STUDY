# L04 NumPy：数组、索引、广播与统计汇总

对应考纲 **b**（数据进入分析软件后的基本分析）。L03 已会把表读进 pandas；本课学 **向量化数值计算** 的底座——NumPy。

**今日只讲**：`np.array`、切片、`reshape`、广播、`mean`/`sum`/`std`、布尔索引。  
**明确不讲**：手写矩阵类、完整线代证明、pandas 清洗（L05）、sklearn、类型标注、venv。

---

## 1. 是什么

| 概念 | 准确定义 | 一眼识别 |
|------|----------|----------|
| **ndarray** | NumPy 的 N 维同质数组：同一 dtype，固定 shape | `type(a)` → `numpy.ndarray` |
| **dtype** | 元素类型（如 `int64`、`float64`） | `a.dtype` |
| **shape** | 各维长度元组 | `a.shape` → `(3, 4)` 表示 3 行 4 列 |
| **axis** | 「沿着哪一维做聚合」 | `axis=0` 沿行方向压成「按列汇总」；`axis=1` 按行汇总 |

```python
import numpy as np

a = np.array([1, 2, 3], dtype=float)
b = np.array([[1, 2], [3, 4]])   # shape (2, 2)
```

**与 Python list 的本质差别**：list 可混类型、嵌套随意，但数值循环慢；ndarray 要求同质、内存连续，算术与聚合可向量化（一次对整块数据运算）。

---

## 2. 为什么（考纲与考法）

考纲 **b** 写「基本分析」。机考/评估常见问法：

- 给定一维或二维数组，求某行/某列均值、总和、标准差  
- 用布尔条件筛出「及格分」再求平均  
- `reshape` 把长度为 12 的向量改成 `(3, 4)` 再按行求和  
- 利用广播给每列减均值（标准化的简化版）

卡分点几乎总是：`axis` 方向搞反、布尔条件用了 Python 的 `and`、`reshape` 元素个数对不上、把切片视图当成独立副本乱改。

---

## 3. 怎么写（简 → 繁）

### 3.1 创建与属性

```python
import numpy as np

x = np.array([10, 20, 30])
print(x.shape, x.ndim, x.dtype)   # (3,) 1 int64（平台相关）

z = np.zeros((2, 3))              # 全 0
o = np.ones((2, 3))               # 全 1
r = np.arange(0, 10, 2)           # 0,2,4,6,8（类似 range）
lin = np.linspace(0, 1, 5)        # 0~1 等分 5 个点
```

二维：

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])
print(M.shape)   # (2, 3)
print(M[1, 2])   # 6 —— 行下标 1，列下标 2
```

### 3.2 切片（左闭右开，与 list 一致）

```python
a = np.arange(10)          # 0..9
print(a[2:7])              # [2 3 4 5 6]
print(a[::2])              # 偶数下标

M = np.arange(12).reshape(3, 4)
print(M[0, :])             # 第 0 行
print(M[:, 1])             # 第 1 列
print(M[0:2, 1:3])         # 子块
```

### 3.3 reshape

总元素个数必须不变：`3*4 == 12`。

```python
v = np.arange(12)
A = v.reshape(3, 4)
B = v.reshape(2, -1)       # -1 表示「另一维自动推」→ (2, 6)
```

### 3.4 广播（broadcasting）

规则直觉：**从尾维对齐**；长度为 1 的维可以「拉伸」去匹配对方。

```python
# (3, 1) + (1, 4) → (3, 4)
col = np.array([[1], [2], [3]])      # shape (3, 1)
row = np.array([[10, 20, 30, 40]])   # shape (1, 4)
print(col + row)

# 每列减均值（简化标准化）
X = np.array([[1., 2., 3.],
              [4., 5., 6.]])
mu = X.mean(axis=0)                  # shape (3,) —— 每列均值
print(X - mu)                        # (2,3) 与 (3,) 广播
```

### 3.5 统计汇总与 axis

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]], dtype=float)

print(M.sum())            # 全体 21
print(M.sum(axis=0))      # 按列：[5. 7. 9.]  shape (3,)
print(M.sum(axis=1))      # 按行：[6. 15.]    shape (2,)
print(M.mean(axis=0))
print(M.std(axis=0))      # 默认总体标准差（ddof=0）；样本标准差用 ddof=1
```

记忆口诀：**`axis=k` 表示「把第 k 维压掉」**。二维时：

| axis | 压掉谁 | 结果含义 |
|------|--------|----------|
| `0` | 行维 | 每一列一个数 |
| `1` | 列维 | 每一行一个数 |

### 3.6 布尔索引

```python
scores = np.array([55, 72, 91, 60, 48])
mask = scores >= 60                 # [False True True True False]
print(scores[mask])                 # [72 91 60]
print(scores[scores >= 60].mean())  # 及格平均
```

二维同样：

```python
M = np.arange(12).reshape(3, 4)
print(M[M % 2 == 0])                # 抽成一维：所有偶数元素
```

---

## 4. 易错点（至少两个，含对照）

### 坑 1：`and` / `or` 不能连接数组条件

```python
# 错
# M[(M > 2) and (M < 8)]

# 对：用 & |，且每边加括号
M[(M > 2) & (M < 8)]
```

### 坑 2：`axis` 方向反了

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])
# 「每一行的和」是 axis=1 → [6, 15]
# 「每一列的和」是 axis=0 → [5, 7, 9]
```

考场若写成反的，后面依赖该结果的题会连环错。

### 坑 3：切片常常是视图（view），改切片可能改原数组

```python
a = np.arange(5)
b = a[1:4]
b[0] = 999
print(a)   # [0 999 2 3 4] —— a 也被改了
# 需要独立副本：b = a[1:4].copy()
```

### 坑 4：`reshape` 元素个数不匹配会直接报错

```python
np.arange(10).reshape(3, 4)   # ValueError：10 != 12
```

---

## 5. 何时用（对比）

| 需求 | 用 | 别用 |
|------|-----|------|
| 同质数值大块加减乘、按轴汇总 | **NumPy** | 多层 Python for |
| 带列名的表、混合类型、读 CSV | **Pandas**（L03/L05） | 硬用纯 ndarray 模拟表 |
| 少量异构对象、只做逻辑容器 | **list / dict** | 无必要转数组 |

| A | B | 怎么选 |
|---|---|--------|
| `list` 循环求和 | `np.sum` / `a.sum()` | 数值向量/矩阵用 NumPy |
| 逐元素 `if` 过滤建新 list | 布尔索引 `a[a>0]` | 条件筛选数值用掩码 |
| 手写双重循环做「每列减均值」 | 广播 `X - X.mean(0)` | 能广播就广播 |

---

## 6. 课堂例题（考研风）

**例 1** 长度为 12 的 `0..11`，改成 `(3,4)`，输出每行和（一行四个数空格分隔？本题要求打印一行三个整数）。

```python
import numpy as np
M = np.arange(12).reshape(3, 4)
print(*M.sum(axis=1).tolist())
# 输出：6 22 38
```

**例 2** 一维分数，输出及格人数与及格平均（保留 2 位小数）；若无人及格平均打印 `NA`。

```python
import numpy as np
scores = np.array([55.0, 72.0, 91.0, 60.0, 48.0])
passed = scores[scores >= 60]
print(len(passed))
print(f"{passed.mean():.2f}" if len(passed) else "NA")
```

---

## 下节预告

**L05**：Pandas 缺失值（`isna`/`fillna`/`dropna`）、类型、`groupby`/`agg`、`merge`/`concat`。
