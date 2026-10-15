# L02 练习（考研/期末风格 · 语法快复）

不要用 pandas/numpy。标准输入输出或按题目写函数均可，验收以样例为准。

## 练习 1：阶乘（函数）

写函数 `fact(n)`，返回 n!（n≥0；约定 0!=1）。主程序读入一行整数 n，打印 `fact(n)`。

**样例输入**：
```text
5
```

**样例输出**：
```text
120
```

**验收**：必须定义函数；可用循环或递归；n=0 输出 1。

---

## 练习 2：统计非空行

假设已有文本内容（可用列表模拟「文件的每一行」）。写函数 `count_nonempty(lines)`：输入字符串列表，返回去掉首尾空白后非空的行数。

主程序：第一行整数 m，随后 m 行文本；把这 m 行放进列表，打印 `count_nonempty(...)`。

**样例输入**：
```text
4
hello

  world

```

**样例输出**：
```text
2
```

**验收**：空行、只有空格的行都不计数；必须写函数。

---

## 练习 3：Student 类

定义类 `Person`，`__init__(self, name)`，方法 `hello(self)` 返回 `I am {name}`。

定义子类 `Student(Person)`，`__init__(self, name, sid)`，覆盖 `hello` 返回 `Student {name} id={sid}`。

主程序：读入一行 `name sid`（空格分隔），构造 `Student`，打印 `hello()`。

**样例输入**：
```text
Qiu 2026001
```

**样例输出**：
```text
Student Qiu id=2026001
```

**验收**：必须有继承；`Student` 使用父类或 `super` 保存 name（推荐）。

---

## 思路提示

1. 循环乘或 `if n<=1: return 1`
2. `sum(1 for ln in lines if ln.strip())`
3. `class Student(Person):` + `super().__init__(name)`
