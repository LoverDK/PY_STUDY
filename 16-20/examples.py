"""16-20综合案例：输入内嵌，运行只打印，不读写文件。"""
from io import StringIO
import math
import pandas as pd

DATA = """order_id,region,amount,status
A,East,20,paid
B,West,40,paid
A, East ,30,paid
C,North,50,cancelled
D,East,bad,paid
"""


def report(text):
    raw = pd.read_csv(StringIO(text), dtype="string")
    required = ["order_id", "region", "amount", "status"]
    if set(required) - set(raw.columns):
        raise ValueError("缺少必需列")
    df = raw[required].copy()
    for col in ("order_id", "region", "status"):
        df[col] = df[col].str.strip().replace("", pd.NA)
    df["status"] = df["status"].str.lower()
    df = df.dropna(subset=["order_id"]).drop_duplicates("order_id", keep="last")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    valid = (
        df["region"].notna()
        & df["amount"].notna()
        & df["amount"].ge(0)
        & df["amount"].lt(float("inf"))
        & df["status"].eq("paid")
    ).fillna(False)
    paid = df.loc[valid].copy()
    summary = (
        paid.groupby("region", as_index=False).agg(revenue=("amount", "sum"))
        .sort_values(["revenue", "region"], ascending=[False, True])
        .reset_index(drop=True)
    )
    return paid, summary


def checked_score(text):
    value = float(text)
    if not math.isfinite(value) or not 0 <= value <= 100:
        raise ValueError("分数必须是有限0–100数值")
    return value


def main():
    paid, summary = report(DATA)
    assert paid["order_id"].tolist() == ["B", "A"]
    assert summary["region"].tolist() == ["West", "East"]
    assert summary["revenue"].tolist() == [40, 30]
    assert summary["revenue"].sum() == paid["amount"].sum() == 70
    assert report("order_id,region,amount,status\n")[1].empty
    latest_bad = "order_id,region,amount,status\nA,East,5,paid\nA,East,bad,paid\n"
    assert report(latest_bad)[0].empty
    rows = [[0] * 3 for _ in range(2)]
    rows[0][0] = 1
    assert rows[1][0] == 0
    assert checked_score(" 85 ") == 85
    for invalid in ("bad", "nan", "inf", "-1", "101"):
        try:
            checked_score(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("无效分数应拒绝")
    print("16-20 综合自检通过；地区收入：")
    print(summary.to_string(index=False))
    print("图表指令：bar；Region / Revenue (CNY)；y从0开始")


if __name__ == "__main__":
    main()
