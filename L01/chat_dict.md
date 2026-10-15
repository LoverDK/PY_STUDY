# 聊天稿：L01 加课 · 字典详解（给用户）

你说字典有点忘了，我在 **L01 里加了一节字典专课**（仍属考纲 a，不开新库）。本地已放进 `L01/`：

- `dict_extra.md` — 完整讲义  
- `dict_examples.py` — 直接跑  
- `dict_homework.md` — 2 道必做 + 1 道选做  

下面是课堂浓缩版；细节以 `dict_extra.md` 为准。

---

## 字典是什么

「键 → 值」映射。键必须可哈希（int/str/tuple 可以，**list/dict/set 不能当键**）。`{}` 是空**字典**；空集合是 `set()`。

## 创建

```python
d = {"ml": 2, "ai": 1}
d = dict(zip(["a", "b"], [1, 2]))
d = {x: x * x for x in range(4)}
```

## 读：下标 vs get vs setdefault

| 写法 | 缺键时 |
|------|--------|
| `d[k]` | **KeyError** |
| `d.get(k, 0)` | 返回 0（**计数首选**） |
| `d.setdefault(k, [])` | 写入默认值再返回（适合「键 → 列表」分组） |

```python
cnt[w] = cnt.get(w, 0) + 1
groups.setdefault(g, []).append(x)
```

## 改 / 删 / 遍历

- 增改：`d[k] = v`；批量 `d.update({...})`  
- 删：`d.pop(k, default)` / `del d[k]`  
- 遍历：`for k, v in d.items()`  
- 按值排序：`sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))`  
- **遍历时不要增删键**；先 `list(d.keys())`

## 必背题型：计数

```python
words = input().split()
cnt = {}
for w in words:
    cnt[w] = cnt.get(w, 0) + 1
ans = sorted([w for w, c in cnt.items() if c >= 2])
print(" ".join(ans) if ans else "NONE")
```

本阶段**不用** `collections.Counter`（大纲未列），手写即可。

## 易错（优先记住）

1. `{}` ≠ 空 set  
2. `in` 查的是**键**  
3. `b = a` 是同一张表；独立用 `a.copy()`  
4. 嵌套取值用 `d.get("id", {}).get("name", "NA")` 更安全  

## 加课作业（机试风）

1. 统计一行里**非空格字符**频次，先输出种类数，再按字符字典序每行 `字符 次数`  
2. 第一行 k，第二行单词；输出出现**恰好 k 次**的单词（字典序）；没有则 `NONE`  
3. 选做：n 行 `姓名 组别 分数`，按组输出平均分（两位小数、组别字典序）

路径：`D:\study\大三上\机器学习\python\L01\`（`dict_extra.md` 等）。先跑 `dict_examples.py`，再做加课作业。
