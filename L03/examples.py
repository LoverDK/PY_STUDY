"""L03 pandas 读入与表结构。在 L03/ 目录运行: python examples.py"""

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def demo_read_csv_and_explore() -> None:
    section("1. read_csv + head / info / describe / shape")
    df = pd.read_csv(HERE / "sales.csv", encoding="utf-8")
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    print("dtypes:\n", df.dtypes, sep="")
    print("\nhead():")
    print(df.head())
    print("\ninfo():")
    df.info()
    print("\ndescribe():")
    print(df.describe())


def demo_read_json() -> None:
    section("2. read_json (对象数组 → DataFrame)")
    stu = pd.read_json(HERE / "students.json", encoding="utf-8")
    print(stu.head())
    print("columns:", stu.columns.tolist())


def demo_column_select() -> None:
    section("3. 列选取：单列 Series vs 多列 DataFrame")
    stu = pd.read_json(HERE / "students.json", encoding="utf-8")
    scores = stu["score"]
    print("type(stu['score']):", type(scores))
    print("mean score:", float(scores.mean()))
    sub = stu[["name", "score"]]
    print("type(stu[['name','score']]):", type(sub))
    print(sub)


def demo_boolean_filter() -> None:
    section("4. 布尔过滤 & 组合条件")
    stu = pd.read_json(HERE / "students.json", encoding="utf-8")
    passed = stu[stu["score"] >= 60]
    print("及格人数:", len(passed))
    hi_stat = stu[(stu["major"] == "统计") & (stu["score"] > 80)]
    print("统计且 >80:")
    print(hi_stat[["name", "major", "score"]])
    out = stu.loc[stu["score"] >= 60, ["name", "score"]]
    print("loc 筛行选列:")
    print(out)


def demo_pitfalls() -> None:
    section("5. 易错对照：括号与双层方括号")
    stu = pd.read_json(HERE / "students.json", encoding="utf-8")
    # 正确写法
    ok = stu[(stu["score"] >= 60) & (stu["major"] == "统计")]
    print("正确 & + 括号:\n", ok[["name", "score"]], sep="")
    ok2 = stu[["name", "score"]]
    print("正确多列:\n", ok2.head(3), sep="")
    # 演示错误会怎样（捕获）
    try:
        _ = stu["name", "score"]  # type: ignore[index]
    except KeyError as e:
        print("错误 stu['name','score'] → KeyError:", e)


def demo_sales_pipeline() -> None:
    section("6. 小流程：华东且 revenue>=5000")
    sales = pd.read_csv(HERE / "sales.csv", encoding="utf-8")
    mask = (sales["region"] == "华东") & (sales["revenue"] >= 5000)
    result = sales.loc[mask, ["date", "product", "revenue"]]
    print(result)
    print("行数:", len(result))
    print("revenue max:", int(sales["revenue"].max()))


if __name__ == "__main__":
    demo_read_csv_and_explore()
    demo_read_json()
    demo_column_select()
    demo_boolean_filter()
    demo_pitfalls()
    demo_sales_pipeline()
    print("\n[L03 examples] all sections done.")
