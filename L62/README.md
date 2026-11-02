# L62 数据划分与评估指标：分类

接着新版L61的重量与类别例子，用已经学过的阈值规则检查未参与训练的记录。适合会基础Python、Pandas、NumPy、Matplotlib，刚接触机器学习的学生。

## 从哪里开始
1. 先读notes.md前两段，手算重量130和150为什么会预测错。
2. 运行examples.py，对照八行计数表，理解四个指标的分母。
3. 按homework.md做三题：数对错、补四格代码、独立完成训练后的测试。
4. 理解正文后再看examples_sklearn.py。它是独立选读，不参与必做评分。

## 文件
- notes.md：五段讲义，含数值演算、完整代码、适用边界与错误反例
- chat_delivery.md：同版课堂稿
- examples.py：只用Pandas，沿用L61阈值训练；没有新分类模型、dataclass或通用框架
- examples_sklearn.py：选读的随机分层划分、指标校对与边界验收
- homework.md：三题递进练习，提示与硬验收
- homework/answers.ipynb：新版作业答案占位，约9:30写标准答案

## 运行
主例需要Python和Pandas：
```bash
python -B L62/examples.py
```
选读另需NumPy、scikit-learn：
```bash
python -B L62/examples_sklearn.py
```
两个程序都不下载数据或写文件。

实际验证：主例只用ID0到3训练，ID4到11测试；候选错分[1,0,1]，固定阈值130；测试矩阵[[3,1],[1,3]]，四项指标均0.75。选读划分得到训练(8,1)、测试(4,1)，正类数量4、2；复现性、ID不重不漏及单样本/无正类预测/无真实正类/非法输入等边界核对通过。选读的新划分与主例固定划分是不同实验，不混用成绩。

## 修订记录
2026-11-02按零基础、手算到代码、递进作业要求重写，并按Humanizer润色。修复原讲义公式中的转义显示问题；旧内容在Git历史中保留。本次不推进课程，不修改progress或catalog。
下一课：L63 评估指标：回归与过拟合欠拟合。
