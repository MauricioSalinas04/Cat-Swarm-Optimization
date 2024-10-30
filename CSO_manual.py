import numpy as np
import random
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

def fs(cat):
    # Posicion de cada dimension
    x = cat.position[0]
    y = cat.position[1]
    # Implementar la función de fitness aquí
    # Implementar la función de fitness
    result = (-20 * math.exp(-0.2 * math.sqrt(0.5 * (x**2 + y**2))) -
            math.exp(0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))) +
            math.exp(1) + 20)
    
    return result

def set_modes(cats, N, MR):
    # Calcular cuántas veces imprimir "tracing"
    tracing_count = int(N * MR)

    modes = []
    # Iniciar el ciclo
    for i in range(N):
        if i < tracing_count:
            modes.append("tracing")
        else:
            modes.append("seeking")

    random.shuffle(modes)

    # Asignar un modo a cada gato basado en su índice
    for index, cat in enumerate(cats):
        cat.mode = modes[index % len(modes)]
    
    return cats

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
   

def cso_algorithm(cats, N, MR, max_iterations, mapSize):

    # Step 2: Asignar modos
    cats = set_modes(cats, N, MR)

    best_cat = None
    best_fitness = float('inf')

    # Iteraciones del algoritmo
    for iteration in range(max_iterations):
        # Step 3: Evaluar valores de fitness
        for cat in cats:
            cat.fs = fs(cat)
            if cat.fs < best_fitness: # Aqui se define el objetivo del problema (<:Min & >:Max)
                best_fitness = cat.fs
                best_cat = cat

        # Step 4: Mover los gatos según su modo
        for cat in cats:
            if cat.mode == 'seeking':
                # Lógica de movimiento para seeking mode
                cat.position = seeking_algorithm(cat)
            else:  # tracing mode
                # Lógica de movimiento para tracing mode
                cat.position = tracing_algorithm(cat, best_cat)

        # Step 5: Re-pick gatos para modos
        cats = set_modes(cats, N, MR)

        # Step 6: Verificar condición de terminación
        if iteration >= max_iterations - 1:  # Por ejemplo, terminar después de un número fijo de iteraciones
            break

    return best_cat.position, best_fitness

# Parámetros del algoritmo
MR = 1/6  # Proporción de gatos en tracing mode
max_iterations = 100  # Número máximo de iteraciones
mapSize = 25

# Step 1: Crear N gatos
N = 6 # Numero de gatos en el modelo
cats = []
cats.append(Cat(3, 1, 1, 0.01357, [10.0482, 1.01839], [0.0248, 0.0809]))    # C1
cats.append(Cat(4, 0, 2, 0.01525, [21.1237, -2.86781], [0.2491, 0.7404]))   # C2
cats.append(Cat(4, 1, 2, 0.00937, [-19.9693, 6.59803], [0.1546, 0.1422]))   # C3
cats.append(Cat(2, 0, 1, 0.00151, [3.29141, 18.993], [0.0596, 0.0274]))     # C4
cats.append(Cat(2, 1, 1, 0.00741, [-8.48734, -15.3779], [0.3579, 0.1792]))  # C5
cats.append(Cat(4, 0, 2, 0.01527, [23.1321, -4.37554], [0.5564, 0.3533]))   # C6

# Ejecutar el algoritmo
best_position, best_fitness = cso_algorithm(cats, N, MR, max_iterations, mapSize)

# Imprimir los resultados
print("Mejor posición encontrada:", best_position)
print("Mejor valor de fitness:", best_fitness)
