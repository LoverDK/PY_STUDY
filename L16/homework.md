# L16 作业：机试综合：Pandas 读洗筛汇小卷

三题Python+Pandas，各题独立可运行，输入表不修改。附完整断言。返回表统一reset_index(drop=True)。整数测试金额使用精确断言；禁止硬编码最终结果。

## 1. 库存读洗（独立输入）
实现clean_stock(csv_text)，用StringIO读取全部为string。列sku,category,stock。
先将sku/category去首尾空格、空串变缺失；去掉缺sku行；按sku保留文件中最后一行；再将stock转数值。保留category非缺失、stock有限非负整数的行。stock转int64，保持保留行的文件顺序。输出仅sku/category/stock。
```python
text = """sku,category,stock
 A ,book,3
B,pen,bad
A,book,5
C,pen,0
D,,2
E,book,-1
F,pen,1.5
G,book,2
G,book,bad
"""
out = clean_stock(text)
assert out.columns.tolist() == ["sku", "category", "stock"]
assert out["sku"].tolist() == ["A", "C"]
assert out["stock"].tolist() == [5, 0]
assert str(out["stock"].dtype) == "int64"
assert clean_stock("sku,category,stock\n").empty
```
笔试：解释为何G的旧库存2不能保留；为何stock缺失不填0？

## 2. 已支付高金额筛选（独立输入）
实现select_orders(df,min_amount=40)。输入已保证order_id唯一，quantity为正整数、unit_price为有限非负数，status已标准化。新增amount=quantity*unit_price；只保留status=="paid"且amount>=min_amount，按amount降序、order_id升序；输出order_id/amount两列。不得修改df。
```python
df = pd.DataFrame({
    "order_id":["A","B","C","D","E"],
    "quantity":[2,3,1,4,1],
    "unit_price":[20,20,60,10,10],
    "status":["paid","pending","paid","paid","cancelled"],
})
before = df.copy(deep=True)
out = select_orders(df)
pd.testing.assert_frame_equal(df,before)
assert out.columns.tolist() == ["order_id","amount"]
assert out["order_id"].tolist() == ["C","A","D"]
assert out["amount"].tolist() == [60,40,40]
assert select_orders(df,1000).empty
assert select_orders(df.iloc[:0]).columns.tolist() == ["order_id","amount"]
```
笔试：>=与>在边界40处的差别；为什么先派生金额、后整体排序能保持订单对应？

## 3. 地区营业报告（独立输入）
实现region_report(df)。输入是一订单一行，order_id唯一、region非缺失、amount有限非负、status标准化。仅汇总paid：order_count=size，revenue=sum(amount)，avg_order=revenue/order_count。按revenue降序、region升序输出region/order_count/revenue/avg_order。空结果必须保留这些列。
```python
df = pd.DataFrame({
    "order_id":["A","B","C","D","E"],
    "region":["East","West","East","North","West"],
    "amount":[20,60,40,60,100],
    "status":["paid","paid","paid","paid","cancelled"],
})
before = df.copy(deep=True)
out = region_report(df)
pd.testing.assert_frame_equal(df,before)
assert out.columns.tolist() == ["region","order_count","revenue","avg_order"]
assert out["region"].tolist() == ["East","North","West"]
assert out["order_count"].tolist() == [2,1,1]
assert out["revenue"].tolist() == [60,60,60]
assert out["avg_order"].tolist() == [30,60,60]
assert out["revenue"].sum() == df.loc[df["status"].eq("paid"),"amount"].sum()
assert region_report(df.iloc[:0]).empty
assert region_report(df.assign(status="cancelled")).columns.tolist() == out.columns.tolist()
```
笔试：订单表改成一单多明细后，为何size可能不是订单数？总额守恒为何不能代替地区级验收？

## 验收
每题结果50%、边界/输入不变25%、书面口径25%。不得沿用其他题的变量或预处理，三题应各自独立运行。
