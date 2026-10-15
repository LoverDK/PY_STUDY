# L05 作业（考研 / 机试风）

要求：用 **pandas** 完成；不要用纯 Python 双重循环扫表做分组/合并（允许最后把结果转成 list/dict）。样例数据可用本目录 CSV，也可在函数内用题面给出的 DataFrame。

---

## 练习 1 · 缺失处理后再求均值

**函数签名**

```python
def filled_score_mean(csv_path: str) -> float:
    """
    读入 scores 风格 CSV（至少含列 score）。
    将 score 列的缺失值填充为「填充前」该列非缺失均值，
    再返回填充后整列 score 的均值（Python float）。
    """
```

**样例**（对本课 `scores.csv`）

- 非缺失 score：88, 57, 91, 72, 60, 45 → 均值 68.8333…
- 两处缺失被填成该均值后，整列 8 个数的均值仍为 **68.8333…**（填均值不改变总体均值）
- 验收时用：`abs(filled_score_mean("scores.csv") - 68.8333333333) < 1e-6`

也可自造小表验证逻辑：`score = [10, None, 30]` → 填充前均值 20 → 填后 `[10,20,30]` → 返回 `20.0`。

**验收**

1. 必须出现 `isna`/`isnull` 检测或依赖 `fillna` 处理缺失（不得假装没有缺失直接 `mean` 却跳过题面要求的填充步骤）  
2. 必须用列均值（或等价：先 `mean` 再 `fillna`）填充，禁止一律填 `0`  
3. 返回值为 `float`；与正确均值绝对误差 ≤ 1e-6

---

## 练习 2 · groupby + agg

**函数签名**

```python
def major_stats(df: "pd.DataFrame") -> "pd.DataFrame":
    """
    输入至少含 major, score, credits 三列的 DataFrame。
    先删除 score 缺失的行，再按 major 聚合，返回 DataFrame，列名为：
      major, avg_score, n, total_credits
    其中 avg_score = score 均值，n = score 非缺失计数，
    total_credits = credits 求和（credits 若仍有缺失，sum 默认跳过 NaN）。
    行按 major 字母序（或默认 groupby 顺序）均可，但列名与含义必须一致。
    """
```

**样例**（用本课 `scores.csv` 读入后传入）

对 `dropna(subset=["score"])` 后的数据：

| major | avg_score | n | total_credits |
|-------|-----------|---|---------------|
| 计科 | 75.5 | 2 | 4.0 |
| 统计 | 72.5 | 2 | 6.0 |
| 金融 | 58.5 | 2 | 4.0 |

（赵五 credits 缺失，其 score=72 仍保留；该行 credits 不计入 sum，故金融 total_credits=4）

**验收**

1. 必须使用 `groupby` + `agg`（或 `groupby` 后分列 `mean`/`count`/`sum` 再拼表）  
2. 结果必须是 DataFrame，且包含列 `major, avg_score, n, total_credits`  
3. 对样例数据：计科 `n==2` 且 `abs(avg_score-75.5)<1e-9`；不得在未处理 score 缺失时把空分行算进 `n`

---

## 练习 3 · merge + 条件汇总

**函数签名**

```python
def paid_amount_by_city(orders_csv: str, customers_csv: str) -> dict[str, float]:
    """
    读入订单表与客户表。
    1) amount 缺失填 0
    2) 以 orders 为左表，按 customer_id 左连接 customers
    3) 只保留 status == "paid" 的行
    4) 按 city 对 amount 求和
    返回 dict：键为城市名（str），值为该城 paid 金额合计（float）。
    左连接后 city 仍为缺失的行：键用 "UNKNOWN"。
    """
```

**样例**（本课 `orders.csv` + `customers.csv`）

- paid 且能匹配城市：C01 上海 120.5；C02 北京 80.0；C99 无客户 → city 缺失 → UNKNOWN 200.0；C03 上海 amount 原缺失 → 0  
- 故：`{"上海": 120.5, "北京": 80.0, "UNKNOWN": 200.0}`（键顺序不限）

**验收**

1. 必须使用 `merge`/`join`，且 `how="left"`（或以 orders 为左的等价写法）  
2. 必须处理 `amount` 缺失为 0；必须过滤 `status == "paid"`  
3. 返回 `dict[str, float]`；样例上上海合计为 120.5，且包含键 `"UNKNOWN"` 值为 200.0  
4. 禁止只用 `concat(axis=1)` 冒充按键合并

---

完成三题后，对照约 15:30 写入的 `homework/answers.ipynb`。
