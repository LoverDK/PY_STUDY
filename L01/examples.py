"""L01 quick review examples. Run: python examples.py"""

def demo_io_and_parse():
    line = "10 20 30"
    nums = list(map(int, line.split()))
    print("parsed:", nums, "sum=", sum(nums))


def demo_containers():
    words = ["ml", "ai", "ml", "stat"]
    uniq = set(words)
    cnt = {}
    for w in words:
        cnt[w] = cnt.get(w, 0) + 1
    print("unique:", uniq)
    print("count:", cnt)


def demo_comprehension():
    xs = range(8)
    print([x for x in xs if x % 2 == 0])
    print(["E" if x % 2 == 0 else "O" for x in xs])


if __name__ == "__main__":
    demo_io_and_parse()
    demo_containers()
    demo_comprehension()
