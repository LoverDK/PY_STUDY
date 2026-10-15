# L01 加课：字典（dict）详解

**定位**：主课 L01 里 dict 只点到「计数用 `get`」。你说有点忘了，所以单独加这一篇——**详实、可当复习手册**，仍属考纲 **a**（容器），**不开新库**。  
**配套**：`dict_examples.py`（直接跑）、`dict_homework.md`（2–3 道机试题）。

---

## 0. 是什么

| 概念 | 一句话 |
|------|--------|
| **字典 dict** | 「键 → 值」的映射表；用键取到对应值 |
| **键 key** | 必须**可哈希**（int、str、tuple 等；**list / dict / set 不能当键**） |
| **值 value** | 任意对象（可以是 list、dict、甚至函数） |
| **可变** | 创建后可以增删改；变量名指向的是同一张表 |

直观类比：通讯录里「姓名 → 电话」；词频统计里「单词 → 出现次数」。

```python
# 最简形态
d = {"ml": 2, "ai": 1}
print(d["ml"])   # 2
```

**为什么要会**：机试 / 期末最爱考「词频、分组、映射替换、嵌套表」；DSBA **a** 明确写了字典。后面 Pandas 的「列名 → 列」也是同一思维。

---

## 1. 怎么创建

### 1.1 字面量（最常用）

```python
empty = {}                    # 空字典（注意：不是 set；空 set 是 set()）
scores = {"Alice": 90, "Bob": 85}
mixed = {1: "one", "two": 2, (3, 4): "tuple_key"}  # 键类型可以混，但别为难自己
```

### 1.2 `dict(...)` 构造

```python
# 关键字参数：键必须是合法标识符
a = dict(x=1, y=2)            # {'x': 1, 'y': 2}

# 键值对序列
b = dict([("a", 1), ("b", 2)])

# 从两个序列 zip
keys = ["a", "b", "c"]
vals = [1, 2, 3]
c = dict(zip(keys, vals))     # {'a': 1, 'b': 2, 'c': 3}
```

### 1.3 字典推导式（过滤 / 变换时很香）

```python
nums = [1, 2, 3, 4]
sq = {x: x * x for x in nums}                 # {1:1, 2:4, 3:9, 4:16}
even_sq = {x: x * x for x in nums if x % 2 == 0}  # {2:4, 4:16}
```

**易错**：`{}` 是空 **dict**，不是空 set。空集合必须写 `set()`。

---

## 2. 怎么访问

### 2.1 下标 `d[key]`

```python
d = {"ml": 2, "ai": 1}
print(d["ml"])     # 2
# print(d["cv"])   # KeyError：键不存在会炸
```

### 2.2 `get`：键不存在时给默认值（**计数题首选**）

```python
d = {"ml": 2}
print(d.get("ml"))          # 2
print(d.get("cv"))          # None（默认）
print(d.get("cv", 0))       # 0  ← 计数时几乎总用这个
```

| 写法 | 键存在 | 键不存在 |
|------|--------|----------|
| `d[k]` | 返回值 | **抛 KeyError** |
| `d.get(k)` | 返回值 | `None` |
| `d.get(k, default)` | 返回值 | `default` |

### 2.3 `setdefault`：不存在就写入默认值再返回

```python
d = {}
# 想保证 d["group"] 一定是 list，再往里 append
d.setdefault("group", []).append("Alice")
d.setdefault("group", []).append("Bob")
print(d)   # {'group': ['Alice', 'Bob']}
```

和「先判断再创建」等价，但更短：

```python
# 啰嗦版
if "group" not in d:
    d["group"] = []
d["group"].append("Alice")
```

**何时用 get / 何时用 setdefault**

| 需求 | 用 |
|------|-----|
| 只读、缺了就当 0 / "" | `get` |
| 缺了要**建好再改**（如挂一个 list） | `setdefault` |
| 确定键一定在 | `d[k]`（更快、意图也清楚） |

---

## 3. 增、改、`update`

```python
d = {"a": 1}
d["b"] = 2          # 新增
d["a"] = 100        # 修改（键已存在就覆盖）
print(d)            # {'a': 100, 'b': 2}

# 批量合并
d.update({"b": 3, "c": 4})
print(d)            # {'a': 100, 'b': 3, 'c': 4}

# update 也可用关键字或 zip
d.update(d=5)
d.update(zip(["e"], [6]))
```

**注意**：`update` 会**覆盖**同名键；不会「只补缺」除非你自己先过滤。

---

## 4. 删

```python
d = {"a": 1, "b": 2, "c": 3}

v = d.pop("a")       # 删除并返回值 → 1
print(v, d)          # 1 {'b': 2, 'c': 3}

v2 = d.pop("z", -1)  # 键不存在：给默认值就不炸 → -1
# d.pop("z")         # 不给默认 → KeyError

del d["b"]           # 只删，不返回
# del d["z"]         # KeyError

item = d.popitem()   # 删并返回某一个 (key, value)（Py3.7+ 实际是「最后插入」的那对）
d.clear()            # 清空整张表
```

| 操作 | 返回值 | 键不存在 |
|------|--------|----------|
| `del d[k]` | 无 | KeyError |
| `d.pop(k)` | 值 | KeyError |
| `d.pop(k, default)` | 值或 default | 安全 |
| `d.popitem()` | `(k, v)` | 空字典时 KeyError |
| `d.clear()` | `None` | — |

---

## 5. `keys` / `values` / `items` 与遍历

```python
d = {"ml": 2, "ai": 1, "stat": 3}

print(list(d.keys()))     # ['ml', 'ai', 'stat']  （Py3.7+ 保插入序）
print(list(d.values()))   # [2, 1, 3]
print(list(d.items()))    # [('ml', 2), ('ai', 1), ('stat', 3)]
```

### 5.1 三种常见 for

```python
# 只遍历键（默认就是键）
for k in d:
    print(k, d[k])

# 键值一起（最常用）
for k, v in d.items():
    print(k, v)

# 只要值
for v in d.values():
    print(v)
```

### 5.2 按值排序、按键排序（机试高频）

```python
# 按键字典序
for k in sorted(d.keys()):
    print(k, d[k])

# 按值从大到小，值相同再按键
for k, v in sorted(d.items(), key=lambda kv: (-kv[1], kv[0])):
    print(k, v)
```

**易错**：遍历时**不要增删键**（会 RuntimeError 或漏项）。要改结构，先 `list(d.keys())` 再循环，或新建一个新字典。

```python
# 危险
# for k in d:
#     if d[k] < 2:
#         del d[k]

# 安全：先拷贝键列表
for k in list(d.keys()):
    if d[k] < 2:
        del d[k]
```

---

## 6. 成员检测与长度

```python
d = {"a": 1}
print("a" in d)       # True  ← 查的是键
print("a" in d.keys())  # 同义，但直接 in d 更惯用
print(1 in d.values())  # True，查值（慢一点，小题无所谓）
print(len(d))           # 1
```

**易错**：`"a" in d` 查的是**键**，不是值。

---

## 7. 嵌套字典

机试里常见「学号 → {姓名, 分数}」或「分组 → 计数」。

```python
students = {
    "001": {"name": "Alice", "score": 90},
    "002": {"name": "Bob", "score": 85},
}

print(students["001"]["name"])          # Alice
print(students.get("003", {}).get("name", "NA"))  # 层层 get，防 KeyError

# 动态往嵌套里加
students.setdefault("003", {})["name"] = "Cara"
students["003"]["score"] = 88
```

列表套字典也很常见（后面读 CSV 时每一行就是一个 dict）：

```python
rows = [
    {"id": 1, "tag": "ml"},
    {"id": 2, "tag": "ai"},
    {"id": 1, "tag": "ml"},
]
```

---

## 8. 核心题型：计数模式（必背）

### 8.1 单词 / 字符计数

```python
words = input().split()
cnt = {}
for w in words:
    cnt[w] = cnt.get(w, 0) + 1
# 或：cnt[w] = cnt.setdefault(w, 0) + 1  （不如 get 直观，计数优先 get）
```

### 8.2 出现 ≥2 次的键（L01 例题同型）

```python
ans = sorted([w for w, c in cnt.items() if c >= 2])
print(" ".join(ans) if ans else "NONE")
```

### 8.3 分组：键 → 列表

```python
pairs = [("train", 1), ("test", 2), ("train", 3)]
groups = {}
for g, x in pairs:
    groups.setdefault(g, []).append(x)
# {'train': [1, 3], 'test': [2]}
```

### 8.4 映射替换

```python
level = {90: "A", 80: "B", 60: "C"}  # 实际常按区间 if；这里示意「查表」
trans = {"Y": 1, "N": 0}
print(trans.get("Y", -1), trans.get("X", -1))
```

---

## 9. 易错点汇总（至少记住这些）

1. **`{}` 是 dict，空 set 是 `set()`。**  
2. **`d[k]` 缺键 → KeyError**；计数用 `d.get(k, 0)`。  
3. **键必须可哈希**：`d[[1,2]] = 1` 会 TypeError；用元组 `(1,2)` 可以。  
4. **`in` 查键不查值。**  
5. **遍历时别增删键**；先 `list(d)`。  
6. **赋值是引用**：`b = a` 两个名字同一张表；要独立副本用 `b = a.copy()`（浅拷贝）或 `copy.deepcopy`（嵌套时，本阶段知道即可）。  

```python
a = {"x": 1}
b = a
b["x"] = 9
print(a)   # {'x': 9}  ← a 也被改了

a = {"x": 1}
b = a.copy()
b["x"] = 9
print(a)   # {'x': 1}  ← 浅拷贝后顶层独立
```

7. **字典推导式里过滤 if 在后**，与列表推导式规则相同。

---

## 10. 何时用（对比表）

| 需求 | 用 dict | 更合适的别的结构 |
|------|---------|------------------|
| 关键字查值、计数、映射 | ✅ | — |
| 只要一堆不重复元素、常问「在不在」 | 可以但浪费 | **set** |
| 只要有序下标 0..n-1 | 别硬用 dict | **list** |
| 固定几个字段且不再增删键 | dict 可以 | 以后才学 namedtuple；本阶段 dict 足够 |
| 键是「区间」 | dict 直接当键难 | **if-elif** 或先离散化 |

---

## 11. 考场小贴士

1. 题干写「输出字典序」→ 对键或对结果列表 `sorted(...)`。  
2. 题干写「频次最高」→ `max(cnt.items(), key=lambda kv: kv[1])`；并列时再比键。  
3. 输入可能重复行 → 先计数再输出，别假设唯一。  
4. 空输入 / 没有任何满足条件的键 → 题目常要求输出 `NONE` 或 `0`，先看清题面。  
5. 本阶段**不要**引入 `collections.Counter`（大纲未列标准库专题）；手写 `get` 计数即可，和 L01 主课一致。

---

## 12. 本加课「记住即可」清单

- 创建：`{}` / `dict(zip(...))` / `{k: v for ...}`  
- 读：`d[k]` vs `d.get(k, default)` vs `setdefault`  
- 写：`d[k] = ...` / `update`  
- 删：`pop` / `del`  
- 遍历：`for k, v in d.items()`；排序用 `sorted(d.items(), key=...)`  
- 题型：计数、`≥k` 次过滤、分组 `setdefault(..., [])`、嵌套 `get` 链  

跑一遍 `dict_examples.py`，再做 `dict_homework.md`。
