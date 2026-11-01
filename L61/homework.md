# L61 作业：机器学习地图
3题Python独立运行，不写文件、不依赖网络。附代码、硬验收与书面说明，禁止硬编码结果。

## 1. route_task(has_labels, target_kind, interaction)
编写确定性任务分流函数：interaction=True时返回"reinforcement"（本题明确指行动改变后续状态、学习累计回报，不是普通在线预测）；否则has_labels=True时，target_kind为"category"返回"classification"，为"number"返回"regression"，其他值抛ValueError；否则返回"unsupervised"。函数输入布尔值由题目保证。
```python
assert route_task(True,"category",False)=="classification"
assert route_task(True,"number",False)=="regression"
assert route_task(False,None,False)=="unsupervised"
assert route_task(False,None,True)=="reinforcement"
assert route_task(True,"category",True)=="reinforcement"
try:
    route_task(True,"unknown",False)
except ValueError:
    pass
else:
    raise AssertionError("目标类型非法应拒绝")
```
笔试：给垃圾邮件分类、房价预测、无标签客户分组、机器人走迷宫各写X/y或状态/动作/奖励。解释本函数是题目规定的分类规则，不是任何真实混合系统的充分判定器。

## 2. threshold_report(xs, ys, threshold)
用固定阈值逐样本预测：x>threshold返回1，否则0；返回(预测列表,错分数)。输入有限实数，ys只允许0/1；长度不一致或非法标签抛ValueError；空输入返回([],0)；不得修改输入。不是训练函数，禁止根据ys调整threshold。
```python
assert threshold_report([1,2,3,4],[0,0,1,1],2.5)==([0,0,1,1],0)
assert threshold_report([2.5,3],[1,1],2.5)==([0,1],1)
assert threshold_report([],[],0)==([],0)
x,y=[1,2],[1,0]
before=(x.copy(),y.copy())
assert threshold_report(x,y,1.5)==([0,1],2)
assert (x,y)==before
for bad_x,bad_y in [([1],[]),([1],[2])]:
    try:
        threshold_report(bad_x,bad_y,0)
    except ValueError:
        pass
    else:
        raise AssertionError("须拒绝非法输入")
```
笔试：画出第一组4步表格；说明分类和回归差别、fit与predict差别，以及为什么不能用测试标签改阈值。

## 3. discounted_return(rewards, gamma)
一条已经发生的固定轨迹有奖励r0,r1,...，计算r0+gamma*r1+gamma²*r2+...。gamma须在[0,1]，否则ValueError；奖励保证有限数。空奖励返回0.0，不修改输入。用循环记录每步权重与累计值，返回(总回报, trace)，trace每项为(下标,当前权重,当前累计回报)。
```python
from math import isclose
value,trace=discounted_return([0,0,1],0.9)
assert isclose(value,0.81)
assert len(trace)==3
assert trace[0]==(0,1.0,0.0)
assert isclose(trace[1][1],0.9)
assert isclose(trace[2][1],0.81)
assert isclose(trace[2][2],0.81)
assert discounted_return([],0.9)==(0.0,[])
assert discounted_return([2,3],1)[0]==5
assert discounted_return([2,3],0)[0]==2
for gamma in (-0.1,1.1):
    try:
        discounted_return([1],gamma)
    except ValueError:
        pass
    else:
        raise AssertionError("非法折扣应拒绝")
```
笔试：该函数为何只是评估已知奖励序列，不是训练强化学习策略？若只看最后一步即时奖励，会漏掉什么？时间与trace空间分别是多少？

## 评分
代码和结果50%，边界/输入不变25%，逐步表格与概念解释25%。本课不要求完整训练RL系统，不使用聚类编号直接当业务标签。
