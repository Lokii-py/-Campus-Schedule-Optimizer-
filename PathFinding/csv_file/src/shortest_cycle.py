import pandas as pd
from pathlib import Path
import pulp

def DataPrep(route="../csv_file/mst_distance_matrix_meters.csv"):
    """Data peperation"""

    csv_path = Path(route)
    df = pd.read_csv(csv_path, index_col = 0)

    buildings = df.columns.tolist()

    distances = df.to_dict('index')

    return buildings, distances

def solve(buildings:list, distances:dict):

    """
    Problem Setup with variables
    a. create a main problem object
    b. create the decision variables
    """
    
    prob = pulp.LpProblem("MST_TSP", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("path", (buildings, buildings), cat="Binary")
    N = len(buildings)
    u = pulp.LpVariable.dicts("order", buildings, lowBound=1, upBound=N, cat='Continuous')


    prob += pulp.lpSum([distances[i][j] * x[i][j] for i in buildings for j in buildings if i != j])

    # Rule 1: Arrive at each building once
    for j in buildings:
        prob += pulp.lpSum([x[i][j] for i in buildings if i != j]) == 1

    # Rule 2: Leave from each building once
    for i in buildings:
        prob += pulp.lpSum([x[i][j] for j in buildings if i != j]) == 1

    # Rule 3: Subtour elimination constraint
    for i in buildings:
        for j in buildings:
            if i != j and (i != buildings[0] and j != buildings[0]):
                prob += u[i] - u[j] + N * x[i][j] <= N - 1

    prob.solve()

    print(f"Status: {pulp.LpStatus[prob.status]}")
    print(f"Total Distance of the optimal tour: {pulp.value(prob.objective)} meters")

    print("\nReconstructing the ordered tour...")

    successors = {i: j for i in buildings for j in buildings if i != j and pulp.value(x[i][j]) == 1}

    current_building = buildings[0]
    ordered_tour = []
    for _ in range(len(buildings)):
        ordered_tour.append(current_building)
        current_building = successors[current_building]

    print("\nOptimal Tour Path:")
    for i, building in enumerate(ordered_tour):
        print(f"  {i+1}. {building} -> {ordered_tour[(i + 1) % len(ordered_tour)]}")
    
    print(f"  {len(ordered_tour)+1}. {ordered_tour[0]} (return to start)")
    
    return ordered_tour


