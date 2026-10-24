"""L11 examples. In-memory only; no file reads or writes."""
import pandas as pd
from pandas.testing import assert_frame_equal

def main():
    raw = pd.Series(["2026-10-24","bad",None,"2026-02-30"],dtype="object")
    dates = pd.to_datetime(raw,format="%Y-%m-%d",errors="coerce")
    assert (raw.notna() & dates.isna()).tolist() == [False,True,False,True]
    assert dates.dt.dayofweek.iloc[0] == 5
    delta = pd.Timestamp("2026-10-24 01:00:00")-pd.Timestamp("2026-10-23 23:00:00")
    assert delta.total_seconds()/3600 == 2 and delta.days == 0

    df = pd.DataFrame({"student":["A","B","C","D"],"score":[90,90,95,90],
                       "minutes":[30,20,25,20]},index=["r8","r2","r9","r1"])
    before = df.copy(deep=True)
    work = df.copy()
    work["_pos"] = range(len(work))
    ranked = work.sort_values(["score","minutes","_pos"],ascending=[False,True,True]).drop(columns="_pos")
    assert ranked["student"].tolist() == ["C","B","D","A"]
    assert_frame_equal(df,before)

    events = pd.DataFrame({
        "order_id":["A","B","A","B","A"],
        "updated_at":["2026-10-23 09:00:00","2026-10-24 08:00:00",
                      "2026-10-24 10:00:00","bad","2026-10-24 10:00:00"],
        "amount":[10.0,20.0,15.0,99.0,18.0],
    },index=["e1","e2","e3","e4","e5"])
    before_events = events.copy(deep=True)
    work = events.copy()
    work["updated_at"] = pd.to_datetime(work["updated_at"],format="%Y-%m-%d %H:%M:%S",errors="coerce")
    work["_pos"] = range(len(work))
    latest = (work.loc[work["updated_at"].notna()]
              .sort_values(["updated_at","_pos"],ascending=[True,True])
              .drop_duplicates(subset=["order_id"],keep="last")
              .sort_values("order_id").drop(columns="_pos"))
    assert latest.index.tolist() == ["e5","e2"]
    assert latest["amount"].tolist() == [18.0,20.0]
    assert_frame_equal(events,before_events)
    times = pd.Series(pd.to_datetime(["2026-10-24 00:00:00","2026-10-24 23:59:59","2026-10-25 00:00:00"],format="%Y-%m-%d %H:%M:%S"))
    assert ((times>=pd.Timestamp("2026-10-24")) & (times<pd.Timestamp("2026-10-25"))).tolist() == [True,True,False]
    strict = pd.Series(["2024-02-29","2026-02-29","2026-1-2",None],dtype="object")
    shape_ok = strict.str.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}",na=False)
    checked = pd.to_datetime(strict.where(shape_ok),format="%Y-%m-%d",errors="coerce")
    assert checked.notna().tolist() == [True,False,False,False]
    assert pd.to_datetime(pd.Series([],dtype="object"),format="%Y-%m-%d",errors="coerce").empty
    all_bad = pd.to_datetime(pd.Series(["bad",None]),format="%Y-%m-%d",errors="coerce")
    assert all_bad.isna().all()
    print("Ranking:",ranked["student"].tolist())
    print("Latest orders:")
    print(latest)
    print("L11 example assertions passed")

if __name__ == "__main__":
    main()
