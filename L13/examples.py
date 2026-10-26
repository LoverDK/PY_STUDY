"""L13 NumPy+Pandas 联用小卷：读表、校验、数组统计。"""

from pathlib import Path

import numpy as np
import pandas as pd

SCORE_COLUMNS = ["quiz", "midterm", "final"]
WEIGHTS = np.array([0.20, 0.30, 0.50], dtype=float)


def validate_scores(df: pd.DataFrame) -> None:
    """验证结构、主键、数值类型与分数范围；失败时给出明确错误。"""
    required = {"student_id", "name", *SCORE_COLUMNS}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"缺少必需列: {sorted(missing)}")
    if df["student_id"].isna().any() or df["student_id"].duplicated().any():
        raise ValueError("student_id 不得缺失且必须唯一")

    for column in SCORE_COLUMNS:
        converted = pd.to_numeric(df[column], errors="coerce")
        newly_invalid = df[column].notna() & converted.isna()
        if newly_invalid.any():
            rows = df.index[newly_invalid].tolist()
            raise ValueError(f"{column} 含非数值内容，行索引: {rows}")
        df[column] = converted

    score_frame = df[SCORE_COLUMNS]
    out_of_range = ((score_frame < 0) | (score_frame > 100)).any(axis=None)
    if out_of_range:
        raise ValueError("分数必须位于 0 到 100；缺失值可以保留")


def analyze_scores(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, float, list[str]]:
    """返回学生结果、考试均值、期末通过率、显著进步名单，不修改输入表。"""
    working = df.copy(deep=True)
    validate_scores(working)

    scores = working[SCORE_COLUMNS].to_numpy(dtype=float, copy=True)
    if scores.shape != (len(working), len(SCORE_COLUMNS)):
        raise AssertionError("成绩矩阵形状异常")

    exam_means = pd.Series(
        np.nanmean(scores, axis=0),
        index=SCORE_COLUMNS,
        name="mean",
    )

    # 加权分要求三项成绩齐全；缺一项则保留 NaN，避免擅自改变权重。
    complete = ~np.isnan(scores).any(axis=1)
    weighted = np.full(len(working), np.nan, dtype=float)
    weighted[complete] = scores[complete] @ WEIGHTS

    # 学生普通平均分忽略缺失项；若一行全缺失，则结果为 NaN。
    valid_counts = (~np.isnan(scores)).sum(axis=1)
    student_average = np.divide(
        np.nansum(scores, axis=1),
        valid_counts,
        out=np.full(len(working), np.nan, dtype=float),
        where=valid_counts > 0,
    )

    final_scores = scores[:, 2]
    valid_final = ~np.isnan(final_scores)
    final_pass_rate = (
        float(np.mean(final_scores[valid_final] >= 60))
        if valid_final.any()
        else float("nan")
    )

    midterm_scores = scores[:, 1]
    improved_mask = (
        ~np.isnan(midterm_scores)
        & ~np.isnan(final_scores)
        & ((final_scores - midterm_scores) >= 10)
    )
    improved_names = working.loc[improved_mask, "name"].tolist()

    result = working.copy()
    result["average"] = np.round(student_average, 2)
    result["weighted_score"] = np.round(weighted, 2)
    result = result.sort_values(
        ["weighted_score", "student_id"],
        ascending=[False, True],
        na_position="last",
        kind="mergesort",
    ).reset_index(drop=True)

    assert len(result) == len(df)
    assert result["student_id"].is_unique
    assert set(result["student_id"]) == set(df["student_id"])
    return result, exam_means, final_pass_rate, improved_names


def main() -> None:
    csv_path = Path(__file__).resolve().parent / "data" / "scores.csv"
    source = pd.read_csv(csv_path)
    source_before = source.copy(deep=True)

    result, exam_means, pass_rate, improved_names = analyze_scores(source)

    # analyze_scores 不得修改调用者传入的原表。
    pd.testing.assert_frame_equal(source, source_before)

    print("各考试均值（忽略缺失值）:")
    print(exam_means.round(2).to_string())
    print(f"\n期末有效考生通过率: {pass_rate:.2%}")
    print("期末比期中提高至少 10 分:", improved_names)
    print("\n按加权分排序（缺项者置后）:")
    print(
        result[
            ["student_id", "name", "average", "weighted_score"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
