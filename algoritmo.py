import math
import pandas as pd
import numpy as np
import variables

#Input data
#variables.objective_function = [2,3]
#variables.restrictions = [[1,1],[3,-1]]
#variables.eq_restrictions = [1,2]   
#variables.symbols = [2,1] #0 menor que, 1 mayor que, 2 igual
#variables.action = [0] #0 minimzar, 1sss maximizar

def dual_simplex():
    iterations = []
    #Conversión de variables de exceso a coeficiente positivo
    conversion() 

    matrix = to_matrix(variables.objective_function, variables.restrictions, variables.eq_restrictions)
    if variables.action[0] == 0:
        return min_dual_simplex(matrix)
    else:
        return max_dual_simplex(matrix)
    
#def conversion(): Funcion que se encarga de verificar que las restricciones tengan coeficiente positivo 
#cuando se pasen a ecuaciones asi como la función objetivo
def conversion():
    #Comenzando con la función objetivo igualandola a cero (multiplicandolla por -1)
    variables.objective_function = to_negative(variables.objective_function)
    equal_counter = 0
    #Si alguna de las restricciones es mayor que la condición, se cambiara su coeficiente a positivo
    for i, s in enumerate(variables.symbols):
        #Si hay un simbolo mayor que y estamos minimizando se multiplica por -1
        if s and variables.action[0] == 0:
            variables.restrictions[i] = to_negative(variables.restrictions[i])
            variables.eq_restrictions[i] *= -1
        #Si hay un simbolo menor que y estamos maximizando
        elif s and variables.action[0] == 1:
            variables.restrictions[i] = to_negative(variables.restrictions[i])
            variables.eq_restrictions[i] *= -1
        if s == 2:
            variables.restrictions.append(to_negative(variables.restrictions[i]))
            variables.eq_restrictions.append(variables.eq_restrictions[i] * -1)
            equal_counter += 1
    #Agregamos el valor del coeficiente
    zero_list = [0] * (len(variables.symbols)+equal_counter)
    #Concatenamos la función objetivo con ceros
    variables.objective_function += zero_list
    #Ahora agregamos el valor de cada coeficiente y los ceros para poder usarla en la tabla
    for i, rest in enumerate(variables.restrictions):
        zero_list[i] = 1
        rest += zero_list
        zero_list[i] = 0    
#def min_dual_simplex(matrix): Es la función que ejecuta el algoritmo para el dual simplex con min Z
def min_dual_simplex(matrix):
    #Matriz donde se guardaran las iteraciones
    iterations = []
    iterations.append([(None,None),0,matrix])
    #Mientras la solución aún no sea positiva seguiremos iterando
    while can_be_improved(matrix):
        pivot_pos = get_pivot_position_for_min(matrix)
        matrix = pivot_step(matrix,pivot_pos)
        #Limpiamos la lista por el np.array
        matrix = [row.tolist() for row in matrix]
        #Guardamos la n iteración
        iterations.append([pivot_pos,variables.pivot_value,matrix]) 
    return iterations
#def max_dual_simplex(matrix): Es la función que ejecuta el algoritmo para el dual simplex con max Z
def max_dual_simplex(matrix):
    #Matriz donde se guardaran las iteraciones
    iterations = []
    iterations.append([(None,None ),0,matrix])
    while can_be_improved(matrix):
        pivot_pos = get_pivot_position_for_max(matrix)
        matrix = pivot_step(matrix,pivot_pos)
        matrix = [row.tolist() for row in matrix]
        iterations.append([pivot_pos,variables.pivot_value,matrix]) 
    return iterations
def get_pivot_position_for_min(matrix):
    #Guardamos soluciones
    sol_entries = [row[-1] for row in matrix[:-1]]
    #Elegimos la solución menor entre ellas
    min_rhs_value = min(sol_entries )
    #Asignamos fila el indice de la solución menor
    row = sol_entries .index(min_rhs_value)
    columns = []
    #Iteramos sobre las fila que tiene la solución menor
    for index, element in enumerate(matrix[row][:-1]):
    #Solamente si los elementos son negativos se anexaran a las posibles elección de columnas
        if element < 0:
            columns.append(index)
    columns_values = []
    #Se hacen la division de los elementos negativos entre la columna Z        
    columns_values = [matrix[-1][c]/matrix[row][c] for c in columns]
    #Se elije el menor entre ellos
    column_min_index = columns_values.index(min(columns_values))
    #Se agrega el indice del menor entre ellos
    column = columns[column_min_index]
    return row, column
def get_pivot_position_for_max(matrix):
    #Guardamos soluciones
    sol_entries  = [row[-1] for row in matrix[:-1]]
    #Elegimos la solución menor entre ellas
    min_rhs_value = min(sol_entries )
    #Asignamos fila el indice de la solución menor
    row = sol_entries .index(min_rhs_value)
    columns = []
    #Iteramos sobre las fila que tiene la solución menor
    for index, element in enumerate(matrix[row][:-1]):
       if element < 0 or element > 0:
        columns.append(index)
    columns_values = []
    #Se hacen la division de los elementos, en este caso pueden entrar divisiones entre cero pero no se tomaran en cuenta      
    columns_values = [abs(matrix[-1][c]/matrix[row][c]) for c in columns if abs(matrix[-1][c]/matrix[row][c]) != 0]
    #Se elije el menor entre ellos
    column_min_index = columns_values.index(min(columns_values))
    #Se agrega el indice del menor entre ellos
    column = columns[column_min_index]
    return row, column
#def pivot_step(matrix, indice(i,j)):
def pivot_step(matrix, pivot_position):
    #Se crea una lista y se hace el resize de acuerdo al numero de elementos que hay 
    new_matrix = [[] for eq in matrix]
    #Obtenemos el indíce del elemento elegido para hacer el pivote
    i, j = pivot_position
    pivot_value = matrix[i][j]
    variables.pivot_value= pivot_value
    #Cambiamos la fila elegida para hacer el pivote y hacemos la respectiva opreración
    new_matrix[i] = np.array(matrix[i]) / pivot_value
    #Realizamos las operaciones respectivas en las demas filas a excepción de la fila del pivote
    for eq_i, eq in enumerate(matrix):
        if eq_i != i:
            multiplier = np.array(new_matrix[i]) * matrix[eq_i][j]
            new_matrix[eq_i] = np.array(matrix[eq_i]) - multiplier
    #Retornamos la matriz con los nuevos valores
    return new_matrix
#def can_be_improved(matrix):
def can_be_improved(tableau):
    #Obtenemos los valores solución sin el valor de Z
    solutions = [row[-1] for row in tableau[:-1]]
    #Si todos los elementos son positivos se retorna true
    return any([sol < 0 for sol in solutions])
#def to_negative(list): Dada una lista retorna la misma lista pero multiplicada por -1       
def to_negative(l):
    def multiplication(num, val):
        return num * val
    return list(map (multiplication, l, [-1] * len (l)))
#def to_tableu(list, list, list):Transforma las listas en una sola matriz
def to_matrix(objective_function, restrictions, eq_restrictions):
    row_w = [eq + [x] for eq, x in zip(restrictions, eq_restrictions)]
    z = objective_function + [0]
    return row_w + [z]
