"""An object-oriented plotting library. """
import matplotlib.pyplot as plt

number = int(input("Ingrese el número de iteraciones: "))
length = 1 / (2 ** number - 1)


def type_a(number_iter, initial_p):
    """
    Esta función traza la curva A de nivel number_iter comenzando en la posición inicial
    initial_p, pero además devuelve su punto donde finaliza.

    Parameters
    ----------
    number_iter: Numero de iteraciones
    initial_p: Vector que indica a partir de donde se va a empezar a trazar la curva,
    es un vector de la forma [point_x, point_y]
    """
    if number_iter == 1:
        point_x = [initial_p[0], initial_p[0] - length, initial_p[0] - length, initial_p[0]]
        point_y = [initial_p[1], initial_p[1], initial_p[1] - length, initial_p[1] - length]
        plt.plot(point_x, point_y)
        return [initial_p[0], initial_p[1] - length]
    if number_iter > 1:
        p_prima = type_b(number_iter - 1, initial_p)
        point_x = [p_prima[0], p_prima[0] - length]
        point_y = [p_prima[1], p_prima[1]]
        plt.plot(point_x, point_y)
        point_2 = type_a(number_iter - 1, [p_prima[0] - length, p_prima[1]])
        point_x2 = [point_2[0], point_2[0]]
        point_y2 = [point_2[1], point_2[1] - length]
        plt.plot(point_x2, point_y2)
        point_3 = type_a(number_iter - 1, [point_2[0], point_2[1] - length])
        point_x3 = [point_3[0], point_3[0] + length]
        point_y3 = [point_3[1], point_3[1]]
        plt.plot(point_x3, point_y3)
        # D(n-1,[point_3[0]+length,point_3[1]])
        return type_d(number_iter - 1, [point_3[0] + length, point_3[1]])


def type_b(number_iter, initial_p):
    """
    Esta función traza la curva B de nivel number_iter comenzando en la posición inicial
    initial_p, pero además devuelve su punto donde finaliza.

    Parameters
    ----------
    number_iter: Numero de iteraciones
    initial_p: Vector que indica a partir de donde se va a empezar a trazar la curva,
    es un vector de la forma [point_x, point_y]
    """
    if number_iter == 1:
        point_x = [initial_p[0], initial_p[0], initial_p[0] - length, initial_p[0] - length]
        point_y = [initial_p[1], initial_p[1] - length, initial_p[1] - length, initial_p[1]]
        plt.plot(point_x, point_y)
        return [initial_p[0] - length, initial_p[1]]

    if number_iter > 1:
        p_prima = type_a(number_iter - 1, initial_p)
        point_x = [p_prima[0], p_prima[0]]
        point_y = [p_prima[1], p_prima[1] - length]
        plt.plot(point_x, point_y)
        point_2 = type_b(number_iter - 1, [p_prima[0], p_prima[1] - length])
        point_x2 = [point_2[0], point_2[0] - length]
        point_y2 = [point_2[1], point_2[1]]
        plt.plot(point_x2, point_y2)
        point_3 = type_b(number_iter - 1, [point_2[0] - length, point_2[1]])
        point_x3 = [point_3[0], point_3[0]]
        point_y3 = [point_3[1], point_3[1] + length]
        plt.plot(point_x3, point_y3)
        # C(n-1,[point_3[0],point_3[1]+length])  #error
        return type_c(number_iter - 1, [point_3[0], point_3[1] + length])


def type_c(number_iter, initial_p):
    """
    Esta función traza la curva C de nivel number_iter comenzando en la posición inicial
    initial_p, pero además devuelve su punto donde finaliza.

    Parameters
    ----------
    number_iter: Numero de iteraciones
    initial_p: Vector que indica a partir de donde se va a empezar a trazar la curva,
    es un vector de la forma [point_x, point_y]
    """
    if number_iter == 1:
        point_x = [initial_p[0], initial_p[0] + length, initial_p[0] + length, initial_p[0]]
        point_y = [initial_p[1], initial_p[1], initial_p[1] + length, initial_p[1] + length]
        plt.plot(point_x, point_y)
        return [initial_p[0], initial_p[1] + length]

    if number_iter > 1:
        p_prima = type_d(number_iter - 1, initial_p)
        point_x = [p_prima[0], p_prima[0] + length]
        point_y = [p_prima[1], p_prima[1]]
        plt.plot(point_x, point_y)
        point_2 = type_c(number_iter - 1, [p_prima[0] + length, p_prima[1]])
        point_x2 = [point_2[0], point_2[0]]
        point_y2 = [point_2[1], point_2[1] + length]
        plt.plot(point_x2, point_y2)
        point_3 = type_c(number_iter - 1, [point_2[0], point_2[1] + length])
        point_x3 = [point_3[0], point_3[0] - length]
        point_y3 = [point_3[1], point_3[1]]
        plt.plot(point_x3, point_y3)
        # B(n-1,[point_3[0]-length,point_3[1]])
        return type_b(number_iter - 1, [point_3[0] - length, point_3[1]])


def type_d(number_iter, initial_p):
    """
    Esta función traza la curva D de nivel number_iter comenzando en la posición inicial
    initial_p, pero además devuelve su punto donde finaliza.

    Parameters
    ----------
    number_iter: Numero de iteraciones
    initial_p: Vector que indica a partir de donde se va a empezar a trazar la curva,
    es un vector de la forma [point_x, point_y]
    """
    if number_iter == 1:
        point_x = [initial_p[0], initial_p[0], initial_p[0] + length, initial_p[0] + length]
        point_y = [initial_p[1], initial_p[1] + length, initial_p[1] + length, initial_p[1]]
        plt.plot(point_x, point_y)
        return [initial_p[0] + length, initial_p[1]]

    if number_iter > 1:
        p_prima = type_c(number_iter - 1, initial_p)
        point_x = [p_prima[0], p_prima[0]]
        point_y = [p_prima[1], p_prima[1] + length]
        plt.plot(point_x, point_y)
        point_2 = type_d(number_iter - 1, [p_prima[0], p_prima[1] + length])
        point_x2 = [point_2[0], point_2[0] + length]
        point_y2 = [point_2[1], point_2[1]]
        plt.plot(point_x2, point_y2)
        point_3 = type_d(number_iter - 1, [point_2[0] + length, point_2[1]])
        point_x3 = [point_3[0], point_3[0]]
        point_y3 = [point_3[1], point_3[1] - length]
        plt.plot(point_x3, point_y3)
        # A(n-1,[point_3[0],point_3[1]-length])
        return type_a(number_iter - 1, [point_3[0], point_3[1] - length])


type_a(number, [1, 1])
plt. axis('off')
plt.show()
