import numpy as np
import math
from itertools import combinations

class Cat:
    def __init__(self, SMP, SPC, CDC, SRD, position, velocity):
        self.SMP = SMP           # Numero de candidatos a nuevas posiciones
        self.SPC = SPC           # Decide si se contempla la posicion actual como un candidato con respecto al proceso SMP (Boolean)
        self.CDC = CDC           # Numero de dimensiones que seran modificadas
        self.SRD = SRD           # Rango de cambio para crear las nuevas posiciones con respecto al proceso SMP
        self.position = position # Posición del gato en el espacio de solución
        self.velocity = velocity # Velocidad del gato
        self.mode = None         # Modo del gato: 'seeking' o 'tracing'
        self.fs = None           # Valor de fitness (Output funcion objetivo)

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

def tracing_algorithm(cat, best_cat):
   
    cat_position = cat.position
    cat_velocity = cat.velocity
    newCat_velocity = []
    # rd = [0.3407, 0.8949] CASO VISTO EN CLASE
    best_position = best_cat.position
    c1 = 1
    
    # Paso 1: Actualizar la velocidad en cada dimensión
    for d in range(len(cat_position)):
        r1 = np.random.rand()  # Generar un valor aleatorio en el rango [0, 1]
        
        # Ecuación (2): Actualización de velocidad
        newCat_velocity.append(cat_velocity[d] + r1 * c1 * (best_position[d] - cat_position[d]))

    # Paso 3: Actualizar la posición según la nueva velocidad
    new_position = np.add(newCat_velocity, cat_position).tolist()  # Suma los elementos correspondientes

    return new_position, newCat_velocity

def seeking_algorithm(cat):

    # Variables
    cat_position = cat.position
    SMP = cat.SMP
    SPC = cat.SPC
    CDC = cat.CDC
    SRD = cat.SRD

    dim = len(cat_position)
    candidate_positions = []
    used_dims_sets = set()
    all_combinations = list(combinations(range(dim), CDC))
    
    # Paso 1: Crear SMP copias de la posición actual
    for i in range(SMP):
        if SPC and i == 0:
            # Si SPC es True, la primera copia es la posición actual del gato
            candidate_positions.append(cat_position.copy())
        else:
            # Crear una copia de la posición actual
            new_position = cat_position.copy()

            # Paso 2: Modificar aleatoriamente CDC dimensiones en esta copia
            if len(used_dims_sets) < len(all_combinations):
                # Mientras haya combinaciones únicas no usadas
                while True:
                    dims_to_change = np.random.choice(dim, CDC, replace=False).tolist()
                    if tuple(dims_to_change) not in used_dims_sets:
                        used_dims_sets.add(tuple(dims_to_change))
                        break
            else:
                # Permitir repeticiones si todas las combinaciones únicas ya se usaron
                dims_to_change = np.random.choice(dim, CDC, replace=False).tolist()

            # Aplicar el cambio en las dimensiones seleccionadas
            for d in dims_to_change:
                # Cambiar la dimensión d por un porcentaje aleatorio dentro de SRD (pos_original*(1-SRD))
                new_position[d] *= (1-SRD)

            candidate_positions.append(new_position)
            
    
    # Paso 3: Calcular la aptitud (fitness) de cada punto candidato
    fitness_values = np.array([fs(pos) for pos in candidate_positions])

    # Paso 4: Calcular la probabilidad de selección de cada punto candidato
    if np.all(fitness_values == fitness_values[0]):
        # Si todos los valores de aptitud son iguales, se asignan probabilidades iguales
        probabilities = np.ones(SMP) / SMP
    else:
        # Calcular la probabilidad proporcional a la aptitud de cada candidato
        max_fitness = np.max(fitness_values)
        min_fitness = np.min(fitness_values)
        fitness_best = max_fitness # En este caso se coloca min por que se busca minimizar
        probabilities = abs(fitness_values - fitness_best) / (max_fitness - min_fitness)
        probabilities /= probabilities.sum()  # Normalizar

    # Paso 5: Seleccionar aleatoriamente una nueva posición basada en las probabilidades
    selected_index = np.random.choice(len(candidate_positions), p=probabilities)
    nueva_posición = candidate_positions[selected_index]

    return nueva_posición

c1 = Cat(3, 1, 1, 0.01357, [10.0482, 1.01839], [0.0248, 0.0809])
c5 = Cat(2, 1, 1, 0.00741, [-8.48734, -15.3779], [0.3579, 0.1792])
c1.fs = fs(c1.position)
c1.fs = fs(c1.position)
print(c1.position)
print(c1.fs)



print(tracing_algorithm(c5, c1))