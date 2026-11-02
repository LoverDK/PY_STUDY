"""L61：先运行第1段，再读第2段，最后读第3段。数据均为虚构教学数据。"""
import numpy as np
import pandas as pd

# 第1段：从熟悉的DataFrame出发。一行是一件物品，不是一个特征。
table = pd.DataFrame({
    "weight": [100.0, 120.0, 140.0, 160.0],
    "kind": [0, 0, 1, 1],
})
X = table[["weight"]].to_numpy()  # 双括号保留列：4行1列
y = table["kind"].to_numpy()      # 单列标签：长度4
print("第1段：数据")
print(table.to_string(index=False))
print("X形状:", X.shape, "y形状:", y.shape)

# 第2段：先使用人为给定的规则，不做训练。
threshold = 130.0
predictions = []
print("第2段：固定规则，weight > 130预测1，否则0")
for i in range(len(y)):
    weight = X[i, 0]
    prediction = 1 if weight > threshold else 0
    predictions.append(prediction)
    print(i, weight, int(y[i]), prediction)
print("固定规则预测:", predictions)

# 第3段：比较三条题目给定的候选规则，这才是本例的“学习”。
candidates = [110.0, 130.0, 150.0]
best_threshold = None
best_errors = len(y) + 1
print("第3段：用训练数据选规则")
for candidate in candidates:
    current_predictions = []
    errors = 0
    for i in range(len(y)):
        prediction = 1 if X[i, 0] > candidate else 0
        current_predictions.append(prediction)
        if prediction != y[i]:
            errors += 1
    print("候选:", candidate, "预测:", current_predictions, "错分:", errors)
    if errors < best_errors:
        best_threshold = candidate
        best_errors = errors
print("学到的阈值:", best_threshold)

# 阈值固定后，预测新输入。这里没有新样本的真实标签，不报告测试准确率。
new_weights = [110.0, 150.0]
new_predictions = []
for weight in new_weights:
    new_predictions.append(1 if weight > best_threshold else 0)
print("新输入:", new_weights, "预测:", new_predictions)

# 以下是可选自检区，不属于首次阅读主线。
assert X.shape == (4, 1) and y.shape == (4,)
assert predictions == [0, 0, 1, 1]
assert best_threshold == 130.0 and best_errors == 0
assert new_predictions == [0, 1]
assert int(130.0 > best_threshold) == 0  # 等于阈值时按约定预测0
assert [int(v > 130.0) for v in []] == []
assert [int(v > 130.0) for v in [140.0]] == [1]
assert [int(v > 130.0) for v in [120.0, 120.0, -1.0]] == [0, 0, 0]
assert np.array_equal(y, np.array([0, 0, 1, 1]))
print("本课数值与适用边界自检通过")
