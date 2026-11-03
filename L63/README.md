# L63 评估指标：回归与过拟合欠拟合

适合刚学完L61、L62的学生。本课从四条真实值和预测值开始，手算MAE、MSE、RMSE、R²，再比较三条教学规则的训练误差与测试误差。

## 阅读顺序
1. notes.md第1至3段：逐条误差和四个指标。
2. notes.md第4段：用三条规则认识欠拟合与过拟合。
3. 运行examples.py，对照两张结果表。
4. 完成homework.md的复现、补全、迁移三题。
5. 理解手算后，再运行examples_sklearn.py校对。

## 文件
- notes.md：五段完整讲义、公式、数值演算、局限与易错点
- chat_delivery.md：同版课堂稿
- examples.py：Pandas与标准库实现，不训练新模型
- examples_sklearn.py：选读，只校对指标边界
- homework.md：三道递进练习与硬验收
- homework/answers.ipynb：约9:30写标准答案

## 运行
主例需要Python和Pandas：
```bash
python -B L63/examples.py
```

选读另需scikit-learn：
```bash
python -B L63/examples_sklearn.py
```

程序不下载数据或写文件。主例实测MAE=1、MSE=1.5、RMSE约1.224744871、R²=0.7；三条规则的训练/测试MAE依次为2/2、0/0.15、0/2。选读已校对均值基线R²=0、完美预测R²=1、较差预测R²<0和常量真值边界。

下一课：L64 线性回归：直觉与 sklearn。
