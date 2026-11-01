# L21 作业：数组与字符串基础操作
三道独立Python题。输入下标保证是整数，元素为整数/字符串按各题规定。不得写文件。每题提交实现、全部断言和时间空间分析。

## 1. delete_at(values, pos)
原地删除指定位置的元素并返回被删值。要求0<=pos<len(values)，非法时抛ValueError且原表不变。用循环将后续元素向左移动，最后pop()删除末项；不得用del、remove、pop(pos)、切片赋值或新列表替代移动。
目标：最坏O(n)时间、O(1)辅助空间（不计输入存储）。
```python
a=[4,8,6]
assert delete_at(a,1)==8
assert a==[4,6]
assert delete_at(a,0)==4
assert a==[6]
assert delete_at(a,0)==6
assert a==[]
for original,pos in [([],0),([1],-1),([1],1)]:
    a=original.copy()
    try:
        delete_at(a,pos)
    except ValueError:
        assert a==original
    else:
        raise AssertionError("需要ValueError")
a=[2,2,2]
assert delete_at(a,1)==2 and a==[2,2]
```
笔试：删除位置pos后移动多少个元素？为何从左到右移动不会覆盖尚需读取的右侧数据？

## 2. first_min(values)
返回(最小值,首次最小值下标)，空列表返回None。不得修改输入，不得使用min、sorted、sort或index；单次线性扫描，O(1)额外空间。
```python
assert first_min([]) is None
assert first_min([5])==(5,0)
assert first_min([4,-3,2,-3])==(-3,1)
assert first_min([-2,-9,-5])==(-9,1)
a=[7,7,7]
before=a.copy()
assert first_min(a)==(7,0)
assert a==before
```
笔试：写出循环不变量，解释比较条件为什么使用<而非<=，以及初始化为0为什么错误。

## 3. mask_ascii_digits(text)
返回新字符串：仅将ASCII字符0–9替换为*，其他字符（空白、中文、全角数字等）原样保留。用一次扫描收集片段再join；不得用正则或isdigit替代ASCII判断。输入字符串不变，时间O(n)，输出空间O(n)。
```python
assert mask_ascii_digits("")==""
assert mask_ascii_digits("A12 b3!")=="A** b*!"
assert mask_ascii_digits("电话:138")=="电话:***"
assert mask_ascii_digits("０1²")=="０*²"
s=" a0\n9 "
assert mask_ascii_digits(s)==" a*\n* "
assert s==" a0\n9 "
assert mask_ascii_digits("abc")=="abc"
```
笔试：为何isdigit可能不符合本题ASCII口径？为何不能s[i]="*"？构造的结果空间为何不能忽略？

## 评分
结果与边界50%，约束和输入修改契约25%，正确性说明/时间空间25%。不可用硬编码结果替代算法。
