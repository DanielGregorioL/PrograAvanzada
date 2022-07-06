"""The csv module implements classes to read and write tabular data in CSV format"""
import csv
import numpy as np
import pandas as pd


def dominado(element, vector_set):
    """
    Esta función recibe un elemento element (un arreglo de n entradas) y una lista S de
    vectores de n entradas vector_set, donde element no está en S. Luego si x domina algún
    elemento de S, elimina al elemento dominado. Análogamente, si algún elemento
    de S domina a element, entonces eliminamos a element. Si element no es
    dominado por ningún elemento de S entonces regresamos el par ordenado
    ([element],new_list) y si element si es dominado entonces regresamos el par ordenado
    ([],new_list), donde new_list contiene todos los elementos de vector_set que no son
    dominados por element.
    """

    new_list = vector_set
    for index, elemento in enumerate(vector_set):
        compare = element >= elemento
        if False not in compare:
            del new_list[index]

    count = 0
    for elemento in new_list:
        compare = elemento >= element
        if False not in compare:
            count += 1
            break
    return ([element], new_list) if count == 0 else ([], new_list)


def paretto_mine(lista):
    """
    Función que devuelve el frente de pareto de un subconjunto finito de puntos en Rn
    lista: es una lista finita de elementos en rn
    """
    pareto_front = []
    garb = 1
    vector_sp = lista
    while garb != 0:
        if len(vector_sp) > 1:
            recursive = dominado(vector_sp[0], vector_sp[1:])
            if recursive[0]:
                pareto_front.append(recursive[0][0])
            if len(recursive[1]) > 1:
                vector_sp = recursive[1]
            if len(recursive[1]) == 1:
                pareto_front.append(recursive[1][0])
                break
            if len(recursive[1]) == 0:
                garb = 0
    return pareto_front


vectors = []
vectors_p = []
elements = []
df = pd.read_csv("statistics.csv")
for i in range(5050):
    vectors.append(list(df.loc[i])[2:])
    vectors_p.append(np.array(list(df.loc[i])[2:]))
    elements.append(list(df.loc[i]))

# print("paretto_mine: "
#    f"{(timeit.timeit('paretto_mine(vectorsp)', number=1, globals=globals()))}")

cara_pareto = paretto_mine(vectors_p)

pareto = []
for item in cara_pareto:
    i = vectors.index(list(item))
    pareto.append(elements[i])

with open('paretto_mine.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    header = ["Symbol 1", "Symbol 2", "APR", "SHARPE", "price"]
    writer.writerow(header)
    for item in pareto:
        writer.writerow(item)


    



