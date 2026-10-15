#!/usr/bin/env python3
"""L04 NumPy 课堂示例：可直接运行。"""
import numpy as np


def section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def demo_create() -> None:
    section("1. 创建与属性")
    x = np.array([10, 20, 30])
    print("x =", x, "| shape", x.shape, "| ndim", x.ndim, "| dtype", x.dtype)
    print("zeros:\n", np.zeros((2, 3)))
    print("arange:", np.arange(0, 10, 2))
    print("linspace:", np.linspace(0, 1, 5))
    M = np.array([[1, 2, 3], [4, 5, 6]])
    print("M shape", M.shape, "M[1,2]=", M[1, 2])


def demo_slice_reshape() -> None:
    section("2. 切片与 reshape")
    a = np.arange(10)
    print("a[2:7] =", a[2:7])
    print("a[::2] =", a[::2])
    M = np.arange(12).reshape(3, 4)
    print("M =\n", M)
    print("第0行:", M[0, :])
    print("第1列:", M[:, 1])
    print("子块 M[0:2,1:3]=\n", M[0:2, 1:3])
    print("reshape(2,-1)=\n", np.arange(12).reshape(2, -1))


def demo_broadcast() -> None:
    section("3. 广播")
    col = np.array([[1], [2], [3]])
    row = np.array([[10, 20, 30, 40]])
    print("col + row =\n", col + row)
    X = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    mu = X.mean(axis=0)
    print("列均值:", mu)
    print("X - mu =\n", X - mu)


def demo_stats() -> None:
    section("4. 统计与 axis")
    M = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)
    print("sum all:", M.sum())
    print("sum axis=0 (按列):", M.sum(axis=0))
    print("sum axis=1 (按行):", M.sum(axis=1))
    print("mean axis=0:", M.mean(axis=0))
    print("std axis=0:", M.std(axis=0))


def demo_boolean() -> None:
    section("5. 布尔索引")
    scores = np.array([55, 72, 91, 60, 48])
    mask = scores >= 60
    print("mask:", mask)
    print("及格:", scores[mask])
    print("及格平均:", scores[scores >= 60].mean())
    M = np.arange(12).reshape(3, 4)
    print("偶数元素:", M[M % 2 == 0])
    print("区间过滤:", M[(M > 2) & (M < 8)])


def demo_pitfalls() -> None:
    section("6. 易错对照：视图")
    a = np.arange(5)
    b = a[1:4]
    b[0] = 999
    print("改切片后 a =", a, "（被连带修改）")
    a2 = np.arange(5)
    c = a2[1:4].copy()
    c[0] = 999
    print("用 copy 后 a2 =", a2, "（保持原样）")


def main() -> None:
    demo_create()
    demo_slice_reshape()
    demo_broadcast()
    demo_stats()
    demo_boolean()
    demo_pitfalls()
    print("\n[L04 examples OK]")


if __name__ == "__main__":
    main()
