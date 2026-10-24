# L11 Pandas 时间与排序·去重

阶段 A：DSBA/Python/可视化/复杂度。仓库路径 L11/。
2026-10-24 经用户主动要求，作为一次周末主课例外推进；仅本次，常规周末不自动开主课的规则保持不变。
范围：to_datetime、NaT、dt 日期属性、时间区间、sort_values 多键及并列、duplicated/drop_duplicates、按业务键保留最新记录。
不讲：时区转换实现、重采样/滚动窗口、复杂索引、模型训练与计算机系统原理。

## 今日目标
1. 把明确格式的时间文本解析为真正的日期时间，而不是靠字符串排序碰运气。
2. 区分原始缺失与解析失败，使用 NaT 和 isna 检查。
3. 解释排序的主键/次键/升降序，给并列情况制定可复现规则。
4. 区分“全行重复”“业务键重复”“索引重复”，明确保留首条/末条的含义。
5. 完成时间清洗、排序排名、保留最新版本三道机试题。

## 一、是什么：时间类型、顺序与重复是三个问题

时间字符串只是文本，例如 "2026-10-02"；解析后的 Timestamp/日期时间列才支持日期提取和时间差。to_datetime 将文本解析成日期时间，errors="raise" 遇到非法内容抛错，errors="coerce" 则转换为 NaT。NaT 表示缺失的日期时间，判断用 isna()/notna()，不要写 value==pd.NaT。

sort_values 按列值重新排列整行，原索引默认跟随记录保留；sort_index 按索引标签排，二者不是同一件事。多列排序按第一列为主键，相同时看第二列，再依次往下看。ascending 可以是一个布尔值，也可以是与排序键对应的布尔列表。

duplicated 返回每一行是否按给定列重复的布尔掩码；drop_duplicates 返回删去重复后的表。subset 指定判重列；不指定时默认比较所有数据列，索引本身不用于全行判重。keep="first"/"last" 指当前行序中保留首条/末条，keep=False 则把重复组所有成员都删掉。

因此“最新记录”必须先由时间确定排序，再按业务键去重。仅 keep="last" 不会替你理解日期。

## 二、为什么：数据处理顺序就是业务规则

订单可能多次修改：同一 order_id 对应多行，不同时间、不同金额。这些记录不一定是错误重复；若需求是“每订单当前状态”，才需要按规则选版本。

先去重再排序，可能留下旧版本，之后再排序也无法找回删掉的新版本。先排序再去重，才能让 first/last 对应你定义的时间优先级。

同一时间有多条记录也必须决定：用版本号、事件序号、或原始输入位置作为次级规则。不能把“刚好排在后面”当作业务定义。稳定排序能保留同键输入顺序，但不是自动解决所有多键并列的万能参数；需要时显式加入原始位置作为最后排序键。

时间文本有歧义时不应猜，比如 01/02/2026 到底是1月2日还是2月1日？本课明确格式 %Y-%m-%d 或 %Y-%m-%d %H:%M:%S。日期时间不含时区，本课统一视为同一当地时间口径；不把 utc=True 当作把当地时间“自动正确转换”的快捷方式。

## 三、怎么写：三个例题与手算

### 例题1：解析、缺失和日期属性
```python
import pandas as pd

raw = pd.Series(["2026-10-24","bad",None,"2026-02-30"], dtype="object")
parsed = pd.to_datetime(raw, format="%Y-%m-%d", errors="coerce")
print(parsed)
# 第一项为有效日期，后三项为 NaT

failed = raw.notna() & parsed.isna()
print(failed.tolist()) # [False,True,False,True]
print(parsed.dt.year)
print(parsed.dt.dayofweek) # 周一=0，周日=6；2026-10-24 是5
```
原始 None 与非法 "bad" 最终都表现为 NaT，因此如果要报告错误数量，应保留 raw 做交叉判断。invalid_count 不应把原本缺失也算成格式错误。
.dt 作用于日期时间 Series，不是任意文本列。格式化展示可用 .dt.strftime，但格式化后又是文本，不应继续把它当日期时间做运算。

日期差：
```python
start = pd.Timestamp("2026-10-23 23:00:00")
end = pd.Timestamp("2026-10-24 01:00:00")
elapsed = end-start
print(elapsed.total_seconds()/3600) # 2.0 小时
print(elapsed.days) # 0，不是跨了一个日历日期就算完整一天
```

### 例题2：时间区间与多键排序
```python
df = pd.DataFrame({
    "student":["A","B","C","D"],
    "score":[90,90,95,90],
    "minutes":[30,20,25,20],
}, index=["r8","r2","r9","r1"])
work = df.copy()
work["_pos"] = range(len(work))
ranked = work.sort_values(
    ["score","minutes","_pos"],
    ascending=[False,True,True],
).drop(columns="_pos")
print(ranked["student"].tolist()) # ["C","B","D","A"]
```
成绩越高越前，用时越短越前，完全并列时保持原输入顺序。B/D 的记录顺序由 _pos 明确决定，而不是按学生姓名偷偷破平局。原始索引 r9/r2/r1/r8 跟着记录保留，不 reset_index。

时间筛选建议常用半开区间 [start,end)：
```python
times = pd.Series(pd.to_datetime(
    ["2026-10-24 00:00:00","2026-10-24 23:59:59","2026-10-25 00:00:00"],
    format="%Y-%m-%d %H:%M:%S",
))
mask = (times>=pd.Timestamp("2026-10-24")) & (times<pd.Timestamp("2026-10-25"))
print(mask.tolist()) # [True,True,False]
```
用次日零点作右边界，比写当天23:59:59更容易覆盖精度更细的时间数据；终点不包含。缺失时间不入选。

### 例题3：保留每订单最新版本
```python
events = pd.DataFrame({
    "order_id":["A","B","A","B","A"],
    "updated_at":["2026-10-23 09:00:00","2026-10-24 08:00:00",
                  "2026-10-24 10:00:00","bad","2026-10-24 10:00:00"],
    "amount":[10,20,15,99,18],
}, index=["e1","e2","e3","e4","e5"])
work = events.copy()
work["updated_at"] = pd.to_datetime(
    work["updated_at"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
)
work["_pos"] = range(len(work))
valid = work.loc[work["updated_at"].notna()]
latest = (
    valid.sort_values(["updated_at","_pos"], ascending=[True,True])
    .drop_duplicates(subset=["order_id"], keep="last")
    .sort_values("order_id")
    .drop(columns="_pos")
)
print(latest[["order_id","amount"]])
# A:18（同时间选原输入更靠后的 e5），B:20（非法时间 e4 排除）
```
本例业务口径是：时间无效的版本不参与选择，时间相同选输入位置较后者，最终按订单编号升序输出。A 同时刻的15与18不能随意选；B 的99虽然在原表更靠后，时间无效，不能当最新。
这是示范口径，不是所有业务都应删除无效时间。生产数据可能需要错误表或人工核查；做题按题面执行。

## 四、易错点：原因与修正

1. 直接按非规范日期文本排序："2026-2-1" 与 "2026-10-1" 的字典序可能不等于时间先后。先解析，再按时间列排。
2. errors="coerce" 后静默忽略错误：保留原文本，统计“源非缺失且结果NaT”的解析失败数。
3. 用 ==NaT 判断缺失：改用 isna；NaT参与比较不能按普通日期相等规则理解。
4. 以为 .dt.dayofweek 周日是0：Pandas周一为0，周末为5/6。不要套另一系统的编号习惯。
5. keep="last" 当最新：它只看当前行序。先按有效时间和明确次级规则排，再判重。
6. 忽略 subset：同订单不同金额是业务键重复，不是全行重复；应该明确 subset=["order_id"]。
7. 给缺失时间 na_position="last" 后 keep="last"：无效时间可能被错误选中。先执行题定有效性规则，再排序。
8. 排序后赋值索引错位：别把排序后的 Series 生硬按位置拼回原表；整行随排序移动，保持标签语义。
9. 把去重等同集合：去重有保留次序和索引契约，不自动 reset_index，不自动汇总金额。
10. 修改输入或泄漏辅助列：使用 copy，结束时移除 _pos 等临时列；空结果也要保留正确日期dtype和列顺序。

## 五、何时用：用“解析→校验→排序→去重→验收”组织流程

要按真实时间筛选、做差、提取月份/星期时，先解析为日期时间。要做排行榜或输出顺序，明确每个排序键的方向及并列规则。要移除复制粘贴的重复行，使用全行判重；要保留每个实体的一条记录，使用业务键判重，并先决定“哪条应留下”。

不要为了减少行数就去重：重复可能代表多次真实交易。也不要把时间无效的记录自动认定为过期。数据质量规则、业务选择规则和展示排序分别写清楚，结果才可解释。

验收至少覆盖：非法日期、原始缺失、闰年、起止边界、并列排序、无序输入、同键同时间、全部无效、空表、原表不变。日期列用 is_datetime64_any_dtype 检查，不强制具体 ns/us 时间精度以免环境差异影响验收。

## 三道练习摘要
1. parse_event_dates：严格格式预校验后解析日期，区分缺失/失败/有效，新增月份和周末标记。
2. rank_attempts：成绩降序、用时升序、并列保持输入顺序，保留原索引。
3. latest_orders：排除无效时间，每订单选最新版本，同时间按原位置破平局。
完整题面和硬验收见 homework.md。答案开课先占位「约 9:30 写标准答案」，不代表标准答案已提交。

## 下节预告
L12 NumPy 进阶：花式索引与轴操作复习。

## 官方参考
https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html
