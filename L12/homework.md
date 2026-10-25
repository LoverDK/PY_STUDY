# L12 作业 · 花式索引与轴操作

Python/NumPy；不读写文件，不修改输入。A均为二维np.ndarray，dtype为有限实数的整数或浮点类型（非bool/complex/object），不要求处理NaN/无穷。输入维度不是2时ValueError。返回新数组，不与输入共享数值存储；输出顺序按题面。不允许用循环逐元素拼结果，核心使用NumPy索引/归约/广播。

## 1. 行列组合子矩阵
```python
def take_submatrix(A: np.ndarray, rows: list[int], cols: list[int]) -> np.ndarray:
    ...
```
使用np.ix_进行核心选择。rows/cols仅接受Python int且不含bool，否则TypeError；位置范围分别[-m,m-1]/[-n,n-1]，越界IndexError。允许乱序、重复、负位置和空列表。
输出shape=(len(rows),len(cols))，dtype同A；行列取所有组合，不是配对取点。即便其中一列表为空，也应检查另一列表所有位置是否有效；空维上的非空索引越界。
样例A=np.arange(12).reshape(3,4)，rows=[2,0]、cols=[3,1]→[[11,9],[3,1]]。
硬验收：配对陷阱、重复/负位置、乱序、rows/cols各自为空、同时为空、(0,3)/(2,0)数组、越界、bool/float位置；shape/dtype/数值准确，修改返回数组不影响A。

## 2. 逐行中心化
```python
def center_each_row(A: np.ndarray) -> np.ndarray:
    ...
```
若A列数为0，ValueError（包括shape=(0,0)）。其余返回Z，Z[i,j]=A[i,j]-第i行均值。必须使用mean(axis=1,keepdims=True)或等价明确保留维度的均值计算。结果float64、shape同A，输入不变且不共享存储。
shape=(0,n),n>0合法，返回同形float64空数组，不产生RuntimeWarning。
样例[[1,2,3],[10,20,30]]→[[-1,0,1],[-10,0,10]]。
硬验收：非方阵、方阵[[1,3],[10,20]]→[[-1,1],[-5,5]]、单列全0、单行、常数行、空行、零列错误；每行均值容差内为0，dtype正确，不在原整型数组上减浮点。

## 3. 筛选后每列均值
```python
def selected_column_means(A: np.ndarray, column: int, threshold: float) -> np.ndarray:
    ...
```
column为Python int且不是bool，否则TypeError；支持负位置。A无列或column越界时IndexError。threshold为有限实数（非bool）。
保留A[:,column]>=threshold的行，再按axis=0计算每列均值，结果shape=(A.shape[1],)，dtype float64。没有命中（包括0行）返回每列np.nan，不执行空mean、不产生RuntimeWarning。输入不变且不共享存储。
样例A=[[60,80],[90,70],[50,100]]，column=0，threshold=60→[75,75]；threshold=101→[nan,nan]。
硬验收：>=边界、负列号、单命中、全部命中、零命中、0行、0列、非法列类型/位置；使用assert_allclose(equal_nan=True)；检查不是选出所有>=阈值元素再求均值。

## 共同验收与笔试
先保存A.copy，再assert_array_equal原输入；shape独立断言，float用atol=1e-9比较；检查dtype与np.shares_memory。
异常输入在核心计算前拒绝；布尔位置不可当作0/1接收。无警告检查可用warnings.catch_warnings并把RuntimeWarning升级为错误。
解释：A[[0,2],[1,3]]与A[np.ix_([0,2],[1,3])]差在哪？(m,)为何不能可靠作为行均值减回(m,n)？视图/副本与直接索引赋值有什么不同？
标准答案路径homework/answers.ipynb，开课先占位「约 9:30 写标准答案」。
