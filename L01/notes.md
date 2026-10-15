# L01 语法快复（上）：IO · 分支循环 · 字符串 · 容器 · 推导式

**对应考纲**：复旦管院 DS&BA / QFFE Python **a**（快过）  
**定位**：你已会这些内容——本课是 **1 节快复**，按考场题型过一遍易错点，**不深挖、不开新库**。  
**下节**：L02 函数/递归/文件/异常/类与继承；L03 起进入 Pandas 等库。

**明确不讲**：迭代器协议、`yield`、类型标注、venv、标准库专题、NumPy/Pandas。

---

## 1. 是什么（本课覆盖地图）

| 块 | 考场常见考法 | 你要能做到 |
|----|--------------|------------|
| IO | 读若干行 / 读到 EOF；格式化输出 | 正确拆分、类型转换、按行打印 |
| 分支循环 | 多条件、嵌套、`break`/`continue` | 边界（空输入、恰好 n 个）不炸 |
| 字符串 | 切片、分割、替换、大小写、判数字 | 清洗输入里的空格与大小写 |
| 容器 | list/tuple 下标；dict 计数；set 去重 | 选对容器，避免 O(n²) 乱找（复杂度细讲在 L07） |
| 列表推导式 | 过滤+变换一行写完 | 过滤 `if` 与三元表达式不写反 |

---

## 2. 为什么还要快复

官方 **a** 仍写在评估范围里：机考前半或混在数据处理题里会默认为「你会」。快复目标是：**30–40 分钟内把易错点扫掉**，把课时留给 b/c/d 的库与模型。

---

## 3. 怎么写（快过 + 易错对照）

### 3.1 输入输出

```python
# 单行多个整数
n = int(input())
a, b = map(int, input().split())

# 读 n 行
rows = [input().strip() for _ in range(n)]

# 输出：空格分隔、保留小数
print(a, b)
print(f"{3.14159:.2f}")  # 3.14
```

**易错**：`input()` 得到的是 **str**；比较数字前先 `int`/`float`。空行、行末空格用 `strip()`。

### 3.2 分支与循环

```python
x = int(input())
if x >= 90:
    level = "A"
elif x >= 60:
    level = "B"
else:
    level = "C"

# 累加到 0 结束（哨兵）
s = 0
while True:
    v = int(input())
    if v == 0:
        break
    s += v
```

**易错**：`elif` 顺序；循环里修改正在遍历的 list 长度——快复阶段优先「新建结果列表」。

### 3.3 字符串

```python
s = "  Hello, ML  ".strip().lower()   # 'hello, ml'
parts = "a,b,c".split(",")            # ['a','b','c']
print("".join(parts))                 # abc
print(s.replace(" ", "_"))
print("123".isdigit(), "12a".isdigit())
```

**易错**：`s[1:3]` 左闭右开；中文与编码本题阶段用默认即可，文件编码问题放到 L03 `read_csv`。

### 3.4 四大容器（只记「何时用」）

| 类型 | 可变 | 典型用途 | 一句代码 |
|------|------|----------|----------|
| list | 是 | 有序序列、栈 | `a.append(x)` |
| tuple | 否 | 固定一对多返回 | `y, m = (2026, 10)` |
| dict | 是 | 计数、映射 | `d[k] = d.get(k, 0) + 1` |
| set | 是 | 去重、成员检测 | `set(lst)` |

```python
nums = [1, 2, 2, 3]
print(list(set(nums)))          # 去重（顺序不保证）
cnt = {}
for x in nums:
    cnt[x] = cnt.get(x, 0) + 1  # {1:1, 2:2, 3:1}
```

**易错**：`dict` 的键必须可哈希（list 不能当键）；`set` 无下标。

### 3.5 列表推导式

```python
squares = [x * x for x in range(5)]
evens = [x for x in range(10) if x % 2 == 0]           # 过滤：if 在后
labels = ["even" if x % 2 == 0 else "odd" for x in range(4)]  # 三元在前
```

**易错对照**：

| 写法 | 含义 |
|------|------|
| `[x for x in xs if cond]` | 丢掉不满足的 |
| `[a if cond else b for x in xs]` | 每个都保留，只是取值不同 |

---

## 4. 易错点汇总

1. **类型**：输入是字符串，算术前转换。  
2. **推导式 if 位置**：过滤 vs 三元不要混。  
3. **dict.get**：计数用 `get(k,0)`，避免 `KeyError`。  
4. **可变默认参数**：快复提醒一句——`def f(a=[])` 别写，下节函数课会再点。

---

## 5. 何时用（对比）

| 需求 | 用 | 不用硬上 |
|------|-----|----------|
| 去重后还要保序 | 有序去重自己写循环 / 后学工具 | 盲目 `set` 再抱怨顺序 |
| 计数 | `dict` | 两层 list 暴力扫（小题尚可，大题慢） |
| 过滤变换 | 推导式 | 无必要的四层嵌套推导 |

---

## 6. 本课「记住即可」清单

`input`/`print`/`map`/`split`/`strip`；`if-elif-else`；`for`/`while`；`list/dict/set` 基本操作；列表推导式两种 if 写法。
