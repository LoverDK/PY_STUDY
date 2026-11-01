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



def trace_first_max(values):
    """记录真实扫描；快照仅为教学，不改变原函数空间分析。"""
    if not values:
        return None, [("empty", None, None, None, None)]
    best, index = values[0], 0
    steps = [("init", 0, values[0], best, index)]
    for i in range(1, len(values)):
        if values[i] > best:
            best, index = values[i], i
        steps.append(("scan", i, values[i], best, index))
    return (best, index), steps


def trace_interval_sum(values, left, right):
    if not 0 <= left <= right <= len(values):
        raise ValueError("需要0 <= left <= right <= n")
    total = 0
    steps = [("init", None, None, 0, 0)]
    for i in range(left, right):
        before = total
        total += values[i]
        steps.append(("add", i, values[i], before, total))
    return total, steps


def trace_insert_at(values, pos, value):
    if not 0 <= pos <= len(values):
        raise ValueError("插入位置越界")
    steps = [("start", None, None, values.copy())]
    values.append(value)
    steps.append(("append", None, value, values.copy()))
    for j in range(len(values) - 1, pos, -1):
        source = values[j - 1]
        values[j] = source
        steps.append(("move", j, source, values.copy()))
    values[pos] = value
    steps.append(("write", pos, value, values.copy()))
    return steps


def trace_replace_char(text, old, new):
    if len(old) != 1 or len(new) != 1:
        raise ValueError("old/new必须各为一个Python字符")
    parts = []
    steps = [("init", None, None, None, [])]
    for i, char in enumerate(text):
        chosen = new if char == old else char
        parts.append(chosen)
        steps.append(("append", i, char, chosen, parts.copy()))
    return "".join(parts), steps


def trace_checks():
    result, steps = trace_first_max([3, -2, 7, 7])
    assert result == (7, 2)
    assert [(r[1], r[2], r[3], r[4]) for r in steps] == [
        (0, 3, 3, 0), (1, -2, 3, 0), (2, 7, 7, 2), (3, 7, 7, 2)
    ]
    result, steps = trace_interval_sum([3, -2, 7, 7], 1, 3)
    assert result == 5
    assert steps == [
        ("init", None, None, 0, 0),
        ("add", 1, -2, 0, -2),
        ("add", 2, 7, -2, 5),
    ]
    a = [2, 4, 6]
    steps = trace_insert_at(a, 1, 9)
    assert [r[3] for r in steps] == [
        [2, 4, 6], [2, 4, 6, 9], [2, 4, 6, 6],
        [2, 4, 4, 6], [2, 9, 4, 6],
    ]
    assert a == [2, 9, 4, 6]
    result, steps = trace_replace_char("a b a", "a", "x")
    assert result == "x b x"
    assert [r[3] for r in steps[1:]] == ["x", " ", "b", " ", "x"]
    # 再对小数组检查trace实现与核心算法一致。
    for n in range(4):
        for items in product((-1, 0, 1), repeat=n):
            a = list(items)
            assert trace_first_max(a)[0] == first_max(a)
            for left in range(n + 1):
                for right in range(left, n + 1):
                    assert trace_interval_sum(a, left, right)[0] == interval_sum(a, left, right)
            for pos in range(n + 1):
                b, c = a.copy(), a.copy()
                trace_insert_at(b, pos, 9)
                insert_at(c, pos, 9)
                assert b == c
    assert trace_replace_char("", "a", "x")[0] == ""
    for text in ("中文a", "aaaa", " a  b ", "０1²"):
        assert trace_replace_char(text, "a", "x")[0] == replace_char(text, "a", "x")
    for function, args in (
        (replace_char, ("a", "", "x")),
        (trace_replace_char, ("a", "a", "xx")),
    ):
        try:
            function(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("应拒绝非法字符长度")


def print_walkthroughs():
    result, steps = trace_first_max([3, -2, 7, 7])
    print("\n首次最大值：(动作, i, 读到值, best, index)")
    for row in steps:
        print(row)
    print("返回", result)
    result, steps = trace_interval_sum([3, -2, 7, 7], 1, 3)
    print("\n区间和：(动作, i, 读到值, total之前, total之后)")
    for row in steps:
        print(row)
    print("返回", result)
    a = [2, 4, 6]
    print("\n原地插入：(动作, 目标位置, 写入值, 当前列表)")
    for row in trace_insert_at(a, 1, 9):
        print(row)
    print("核心insert_at返回None，修改后", a)
    result, steps = trace_replace_char("a b a", "a", "x")
    print("\n字符替换：(动作, i, 原字符, 追加字符, parts)")
    for row in steps:
        print(row)
    print("返回", repr(result))

if __name__ == "__main__":
    main()
    trace_checks()
    print("trace与讲义状态表及核心实现一致")
    print_walkthroughs()
