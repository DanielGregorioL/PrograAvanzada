import csv
import numpy as np 
import pandas as pd
import timeit


def is_pareto_efficient(costs, return_mask = True):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :param return_mask: True to return a mask
    :return: An array of indices of pareto-efficient points.
        If return_mask is True, this will be an (n_points, ) boolean array
        Otherwise it will be a (n_efficient_points, ) integer array of indices.
    """
    is_efficient = np.arange(costs.shape[0])
    n_points = costs.shape[0]
    next_point_index = 0  # Next index in the is_efficient array to search for
    while next_point_index<len(costs):
        nondominated_point_mask = np.any(costs>costs[next_point_index], axis=1)
        nondominated_point_mask[next_point_index] = True
        is_efficient = is_efficient[nondominated_point_mask]  # Remove dominated points
        costs = costs[nondominated_point_mask]
        next_point_index = np.sum(nondominated_point_mask[:next_point_index])+1

    if return_mask:
        is_efficient_mask = np.zeros(n_points, dtype = bool)
        is_efficient_mask[is_efficient] = True
        return is_efficient_mask
    else:
        return is_efficient


vectors = []
elements = []
df = pd.read_csv("statistics.csv")
for i in range(5050):
     vectors.append(list(df.loc[i])[2:])  
     elements.append(list(df.loc[i]))

costs = np.array(vectors)

#print("is_pareto_efficient: "
#    f"{(timeit.timeit('is_pareto_efficient(costs)', number=5, globals=globals()))/5}")

lista = is_pareto_efficient(costs)

pareto = []
for index, element in enumerate(lista):
    if element:
        pareto.append(elements[index])

with open('is_pareto_efficient.csv', 'w') as file:
    writer = csv.writer(file)
    header = ["Symbol 1", "Symbol 2", "APR", "SHARPE", "price"]
    writer.writerow(header)
    for item in pareto:
        writer.writerow(item)
