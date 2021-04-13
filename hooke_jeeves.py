import math
import numpy as np
from matplotlib.patches import ConnectionPatch


def norm(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


dim = 2


def hooke_jeeves(fun, u, h, eps_step, eps_abs, max_iterations, plot):
    """
    Implementation of the Hooke-Jeeves algorithm

    :param fun: function to be minimized
    :param u: initial approximation of the minimum
    :param h: initial step size
    :param eps_step: step epsilon size constraint
    :param eps_abs: absolute epsilon size constraint
    :param max_iterations: max number of iterations
    :param plot: the plot on which to draw progress
    :return: position of the apparent minimum, value at that point
    """

    print("Algorytm Hooke'a-Jeevesa")

    # transform to numpy array to use vector functions
    u = np.array(u)
    minimum = fun(u)

    for i in range(max_iterations):
        # Exploratory moves
        u0 = u
        min0 = minimum
        du = np.array([0, 0])

        # See if any of the dimensions
        # Change each entry by +- h
        # To see if it gives a smaller value (better approx of minimum)
        print('------------ Etap próbny ----------')
        for j in range(dim):
            du[j] = -h
            fn = fun(u + du)

            du[j] = h
            fp = fun(u + du)

            # If adding h gives a smaller value
            # than having 0 or -h as du[j]
            # then we update the minimum to fp
            if (fp < fn) and (fp < minimum):
                minimum = fp
            # If -h gives a smaller value,
            # update the jth entry to reflect it
            # store the fn value
            elif fn < minimum:
                du[j] = -h
                minimum = fn
            # If neither + or - h gives a smaller value
            # Reset du[j] to 0
            else:
                du[j] = 0

        # Finally update u by adding the du
        # Value at this point equals minimum
        print(f'Kierunek {du} w punkcie: {u}, iter: {i}')
        u += du

        # Check conditions
        # If no change gave a better approx of minimum (norm(du) == 0)
        print('------------ Sprawdzanie warunków ----------')
        if norm(du) == 0:
            if h < eps_step:
                # Return the best approximation of minimum
                print(f'Znaleziono minimum w {u}: {minimum}, iter: {i}')
                return u, minimum
            else:
                # If h is too large, divide it by 2 and return to the start of the for loop
                h /= 2
                print(f'Nowa wartość kroku po dzieleniu przez 2: {h}')
                continue

        # Pattern moves (we found a du that makes a change - we move in this direction)
        print('------------ Etap roboczy ----------')
        k = 0
        while k < max_iterations:
            fm = fun(u + du)
            k += 1
            # If found a new minimum value, store it
            if fm < minimum:
                # Draw a simple arrow between two points in axes coordinates
                # within a single axes.
                new_u = u + du
                con = ConnectionPatch(u, new_u, 'data', 'data',
                                      arrowstyle="->", shrinkA=2, shrinkB=2,
                                      mutation_scale=10, fc=None)
                plot.add_artist(con)
                u = new_u
                minimum = fm
                print(f'Nowe minimum to {minimum} w punkcie: {u}, iter: {k}')
            # We came to the end in this direction, stop
            else:
                break

        # Check:
        # number of iterations and
        # the distance between previous minimum (u0) and current (u) is less than step size and
        # distance between previous and current approx of minimum is less than eps_abs
        if (k < max_iterations and norm(u - u0) < eps_step) and min0 - minimum < eps_abs:
            # Done, return the minimum
            print(f'Znaleziono minimum w {u}: {minimum}, iter: {i}')
            return u, minimum

    # Zero vector - approx, no value
    print('Nie znaleziono minimum.')
    return [0, 0], np.nan
