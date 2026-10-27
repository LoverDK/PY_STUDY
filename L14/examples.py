"""L14 算法复杂度入门：精确计数，不用秒数代替增长分析。"""


def scan_max(values):
    """返回 (最大值, 值比较次数)；空输入返回 (None, 0)。"""
    if not values:
        return None, 0
    best = values[0]
    comparisons = 0
    for i in range(1, len(values)):
        comparisons += 1
        if values[i] > best:
            best = values[i]
    return best, comparisons


def count_pairs(n):
    """返回 i<j 的位置对数；非负整数 n。循环体真正累加。"""
    if type(n) is not int or n < 0:
        raise ValueError("n 必须是非负整数")
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            count += 1
    return count


def halving_steps(n):
    """每轮整除 2，直到不大于 1；返回实际轮数。"""
    if type(n) is not int or n < 0:
        raise ValueError("n 必须是非负整数")
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


def prefix_totals(values):
    """返回前缀和：线性时间，计入输出的额外空间为线性。"""
    output = []
    total = 0
    for value in values:
        total += value
        output.append(total)
    return output


def self_check():
    assert scan_max([]) == (None, 0)
    assert scan_max([5]) == (5, 0)
    assert scan_max([4, 1, 7, 3]) == (7, 3)
    assert scan_max([-8, -2, -5]) == (-2, 2)
    for n in range(65):
        assert count_pairs(n) == n * (n - 1) // 2
        expected = n.bit_length() - 1 if n else 0
        assert halving_steps(n) == expected
    original = [4, 1, 7, 3]
    assert prefix_totals(original) == [4, 5, 12, 15]
    assert original == [4, 1, 7, 3]
    assert prefix_totals([]) == []
    for bad in (-1, 1.5, True):
        for function in (count_pairs, halving_steps):
            try:
                function(bad)
            except ValueError:
                pass
            else:
                raise AssertionError("非法规模应拒绝")


def main():
    self_check()
    print("所有精确计数与边界断言通过")
    print("n | 扫描比较 | 三角位置对 | 减半轮数")
    for n in (1, 2, 4, 8, 16, 32):
        _, comparisons = scan_max(list(range(n)))
        print(n, comparisons, count_pairs(n), halving_steps(n), sep=" | ")
    print("前缀和:", prefix_totals([4, 1, 7, 3]))


if __name__ == "__main__":
    main()
