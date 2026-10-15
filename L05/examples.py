#!/usr/bin/env python3
"""L05 Pandas 课堂示例：缺失值、类型、分组与合并。在 L05/ 目录下运行。"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def demo_isna() -> None:
    section("1. 检测缺失 isna / notna")
    df = pd.read_csv(HERE / "scores.csv", encoding="utf-8")
    print(df)
    print("\n各列缺失数:\n", df.isna().sum())
    print("每行缺失数:", df.isna().sum(axis=1).tolist())
    print("score 非空行数:", int(df["score"].notna().sum()))


def demo_fillna_dropna() -> None:
    section("2. fillna / dropna")
    df = pd.read_csv(HERE / "scores.csv", encoding="utf-8")
    print("fillna(0) 后 score:\n", df["score"].fillna(0))
    mean_s = df["score"].mean()
    print("列均值:", mean_s)
    print("fillna(均值) 后 score:\n", df["score"].fillna(mean_s))

    s = pd.Series([1.0, None, None, 4.0])
    print("ffill:", s.ffill().tolist())

    print("\ndropna 默认（任空即删）行数:", len(df.dropna()))
    print("dropna subset=score 行数:", len(df.dropna(subset=["score"])))
    print("dropna how=all 行数:", len(df.dropna(how="all")))

    # 赋值对照
    df_wrong = df.copy()
    df_wrong["score"].fillna(0)  # 未赋值
    print("未赋值时 score 仍有缺失:", int(df_wrong["score"].isna().sum()))
    df_ok = df.copy()
    df_ok["score"] = df_ok["score"].fillna(0)
    print("赋值后 score 缺失:", int(df_ok["score"].isna().sum()))


def demo_astype() -> None:
    section("3. astype 与 to_numeric")
    df = pd.read_csv(HERE / "scores.csv", encoding="utf-8")
    print("dtypes:\n", df.dtypes)
    cleaned = df["score"].dropna()
    print("score.dropna().astype(int):", cleaned.astype(int).tolist())

    raw = pd.Series(["10", "20", "x", "30"])
    num = pd.to_numeric(raw, errors="coerce")
    print("to_numeric coerce:", num.tolist())
    print("再 fillna(0).astype(int):", num.fillna(0).astype(int).tolist())


def demo_groupby() -> None:
    section("4. groupby / agg")
    df = pd.read_csv(HERE / "scores.csv", encoding="utf-8")
    work = df.dropna(subset=["score"]).copy()
    print("按 major 均分:\n", work.groupby("major")["score"].mean())
    print("size:\n", work.groupby("major").size())
    print("count:\n", work.groupby("major")["score"].count())
    print(
        "agg 多指标:\n",
        work.groupby("major").agg(
            avg_score=("score", "mean"),
            n=("score", "count"),
            total_credits=("credits", "sum"),
        ),
    )
    print(
        "as_index=False:\n",
        work.groupby("major", as_index=False)["score"].mean(),
    )


def demo_concat_merge() -> None:
    section("5. concat / merge")
    a = pd.DataFrame({"id": [1, 2], "v": [10, 20]})
    b = pd.DataFrame({"id": [3, 4], "v": [30, 40]})
    print("concat axis=0 ignore_index:\n", pd.concat([a, b], ignore_index=True))

    c = pd.concat([a, b], axis=0)
    print("未 ignore_index 时 loc[0]:\n", c.loc[0])

    customers = pd.read_csv(HERE / "customers.csv", encoding="utf-8")
    orders = pd.read_csv(HERE / "orders.csv", encoding="utf-8")
    print("\ninner:\n", pd.merge(orders, customers, on="customer_id", how="inner"))
    print("\nleft:\n", pd.merge(orders, customers, on="customer_id", how="left"))
    print("\nouter 行数:", len(pd.merge(orders, customers, on="customer_id", how="outer")))

    # 笛卡尔膨胀
    left = pd.DataFrame({"k": [1, 1], "a": ["x", "y"]})
    right = pd.DataFrame({"k": [1, 1], "b": ["p", "q"]})
    print("一对多×一对多 → 行数:", len(pd.merge(left, right, on="k")))


def demo_exam_style() -> None:
    section("6. 课堂例题串讲")
    df = pd.read_csv(HERE / "scores.csv", encoding="utf-8")
    df = df.copy()
    df["score"] = df["score"].fillna(df["score"].mean())
    print("填均值后按专业均分:\n", df.groupby("major")["score"].mean().round(2))

    orders = pd.read_csv(HERE / "orders.csv", encoding="utf-8")
    customers = pd.read_csv(HERE / "customers.csv", encoding="utf-8")
    orders = orders.copy()
    orders["amount"] = orders["amount"].fillna(0)
    merged = pd.merge(orders, customers, on="customer_id", how="left")
    paid = merged[merged["status"] == "paid"].copy()
    # groupby 默认丢弃分组键为 NaN 的行，先标成 UNKNOWN
    paid["city"] = paid["city"].fillna("UNKNOWN")
    print(
        "paid 按 city 金额和:\n",
        paid.groupby("city", as_index=False)["amount"].sum(),
    )


def main() -> None:
    demo_isna()
    demo_fillna_dropna()
    demo_astype()
    demo_groupby()
    demo_concat_merge()
    demo_exam_style()
    print("\n[L05 examples OK]")


if __name__ == "__main__":
    main()
