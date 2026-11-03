"""L63选读：用sklearn校对手算结果，不训练模型。"""
from math import sqrt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, root_mean_squared_error

y_true = [2.0, 4.0, 6.0, 8.0]
y_pred = [3.0, 4.0, 5.0, 10.0]

mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = root_mean_squared_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
print("sklearn校对:", {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2})

assert mae == 1.0
assert mse == 1.5
assert abs(rmse - sqrt(1.5)) < 1e-12
assert abs(r2 - 0.7) < 1e-12

mean_pred = [5.0, 5.0, 5.0, 5.0]
perfect_pred = y_true
bad_pred = [20.0, 20.0, 20.0, 20.0]
assert abs(r2_score(y_true, mean_pred) - 0.0) < 1e-12
assert abs(r2_score(y_true, perfect_pred) - 1.0) < 1e-12
assert r2_score(y_true, bad_pred) < 0

# 常量真值没有可比较的离差。本课手算函数返回None；sklearn默认将完美常量预测修正为1。
assert r2_score([5.0, 5.0], [5.0, 5.0]) == 1.0
print("均值基线、完美预测、负R²与常量真值边界校对通过")
