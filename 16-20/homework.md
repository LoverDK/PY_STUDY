# 16-20 综合作业
三题独立Python运行；不得硬编码结果，不写本地文件。

## 1. clean_report(text)
输入CSV列order_id,region,amount,status。文本去空格，空串变缺失，status小写；剔除缺订单号，按文件顺序保留最后行，再转换金额。只保留地区非缺失、金额有限非负、status为paid的行。按地区汇总revenue，收入降序地区升序；返回region/revenue两列，索引重置。缺必需列抛ValueError，空结果保留列。
```python
s="order_id,region,amount,status\nA,East,10,paid\nB,West,30,paid\nA,East,20,paid\nC,West,bad,paid\nD,North,99,cancelled\n"
out=clean_report(s)
assert out.columns.tolist()==["region","revenue"]
assert out["region"].tolist()==["West","East"]
assert out["revenue"].tolist()==[30,20]
assert clean_report("order_id,region,amount,status\n").empty
assert clean_report("order_id,region,amount,status\nA,East,2,paid\nA,East,bad,paid\n").empty
```
书面说明去重顺序、总额验收、空表和缺列的区别。

## 2. chart_spec(summary)
输入已按展示顺序排列的DataFrame，列region/revenue、地区唯一、收入有限非负。返回字典，键kind,x,y,xlabel,ylabel,ymin；kind="bar"，x/y按输入顺序分别取列表，xlabel="Region"，ylabel="Revenue (CNY)"，ymin=0。输入不改动；不创建图片。再写出实际Matplotlib作图的5条核心指令，并解释柱图零基线。
```python
import pandas as pd
df=pd.DataFrame({"region":["West","East"],"revenue":[30,20]})
before=df.copy(deep=True)
out=chart_spec(df)
assert out=={"kind":"bar","x":["West","East"],"y":[30,20],"xlabel":"Region","ylabel":"Revenue (CNY)","ymin":0}
pd.testing.assert_frame_equal(df,before)
assert chart_spec(df.iloc[:0])["x"]==[]
assert chart_spec(df.iloc[:0])["y"]==[]
```

## 3. parse_scores(items, strict=True)
输入字符串列表。逐项float转换，并验证有限且0<=值<=100。严格模式遇首个无效项立即抛ValueError，错误文字包含其0起始索引；宽容模式返回(有效值列表,错误索引列表)。严格模式成功也返回该二元组。只捕获需要的转换异常，不吞掉所有异常。输入不修改。
```python
assert parse_scores(["0"," 90 ","100"])==([0.0,90.0,100.0],[])
assert parse_scores([],False)==([],[])
assert parse_scores(["80","bad","nan","-1","100"],False)==([80.0,100.0],[1,2,3])
try:
    parse_scores(["80","inf"])
except ValueError as exc:
    assert "1" in str(exc)
else:
    raise AssertionError("必须抛出异常")
a=["50","bad"]
before=a.copy()
parse_scores(a,False)
assert a==before
```
书面说明裸except的问题、可变默认参数风险以及处理m项的时间/输出空间（另计字符串解析长度）。
