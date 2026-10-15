"""L01 加课：字典 dict —— 可直接运行的示例。
对应讲义：dict_extra.md
运行：python dict_examples.py
"""


def section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    # ---------- 1. 创建 ----------
    section("1. 创建")
    empty = {}
    scores = {"Alice": 90, "Bob": 85}
    from_pairs = dict([("a", 1), ("b", 2)])
    from_zip = dict(zip(["x", "y", "z"], [10, 20, 30]))
    from_comp = {n: n * n for n in range(1, 5)}
    print("empty:", empty, "type:", type(empty).__name__)
    print("scores:", scores)
    print("from_pairs:", from_pairs)
    print("from_zip:", from_zip)
    print("from_comp:", from_comp)
    print("空 set 对比:", set(), "← 空集合必须用 set()")

    # ---------- 2. 访问 / get / setdefault ----------
    section("2. 访问、get、setdefault")
    d = {"ml": 2, "ai": 1}
    print("d['ml'] =", d["ml"])
    print("d.get('ml') =", d.get("ml"))
    print("d.get('cv') =", d.get("cv"))
    print("d.get('cv', 0) =", d.get("cv", 0))

    groups = {}
    groups.setdefault("train", []).append(1)
    groups.setdefault("train", []).append(3)
    groups.setdefault("test", []).append(2)
    print("groups:", groups)

    # ---------- 3. 增改 update ----------
    section("3. 增、改、update")
    d2 = {"a": 1}
    d2["b"] = 2
    d2["a"] = 100
    d2.update({"b": 3, "c": 4})
    print("d2:", d2)

    # ---------- 4. 删除 ----------
    section("4. 删除")
    d3 = {"a": 1, "b": 2, "c": 3}
    print("pop a ->", d3.pop("a"), "剩余:", d3)
    print("pop 缺键给默认 ->", d3.pop("z", -1))
    del d3["b"]
    print("del b 后:", d3)
    print("popitem ->", d3.popitem(), "剩余:", d3)

    # ---------- 5. 遍历与排序 ----------
    section("5. keys / values / items 与排序")
    cnt = {"ml": 2, "ai": 1, "stat": 3}
    print("keys:", list(cnt.keys()))
    print("values:", list(cnt.values()))
    print("items:", list(cnt.items()))
    print("按键字典序:")
    for k in sorted(cnt.keys()):
        print(" ", k, cnt[k])
    print("按值降序，值同按键升序:")
    for k, v in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
        print(" ", k, v)

    # ---------- 6. 成员与长度 ----------
    section("6. in 与 len")
    print("'ml' in cnt:", "ml" in cnt)
    print("2 in cnt.values():", 2 in cnt.values())
    print("len:", len(cnt))

    # ---------- 7. 嵌套 ----------
    section("7. 嵌套字典")
    students = {
        "001": {"name": "Alice", "score": 90},
        "002": {"name": "Bob", "score": 85},
    }
    print("001 name:", students["001"]["name"])
    print("缺学号安全取:", students.get("003", {}).get("name", "NA"))
    students.setdefault("003", {})["name"] = "Cara"
    students["003"]["score"] = 88
    print("students:", students)

    # ---------- 8. 计数模式 ----------
    section("8. 计数 / 过滤 / 分组")
    words = ["ml", "ai", "ml", "stat", "ai", "ml"]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    print("freq:", freq)
    ge2 = sorted([w for w, c in freq.items() if c >= 2])
    print("出现>=2:", ge2)

    pairs = [("train", 1), ("test", 2), ("train", 3)]
    bucket = {}
    for g, x in pairs:
        bucket.setdefault(g, []).append(x)
    print("分组:", bucket)

    # ---------- 9. 浅拷贝陷阱 ----------
    section("9. 赋值是引用 vs copy")
    a = {"x": 1}
    b = a
    b["x"] = 9
    print("同引用 a:", a)

    a = {"x": 1}
    b = a.copy()
    b["x"] = 9
    print("copy 后 a:", a, "b:", b)

    print("\n全部示例跑完。对照 dict_extra.md 看注释与易错点。")


if __name__ == "__main__":
    main()
