"""L16：订单读洗筛汇。只读取课程 CSV 并打印，不写文件。"""
from io import StringIO
from pathlib import Path
import pandas as pd

COLUMNS = ["order_id", "region", "product", "quantity", "unit_price", "status"]


def clean_orders(raw):
    """先标准化键，按文件顺序保留同订单最后一行，再验证数值。"""
    missing = set(COLUMNS) - set(raw.columns)
    if missing:
        raise ValueError(f"缺少列: {sorted(missing)}")
    df = raw[COLUMNS].copy(deep=True)
    for column in ["order_id", "region", "product", "status"]:
        df[column] = df[column].astype("string").str.strip()
        df[column] = df[column].replace("", pd.NA)
    df["status"] = df["status"].str.lower()
    df = df.dropna(subset=["order_id"])
    df = df.drop_duplicates(subset=["order_id"], keep="last")
    for column in ["quantity", "unit_price"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    valid = (
        df[["region", "product", "status", "quantity", "unit_price"]].notna().all(axis=1)
        & df["quantity"].gt(0)
        & df["quantity"].mod(1).eq(0)
        & df["unit_price"].ge(0)
        & df["unit_price"].lt(float("inf"))
        & df["quantity"].lt(float("inf"))
        & df["status"].isin(["paid", "pending", "cancelled"])
    )
    clean = df.loc[valid].copy()
    clean["quantity"] = clean["quantity"].astype("int64")
    clean["amount"] = clean["quantity"] * clean["unit_price"]
    return clean.reset_index(drop=True)


def summarize_paid(clean):
    paid = clean.loc[clean["status"].eq("paid")].copy()
    summary = (
        paid.groupby("region", as_index=False, sort=True)
        .agg(order_count=("order_id", "size"),
             quantity_total=("quantity", "sum"),
             revenue=("amount", "sum"))
        .sort_values(["revenue", "region"], ascending=[False, True])
        .reset_index(drop=True)
    )
    return paid, summary


def analyze_csv(csv_text):
    # 所有列先保留文本，防止学号/订单号前导零消失。
    raw = pd.read_csv(StringIO(csv_text), dtype="string")
    before = raw.copy(deep=True)
    clean = clean_orders(raw)
    paid, summary = summarize_paid(clean)
    pd.testing.assert_frame_equal(raw, before)
    assert clean["order_id"].is_unique
    return clean, paid, summary


def self_check(csv_text):
    clean, paid, summary = analyze_csv(csv_text)
    assert clean["order_id"].tolist() == ["O01", "O03", "O02", "O06", "O07", "O10"]
    assert paid["order_id"].tolist() == ["O01", "O02", "O06", "O07"]
    assert summary["region"].tolist() == ["West", "East", "North"]
    assert summary["order_count"].tolist() == [1, 2, 1]
    assert summary["quantity_total"].tolist() == [5, 5, 2]
    assert summary["revenue"].tolist() == [100, 50, 40]
    assert paid["amount"].sum() == summary["revenue"].sum() == 190
    empty_text = ",".join(COLUMNS) + "\n"
    empty_clean, empty_paid, empty_summary = analyze_csv(empty_text)
    assert empty_clean.empty and empty_paid.empty and empty_summary.empty
    assert empty_summary.columns.tolist() == [
        "region", "order_count", "quantity_total", "revenue"
    ]
    # 最新行无效，旧有效行不能被“复活”。
    duplicate = (
        "order_id,region,product,quantity,unit_price,status\n"
        "A,East,Pen,1,10,paid\n"
        "A,East,Pen,bad,10,paid\n"
    )
    assert analyze_csv(duplicate)[0].empty
    try:
        clean_orders(pd.DataFrame({"order_id": ["A"]}))
    except ValueError:
        pass
    else:
        raise AssertionError("缺列应被拒绝")


def main():
    csv_text = (Path(__file__).resolve().parent / "data" / "orders.csv").read_text(
        encoding="utf-8"
    )
    self_check(csv_text)
    clean, paid, summary = analyze_csv(csv_text)
    print("验收通过：原始11行→清洗6行→已支付4行；收入190")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
