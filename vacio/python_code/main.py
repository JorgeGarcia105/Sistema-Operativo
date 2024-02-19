# main.py
import ctypes

# Cargar la biblioteca compartida
#cargar la biblioteca compartida
lib = ctypes.CDLL('../vacio/build/sum.so')  # Ruta a la biblioteca compartida en formato SO
#lib = ctypes.CDLL('../vacio/build/sum.dll')  # Ruta a la biblioteca compartida en formato DLL

# Definir los tipos de argumentos y valores de retorno
lib.sum_c.argtypes = (ctypes.c_int, ctypes.c_int)
lib.sum_c.restype = ctypes.c_int

# Llamar a la función sum_c
result = lib.sum_c(3, 4)
print("El resultado de la suma es:", result)


