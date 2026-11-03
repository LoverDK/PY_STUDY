"""L63：先计算一组回归误差，再比较欠拟合、合适与过拟合的表现。"""
from math import sqrt
import pandas as pd


def regression_metrics(y_true, y_pred):
    """返回逐条明细、MAE、MSE、RMSE和R²。"""
    if len(y_true) == 0 or len(y_true) != len(y_pred):
        raise ValueError("y_true和y_pred必须非空且等长")

    rows = []
    absolute_error_sum = 0.0
    squared_error_sum = 0.0
    for i in range(len(y_true)):
        error = y_pred[i] - y_true[i]
        absolute_error = abs(error)
        squared_error = error ** 2
        absolute_error_sum += absolute_error
        squared_error_sum += squared_error
        rows.append({
            "i": i,
            "true": y_true[i],
            "pred": y_pred[i],
            "error": error,
            "abs_error": absolute_error,
            "squared_error": squared_error,
        })

    n = len(y_true)
    mae = absolute_error_sum / n
    mse = squared_error_sum / n
    rmse = sqrt(mse)

    mean_true = sum(y_true) / n
    baseline_squared_error = 0.0
    for value in y_true:
        baseline_squared_error += (value - mean_true) ** 2
    r2 = None
    if baseline_squared_error > 0:
        r2 = 1 - squared_error_sum / baseline_squared_error

    return rows, {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}


# 第一段：同一批真实值与预测值，逐项计算误差。
y_true = [2.0, 4.0, 6.0, 8.0]  # 单位：十万元
y_pred = [3.0, 4.0, 5.0, 10.0]
rows, scores = regression_metrics(y_true, y_pred)
print("逐条回归误差")
print(pd.DataFrame(rows).to_string(index=False))
print("指标:", scores)

# 第二段：同一训练集和测试集，比较三条教学规则。
train_area = [50.0, 70.0, 90.0, 110.0]
train_price = [2.0, 4.0, 6.0, 8.0]
test_area = [60.0, 80.0, 100.0, 120.0]
test_price = [3.2, 4.8, 7.1, 8.9]

def constant_rule(areas):
    return [5.0 for _ in areas]

def trend_rule(areas):
    return [area / 10 - 3 for area in areas]

memory = dict(zip(train_area, train_price))

def memory_rule(areas):
    return [memory.get(area, 5.0) for area in areas]

rules = {
    "过于简单的常数规则": constant_rule,
    "能表达总体趋势的规则": trend_rule,
    "只记训练样本的规则": memory_rule,
}

comparison = []
for name, rule in rules.items():
    train_pred = rule(train_area)
    test_pred = rule(test_area)
    _, train_scores = regression_metrics(train_price, train_pred)
    _, test_scores = regression_metrics(test_price, test_pred)
    comparison.append({
        "rule": name,
        "train_pred": train_pred,
        "test_pred": test_pred,
        "train_mae": train_scores["mae"],
        "test_mae": test_scores["mae"],
    })
print("\n三条规则的训练与测试表现")
print(pd.DataFrame(comparison).to_string(index=False))

# 读完主线再看自检。
assert [row["error"] for row in rows] == [1.0, 0.0, -1.0, 2.0]
assert scores["mae"] == 1.0
assert scores["mse"] == 1.5
assert abs(scores["rmse"] - sqrt(1.5)) < 1e-12
assert abs(scores["r2"] - 0.7) < 1e-12

assert comparison[0]["train_mae"] == 2.0
assert comparison[0]["test_mae"] == 2.0
assert comparison[1]["train_mae"] == 0.0
assert abs(comparison[1]["test_mae"] - 0.15) < 1e-12
assert comparison[2]["train_mae"] == 0.0
assert comparison[2]["test_mae"] == 2.0

assert regression_metrics([5.0], [5.0])[1]["r2"] is None
for bad_true, bad_pred in [([], []), ([1.0], []), ([1.0], [1.0, 2.0])]:
    try:
        regression_metrics(bad_true, bad_pred)
    except ValueError:
        pass
    else:
        raise AssertionError("空输入或长度不等时应拒绝")
print("\n主例、三条规则与输入边界自检通过")
