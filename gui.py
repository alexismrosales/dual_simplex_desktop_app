from tkinter import * 
from tkinter import messagebox, ttk
import customtkinter as CTk
from algoritmo import dual_simplex
import variables


root = Tk()
eqs_window = None
iterations_window = None
frame = None
   
#Variables de colores
first_color = "#894CA8"
second_color = "#CB85EE"


#Inputs:
#Primera ventana:
n_vars = None
n_rest = None
#Segunda ventana:
count_times = 0
var_res = 0
var_obj = 0
var_eq_res = 0
var_symbols = 0
list_values = [] 
list_values_obj = []
list_values_eq_res= []
list_values_symbols = []

def main():
    main_window()
    window_config()
    
#Configuración de la ventana    
def window_config():
    #Cambiamos el cursor
    root.config(cursor="left_ptr")
    #Cambiamos resolución de la pantalla
    root.geometry(f"1000x700")
    #Bloqueamos botón de maximizar
    root.attributes("-type", "splash") # esto deshabilita los botones de maximizar y minimizar
    root.attributes("-alpha", 0.9)
    root.mainloop()
#Contenido de la ventana principal
def main_window():
    global var1, var2
    #Titulo de la ventana
    root.title("Dual simplex calculadora")
    #Titulo de la aplicación    
    title = Label(master=root, text="Método Dual Simplex",font = ("Ubuntu",30), anchor="w" ,fg=first_color)
    title.place(relx=0.5, rely=0.2, anchor=CENTER)
    ask_for_input_mw()
    weight_for_rowsandcols()
    
def ask_for_input_mw():
    global n_vars, n_rest 
    var1 = StringVar()
    var2 = StringVar()
    var3 = StringVar()
    def only_int_numbers(val):
        if not val:
            return False
        try:
            int(val)
            return True
        except ValueError:
            return False
    def input_vars():
        global n_vars, n_rest
        variables.action.clear()
        variables.objective_function = []
        variables.restrictions = []
        variables.eq_restrictions = []
        variables.symbols = []
        # Obtener los valores de las variables de control
        num_vars = var1.get()
        num_rest = var2.get()
        action_todo = var3.get()
        if not only_int_numbers(num_vars) or not only_int_numbers(num_rest):
            messagebox.showwarning("Advertencia", "Por favor, solo introduzca números enteros.")
        else:
            if int(num_vars) > 7 or int(num_rest) > 7:
                 messagebox.showwarning("Límite superado ", "No introducir mas de 7 variables o 7 restricciones.")
            elif int(num_vars) == 0 or int(num_rest) == 0:
                messagebox.showwarning("Límite mínimo ", "Introduzca números mayores que cero.")
            else:
            # En caso de pasar las condiciones llamaremos la otra ventana
                n_vars = int(num_vars)
                n_rest = int(num_rest)
                if action_todo == "Maximizar":
                    variables.action.append(1)
                else:
                    variables.action.append(0)
                eqs_input_window()
                print("Acción:", variables.action)
                print("Número de variables:", num_vars)
                print("Número de restricciones:", num_rest)
        
                
    label_variables = Label(root, text="Introduzca el número de variables:",font = ("Ubuntu",16))
    label_variables.grid(row=1, column=0)
    
    e_1 = Entry(root, width=35, borderwidth=5,textvariable=var1)
    e_1.insert(0,"")
    e_1.grid(row = 1, column = 1)
    
    label_variables = Label(root, text="Introduzca el número de restricciones: ",font = ("Ubuntu",16))
    label_variables.grid(row=2, column=0)
    e_2 = Entry(root, width=35, borderwidth=5, textvariable=var2)
    e_2.insert(0,"")
    e_2.grid(row = 2, column = 1, pady=10)

    combo = ttk.Combobox(root,
                    state="readonly",
                    width = 30,
                    values=["Maximizar", "Minimizar"],
                    textvariable= var3
            )
    combo.set("Maximizar")
    combo.place(relx=0.2, rely=0.9, anchor=CENTER)
    
    input_button = Button(root, text="Aceptar", padx=40, pady=20, command=input_vars)
    input_button.place(relx=0.5, rely=0.9, anchor=CENTER)



def eqs_input_window():
    eqs_window_config()
    ask_for_input_ew()
 
def ask_for_input_ew():
    global var_res, frame
    global list_values, var_obj, list_values_obj
    global  var_eq_res, list_values_eq_res
    global  var_symbols, list_values_symbols
    global iterations, eqs_window
    
    def input_rest():
        global count_times
        variables.objective_function = []
        variables.restrictions = []
        variables.eq_restrictions = []
        variables.symbols = []
        
        val_entry = None
        
        for i, val in enumerate(list_values_obj):
            val_entry = val.get() 
            if not only_float_numbers(val_entry):
                messagebox.showwarning("Advertencia", "Por favor, solo introduzca números. "+ "Error en la función objetivo "
                                           +" variable X"+str(i+1))
                val_entry = None
            else:
                variables.objective_function.append(float(val_entry))
        for i in range(n_rest):
            row = []
            for j in range(n_vars):
                val_entry = list_values[i*n_vars + j].get()
                if not only_float_numbers(val_entry): 
                    messagebox.showwarning("Advertencia", "Por favor, solo introduzca números. "+ "Error en la desigualdad "
                                           +str(i+1)+" variable X"+str(j+1))
                    val_entry = None
                else:
                    row.append(float(val_entry))
            # Agregar el valor a la sublista
            variables.restrictions.append(row)
        for i, val in enumerate(list_values_eq_res):
            val_entry = val.get()
            if not only_float_numbers(val_entry):
                messagebox.showwarning("Advertencia", "Por favor, solo introduzca números. "+ "Error en el valor de la desigualdad objetivo "
                                          + str(i+1))
                val_entry = None
            else:
                variables.eq_restrictions.append(float(val_entry))
        for val in list_values_symbols:
            val_entry = val.get()
            if val_entry == "<=":
                variables.symbols.append(0)
            elif val_entry == ">=":
                variables.symbols.append(1)
            else: #Si hay un signo = 
                variables.symbols.append(2)
        #Hacemos varios filtros para verificar que todos los datos estan correctos
        
        print(variables.objective_function)
        print(variables.restrictions)
        print(variables.eq_restrictions)
        print(variables.symbols)
        #Acción
        iterations = dual_simplex()
        eqs_window.destroy()
        #Mostramos la ventana con los datos de salida
        show_iterations_window(iterations)
        list_values.clear()
        list_values_obj.clear()
        list_values_eq_res.clear()
        list_values_symbols.clear()
            
    #Titulo
    instructions_label = Label(master=eqs_window, text="Introduzca las restricciones:",font = ("Ubuntu",16), anchor="w" )
    instructions_label.place(relx=0.5, rely=0.25, anchor=CENTER)
    #Le damos un valor al frame para mostrarlo
    frame = Frame(eqs_window)
    frame.grid()
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    objFun_label = Label(frame, text="Función objetivo",font = ("Ubuntu",14), anchor="w")
    objFun_label.grid()
    objFun_label.place(relx=0.5, rely=0.05, anchor=CENTER)
    print(n_vars)
    #Introducimos la función objetivo 
    for i in range(n_vars):
        var_obj += 1
        globals()["var" + str(var_obj)] = StringVar()
        e = Entry(frame, width=10,textvariable=globals()["var" + str(var_obj)])
        e.grid(row=0, column=i*2, padx=5, pady=30)
        list_values_obj.append(globals()["var" + str(var_obj)])
        if i  == n_vars-1:
            txt = "X"+str(i+1)
        else:
            txt = "X"+str(i+1)+" +"
        x_label = Label(frame,text=txt,font=("Ubuntu",14))
        x_label.grid(row=0, column=i*2+1, padx=5, pady=5)
    #Iteramos para impimir los inputs y labels necesarios
    for i in range(n_rest):
        frame.grid_rowconfigure(i, weight=1)
        restriction = []
        for j in range(n_vars):
            #Incremento la variable
            var_res += 1
            #Creo una variable de tipo StringVar con el nombre "var" + el número de la variable de control
            globals()["var" + str(var_res)] = StringVar()
            e = Entry(frame, width=10,textvariable=globals()["var" + str(var_res)])
            e.grid(row=i+1, column=j*2, padx=5, pady=5)
            list_values.append(globals()["var" + str(var_res)])
            if j  == n_vars-1:
                txt = "X"+str(j+1)
            else:
                txt = "X"+str(j+1)+" +"
            x_label = Label(frame,text=txt,font=("Ubuntu",14))
            x_label.grid(row=i+1, column=j*2+1, padx=5, pady=5)
            col_n = j*2+2
        #Imprimo el combobox con la opción de la desigualdad
        var_symbols += 1
        globals()["var" + str(var_symbols)] = StringVar()
        combo = ttk.Combobox(frame,
                    state="readonly",
                    width = 10,
                    values=["=", ">=", "<="],
                    textvariable=globals()["var" + str(var_symbols)]
            )
        combo.set("=")
        combo.grid(row=i+1, column=col_n, padx= 5, pady=5)
        list_values_symbols.append(globals()["var" + str(var_symbols)])
        #Pido datos del la restricción 
        var_eq_res += 1
        globals()["var" + str(var_eq_res)] = StringVar()
        e = Entry(frame, width=10,textvariable=globals()["var" + str(var_eq_res)])
        e.grid(row=i+1, column=col_n+1, padx=5, pady=5)
        list_values_eq_res.append(globals()["var" + str(var_eq_res)])
        
    accept_button = Button(frame, text="Calcular", command=input_rest)
    accept_button.grid(row=n_rest+2,column=n_vars*2)
    objFun_label.place( anchor=CENTER)

         
def eqs_window_config():
    global eqs_window
    #Configuración de la ventana
    eqs_window = Toplevel(root)
    eqs_window.title("Entrada de ecuaciones y desigualdades")
    eqs_window.geometry(f"1000x800")
    eqs_window.grab_set()
    
    title_eqs_window = Label(master=eqs_window, text="Método Dual Simplex",font = ("Ubuntu",30), anchor="w",fg=first_color)
    title_eqs_window.place(relx=0.5, rely=0.1, anchor=CENTER)

def show_iterations_window(iterations):
    iterations_window_config()
    show_iterations(iterations)
    
def show_iterations(iterations):
    global iterations_window, n_vars, n_rest
    #Titulo
    instructions_label = Label(iterations_window, text="Iteraciones:",font = ("Ubuntu",16), anchor="w" )
    instructions_label.grid(row=0, column=0, sticky="nsew")
    scrollable_frame = CTk.CTkScrollableFrame(iterations_window, width=1000, height=800)
    # Posicionar el frame en el centro de la subventana
    scrollable_frame.grid(row=1, column=0,sticky="nsew")
    space = 0
    column_zero = ["S{}".format(i) for i in range(1, n_rest+1)]
    results = [None]*len(variables.restrictions)
    x_variable = None
    row_zero =  ["     "] +  ["X{}".format(i) for i in range(1, n_vars+1)]+["S{}".format(i) for i in range(1, n_rest+1)] + ["Sol"]
    print(row_zero)
    for n, iteration in enumerate(iterations):

        iteration_label =CTk.CTkLabel(scrollable_frame, text="Iteracion " + str(n+1) +", con el pivote " + str(iteration[1])+":",font = ("Ubuntu",20), anchor="w" )
         # Usar el método pack para posicionar el pivote
        iteration_label.pack(side="top")
        # Crear un widget de tipo Frame para mostrar la matriz de la iteración
        matrix_frame = CTk.CTkFrame(scrollable_frame)
        # Usar el método pack para posicionar el frame
        matrix_frame.pack()
        
        #pivot_pos
        m, n = iteration[0]
    
        if n != None: 
            if n < len(variables.restrictions):
                
                x_variable = "X"+str(n+1)
            else:
                x_variable = "S"+str(n+1)
            column_zero[m] = x_variable
            
        for j, column in enumerate(row_zero):
            # Crear un widget de tipo Label para mostrar el elemento de la matriz
            label = CTk.CTkLabel(matrix_frame, text=column + "     ", width=15,font=("Ubuntu",22))
            label.grid(row=0, column=j)
        # Gur
        for i, row in enumerate(iteration[2]):
            if x_variable == None:
                x_variable = "     "
            if i < len(iteration[2])-1:
                label_var = CTk.CTkLabel(matrix_frame, text=column_zero[i] + "     ", width=15,font=("Ubuntu",22))
                label_var.grid(row=i+1, column=0)
            else:
                label_var = CTk.CTkLabel(matrix_frame, text="Z" + "     ", width=15,font=("Ubuntu",22))
                label_var.grid(row=i+1, column=0)
            for j, column in enumerate(row):
                # Crear un widget de tipo Label para mostrar el elemento de la matriz
                label = CTk.CTkLabel(matrix_frame, text=str(round(column,2)) + "     ", width=15,font=("Ubuntu",22))
                label.grid(row=i+1, column=j+1)
        invisible_label_2 = CTk.CTkLabel(scrollable_frame, text="")
        invisible_label_2.pack()
        # Ocultar el label invisible
        invisible_label_2.place_forget()
    for i, item in enumerate(iterations[-1][-1][:-1]):
        print(item[-1])
        results[i] = item[-1]
    result_label =CTk.CTkLabel(scrollable_frame, text="Los resultados son: ",font = ("Ubuntu",22), anchor="w" )
    result_label.pack(side="top")
    for i, result in enumerate(column_zero):
        if result[0] == 'X':
            iteration_label =CTk.CTkLabel(scrollable_frame, text="X"+result[1]+ " = " + str(round(results[i],2)),font = ("Ubuntu",22), anchor="w" )
            iteration_label.pack(side="top")
    z_result =CTk.CTkLabel(scrollable_frame, text="Z = " + str(round(iterations[-1][-1][-1][-1],2)),font = ("Ubuntu",22), anchor="w" )
    z_result.pack(side="top")
    
        
 
def iterations_window_config():
    global iterations_window
    iterations_window = CTk.CTkToplevel(root)
    iterations_window.title("Resultados")
    iterations_window.geometry(f"1000x800")
    iterations_window.grab_set()
    
def only_float_numbers(val):
        if not val:
            return False
        try:
            float(val)
            return True
        except ValueError:
            return False    
def weight_for_rowsandcols():
    root.rowconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)
    
    root.columnconfigure(0, weight=1)
    root.columnconfigure(2, weight=1)

if __name__ == "__main__":
    main()
