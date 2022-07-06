import csv
import numpy as np 
import pandas as pd
import timeit


def is_pareto_efficient_simple(costs):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    is_efficient = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
    
        if is_efficient[i]:
            
            is_efficient[is_efficient] = np.any(costs[is_efficient]>c, axis=1)  # Keep any point with a lower cost
            is_efficient[i] = True  # And keep self

    return is_efficient


vectors = []
elements = []
df = pd.read_csv("statistics.csv")
for i in range(5050):
     vectors.append(list(df.loc[i])[2:])
     
     elements.append(list(df.loc[i]))

costs = np.array(vectors)

#print("is_pareto_efficient_simple: "
#    f"{(timeit.timeit('is_pareto_efficient_simple(costs)', number=5, globals=globals()))/5}")

lista = is_pareto_efficient_simple(costs)

pareto = []
for index, element in enumerate(lista):
    if element:
        pareto.append(elements[index])

with open('is_pareto_efficient_simple.csv', 'w') as file:
    writer = csv.writer(file)
    header = ["Symbol 1", "Symbol 2", "APR", "SHARPE", "price"]
    writer.writerow(header)
    for item in pareto:
        writer.writerow(item)

