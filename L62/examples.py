"""L62：先看划分，再看训练与测试，最后计算指标。只用Pandas。"""
import pandas as pd

# 第1段：前4条是L61的数据，后8条是本课另留的测试记录。
table = pd.DataFrame({
    "id": list(range(12)),
    "weight": [100., 120., 140., 160., 110., 130., 150., 170., 90., 125., 145., 180.],
    "kind": [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
})
train = table.iloc[:4].copy()
test = table.iloc[4:].copy()
print("训练ID:", train["id"].tolist())
print("测试ID:", test["id"].tolist())

# 第2段：仍用L61的方法，只根据训练记录选参数。
candidates = [110., 130., 150.]
best_threshold = None
best_errors = len(train) + 1
for threshold in candidates:
    errors = 0
    for i in range(len(train)):
        prediction = 1 if train.iloc[i]["weight"] > threshold else 0
        if prediction != train.iloc[i]["kind"]:
            errors += 1
    print("训练候选:", threshold, "错分:", errors)
    if errors < best_errors:
        best_threshold = threshold
        best_errors = errors
print("固定选中的阈值:", best_threshold)

# 第3段：参数固定后才预测测试记录，不再根据测试答案修改它。
y_true = test["kind"].tolist()
y_pred = []
for weight in test["weight"]:
    prediction = 1 if weight > best_threshold else 0
    y_pred.append(prediction)
print("测试真实:", y_true)
print("测试预测:", y_pred)

# 第4段：逐条归入四格。状态输出顺序为TN、FP、FN、TP。
tn = fp = fn = tp = 0
trace = []
for i in range(len(y_true)):
    actual = y_true[i]
    predicted = y_pred[i]
    if actual == 1 and predicted == 1:
        tp += 1
        bucket = "TP"
    elif actual == 0 and predicted == 1:
        fp += 1
        bucket = "FP"
    elif actual == 1 and predicted == 0:
        fn += 1
        bucket = "FN"
    else:
        tn += 1
        bucket = "TN"
    row = (i, actual, predicted, bucket, tn, fp, fn, tp)
    trace.append(row)
    print(row)

# 第5段：分母为0时，本课约定该指标记0，并报告原因。
accuracy = (tp + tn) / len(y_true)
precision = tp / (tp + fp) if tp + fp > 0 else 0.0
recall = tp / (tp + fn) if tp + fn > 0 else 0.0
f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn > 0 else 0.0
print("混淆矩阵:", [[tn, fp], [fn, tp]])
print("accuracy/precision/recall/F1:", accuracy, precision, recall, f1)

# 读完主线再看自检。
assert train.shape == (4, 3) and test.shape == (8, 3)
assert set(train["id"]).isdisjoint(set(test["id"]))
assert set(train["id"]) | set(test["id"]) == set(table["id"])
assert best_threshold == 130. and best_errors == 0
assert y_pred == [0, 0, 1, 1, 0, 0, 1, 1]
assert (tn, fp, fn, tp) == (3, 1, 1, 3)
assert [row[3] for row in trace] == ["TN", "FN", "FP", "TP", "TN", "TN", "TP", "TP"]
assert accuracy == precision == recall == f1 == 0.75
assert int(130. > best_threshold) == 0
print("主例与ID不重不漏自检通过")
