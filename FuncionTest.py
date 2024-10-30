import numpy as np
import random
import math

def fs(position):
    # Posicion de cada dimension
    x = position[0]
    y = position[1]
    # Implementar la función de fitness aquí
    # Implementar la función de fitness
    result = (-20 * math.exp(-0.2 * math.sqrt(0.5 * (x**2 + y**2))) -
            math.exp(0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))) +
            math.exp(1) + 20)

    return result

position = [2,1]
r = fs(position)

print(position[0])
print(position[1])
print(position)
print(r)