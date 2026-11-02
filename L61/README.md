# L61 机器学习地图：监督/无监督/强化学习

适合会基础Python、Pandas、NumPy和Matplotlib，刚接触机器学习的学生。
## 阅读顺序
1. notes.md第1、2段：从表格认出特征/标签，理解固定规则预测。
2. examples.py第1、2段：直接运行并对照四行输出。
3. notes.md第3段和examples.py第3段：比较三个候选，理解训练。
4. notes.md第4段：只认识无监督与强化学习用途，不要求实现。
5. homework.md：先读数据，再补全代码，最后自己换数据练习。
## 文件
- notes.md：完整五段讲义及逐段解释
- chat_delivery.md：与讲义一致的课堂稿
- examples.py：用Pandas/NumPy完成数据提取、固定规则预测和候选比较
- homework.md：三道递进练习，输入输出、提示、硬验收齐全
- homework/answers.ipynb：新版题目答案占位，约9:30写标准答案
## 验证
运行python -B L61/examples.py；无需下载数据或写文件。
本次实测：X(4,1)、y(4,)；候选110/130/150错分1/0/1；选130；新输入110/150预测0/1；适用边界断言通过。
## 修订记录
2026-11-02重写入门讲解并按Humanizer润色。本次修订不增加进度，原版可在Git提交历史中查看。聚类、强化学习更新和折扣回报不属于本课必学要求。
教学规则见仓库根目录teaching_guidelines.md。下一课L62 数据划分与评估指标：分类。
