"""L15：实际循环计数；只打印文本，不读写文件。"""


def validate_size(n):
    if type(n) is not int or n < 0:
        raise ValueError("规模必须是非负整数")


def triangular_visits(n):
    validate_size(n)
    visits = 0
    for i in range(n):
        for _ in range(i + 1):
            visits += 1
    return visits


def pointer_counts(n, reset):
    """返回 (移动次数, while 条件检查次数)。"""
    validate_size(n)
    moves = checks = 0
    j = 0
    for i in range(n):
        if reset:
            j = 0
        while True:
            checks += 1
            if not (j <= i):
                break
            j += 1
            moves += 1
    return moves, checks


def doubling_batches(n):
    validate_size(n)
    width = 1
    work = levels = 0
    while width < n:
        for _ in range(width):
            work += 1
        levels += 1
        width *= 2
    return work, levels


def growth_model(m):
    """教学模型：初始容量1，满时翻倍，逐个计数复制事件。"""
    validate_size(m)
    capacity = 1
    size = writes = copies = peak = 0
    for _ in range(m):
        current = 0
        if size == capacity:
            for _ in range(size):
                copies += 1
                current += 1
            capacity *= 2
        size += 1
        writes += 1
        current += 1
        peak = max(peak, current)
    return writes, copies, writes + copies, peak


def self_check():
    for n in range(130):
        triangular = n * (n + 1) // 2
        assert triangular_visits(n) == triangular
        assert pointer_counts(n, True) == (triangular, triangular + n)
        assert pointer_counts(n, False) == (n, 2 * n)
        k = (n - 1).bit_length() if n > 1 else 0
        assert doubling_batches(n) == ((1 << k) - 1, k)
        w, c, total, peak = growth_model(n)
        assert w == n and total == w + c
        assert total < 3 * n if n else total == peak == 0
        if n > 0:
            assert c == (1 << ((n - 1).bit_length())) - 1
            assert peak == (1 if n == 1 else (1 << ((n - 1).bit_length() - 1)) + 1)
    assert growth_model(5) == (5, 7, 12, 5)
    for bad in (-1, 1.5, True):
        try:
            growth_model(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("非法规模应拒绝")


def main():
    self_check()
    print("L15 所有计数、边界与非法规模检查通过")
    print("n | 三角访问 | 重置移动 | 共享移动 | 分批工作 | 扩容模型")
    for n in (0, 1, 2, 5, 8, 9, 16, 17):
        print(n, triangular_visits(n), pointer_counts(n, True)[0],
              pointer_counts(n, False)[0], doubling_batches(n)[0],
              growth_model(n), sep=" | ")


if __name__ == "__main__":
    main()
