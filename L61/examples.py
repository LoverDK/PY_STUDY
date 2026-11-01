"""L61：三类学习的可追踪小例子；数据内嵌，不读写磁盘。"""
from math import isclose


def fit_threshold(xs, ys):
    if not xs or len(xs) != len(ys):
        raise ValueError("训练输入须非空且长度一致")
    if any(y not in (0, 1) for y in ys):
        raise ValueError("标签须为0或1")
    unique = sorted(set(xs))
    if len(unique) < 2:
        raise ValueError("本教学模型至少需要两个不同输入")
    candidates = [(a+b)/2 for a,b in zip(unique, unique[1:])]
    best_t, best_errors = None, len(xs)+1
    trace = []
    for t in candidates:
        predictions = [int(x > t) for x in xs]
        errors = sum(p != y for p,y in zip(predictions, ys))
        trace.append((t, predictions, errors))
        if errors < best_errors:
            best_t, best_errors = t, errors
    return best_t, trace


def cluster_round(points, centers):
    if not centers:
        raise ValueError("中心不能为空")
    groups = [[] for _ in centers]
    labels, trace = [], []
    for x in points:
        distances = [abs(x-c) for c in centers]
        group = min(range(len(centers)), key=lambda j: distances[j])
        labels.append(group)
        groups[group].append(x)
        trace.append((x, distances, group))
    updated = [
        sum(group)/len(group) if group else centers[j]
        for j,group in enumerate(groups)
    ]
    return labels, updated, trace


def q_update(q, state, action, reward, next_state, done,
             alpha=0.5, gamma=0.9):
    old = q.get((state, action), 0.0)
    future = 0.0 if done else max(
        q.get((next_state, a), 0.0) for a in ("L","R")
    )
    target = reward + gamma*future
    new = old + alpha*(target-old)
    q[(state, action)] = new
    return old, future, target, new


def q_demo():
    q = {}
    transitions = [
        (0, "R", 0, 1, False),
        (1, "R", 1, 2, True),
        (0, "R", 0, 1, False),
        (1, "R", 1, 2, True),
    ]
    trace = []
    for transition in transitions:
        trace.append((transition, q_update(q, *transition)))
    return q, trace


def sklearn_demo():
    # 仅API体验；树的训练算法将在L68展开。两条新输入不参与fit。
    from sklearn.tree import DecisionTreeClassifier
    X_train = [[1.0], [2.0], [3.0], [4.0]]
    y_train = [0, 0, 1, 1]
    X_test = [[1.2], [3.2]]
    model = DecisionTreeClassifier(max_depth=1, random_state=0)
    model.fit(X_train, y_train)
    return model.predict(X_test).tolist()


def self_check():
    xs, ys = [1,2,3,4], [0,0,1,1]
    before_x, before_y = xs.copy(), ys.copy()
    threshold, trace = fit_threshold(xs, ys)
    assert threshold == 2.5
    assert trace == [
        (1.5, [0,1,1,1], 1),
        (2.5, [0,0,1,1], 0),
        (3.5, [0,0,0,1], 1),
    ]
    assert xs == before_x and ys == before_y
    # 并列错误时保留较小候选。
    assert fit_threshold([1,2,3], [0,1,0])[0] == 1.5
    for x, y in [([], []), ([1], [0]), ([1,2], [0]), ([1,2], [0,2])]:
        try:
            fit_threshold(x, y)
        except ValueError:
            pass
        else:
            raise AssertionError("非法训练输入应拒绝")
    points, centers = [0,2,4,6], [0,6]
    labels, updated, trace = cluster_round(points, centers)
    assert labels == [0,0,1,1] and updated == [1,5]
    assert trace == [(0,[0,6],0),(2,[2,4],0),(4,[4,2],1),(6,[6,0],1)]
    assert points == [0,2,4,6] and centers == [0,6]
    assert cluster_round([3], [0,6])[:2] == ([0], [3,6])
    assert cluster_round([], [0,6])[:2] == ([], [0,6])
    q, trace = q_demo()
    assert isclose(q[(0,"R")], 0.225)
    assert isclose(q[(1,"R")], 0.75)
    expected = [(0,0,0,0),(0,0,1,0.5),(0,0.5,0.45,0.225),(0.5,0,1,0.75)]
    for (_, actual), want in zip(trace, expected):
        assert all(isclose(a,b) for a,b in zip(actual,want))
    # 终止状态即使误留很大的Q也不应被加入目标。
    terminal = {(2,"R"): 999}
    assert q_update(terminal,1,"R",1,2,True)[-1] == 0.5
    assert sklearn_demo() == [0,1]
    # 对照讲义中的理论数值：经验风险、聚类目标、折扣回报。
    _, risk_rows = fit_threshold([1,2,3,4], [0,0,1,1])
    assert [row[2]/4 for row in risk_rows] == [0.25,0.0,0.25]
    points, assignments = [0,2,4,6], [0,0,1,1]
    before = sum((x-[0,6][j])**2 for x,j in zip(points,assignments))
    after = sum((x-[1,5][j])**2 for x,j in zip(points,assignments))
    assert (before, after) == (8, 4)
    assert isclose(sum((0.9**t)*r for t,r in enumerate([0,1])), 0.9)


def main():
    self_check()
    print("L61全部自检通过")
    threshold, rows = fit_threshold([1,2,3,4], [0,0,1,1])
    print("\n监督：(候选阈值,训练预测,错分数)")
    for row in rows:
        print(row)
    print("最终阈值", threshold, "新输入预测", [int(x>threshold) for x in [1.2,3.2]])
    labels, centers, rows = cluster_round([0,2,4,6], [0,6])
    print("\n无监督一轮：(输入,到旧中心距离,簇号)")
    for row in rows:
        print(row)
    print("新中心", centers)
    q, rows = q_demo()
    print("\n固定经历Q更新：(经历,(旧Q,future,target,新Q))")
    for row in rows:
        print(row)
    print("最终Q", q)
    print("\nsklearn fit/predict新输入结果", sklearn_demo())


if __name__ == "__main__":
    main()
