# L02 语法快复（下）：函数 · 递归 · 文件 · 异常 · 类与继承

**对应考纲**：复旦管院 DS&BA / QFFE Python **a**（函数/参数）+ **c** 中的 OOP（快过）
**定位**：你已会这些——本课是第 2 节快复，按机试题型扫易错点，**不深挖、不开新库**。
**下节**：L03 起进入 Pandas（考纲 **b**）。

**明确不讲**：venv；魔法方法大全；`yield` 管道；类型标注；标准库专题。

---

## 1. 是什么（本课覆盖地图）

| 块 | 考场常见考法 | 你要能做到 |
|----|--------------|------------|
| 函数 | 写函数算结果；默认参数；返回多个值 | 参数顺序对、返回值用对 |
| 递归 | 阶乘、斐波那契、简单分治 | 写清出口条件，避免无限递归 |
| 文件 | 读文本行、写结果文件 | `with open`；注意编码与换行 |
| 异常 | 输入非法、文件不存在 | `try/except` 接住，给合理提示或默认 |
| 类与继承 | 简单数据类、子类扩展方法 | `__init__`、`self`、继承后调用父类 |

---

## 2. 为什么还要快复

官方 **a** 含函数与参数传递；**c** 含面向对象。机考常把「读文件 → 处理 → 写回/打印」和简单类混在一道里。快复目标：**约 30–40 分钟扫掉易错点**，把课时留给 L03 起的库。

---

## 3. 怎么写（快过 + 易错对照）

### 3.1 函数与参数

```python
def add(a, b=0):
    return a + b

def stats(xs):
    return len(xs), sum(xs)  # 多返回值 → 元组

n, s = stats([1, 2, 3])
```

**易错**：
- 默认参数不要用可变对象：`def f(a, box=[])` 会跨调用共享同一个 list。用 `None` 再在函数里新建。
- 位置参数在前，默认参数在后：`def f(a, b=1)` 对；`def f(a=1, b)` 错。

### 3.2 递归

```python
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)
```

**易错**：忘记出口条件；`n` 很大时栈溢出（机试小题 normally n 很小）。能写循环就别为炫技硬递归。

### 3.3 文件

```python
# 读
with open("data.txt", "r", encoding="utf-8") as f:
    lines = [ln.strip() for ln in f if ln.strip()]

# 写
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")
```

**易错**：忘记 `with` 导致没关文件；Windows 下中文建议显式 `encoding="utf-8"`；`read()` 一次读完 vs 按行迭代。

### 3.4 异常

```python
try:
    x = int(input())
except ValueError:
    x = 0  # 或 print("bad"); continue
```

**易错**：`except:` 裸捕会吞掉所有错，调试时难查；先捕具体异常（`ValueError`、`FileNotFoundError`）。

### 3.5 类与继承

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def hello(self):
        return f"I am {self.name}"

class Dog(Animal):
    def hello(self):
        return f"Woof, I am {self.name}"
```

**易错**：方法第一个参数必须是 `self`；子类要扩展初始化时记得 `super().__init__(...)`（本课小题若字段简单可直接在子类 `__init__` 里赋值）。

### 3.6 何时用

| 需求 | 用 | 别用 |
|------|-----|------|
| 重复逻辑 | 函数 | 复制粘贴三遍 |
| 深度很小的分治 | 递归 | 无出口的递归 |
| 读配置/数据文件 | `with open` | 假设文件一定存在还不 catch |
| 多种「同类对象」 | 类/继承 | 一堆平行全局变量 |

---

## 4. 两道带输入输出的例题

**例 1**：读入 n，输出 n!（用函数，可用递归或循环）。

```text
输入：5
输出：120
```

```python
def fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r

n = int(input())
print(fact(n))
```

**例 2**：文件 `nums.txt` 每行一个整数。写程序读入并打印总和。（演示时可用字符串模拟行。）

```python
def sum_file(path):
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            total += int(ln)
    return total
```

---

## 5. 三道练习与验收

见 `homework.md`。

**下节预告 · L03**：pandas 读 CSV/JSON、表结构、`head`/`info`/`describe`、列选取与布尔过滤。
