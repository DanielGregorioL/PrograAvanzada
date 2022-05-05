g = {('0', '0'): '0', ('0', '1'): '1', ('1', '0'): '1', ('1', '1'): '2', ('0', '2'): '2', ('2', '0'): '2',
     ('1', '2'): '0', ('2', '1'): '0', ('2', '2'): '1'}


def g_elements(x):
    """
    función para obtener los elementos de un grupo
    :param x: un diccionario que contiene la información de como se realiza la operacion de suma
    entre cada dos elementos
    :return: regresa los elementos del grupo
    """
    elements = set()
    for a in x:
        elements.add(a[0])
        elements.add(a[1])
    return elements


def is_closed(x):
    """
    función para derteminar si el conjunto que nos estan mostrando es cerrado bajo la operación
    :param x: un diccionario que contiene la información de como se realiza la operacion de suma
    entre cada dos elementos
    :return: True si es cerrado, False en otro caso
    """
    a = g_elements(x)
    b = set(x.values())
    if a == b:
        return True
    else:
        return False


def is_associative(x):
    """
    función para derteminar si la operación es asociativa
    :param x: un diccionario que contiene la información de como se realiza la operacion de suma
    entre cada dos elementos
    :return: True si es asociativa, False en otro caso
    """
    elements = g_elements(x)
    for a in elements:
        for b in elements:
            ab = x[(a, b)]
            for c in elements:
                bc = x[(b, c)]
                ab_c = x[(ab, c)]
                a_bc = x[(a, bc)]
                if ab_c != a_bc:
                    return False
    return True


def identity_element(x):
    """
    función para derteminar si el conjunto tiene un elemento neutro (de hecho solo debe haber uno)
    :param x: un diccionario que contiene la información de como se realiza la operacion de suma
    entre cada dos elementos
    :return: el neutro  si es que lo hay False en otro caso
    """
    elements = g_elements(x)
    k = len(elements)
    neutro = []
    count = 0
    for a in elements:
        n = 0
        for b in elements:
            if x[(a, b)] == b and x[(b, a)] == b:
                n = n + 1
        if n == k:
            neutro.append(a)
            count = count + 1
    if count != 1:
        return False
    else:
        return neutro[0]


def closed_inverse_element(x):
    """
    función para derteminar si todo elemento tiene inverso, el cual solo tiene sentido si el conjunto
    tiene un elemento neutro
    :param x: un diccionario que contiene la información de como se realiza la operacion de suma
    entre cada dos elementos
    :return: True si todos tienen inverso, False en otro caso
    """

    e = identity_element(x)
    elements = g_elements(x)
    k = len(elements)
    count = 0
    for a in elements:
        for b in elements:
            if x[(a, b)] == e and x[(b, a)] == e:
                count = count + 1
    if count != k:
        return False
    else:
        return True


def inverse_element(o):
    """
    función para derteminar el inverso de un elemento
    :param o: el elemento del grupo
    :return: el inverso de un elemento del grupo
    """

    e = identity_element(g)
    elements = g_elements(g)
    for a in elements:
        if g[(o, a)] == e and g[(a, o)] == e:
            return a


def is_conmutative(x):
    """
    función para derteminar si el grupo es conmutativo o no
    tiene un elemento neutro
    :param x: un diccionario que contiene la información de como se realiza la operacion de suma
    entre cada dos elementos
    :return: True si el grupo es conmutativo, False en otro caso
    """
    elements = g_elements(x)
    count = 0
    for a in elements:
        for b in elements:
            ab = x[(a, b)]
            ba = x[(b, a)]
            if ab != ba:
                count = count + 1
    if count != 0:
        return False
    else:
        return True


def orden_element(u: str):
    """
    función para dertemina el orden de un elemento del grupo
    :param u: el elemento del grupo al cual le vamos a calcular su orden
    :return: una lista con los ordenes de todos los elementos
    """
    e = identity_element(g)
    elements = g_elements(g)
    lista = [u]
    for j in range(1, len(elements)):
        p = (lista[j-1], u)
        lista.append(g[p])
    m = lista.index(e)
    order = m + 1
    return order


class G:
    def __init__(self, a):
        self.a = a

    # adding two objects
    def __add__(self, o):
        return G(g[(self.a, o.a)])

    def __sub__(self, o):
        return G(g[(self.a, inverse_element(o.a))])

    def __str__(self):
        return f'{self.a}'


cl = is_closed(g)
asso = is_associative(g)
iden = identity_element(g)
inve = closed_inverse_element(g)
conmutativo = is_conmutative(g)
if g != {}:
    if cl and asso and iden is not False and inve:
        print("En efecto, lo que usted ingresó es la tabla de multiplicación de un grupo")
    else:
        print("Lo que ingresó no es la tabla de multiplicación de un grupo")

    if conmutativo is True:
        print("El grupo es conmutativo")
    else:
        print("El grupo no es conmutativo")
else:
    print("El grupo no debe ser vacío")


print(f"el orden de {'0'} es {orden_element('0')}")

print(G("2") + G("2") - G("1"))
