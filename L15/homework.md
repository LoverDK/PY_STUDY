# L15 作业：复杂度估题专项：循环嵌套与均摊直觉

三题均用 Python，独立运行，附验收断言和书面推导。输入 n/m 保证为非负整数；函数不得写文件。计数必须在真实循环事件处累加，不得直接用答案公式代替执行。固定大小整数采用常数成本模型。

## 1. 重置指针、步长为 2
实现 reset_by_two(n) -> int。对每个 i in range(n)，重新令 j=0；当 j<=i 时执行一次核心工作，然后 j+=2。返回核心工作总次数。无需构造列表或保存访问轨迹。
硬验收：
```python
assert reset_by_two(0) == 0
assert reset_by_two(1) == 1
assert reset_by_two(2) == 2
assert reset_by_two(3) == 4
assert reset_by_two(5) == 9
assert reset_by_two(6) == 12
for n in range(41):
    assert reset_by_two(n) == ((n + 1) ** 2) // 4
```
笔试：写出每轮工作次数 floor(i/2)+1，分 n=2q、n=2q+1 推导总数，报告时间紧确阶和额外空间。解释“步长加倍”为什么没有把二次变成线性。

## 2. 跨轮共享指针
实现 shared_pointer(n) -> tuple[int, int]。外层 i 从 0 到 n-1，j 只在外层之前初始化为 0。每轮当 j<i+2 时执行 j+=1。返回 (全部移动次数, while 条件检查次数)，每次成功和最终失败的条件求值都计一次。
硬验收：
```python
assert shared_pointer(0) == (0, 0)
assert shared_pointer(1) == (2, 3)
assert shared_pointer(2) == (3, 5)
assert shared_pointer(5) == (6, 11)
for n in range(1, 51):
    assert shared_pointer(n) == (n + 1, 2 * n + 1)
```
笔试：证明 j 的初始、终止位置与单调性；解释内层为何总计线性。若把 j=0 移入外层，每轮成功次数变为多少、总次数是多少？分析中同时算外层与条件检查。

## 3. 扩容成本报告
实现 append_costs(m) -> tuple[int, int, int, int]，返回 (写入次数, 复制次数, 总成本, 单次最大成本)。
模型：初始空表、容量1；每次追加之前若已满，逐个复制全部现有元素后容量翻倍；追加本身再写入1次。复制/写入一次各成本1，其他工作不计入本报告成本。m=0 时四项为0。不要求实际创建动态数组，但必须用循环逐个计数复制事件，不使用内置容器真实扩容行为来推测模型。
硬验收：
```python
assert append_costs(0) == (0, 0, 0, 0)
assert append_costs(1) == (1, 0, 1, 1)
assert append_costs(2) == (2, 1, 3, 2)
assert append_costs(4) == (4, 3, 7, 3)
assert append_costs(5) == (5, 7, 12, 5)
assert append_costs(8) == (8, 7, 15, 5)
assert append_costs(9) == (9, 15, 24, 9)
for m in range(1, 101):
    writes, copies, total, peak = append_costs(m)
    assert writes == m
    assert copies == 2 ** ((m - 1).bit_length()) - 1
    assert total == writes + copies
    assert m <= total < 3 * m
    assert 1 <= peak <= total
```
笔试：证明总成本 Θ(m) 和均摊 Θ(1)；说明单次最坏成本、均摊成本、随机平均成本的区别。分别报告计数模拟器的额外空间，以及被模拟动态数组的容量阶。若容量每次只增加1，复制总量为何变为 Θ(m²)？

## 评分
每题：结果和接口40%，真实计数与全部边界断言35%，推导/口径25%。仅通过断言而未给书面分析不算完整。禁止在答案中使用硬编码查表替代算法。
