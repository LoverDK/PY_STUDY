# L62 数据划分与评估指标：分类

阶段：经典机器学习。仓库路径：L62/。

你在L61已经见过一张重量和类别的表，也用三个候选选出了阈值130。这一课继续用它：把新记录留到训练之后，看它究竟预测对了多少，以及错在什么地方。

需要的旧知识是DataFrame选行、列表、比较和循环。本课新增训练集与测试集、误报与漏报、四格计数，以及四个分类指标。读完正文后，再看分层随机划分与sklearn校对，那里是选读。

本课不训练决策树或其他新模型。回归指标、过拟合与欠拟合在L63，逻辑回归在L65，交叉验证在L73，系统处理类别不平衡与阈值在L74。计算机系统原理不在课程范围内。

学完后，你应该能把数据划分、选参数、预测、评估连起来，亲手算出本例的四项指标，并解释为什么一张准确率成绩单还不够。

## 第一段：训练时全对，为什么还要测试

先回看L61的四件物品：

|ID|重量|真实类别|本课用途|
|---:|---:|---:|---|
|0|100|0|训练|
|1|120|0|训练|
|2|140|1|训练|
|3|160|1|训练|

三个候选阈值110、130、150的训练错分数依次为1、0、1，于是选130。规则仍是重量>130预测1，否则预测0。

现在另留八条记录，只用于检查选好的规则。它们也都是虚构教学数据：

|ID|重量|真实类别|
|---:|---:|---:|
|4|110|0|
|5|130|1|
|6|150|0|
|7|170|1|
|8|90|0|
|9|125|0|
|10|145|1|
|11|180|1|

只用前四条选参数，它们叫训练集；后八条不参与选择，叫测试集。代码直接使用你会的选行方法：

```python
train = table.iloc[:4].copy()
test = table.iloc[4:].copy()
```

iloc[:4]取位置0到3，iloc[4:]从位置4取到末尾。copy创建两份独立表。两边仍保留weight与kind的原始对应关系。预测阶段只读测试重量，等预测出来后才读取测试标签算成绩。

我们故意让测试集中出现两个不符合简单重量规则的记录。重量130真实类别是1，但规则会报0；重量150真实类别是0，规则会报1。训练数据的零错误没有延续到测试数据。

测试集之所以有用，是因为它没有帮我们挑参数，能检查规则对未参与训练的样本是否仍然合适。这种能力叫泛化。不过八条记录太少，又是人工编的，成绩只用于理解流程，不能用来证明实际部署能力。若未来数据的采集渠道、类别含义或分布变了，旧测试结果也可能不再适用。

划分应在选参数之前确定。不能把测试错误看一遍、改阈值，再继续称它为一次独立测试；也不能让同一条记录同时出现在训练和测试里。真实数据若包含同一个人的多条记录，往往还要按人分组；时间预测则要遵守先后顺序。本例按位置切只是为了看清每条记录的去向，并不建议真实数据一律按前几行训练、后几行测试。这里4条训练、8条测试的比例也只是演示安排。

## 第二段：固定参数，先把预测一条条写出来

训练代码与L61相同，只循环train，选中的参数是130。此后不再修改它。

```python
y_true = test["kind"].tolist()
y_pred = []
for weight in test["weight"]:
    prediction = 1 if weight > best_threshold else 0
    y_pred.append(prediction)
```

y_true保存真实类别，y_pred保存模型输出。两个列表中下标相同的元素指同一件物品。预测循环只需要重量和阈值，真实标签不参与判断。

|测试下标|ID|重量|是否>130|预测|真实|结果|
|---:|---:|---:|---|---:|---:|---|
|0|4|110|否|0|0|对|
|1|5|130|否|0|1|漏掉一个正类|
|2|6|150|是|1|0|把负类误报成正类|
|3|7|170|是|1|1|对|
|4|8|90|否|0|0|对|
|5|9|125|否|0|0|对|
|6|10|145|是|1|1|对|
|7|11|180|是|1|1|对|

最后得到：

```text
真实：[0, 1, 0, 1, 0, 0, 1, 1]
预测：[0, 0, 1, 1, 0, 0, 1, 1]
```

边界值130依然预测0，因为用的是>。这次该样本真实为1，于是模型会犯错。不能为了让它答对，悄悄把比较符改成>=再报同一份测试成绩。

比较时也要保持顺序。如果把y_pred单独排序，两个列表就不再一一对应，得到的错误数没有意义。

## 第三段：把错法分开，建立混淆矩阵

先约定类别1是这次关注的正类，类别0是负类。正、负在这里是类别名称，没有好坏含义。

预测只可能是0或1，真实类别也只可能是0或1，因此一共四种组合：

|真实|预测|简称|中文意思|
|---:|---:|---|---|
|1|1|TP|真正例，正类抓到了|
|0|1|FP|假正例，发生误报|
|1|0|FN|假负例，发生漏报|
|0|0|TN|真负例，负类判断正确|

T表示判断正确，F表示判断错误；P或N指预测为正或预测为负。记FP时，可以先想“报了正，结果报错了”；FN则是“报了负，漏掉了真正的正类”。

从四个0开始，每条记录只给相应的一格加1。下面状态的顺序固定为(TN,FP,FN,TP)：

|下标|真实|预测|归入|更新后的状态|原因|
|---:|---:|---:|---|---|---|
|0|0|0|TN|(1,0,0,0)|负类判断正确|
|1|1|0|FN|(1,0,1,0)|正类被漏掉|
|2|0|1|FP|(1,1,1,0)|负类被误报|
|3|1|1|TP|(1,1,1,1)|正类抓到了|
|4|0|0|TN|(2,1,1,1)|再正确排除一个|
|5|0|0|TN|(3,1,1,1)|第三个真负例|
|6|1|1|TP|(3,1,1,2)|第二个真正例|
|7|1|1|TP|(3,1,1,3)|第三个真正例|

最终TN=3、FP=1、FN=1、TP=3，四格相加是8。写成下面这张表，就叫混淆矩阵：

|真实类别与预测类别|预测0|预测1|
|---|---:|---:|
|真实0|TN=3|FP=1|
|真实1|FN=1|TP=3|

本课和sklearn的labels=[0,1]约定一致：行是真实，列是预测。若看别人的图，要先读坐标定义，有些资料把两轴交换。

代码按这四种互斥情况写if/elif/else，每次只进入一个分支。处理完前k条，计数器就准确记录前k条的四种情况；处理到第8条时结束，不会漏记或重复。这也是检查实现是否正确的方法：每处理一条，四格总数应该增加1。

容易出错的地方，一是把真实与预测的位置交换，会把FP和FN对调；二是换了“正类”的含义，却仍照旧解释召回率。例如本课关注类别1，若以后把类别0当作关注对象，就要重新定义这些计数。

## 第四段：从四个计数算出四个指标

先问最直接的问题：八次判断里有几次答对？真正例与真负例都算答对，所以：

准确率Accuracy = (TP+TN)/全部样本数 = (3+3)/8 = 0.75。

它适合描述总体正确比例，但没有区分两种错误的后果。若漏掉一个正类特别贵，只看它就不够了。

精确率Precision换了一个分母：只看被模型报成正类的记录。这里报正的有TP+FP=4件，其中3件确实是正类，所以：

Precision = TP/(TP+FP) = 3/(3+1) = 0.75。

当误报会占用昂贵复核资源时，这个问题很有用：“报出来的这些，能信多少？”

召回率Recall看的是所有真实正类。这里实际有TP+FN=4件，抓到3件，所以：

Recall = TP/(TP+FN) = 3/(3+1) = 0.75。

漏报代价高时，更关心真实正类还漏掉多少。Precision和Recall分母不同，只是本例恰好算出同一个数。假如另一次评估得到TP=2、FP=1、FN=2、TN=5，Precision是2/3，Recall是2/4=0.5，Accuracy则是7/10=0.7。

如果希望用一个数同时考虑Precision与Recall，可以看F1。令P表示Precision、R表示Recall，N表示测试样本总数：

$$
Accuracy=\frac{TP+TN}{N},\qquad
Precision=\frac{TP}{TP+FP},\qquad
Recall=\frac{TP}{TP+FN}
$$

$$
F1=\frac{2PR}{P+R}
=\frac{2TP}{2TP+FP+FN}
$$

本例F1 = 2×3/(2×3+1+1) = 6/8 = 0.75。刚才另一组计数的F1则是4/(4+1+2)=4/7，约0.571。

F1是P和R的调和平均，比算术平均更受较小一方影响，因此两者都高时它才会高。它的公式不含TN，不能完整描述所有业务；如果误报和漏报的损失不同，还需要另外考虑成本。

再看一个反例：10条记录里9条是0、只有1条是1，模型全部报0。它答对9条，Accuracy=0.9；但TP=0、FN=1，Recall=0，一个正类也没找到。这个“总猜多数类”的结果是一个简单基线，能提醒我们先看类别比例，再判断准确率是否值得满意。

若模型一次也不报正，TP+FP就是0，Precision在数学上没有定义；若测试集没有正类，Recall也会没有定义。本课为方便程序继续运行，把这些分母为0的指标记为0，并同时报告原因和四格计数。这是计算约定，不代表数学上的0/0等于0。F1分母为0时也采用相同约定。

选指标时，先问业务更怕什么。类别相对均衡、两类错误代价接近时，Accuracy比较直观；误报贵时看Precision；漏报贵时看Recall。需要综合两者时可以看F1，但仍应保留混淆矩阵，避免一个数字遮住错误的具体分布。

## 第五段：把流程连成能运行的代码

完整examples.py如下。先读前3段，确认训练与测试各用了哪些记录；再读第4、5段，对照前面的计数表。

```python
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
```

这里只导入pandas来创建表，没有引入新模型。DataFrame包含ID、weight、kind三列；因此train.shape是(4,3)，test.shape是(8,3)。其中ID只用于核对去向，kind是标签，只有weight是输入特征，不能把三列全部当作模型输入。

训练循环里的errors每换一个候选就清零，best_threshold跨候选保留。预测阶段只读test的weight列；完成预测后才把y_true和y_pred配起来计数。

四格循环中actual是真实值、predicted是预测值，bucket保存这一条落入哪格的简称。trace保存每轮结果，方便与讲义逐行核对。计算指标时，条件表达式先检查分母，避免直接除以0。Accuracy的分母是测试样本数，这段主例有8条；空测试集不应硬算成绩。

实测得到阈值130、训练错分0、测试错分2、矩阵[[3,1],[1,3]]，四项指标均为0.75。ID核验也通过：训练与测试没有交集，合起来刚好是全部12条记录。examples_sklearn.py另外检查了单样本、重复标签、没有报正、没有真实正类、空输入、长度不等、非法标签等边界。

计数只扫测试集一遍，n条测试样本需要O(n)时间。四个计数器本身是O(1)辅助空间；保存全部预测和trace各需要O(n)空间。训练部分仍是L61的m个候选各扫一遍n_train条记录，时间O(m×n_train)，本课没有增加新训练算法。

### 选读：随机划分和分层是什么意思

手动切分让你能逐条追踪数据去向。真实的独立同分布分类样本常用随机划分，训练和测试仍必须一一对应。sklearn提供train_test_split完成这一件事：

```python
X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
    X, y, ids, test_size=1/3, random_state=42, stratify=y
)
```

X是12行1列重量，y是12个标签，ids是12个编号。把三者同时传入，函数会用同一组行索引切分它们，并按每个输入依次返回训练、测试两份，共6个结果。test_size=1/3表示12条里留4条测试、8条训练；random_state=42便于重复得到同样结果，42本身没有特殊统计含义。

stratify=y表示按类别分层，让两边的类别比例尽量接近总体。这12条总体有6个0、6个1，本次实际划分得到训练集4个正类、测试集2个正类。若某类只有1条，就无法让两边都含有它；分层不能创造数据，也不保证所有特征分布相同。时间数据和同一人的重复记录也需要另外的划分策略。

这次随机划分是另一次独立演示，不能把它产生的测试集与正文固定划分的0.75成绩混在一起。examples_sklearn.py分开演示了划分和指标校对；校对指标时使用的是正文原来的8条真值与预测。

若将来要缩放或填补数据，先切分，再只用训练集确定处理参数，并原样应用到测试集。这样可以避免把测试信息带回训练过程，称为避免数据泄漏。Pipeline和这些处理器在L66再写代码；今天不用实现它们。模型或阈值若需要反复选择，应另外用验证数据，最后保留测试集做检查；交叉验证留到L73。

## 作业与下一课

第1题直接对照四条真值与预测，数答对几条；第2题按骨架填四格计数与指标；第3题沿用L61训练法，对一组新测试数据独立完成预测和评估。详细提示与验收在homework.md。选读文件不参与必做评分。

下一课：L63 评估指标：回归与过拟合欠拟合。

## 参考与修订

- train_test_split：https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- confusion_matrix：https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
- f1_score：https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html

2026-11-02按零机器学习基础重写，并依据Humanizer润色。原版保留在Git历史中；本次不改变交付日期、课名、课表或下一课。
