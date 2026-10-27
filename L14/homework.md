# L14 作业：算法复杂度入门：大 O 与常见对照

共 3 题；每题使用 Python 内置功能即可，独立运行，代码末尾包含验收。不得将计数公式直接作为返回计数代替实际循环；基本操作必须在真实执行位置加一。复杂度分析使用固定大小数值的常数成本模型。输入不修改，列表元素是整数，无需校验元素类型。

## 第 1 题：首次命中与比较次数

实现 first_match(values, target)，返回 (首次出现的下标, 实际值相等比较次数)。不存在返回 (-1, n)。每次执行一次 value == target，计数加一；找到后立即停止。不得调用 index、in 等隐藏搜索。

硬验收：
```python
assert first_match([], 7) == (-1, 0)
assert first_match([7], 7) == (0, 1)
assert first_match([7, 2, 7], 7) == (0, 1)
assert first_match([4, 2, 7, 7], 7) == (2, 3)
assert first_match([4, 2, 3], 7) == (-1, 3)
for n in (1, 4, 16, 64):
    assert first_match(list(range(n)), -1) == (-1, n)
```
笔试部分：分别解释最好、最坏时间与额外空间；说明为什么没有给定分布就不能断言“平均只查一半”。

## 第 2 题：符合目标和的位置对

实现 pair_sum_report(values, target)，遍历所有 i<j 的位置对，返回 (命中对数, 候选比较次数)。每个候选恰好判断一次 values[i]+values[j] == target，不提前停止，不保存对列表。重复值按不同位置分别计数。

硬验收：
```python
assert pair_sum_report([], 4) == (0, 0)
assert pair_sum_report([2], 4) == (0, 0)
assert pair_sum_report([1, 2, 3, 2], 4) == (2, 6)
assert pair_sum_report([2, 2, 2], 4) == (3, 3)
assert pair_sum_report([1, 1, 1, 1], 9) == (0, 6)
for n in (0, 1, 4, 16):
    hits, checks = pair_sum_report([0] * n, 0)
    assert hits == checks == n * (n - 1) // 2
```
笔试部分：推导候选次数的求和公式、时间紧确阶、额外空间；解释命中 0 对为什么不改变当前实现的候选次数。

## 第 3 题：前缀和与新增存储

实现 prefix_report(values)，返回 (前缀和新列表, 加法次数)。从 total=0 开始，每访问一个输入执行一次 total += value，计数加一；不得反复切片求和，不得修改原列表。

硬验收：
```python
assert prefix_report([]) == ([], 0)
assert prefix_report([5]) == ([5], 1)
assert prefix_report([3, -2, 4]) == ([3, 1, 5], 3)
source = [1, 2, 3, 4]
before = source.copy()
out, additions = prefix_report(source)
assert out == [1, 3, 6, 10]
assert additions == 4
assert source == before
assert out is not source
for n in (0, 1, 8, 32):
    out, additions = prefix_report([1] * n)
    assert out == list(range(1, n + 1))
    assert additions == n
```
笔试部分：报告时间、计入输出的额外空间、排除输出后的辅助空间。对比 [sum(values[:i+1]) for i in range(len(values))]：为什么重复求和导致总访问量为二次，而最终输出仍只有线性长度？

## 评分口径

每题：正确结果 40%、实际计数和边界 35%、复杂度解释与空间口径 25%。三题均须通过全部断言；用硬编码答案或公式伪造执行计数不合格。
