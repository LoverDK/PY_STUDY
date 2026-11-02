# L62 作业：数据划分与评估指标（分类）

统一要求：每题独立可运行；不得只调用一个现成函数后打印结果；输出中必须显示关键中间状态。可使用 Python 标准库、NumPy、scikit-learn。

## 第1题：手写二分类评估器

实现 `evaluate_binary(y_true, y_pred, positive_label=1)`，返回 TN、FP、FN、TP、accuracy、precision、recall、F1，并返回每条样本落入哪一格的 trace。

输入：
```python
y_true = [1, 0, 1, 1, 0, 0, 1, 0]
y_pred = [1, 1, 1, 0, 0, 0, 1, 0]
```

硬验收：
1. 必须得到 `TN=3, FP=1, FN=1, TP=3`，四项指标都为 `0.75`；
2. trace 恰有 8 行，依次为 `TP,FP,TP,FN,TN,TN,TP,TN`；
3. 空输入、长度不等、出现不属于二分类标签的值必须抛 `ValueError`；
4. `[0,0,1,1]` 对 `[0,0,0,0]` 时 precision、recall、F1 按约定为 0，不能除零崩溃；
5. 用 sklearn `confusion_matrix(..., labels=[0,1])` 反查得到 `[[3,1],[1,3]]`。

## 第2题：可审计的分层划分

用 `make_classification` 创建 120 条、5 特征、正类约 25% 的二分类数据；另建 `ids=np.arange(120)`。以 `test_size=0.25, random_state=2026, stratify=y` 同时切分 X、y、ids。

硬验收：
1. 打印四个数组形状，训练 90 行、测试 30 行，特征列数均为 5；
2. 断言训练 ID 与测试 ID 无交集，并集恰为 `0..119`；
3. 打印总体/训练/测试正类比例，训练、测试与总体差的绝对值均不超过 0.03；
4. 用完全相同参数再切一次，断言两次 ID 完全相同；把 `random_state` 改为 7 后，至少一个测试 ID 改变；
5. 用注释说明为何不能先在全部 120 条上拟合标准化器再切分。

## 第3题：基线、模型与业务指标

沿用第2题的固定划分。训练：
- `DummyClassifier(strategy="most_frequent")`
- `DecisionTreeClassifier(max_depth=3, random_state=2026)`

对两个模型分别打印混淆矩阵、accuracy、precision、recall、F1。再写函数 `business_cost(fp, fn, fp_cost=5, fn_cost=30)`。

硬验收：
1. 两个模型都只能在训练集 `fit`，只能用测试集做最终 `predict/score`；
2. 每个混淆矩阵四格之和必须等于 30；
3. 手写指标与 sklearn 对应指标逐项误差小于 `1e-12`；
4. 多数类基线若从未预测正类，precision/recall/F1 必须按 0 处理并解释其准确率为何仍可能较高；
5. 输出两个模型的业务成本 `5×FP+30×FN`，不能因为 accuracy 高就直接宣布成本更低；
6. 最后用 4–6 句话说明：本题结果只适用于固定合成数据/划分，不能证明某类模型普遍更好。
