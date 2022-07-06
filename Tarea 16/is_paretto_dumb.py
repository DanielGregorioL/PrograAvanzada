import csv
import numpy as np 
import pandas as pd
import timeit


# Very slow for many datapoints.  Fastest for many costs, most readable
def is_pareto_efficient_dumb(costs):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    is_efficient = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
        is_efficient[i] = np.all(np.any(costs[:i]<c, axis=1)) and np.all(np.any(costs[i+1:]<c, axis=1))
    return is_efficient


vectors = []
elements = []
df = pd.read_csv("statistics.csv")
for i in range(5050):
     vectors.append(list(df.loc[i])[2:])
     
     elements.append(list(df.loc[i]))

costs = np.matrix(vectors)

#print("is_pareto_efficient_dumb: "
#    f"{(timeit.timeit('is_pareto_efficient_dumb(costs)', number=5, globals=globals()))/5}")

lista = is_pareto_efficient_dumb(costs)

pareto = []
for index, element in enumerate(lista):
    if element:
        pareto.append(elements[index])

with open('is_pareto_efficient_dumb.csv', 'w') as file:
    writer = csv.writer(file)
    header = ["Symbol 1", "Symbol 2", "APR", "SHARPE", "price"]
    writer.writerow(header)
    for item in pareto:
        writer.writerow(item)