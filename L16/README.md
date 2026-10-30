# L16 机试综合：Pandas 读洗筛汇小卷

阶段A，2026-10-30交付。先阅读notes.md，运行examples.py，再独立完成homework.md。

## 文件
- notes.md：五段详讲及综合例题
- chat_delivery.md：课堂稿，与notes.md一致
- examples.py：订单读洗筛汇及自检
- data/orders.csv：教学订单数据
- homework.md：三题独立作业、硬验收和笔试分析
- homework/answers.ipynb：约 9:30 写标准答案（本次仅占位）

## 运行
依赖Python和Pandas。在仓库根目录：
```bash
python -B L16/examples.py
```
程序读取本课CSV，仅打印，不写文件。预期：11行→清洗6单→paid4单，West/East/North收入100/50/40，总收入190。

口径：字符串去空格→缺键剔除→同键留文件最后行→数值和业务合法性校验→金额→筛paid→聚合。最新非法行不回退到旧行。数量为正整数、价格有限非负；本课使用小整数教学金额。

下一课：L17 机试综合：可视化读图与作图指令。
