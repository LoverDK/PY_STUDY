# L63 评估指标：回归与过拟合欠拟合

阶段：经典机器学习。仓库路径：L63/。

L62评估的是类别预测，例如类别0和类别1；L63换成连续数值预测。我们仍按同一条主线学习：先列出真实值和预测值，再逐条计算误差，最后看训练集与测试集的表现是否一致。

你已经学过训练集、测试集、训练、预测和分类指标。本课新增MAE、MSE、RMSE、R²，以及欠拟合和过拟合。例子只用Python循环、Pandas和平方根。线性回归如何训练留到L64，本课不会用一行fit跳过模型原理。

本课的数值都由虚构数据构成。价格单位设为十万元，方便手算。完成本课后，你应该能从四条记录算出四个回归指标，解释每个指标的单位与偏好，并通过训练误差和测试误差判断一条规则是否可能欠拟合或过拟合。

## 第一段：回归误差从哪里来

假设模型预测四套房的价格。真实值与预测值如下，单位是十万元：

|下标|真实值 y|预测值 ŷ|
|---:|---:|---:|
|0|2|3|
|1|4|4|
|2|6|5|
|3|8|10|

回归输出是数值，因此“类别是否相同”已经不够用了。预测3和真实2相差1；预测10和真实8相差2。我们要保留差了多少。

本课把单条误差定义为：

$$
e_i=\hat y_i-y_i
$$

其中，$y_i$ 是第i条记录的真实值，$hat y_i$ 是模型预测值，$e_i$ 是预测减真实。正数表示预测偏高，负数表示预测偏低。

逐条代入：

|i|真实 y|预测 ŷ|误差 ŷ-y|绝对误差|平方误差|
|---:|---:|---:|---:|---:|---:|
|0|2|3|1|1|1|
|1|4|4|0|0|0|
|2|6|5|-1|1|1|
|3|8|10|2|2|4|
|合计|||2|4|6|

误差合计是2，但这个数不能代表整体误差大小。第一条高估1、第三条低估1，两者相加会抵消。模型并没有因此少犯两次错误。

代码中的对应过程很直接：

```python
error = y_pred[i] - y_true[i]
absolute_error = abs(error)
squared_error = error ** 2
```

error保留方向，适合检查模型经常高估还是低估；absolute_error和squared_error都把负号去掉，用来衡量偏离大小。不要把真实值减预测值和预测值减真实值混着用。对绝对值和平方值而言，方向反过来不改变结果，但误差列的解释会相反。

这类逐条误差适用于房价、销量、温度等数值预测。类别0和类别1没有自然距离时，应使用分类指标。

## 第二段：MAE、MSE和RMSE怎样计算

### MAE：平均每条差多少

MAE是平均绝对误差：

$$
MAE=\frac{1}{n}\sum_{i=1}^{n}|\hat y_i-y_i|
$$

n是样本数，本例n=4。四条绝对误差为1、0、1、2，因此：

$$
MAE=\frac{1+0+1+2}{4}=1
$$

价格单位是十万元，所以MAE=1表示这四条记录平均相差十万元。这里的“平均”是绝对误差平均，不能说每条都刚好差十万元。

MAE的优点是单位与目标一致，解释直观。每增加1个单位的绝对误差，累计值就增加1。它不会像平方那样特别放大较大的错误。

### MSE：让大错误受到更重惩罚

MSE是均方误差：

$$
MSE=\frac{1}{n}\sum_{i=1}^{n}(\hat y_i-y_i)^2
$$

本例平方误差为1、0、1、4，所以：

$$
MSE=\frac{1+0+1+4}{4}=1.5
$$

误差2经过平方变成4；误差1平方后仍是1。因此MSE对较大误差更敏感。若一次大错比几次小错更难接受，MSE能把这种偏好带进指标。

MSE的单位也被平方了。本例目标单位是十万元，MSE单位相当于“十万元的平方”，不如MAE直观。

### RMSE：把单位变回来

RMSE是MSE的平方根：

$$
RMSE=\sqrt{MSE}=\sqrt{1.5}\approx1.225
$$

RMSE与目标值使用相同单位，同时保留平方误差对大错误的敏感性。本例约为12.25万元。

MAE与RMSE不需要二选一。报告哪一个取决于问题：若希望每个误差按大小线性计入，MAE更直观；若较大的偏差尤其重要，可以看RMSE。比较模型时，必须在同一数据、同一单位和同一计算方式下比较。

两个常见错误值得记住。第一，先求误差平均再取绝对值，会发生正负抵消，结果不是MAE。第二，RMSE要在平均平方误差之后开根号；逐项开根再平均，得到的是MAE。

## 第三段：R²在和谁比较

MAE、MSE和RMSE都从0开始，越小越好。R²换了一个问题：当前预测比“完全不看输入、每次都猜真实值均值”的基线好多少？

先求真实值均值：

$$
\bar y=\frac{2+4+6+8}{4}=5
$$

若每条都预测5，平方误差总和为：

$$
(2-5)^2+(4-5)^2+(6-5)^2+(8-5)^2=9+1+1+9=20
$$

这个20记作总离差平方和。当前预测的平方误差总和是6。R²定义为：

$$
R^2=1-\frac{\sum_i(y_i-\hat y_i)^2}{\sum_i(y_i-\bar y)^2}
$$

代入本例：

$$
R^2=1-\frac{6}{20}=0.7
$$

R²=0.7表示，在这批数据上，与始终预测真实均值5相比，当前预测减少了70%的平方误差。它是相对基线的分数，不表示“每条预测准确70%”，也不等于相关系数。

三个边界可以帮助理解：
- 完美预测时，分子为0，R²=1。
- 每条都预测真实均值时，分子与分母相等，R²=0。
- 预测比均值基线更差时，分子大于分母，R²会小于0。负数是合法结果。

如果所有真实值都相同，例如[5,5]，分母为0，手算公式没有定义。本课的手写函数返回None，并说明原因。scikit-learn为了让常见计算流程得到有限结果，默认会对常量真值进行修正；阅读库输出时要知道这个约定。

R²适合在同一目标和数据上比较回归表现，但它不告诉你误差单位，也不会说明一次具体错误有多大。实际报告常把R²与MAE或RMSE放在一起。

## 第四段：从训练误差和测试误差看欠拟合、过拟合

用一个小型价格例子比较三条规则。训练数据如下：

|面积|真实价格|
|---:|---:|
|50|2|
|70|4|
|90|6|
|110|8|

测试数据使用没参与训练的面积：

|面积|真实价格|
|---:|---:|
|60|3.2|
|80|4.8|
|100|7.1|
|120|8.9|

我们只比较教学规则，不在这里训练正式回归模型。

第一条规则无论面积多大都预测5。它没有利用面积变化，训练预测为[5,5,5,5]，训练MAE=2；测试MAE也是2。规则表达能力太弱，连训练数据中的明显趋势也没抓住，这是欠拟合的典型表现。

第二条规则按面积变化：预测值=面积/10-3。训练预测为[2,4,6,8]，训练MAE=0；测试预测为[3,5,7,9]，测试MAE=0.15。它抓住了这份虚构数据的总体趋势。测试误差略高，是因为测试真实值带有小幅偏离。

第三条规则用字典记住四个训练面积及价格。遇到50、70、90、110时能原样返回，因此训练MAE=0；遇到新面积时统一返回5，测试MAE=2。它在训练集上看起来完美，却没有学到面积变化的规律。这是过拟合的简化示意。

|规则|训练MAE|测试MAE|观察|
|---|---:|---:|---|
|常数5|2.00|2.00|训练和测试都差，可能欠拟合|
|面积/10-3|0.00|0.15|训练与测试都较好|
|记忆训练样本，未知返回5|0.00|2.00|训练好、测试明显变差，可能过拟合|

欠拟合通常表现为训练集也做不好，原因可能是规则过于简单、特征缺失或训练不足。过拟合通常表现为训练集很好，而独立数据明显变差，模型可能记住了训练样本的细节或噪声。

不能只凭“训练误差0”断言过拟合，因为第二条和第三条规则的训练MAE都是0。测试表现把它们区分开来。也不能只看训练误差与测试误差差距：若两边误差都很高，差距可能很小，但模型仍然欠拟合。

真实项目还需要更多样本、验证集或交叉验证。选择规则和超参数时，应使用训练/验证流程，把测试集留到最后。L73会系统学习交叉验证。本课用“测试”一词演示现象，不能反复根据这四条测试记录修改规则。

本例的记忆规则是为了让现象清楚，不代表所有复杂模型都会过拟合，也不代表简单模型一定欠拟合。判断依赖数据、特征、模型和训练过程。

## 第五段：把指标与三条规则写成代码

examples.py先实现regression_metrics，再用它检查三条规则。完整代码如下：

```python
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
```

regression_metrics接收两个等长列表。rows保存逐条误差，scores保存四个汇总指标。absolute_error_sum和squared_error_sum从0开始，每处理一条就累加一次。循环结束后再除以n，得到平均值。

mean_true是真实值均值，baseline_squared_error计算每个真实值与均值的平方距离。分母大于0时才计算R²；所有真实值相同则返回None。

三条规则都接收面积列表并返回同样长度的预测列表。constant_rule忽略面积；trend_rule按同一公式计算每条预测；memory_rule通过字典记住训练样本，遇到没见过的面积时返回5。代码分别在训练集与测试集上算MAE，结果与第四段表格一致。

主例实际运行结果：
- 误差为[1,0,-1,2]；
- MAE=1，MSE=1.5，RMSE约1.224744871，R²=0.7；
- 常数规则训练/测试MAE为2/2；
- 趋势规则为0/0.15；
- 记忆规则为0/2。

函数还检查了空输入、长度不一致和常量真值。examples_sklearn.py是选读文件，只用官方指标函数校对同一组数字，不训练新模型。校对结果完全一致，并验证了R²为1、0和负数的三个边界。

计算n条记录的四个指标只需遍历有限次，时间为O(n)。rows保存n条明细，空间为O(n)；如果只保留累计和，辅助空间可以降到O(1)。返回的预测列表属于输出空间。

### 易错点与使用建议

1. 分类指标不能直接套到回归数值上。预测5.9与真实6.0的差距应保留，而不是先粗暴判断“相等/不相等”。
2. 比较模型时要使用同一测试集和同一目标单位。一个以元计价、另一个以十万元计价，MAE数值不能直接比较。
3. MSE与RMSE名称相近，单位不同。报告时要写清开没开平方。
4. R²可以为负，也不能解释成百分比准确率。
5. 测试集用于检查泛化。反复用它选择规则会让结果逐渐偏乐观。

MAE适合直观报告平均偏差；RMSE适合需要强调较大错误的场景；R²说明相对均值基线改善了多少。训练与测试误差一起看，可以初步发现欠拟合或过拟合，但最终判断还要结合更多数据、模型结构与业务代价。

## 三道练习与下节课

作业按三个台阶安排：
1. 直接复现四条记录的误差、MAE和MSE；
2. 补全RMSE与R²计算，处理常量真值；
3. 换一组训练/测试数据，比较欠拟合、合适和记忆规则。

每题的代码骨架、提示、预期结果和硬验收在homework.md。必做题不要求sklearn。

下一课：L64「线性回归：直觉与 sklearn」。届时会从一条直线怎样产生预测讲起，再解释fit学到了什么。

## 参考与修订

- scikit-learn回归指标：https://scikit-learn.org/stable/modules/model_evaluation.html
- MAE：https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html
- 欠拟合与过拟合示例：https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html
- 学习曲线说明：https://scikit-learn.org/stable/modules/learning_curve.html

正文按用户指定的Humanizer 3.1.0润色。公式、数值、代码和验收条件保持一致。
