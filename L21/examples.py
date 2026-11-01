"""L21 数组与字符串基础操作：只在内存运行，不读写文件。"""
from itertools import product


def first_max(values):
    if not values:
        return None
    best, index = values[0], 0
    for i in range(1, len(values)):
        if values[i] > best:
            best, index = values[i], i
    return best, index


def interval_sum(values, left, right):
    if not 0 <= left <= right <= len(values):
        raise ValueError("需要0 <= left <= right <= n")
    total = 0
    for i in range(left, right):
        total += values[i]
    return total


def insert_at(values, pos, value):
    if not 0 <= pos <= len(values):
        raise ValueError("插入位置越界")
    values.append(value)
    for j in range(len(values) - 1, pos, -1):
        values[j] = values[j - 1]
    values[pos] = value


def replace_char(text, old, new):
    if len(old) != 1 or len(new) != 1:
        raise ValueError("old/new必须各为一个Python字符")
    parts = []
    for char in text:
        parts.append(new if char == old else char)
    return "".join(parts)


def self_check():
    assert first_max([]) is None
    assert first_max([-9, -2, -2]) == (-2, 1)
    assert interval_sum([3, -2, 7, 7], 1, 3) == 5
    assert interval_sum([], 0, 0) == 0
    assert replace_char("a b a", "a", "x") == "x b x"
    assert replace_char("", "a", "x") == ""
    assert replace_char("中文a", "a", "中") == "中文中"
    # 穷举长度0至4、取值-1/0/1的小数组，与独立内置结果对照。
    for n in range(5):
        for items in product((-1, 0, 1), repeat=n):
            a = list(items)
            before = a.copy()
            expected = (max(a), a.index(max(a))) if a else None
            assert first_max(a) == expected
            for left in range(n + 1):
                for right in range(left, n + 1):
                    assert interval_sum(a, left, right) == sum(a[left:right])
            assert a == before
            for pos in range(n + 1):
                b = a.copy()
                assert insert_at(b, pos, 9) is None
                assert b == a[:pos] + [9] + a[pos:]
    for left, right in [(-1, 0), (2, 1), (0, 3)]:
        try:
            interval_sum([1, 2], left, right)
        except ValueError:
            pass
        else:
            raise AssertionError("非法区间应拒绝")
    for pos in (-1, 3):
        a = [1, 2]
        try:
            insert_at(a, pos, 9)
        except ValueError:
            assert a == [1, 2]
        else:
            raise AssertionError("非法插入应拒绝")


def main():
    self_check()
    print("L21全部边界、输入不变性与小规模穷举检查通过")
    a = [3, -2, 7, 7]
    print("首次最大值:", first_max(a))
    print("[1,3)区间和:", interval_sum(a, 1, 3))
    b = a.copy()
    insert_at(b, 1, 9)
    print("插入后:", b)
    print("字符替换:", replace_char("a b a", "a", "x"))


if __name__ == "__main__":
    main()
