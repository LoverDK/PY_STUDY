from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import numpy as np
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

@dataclass(frozen=True)
class BinaryCounts:
    tn: int
    fp: int
    fn: int
    tp: int

def confusion_trace(y_true: Iterable[int], y_pred: Iterable[int]):
    truth, pred = list(y_true), list(y_pred)
    if not truth or len(truth) != len(pred):
        raise ValueError("y_true和y_pred必须非空且等长")
    if any(v not in (0, 1) for v in truth + pred):
        raise ValueError("本课二分类演示只接受0/1")
    tn = fp = fn = tp = 0
    trace = []
    for i, (actual, guessed) in enumerate(zip(truth, pred)):
        if actual == 1 and guessed == 1:
            tp += 1; bucket = "TP"
        elif actual == 0 and guessed == 1:
            fp += 1; bucket = "FP"
        elif actual == 1 and guessed == 0:
            fn += 1; bucket = "FN"
        else:
            tn += 1; bucket = "TN"
        trace.append((i, actual, guessed, bucket, tn, fp, fn, tp))
    return BinaryCounts(tn, fp, fn, tp), trace

def safe_ratio(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else numerator / denominator

def metrics_from_counts(c: BinaryCounts):
    total = c.tn + c.fp + c.fn + c.tp
    if total == 0:
        raise ValueError("至少需要一条样本")
    accuracy = (c.tp + c.tn) / total
    precision = safe_ratio(c.tp, c.tp + c.fp)
    recall = safe_ratio(c.tp, c.tp + c.fn)
    f1 = safe_ratio(2 * precision * recall, precision + recall)
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}

def evaluate(y_true, y_pred):
    counts, trace = confusion_trace(y_true, y_pred)
    return counts, metrics_from_counts(counts), trace

def stratified_demo():
    X, y = make_classification(n_samples=200, n_features=4, n_informative=3, n_redundant=0, weights=[0.8, 0.2], class_sep=1.2, random_state=7)
    ids = np.arange(len(y))
    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(X, y, ids, test_size=0.25, random_state=42, stratify=y)
    models = {"majority_baseline": DummyClassifier(strategy="most_frequent"), "depth3_tree": DecisionTreeClassifier(max_depth=3, random_state=42)}
    reports = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        reports[name] = {
            "accuracy": accuracy_score(y_test, pred),
            "precision": precision_score(y_test, pred, zero_division=0),
            "recall": recall_score(y_test, pred, zero_division=0),
            "f1": f1_score(y_test, pred, zero_division=0),
            "matrix": confusion_matrix(y_test, pred, labels=[0, 1]).tolist(),
        }
    return (X, y, X_train, X_test, y_train, y_test, id_train, id_test, reports)

def self_test():
    y_true = [1, 0, 1, 1, 0, 0, 1, 0]
    y_pred = [1, 1, 1, 0, 0, 0, 1, 0]
    counts, scores, trace = evaluate(y_true, y_pred)
    assert counts == BinaryCounts(tn=3, fp=1, fn=1, tp=3)
    assert all(abs(scores[k] - 0.75) < 1e-12 for k in scores)
    assert confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist() == [[3, 1], [1, 3]]
    assert len(trace) == 8
    counts2, scores2, _ = evaluate([0, 0, 1, 1], [0, 0, 0, 0])
    assert counts2 == BinaryCounts(tn=2, fp=0, fn=2, tp=0)
    assert scores2 == {"accuracy": 0.5, "precision": 0.0, "recall": 0.0, "f1": 0.0}
    for bad in [([], []), ([0], [0, 1]), ([2], [0])]:
        try:
            evaluate(*bad)
            raise AssertionError("非法输入应抛出ValueError")
        except ValueError:
            pass
    X, y, X_train, X_test, y_train, y_test, id_train, id_test, reports = stratified_demo()
    assert X.shape == (200, 4) and X_train.shape == (150, 4) and X_test.shape == (50, 4)
    assert set(id_train).isdisjoint(set(id_test))
    assert set(id_train) | set(id_test) == set(range(200))
    assert abs(y_train.mean() - y.mean()) < 0.02
    assert abs(y_test.mean() - y.mean()) < 0.02
    for report in reports.values():
        assert all(0.0 <= report[k] <= 1.0 for k in ("accuracy", "precision", "recall", "f1"))
        assert sum(map(sum, report["matrix"])) == 50
    return trace, y, y_train, y_test, reports

if __name__ == "__main__":
    trace, y, y_train, y_test, reports = self_test()
    print("逐条混淆矩阵轨迹")
    for row in trace:
        print(row)
    print(f"全体/训练/测试正类比例: {y.mean():.3f}/{y_train.mean():.3f}/{y_test.mean():.3f}")
    for name, report in reports.items():
        print(name, report)
    print("全部边界与一致性验收通过")
