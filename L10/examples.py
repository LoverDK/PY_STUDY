"""L10 classroom examples. In-memory only; no file writes."""
import pandas as pd
from pandas.testing import assert_frame_equal

def course_name(value):
    if pd.isna(value):
        return "Missing"
    return {"PY": "Python", "SQL": "SQL"}.get(value, "Unknown")

def grade(value):
    if pd.isna(value):
        return "Missing"
    if value >= 90:
        return "Excellent"
    if value >= 60:
        return "Pass"
    return "Fail"

def shipping(row):
    if pd.isna(row["price"]) or pd.isna(row["qty"]):
        return float("nan")
    return 0.0 if row["price"]*row["qty"] >= 50 else 5.0

def main():
    codes = pd.Series(["PY", "SQL", "X", None], index=["s1","s2","s3","s4"], dtype="object")
    names = codes.map(course_name)
    assert names.tolist() == ["Python","SQL","Unknown","Missing"]
    scores = pd.Series([59,60,89,90,None], dtype="float64")
    expected = ["Fail","Pass","Pass","Excellent","Missing"]
    assert scores.map(grade).tolist() == expected
    assert scores.apply(grade).tolist() == expected
    assert pd.Series([], dtype="object").map(course_name).empty

    orders = pd.DataFrame({"price":[10.0,20.0,None],"qty":[2,3,1]}, index=["o3","o1","o8"])
    before = orders.copy(deep=True)
    result = orders.assign(
        amount=lambda d: d["price"]*d["qty"],
        fee=lambda d: d["amount"]*0.05,
    )
    assert result["amount"].iloc[:2].tolist() == [20.0,60.0]
    assert pd.isna(result["amount"].iloc[2])
    result["shipping"] = result.apply(shipping, axis=1)
    assert result["shipping"].iloc[:2].tolist() == [5.0,0.0]
    assert pd.isna(result["shipping"].iloc[2])
    result["bonus"] = pd.Series([7,3], index=["o1","o3"])
    assert result["bonus"].iloc[:2].tolist() == [3.0,7.0]
    assert pd.isna(result["bonus"].iloc[2])
    assert_frame_equal(orders,before)
    numeric = pd.DataFrame({"a":[1,2],"b":[10,20]})
    assert numeric.apply(lambda col: col.max()-col.min(),axis=0).tolist() == [1,10]
    empty = orders.iloc[:0].copy()
    empty["shipping"] = pd.Series(index=empty.index,dtype="float64")
    assert empty.empty and str(empty["shipping"].dtype) == "float64"
    print(names)
    print(result)
    print("L10 example assertions passed")

if __name__ == "__main__":
    main()
