# L16 机试综合：Pandas 读洗筛汇小卷

阶段：A — DSBA / Python / 可视化 / 复杂度。仓库路径：L16/。
范围：CSV类型、字符串标准化、业务键去重、数值校验、布尔筛选、命名聚合、结果排序与验收。
不讲：数据库、机器学习、复杂数据工程、计算机系统原理。

## 目标
独立把一张有脏数据的订单表转成可复核的地区收入报表；明确每一步处理口径，保留输入不变，处理空结果，并用精确断言核对订单、金额和分组结果。示例数据金额为教学小整数；一般货币系统宜用整数分或明确的十进制口径，不能把浮点展示当精确账务保证。

## 第一段：读入时先保留含义，再检查结构
是什么：read_csv 把文本转成带列名、索引和类型的 DataFrame。入口应验证必需列，并防止标识符被自动推断成数值。
为什么：订单号001不应变成1；金额列里有bad时不能假装已是合法数字。读取成功只是解析成功，不代表业务有效。
怎么写：
```python
raw = pd.read_csv(StringIO(csv_text), dtype="string")
required = {"order_id", "region", "product", "quantity", "unit_price", "status"}
if required - set(raw.columns):
    raise ValueError("缺少必需列")
```
StringIO适合机试内嵌数据，无须临时文件；示例程序也能读取课程data/orders.csv。先观察shape、dtypes和isna().sum()，不要直接开始聚合。保留原表，清洗函数在副本上工作。
易错点：①数值推断破坏前导零；②把整表缺失统计当成业务校验，忽略必需列不存在；③使用当前工作目录找文件，导致换目录运行失败。
何时用：所有文件入口、自动报表和机试读表题。

## 第二段：先定清洗顺序，去重不是随意删行
是什么：标准化表示，再按业务键处理重复，最后应用有效性规则。示例规定同order_id的最后一行是最新记录，“最后”指文件顺序，不是假定时间最新。
为什么：先清掉无效最新记录再去重，会把旧有效记录重新当成现状。顺序本身就是业务规则。
怎么写：
```python
df["order_id"] = df["order_id"].astype("string").str.strip()
df["order_id"] = df["order_id"].replace("", pd.NA)
df = df.dropna(subset=["order_id"])
df = df.drop_duplicates("order_id", keep="last")
```
region/product/status也去首尾空格、空串变缺失；status统一小写。然后to_numeric(errors="coerce")将无法解析内容标成缺失，显式剔除，不用0伪装。数量必须为正整数；价格必须有限且非负；必需文本不得缺失；status仅允许paid/pending/cancelled。
易错点：①drop_duplicates不指定业务键，无法合并订单更新；②误以为keep="last"会自动按时间寻找最新；③先过滤再去重，复活旧行；④把缺数量填0后保留，改变订单含义。
何时用：订单更新、报名记录、同一实体多版本的数据。若题目给时间列，应先明确按时间排序和并列规则，本课不擅自增加该规则。

## 第三段：布尔筛选要对应明确的业务集合
是什么：一列布尔值选择符合条件的行。清洗有效不等于可以计入收入：pending和cancelled可以是合法记录，但本例收入只认paid。
怎么写：
```python
clean["amount"] = clean["quantity"] * clean["unit_price"]
paid = clean.loc[clean["status"].eq("paid")].copy()
```
可叠加金额阈值等条件：
```python
selected = clean.loc[
    clean["status"].eq("paid") & clean["amount"].ge(40)
].copy()
```
为什么：先得到有效订单全集，再筛业务子集，便于核对到底是输入错误还是未达业务条件。多条件用逐元素&、|，每个比较加括号；使用loc并copy后派生新列，减少修改对象含混。
易错点：①用and连接Series；②把pending也加进收入；③先筛paid再保留重复订单最后行，可能将最新取消的订单旧付款行算入；④布尔掩码来自另一张重排后的表，造成对齐错误。
何时用：营业收入、有效报名、达标人群或多条件机试筛选。

## 第四段：聚合前明确“一行代表什么”
是什么：groupby按地区聚组，再分别计算订单数、件数和收入。
怎么写：
```python
summary = paid.groupby("region", as_index=False).agg(
    order_count=("order_id", "size"),
    quantity_total=("quantity", "sum"),
    revenue=("amount", "sum"),
)
```
为什么：本例清洗后每行一个订单，故size是订单数；若一订单多商品明细行，size变成明细数，订单数应按业务需要用nunique。sum(quantity)是件数，不能与订单数混淆。命名聚合让输出列名可预测。
为了可复现，最后按revenue降序、region升序排列。同收入时地区名是第二排序键。缺失地区在清洗阶段已剔除，不依赖groupby默认缺失键行为。
易错点：①把行数当商品件数；②未去重就统计订单数；③对含缺失列用count时，它只数非缺失值，可能与size不同；④默认分组顺序不是收入排行榜。
何时用：分类报表、地区汇总、题目要求固定输出列和顺序的机试。

## 第五段：验收看明细、汇总与边界
是什么：用断言固定业务结果，而不是只看“打印出来似乎合理”。
怎么写：
```python
assert clean["order_id"].is_unique
assert paid["amount"].sum() == summary["revenue"].sum()
assert summary.columns.tolist() == [
    "region", "order_count", "quantity_total", "revenue"
]
```
本例使用小整数金额，可做精确相等核对；一般浮点统计可采用容差，或在货币业务改用整数分。输入不变性用pd.testing.assert_frame_equal检查。空输入/全部被过滤时，输出应为空但保留规定列。
为什么：守恒检查能发现漏分组和重复累计，但总额相等还不够，必须同时核对各地区数值及顺序。对非法最新行的专项测试可确认清洗顺序。
易错点：①只验总额，地区错配仍可能通过；②只用干净数据，无法验证清洗；③空表直接取第一行导致异常；④口头说保留原表却在函数中原地改列。
何时用：机试提交前、自动报表更新、多人协作的可复核数据分析。

## 综合例题
data/orders.csv原始11行。O02重复，最后一行数量5覆盖旧数量3。数量缺失、坏价格、地区缺失、负数量被剔除。清洗后6个订单，保留cancelled和pending作为合法状态；收入筛选后4个paid订单。
West：1单/5件/收入100；East：2单/5件/收入50；North：1单/2件/收入40。总收入190。
顺序是读→标准化→按键留最后→校验→派生金额→筛paid→分组→排序→验收。

## 作业
三道独立任务：库存读洗；订单筛选；地区汇总。题目均包含固定口径、边界与硬验收，见homework.md。答案文件先占位。

## 下节
L17 机试综合：可视化读图与作图指令
