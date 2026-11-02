"""选读：会手算后，再用sklearn校对。这个文件独立运行，不训练新模型。"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# 与主例相同的12条记录，只演示另一种划分，不能把两次实验的指标混用。
X = np.array([100., 120., 140., 160., 110., 130., 150., 170., 90., 125., 145., 180.]).reshape(-1, 1)
y = np.array([0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1])
ids = np.arange(12)
X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
    X, y, ids, test_size=1/3, random_state=42, stratify=y
)
print("随机分层训练/测试形状:", X_train.shape, X_test.shape)
print("正类数:", int(y_train.sum()), int(y_test.sum()))
assert X_train.shape == (8, 1) and X_test.shape == (4, 1)
assert y_train.sum() == 4 and y_test.sum() == 2
assert set(id_train).isdisjoint(set(id_test))
assert set(id_train) | set(id_test) == set(range(12))
again = train_test_split(ids, test_size=1/3, random_state=42, stratify=y)
assert np.array_equal(again[0], id_train) and np.array_equal(again[1], id_test)

# 校对的是主例原先那8条固定测试记录，不是上面的随机测试集。
truth = [0, 1, 0, 1, 0, 0, 1, 1]
pred = [0, 0, 1, 1, 0, 0, 1, 1]
assert confusion_matrix(truth, pred, labels=[0, 1]).tolist() == [[3, 1], [1, 3]]
for score in (accuracy_score, precision_score, recall_score, f1_score):
    assert abs(score(truth, pred) - 0.75) < 1e-12

# 只用于验收的小函数，主例暂时不需要封装成通用接口。
def check_counts(truth, pred):
    if not truth or len(truth) != len(pred):
        raise ValueError("非空且等长")
    if any(v not in (0, 1) for v in truth + pred):
        raise ValueError("只接受0/1")
    tn = fp = fn = tp = 0
    for actual, predicted in zip(truth, pred):
        if actual == 1 and predicted == 1:
            tp += 1
        elif actual == 0 and predicted == 1:
            fp += 1
        elif actual == 1 and predicted == 0:
            fn += 1
        else:
            tn += 1
    return [tn, fp, fn, tp]

for truth, pred in [
    ([1], [1]), ([0], [0]), ([0, 1, 0], [1, 1, 0]),
    ([1, 1], [0, 0]), ([0, 0], [0, 0]),
    ([0] * 9 + [1], [0] * 10),
]:
    tn, fp, fn, tp = check_counts(truth, pred)
    assert confusion_matrix(truth, pred, labels=[0, 1]).ravel().tolist() == [tn, fp, fn, tp]
    p = tp / (tp + fp) if tp + fp else 0.
    r = tp / (tp + fn) if tp + fn else 0.
    f = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.
    assert abs(p - precision_score(truth, pred, zero_division=0)) < 1e-12
    assert abs(r - recall_score(truth, pred, zero_division=0)) < 1e-12
    assert abs(f - f1_score(truth, pred, zero_division=0)) < 1e-12
for truth, pred in [([], []), ([0], []), ([2], [0]), ([0], [-1])]:
    try:
        check_counts(truth, pred)
    except ValueError:
        pass
    else:
        raise AssertionError("非法输入应拒绝")
print("选读校对与边界验收通过")
