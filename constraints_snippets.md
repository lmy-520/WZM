# 约束模板库（优化题最值）

> 每条模板包含三段：中文含义、数学式、PuLP 代码片段。

---

## 1) 最多选 K 个
- 中文含义：从候选集合中最多选择 `K` 个对象。
- 数学式：
  $$\sum_i y_i \le K,\quad y_i\in\{0,1\}$$
- PuLP：
```python
prob += pulp.lpSum(y[i] for i in I) <= K
```

## 2) 蕴含约束（若选 A 则选 B）
- 中文含义：A 被选择时，B 必须被选择。
- 数学式：
  $$y_A \le y_B$$
- PuLP：
```python
prob += y["A"] <= y["B"]
```

## 3) 互斥约束（A 与 B 不能同时选）
- 中文含义：A、B 至多选一个。
- 数学式：
  $$y_A + y_B \le 1$$
- PuLP：
```python
prob += y["A"] + y["B"] <= 1
```

## 4) 容量约束
- 中文含义：设施 `i` 的分配总量不能超过容量上限。
- 数学式：
  $$\sum_j x_{ij} \le \mathrm{Cap}_i$$
- PuLP：
```python
for i in I:
    prob += pulp.lpSum(x[i][j] for j in J) <= cap[i]
```

## 5) 需求满足约束
- 中文含义：每个需求点 `j` 的需求必须被满足（可按等于/大于设置）。
- 数学式：
  $$\sum_i x_{ij} = d_j$$
- PuLP：
```python
for j in J:
    prob += pulp.lpSum(x[i][j] for i in I) == demand[j]
```

## 6) 启用-分配联动（Big-M）
- 中文含义：只有启用设施 `i`，才允许给它分配流量。
- 数学式：
  $$\sum_j x_{ij} \le M\,y_i$$
- PuLP：
```python
for i in I:
    prob += pulp.lpSum(x[i][j] for j in J) <= M * y[i]
```

## 7) 预算约束
- 中文含义：总成本不能超过预算上限。
- 数学式：
  $$\sum_i c_i y_i + \sum_{i,j} c_{ij}x_{ij} \le B$$
- PuLP：
```python
prob += (
    pulp.lpSum(c_open[i] * y[i] for i in I)
    + pulp.lpSum(c_ship[i][j] * x[i][j] for i in I for j in J)
    <= budget
)
```

## 8) 变量取值域模板
- 中文含义：统一声明变量类型与上下界。
- 数学式：
  $$x_{ij}\ge 0,\quad y_i\in\{0,1\}$$
- PuLP：
```python
x = pulp.LpVariable.dicts("x", (I, J), lowBound=0, cat="Continuous")
y = pulp.LpVariable.dicts("y", I, lowBound=0, upBound=1, cat="Binary")
```
