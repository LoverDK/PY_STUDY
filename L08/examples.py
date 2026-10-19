"""L08 classroom examples. In-memory data only; no file writes."""
from io import StringIO
from math import isclose
import pandas as pd

DEMO_CSV = "student,track,score,minutes\ns1,Python,60,10\ns2,SQL,70,15\ns3,Python,80,20\ns4,,90,25\ns5,C,,30\ns6,SQL,,40\n"

def main():
    df = pd.read_csv(StringIO(DEMO_CSV))
    score = df["score"]
    print("Numeric summary:")
    print(df[["score", "minutes"]].describe())
    assert len(score) == 6
    assert int(score.count()) == 4
    assert int(score.isna().sum()) == 2
    assert isclose(float(score.mean()), 75.0)
    assert isclose(float(score.median()), 75.0)
    assert isclose(float(score.std(ddof=1)), (500/3)**0.5)
    assert isclose(float(score.std(ddof=0)), (500/4)**0.5)
    quantiles = score.quantile([0.25, 0.5, 0.75], interpolation="linear")
    assert quantiles.tolist() == [67.5, 75.0, 82.5]

    track = df["track"]
    counts = track.value_counts()
    valid_share = track.value_counts(normalize=True)
    all_share = track.value_counts(normalize=True, dropna=False)
    print("\nCounts:", counts.to_dict())
    print("Valid denominator:", valid_share.to_dict())
    print("All-row denominator:", all_share.to_dict())
    assert int(counts.sum()) == 5
    assert isclose(float(valid_share["Python"]), 2/5)
    assert isclose(float(all_share["Python"]), 2/6)
    assert isclose(float(all_share.sum()), 1.0)

    table = counts.rename_axis("label").reset_index(name="count")
    table = table.sort_values(["count", "label"], ascending=[False, True])
    print("\nExplicit tie order:")
    print(table.reset_index(drop=True))
    assert table["label"].tolist() == ["Python", "SQL", "C"]

    skewed = pd.Series([10, 10, 10, 10, 100], dtype="float64")
    assert skewed.mean() == 28.0
    assert skewed.median() == 10.0
    single = pd.Series([None, 5], dtype="float64")
    assert pd.isna(single.std(ddof=1))
    assert single.std(ddof=0) == 0.0
    empty = pd.Series([], dtype="float64")
    assert empty.count() == 0 and pd.isna(empty.mean())
    missing = pd.Series([None, None], dtype="float64")
    assert missing.count() == 0 and pd.isna(missing.mean())
    assert len(pd.Series([], dtype="object").value_counts()) == 0
    print("\nL08 example assertions passed")

if __name__ == "__main__":
    main()
