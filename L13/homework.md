# L13 作业：NumPy+Pandas 联用小卷

## 提交要求

- 共 3 题，每题应能独立运行。
- 默认使用 Python、Pandas、NumPy；不得手工把最终答案写死。
- 每题都要保留输入校验，并用断言完成“硬验收”。
- 缺失值口径必须写在代码注释中。

---

## 第 1 题：销售表读取与数组统计

给定 CSV 文本：

```csv
order_id,region,jan,feb,mar
O01,East,120,135,150
O02,West,90,110,105
O03,East,200,,220
O04,North,80,95,100
```

编写函数：

```python
def sales_summary(csv_text: str) -> tuple[pd.DataFrame, pd.Series]:
    ...
```

要求：

1. 用 `StringIO` 和 `pd.read_csv` 读取，不得落地临时文件。
2. 校验 `order_id` 唯一，月份列必须能转为数值且非缺失值位于 `[0, +∞)`。
3. 将 `jan/feb/mar` 转为 NumPy 数组。
4. 为每个订单计算 `quarter_total`，缺失月份按 0 计。
5. 计算各月均值，均值忽略缺失值，返回索引为 `jan/feb/mar` 的 Series。

### 硬验收

```python
result, month_mean = sales_summary(CSV_TEXT)
assert result["order_id"].tolist() == ["O01", "O02", "O03", "O04"]
assert result["quarter_total"].tolist() == [405.0, 305.0, 420.0, 275.0]
assert np.allclose(month_mean.to_numpy(), [122.5, 113.3333333333, 143.75])
assert month_mean.index.tolist() == ["jan", "feb", "mar"]
```

---

## 第 2 题：传感器有效率与告警行

给定数组，每行是一台设备，每列依次为 08:00、12:00、16:00 的温度；NaN 表示未上报：

```python
device_ids = np.array(["D1", "D2", "D3", "D4"])
temps = np.array([
    [22.0, 25.0, 27.0],
    [31.0, np.nan, 35.0],
    [18.0, 19.0, 20.0],
    [np.nan, np.nan, np.nan],
])
```

编写函数：

```python
def sensor_report(device_ids: np.ndarray, temps: np.ndarray) -> pd.DataFrame:
    ...
```

规则：

- 有效率 = 非 NaN 数量 / 3。
- 平均温度忽略 NaN；全缺失设备的平均温度为 NaN。
- 只要任一有效温度大于等于 30℃，`alert=True`。
- 返回列：`device_id, valid_rate, mean_temp, alert`，顺序与输入一致。

### 硬验收

```python
report = sensor_report(device_ids, temps)
assert report["device_id"].tolist() == ["D1", "D2", "D3", "D4"]
assert np.allclose(report["valid_rate"], [1.0, 2/3, 1.0, 0.0])
assert np.allclose(
    report["mean_temp"].iloc[:3], [74/3, 33.0, 19.0]
)
assert np.isnan(report.loc[3, "mean_temp"])
assert report["alert"].tolist() == [False, True, False, False]
```

---

## 第 3 题：成绩加权、资格筛选与稳定排名

输入 DataFrame 包含 `student_id, name, quiz, midterm, final`。编写函数：

```python
def rank_students(df: pd.DataFrame) -> pd.DataFrame:
    ...
```

规则：

1. 校验学号唯一、三项成绩均为 0–100 的数值。
2. 任一成绩缺失者 `eligible=False`，加权分为 NaN。
3. 三项齐全者按 `quiz*0.2 + midterm*0.3 + final*0.5` 计算 `weighted_score`。
4. 资格学生按加权分降序，同分按 `student_id` 升序；无资格学生置后，也按学号升序。
5. 返回新 DataFrame，不得修改输入对象。

测试数据：

```python
df = pd.DataFrame({
    "student_id": ["S03", "S01", "S04", "S02"],
    "name": ["丙", "甲", "丁", "乙"],
    "quiz": [80, 90, 70, 90],
    "midterm": [80, 80, 75, 80],
    "final": [80, 80, np.nan, 80],
})
```

### 硬验收

```python
before = df.copy(deep=True)
ranked = rank_students(df)
pd.testing.assert_frame_equal(df, before)
assert ranked["student_id"].tolist() == ["S01", "S02", "S03", "S04"]
assert ranked["eligible"].tolist() == [True, True, True, False]
assert np.allclose(ranked["weighted_score"].iloc[:3], [82.0, 82.0, 80.0])
assert np.isnan(ranked["weighted_score"].iloc[3])
assert ranked["rank"].iloc[:3].tolist() == [1, 2, 3]
assert pd.isna(ranked["rank"].iloc[3])
```

> 提示：为了让并列结果可复现，先按 `eligible`、`weighted_score`、`student_id` 排序，再生成顺序排名。