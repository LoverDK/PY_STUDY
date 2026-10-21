"""L09 classroom examples: filtering, loc and iloc.
Uses in-memory CSV only and writes no files.
"""
from io import StringIO
import pandas as pd
from pandas.testing import assert_frame_equal

CSV_TEXT = """student,track,score,minutes
s1,Python,78,25
s2,SQL,88,32
s3,Python,92,20
s4,C,85,28
s5,SQL,,18
s6,Python,88,30
"""

def main() -> None:
    df = pd.read_csv(StringIO(CSV_TEXT), index_col="student")
    original = df.copy(deep=True)

    mask = (
        df["score"].notna()
        & (df["score"] >= 80)
        & df["track"].isin(["Python", "SQL"])
        & df["minutes"].between(20, 30, inclusive="both")
    )
    selected = df.loc[mask, ["track", "score", "minutes"]]
    expected = df.loc[["s3", "s6"], ["track", "score", "minutes"]]
    assert_frame_equal(selected, expected)

    mixed = (
        ((df["track"] == "Python") & (df["score"] >= 85))
        | ((df["track"] == "SQL") & (df["minutes"] <= 20))
    )
    assert df.index[mixed].tolist() == ["s3", "s5", "s6"]

    block = df.loc["s2":"s4", ["score", "minutes"]]
    assert block.index.tolist() == ["s2", "s3", "s4"]
    assert block.columns.tolist() == ["score", "minutes"]

    positional = df.iloc[1:4, 1:3]
    assert positional.index.tolist() == ["s2", "s3", "s4"]
    assert positional.columns.tolist() == ["score", "minutes"]

    qualified = df.loc[df["score"] >= 80, ["track", "score"]]
    first_two = qualified.iloc[:2]
    assert first_two.index.tolist() == ["s2", "s3"]

    empty = df.loc[df["score"] > 100, ["track", "score"]]
    assert empty.empty
    assert empty.columns.tolist() == ["track", "score"]

    assert_frame_equal(df, original)
    print("Selected candidates:")
    print(selected)
    print("\nLabel block:")
    print(block)
    print("\nL09 example assertions passed")

if __name__ == "__main__":
    main()
