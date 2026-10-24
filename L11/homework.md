# L11 作业 · 时间、排序与去重

Python/Pandas；不读写文件，不修改输入。索引唯一、列名唯一；禁止偷偷重置索引。除题面外无需处理任意类型、时区和超出Pandas支持范围的年份。若使用辅助列，必须移除；输入不含辅助列同名冲突。输入日期年份限定1900..2100。

## 1. 日期解析与质量标记
```python
def parse_event_dates(df: pd.DataFrame) -> pd.DataFrame:
    ...
```
输入列顺序 ["event_id","date_text"]，date_text 为 object dtype，元素是 str/None。
返回原列后追加 date、status、month、is_weekend：
- 非缺失文本先严格检查形如4位年-2位月-2位日（ASCII数字），不strip，不接受额外空格；再按 %Y-%m-%d 用 pd.to_datetime(errors="coerce") 检查日期有效性。
- 原始None：status="missing"；非缺失但格式或日期非法："invalid"；成功："valid"。status为object。
- date 为无时区datetime列，无效/缺失为NaT；不强制具体时间精度。
- month 为Pandas Int64，可缺失；is_weekend为Pandas boolean，周六/日True，工作日False，无效/缺失pd.NA。
- 不删除任何记录，保留原序和索引。空表输出同样列结构。

样例 date_text：
["2026-10-24","2026-10-26","2024-02-29","2026-02-29",None,"2026-1-2"," 2026-10-24"]
status→["valid","valid","valid","invalid","missing","invalid","invalid"]。
前三条month为10/10/2；前三条is_weekend为True/False/False，其余缺失。
硬验收：样例、空串、真实文本"None"、合法闰日/非法闰日、原始缺失、空表及单行；严格列序与dtype；date用isna核对；输入不变。可用Series.str.fullmatch做格式预检，正则只是辅助不展开专题。

## 2. 排行榜与并列
```python
def rank_attempts(df: pd.DataFrame) -> pd.DataFrame:
    ...
```
输入列顺序 ["student","score","minutes"]；student为非缺失str，score/minutes为float64。
score可缺失，非缺失须在[0,100]；minutes全部非缺失且>=0。非法数值抛ValueError；所有数值有限且不含bool。
排除score缺失行，按score降序、minutes升序，完全并列按原输入顺序；保留原列和dtype，原索引不变、不添加名次列。
样例 student=["A","B","C","D"]，score=[90,90,95,90]，minutes=[30,20,25,20]→student=["C","B","D","A"]。
硬验收：完全并列不按姓名重排；无序/非默认索引；空表/全缺失score；0/100边界；-1/101成绩、负/缺失minutes抛ValueError（即使该行score也缺失）。输入不变。

## 3. 每订单保留最新版本
```python
def latest_orders(df: pd.DataFrame) -> pd.DataFrame:
    ...
```
输入列顺序 ["order_id","updated_at","amount"]。order_id为非空、非缺失str；amount为有限float64，无需范围校验；updated_at为object，元素str/None。
- 时间文本先严格匹配 YYYY-MM-DD HH:MM:SS（ASCII数字），再按 %Y-%m-%d %H:%M:%S 解析errors="coerce"，无时区；不strip，不接受日期缩写或额外空白。
- 无效/缺失时间行不参与版本选择；某订单全无效则不输出该订单。
- 每个order_id选择时间最大行；同时间多条选原输入位置最后一条，不依据索引标签大小或amount。
- 最终按order_id原字符串字典序升序，保留被选行的原索引。
- 输出且仅输出原三列，updated_at替换为解析后的datetime列，其他dtype保持。
- 必须使用sort_values和drop_duplicates完成核心版本选择；不修改输入；空表/全无效返回结构正确空表。

样例见notes.md例题3：最终索引e5/e2，A金额18，B金额20。
硬验收：乱序输入、同时间并列、无效时间位于末尾、全无效订单、空表、一个订单、不同索引标签顺序；同一业务键多条而非全行相同时仍正确判重；不存在辅助列。使用assert_frame_equal比较，日期精度可归一后核对。

## 共同自检
每题保留输入deep copy并比较；同时检查返回对象不是输入。检查边界和空表，而不只检查样例。
笔试：keep="last"为什么不自动代表最新？subset判重是否包含索引？区间[start,end)有什么好处？如何区分原始缺失与解析失败？
标准答案路径homework/answers.ipynb，开课占位「约 9:30 写标准答案」。
