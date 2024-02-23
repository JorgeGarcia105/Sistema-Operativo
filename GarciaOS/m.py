import time

def inicio():
    respuesta = input("¿Desea ejecutar el main.py? (si/no): ")
    if respuesta.lower() == "si":
        print("Ejecutando main.py")
        arranque()
    else:
        print("No se ejecutará main.py")









#mensaje inicial python
def arranque():
    print("Bienvenido a GarciaOS")
    #mensajes temporales de 1% a 100% distribuidos en 100 milisegundos
    #mensaje cada 10% de carga, con 1000 milisegundos de espera en un ciclo de 10
    for i in range(0, 101, 10):
        time.sleep(1)
        print("Cargando GarciaOS al " + str(i) + "%")
    #mensaje de carga completa
    print("GarciaOS cargado al 100%")

    #mensaje de inicio de sesion
    print("Iniciando sesion en GarciaOS")
    #mensaje de bienvenida
    print("Bienvenido a GarciaOS")

    #mensaje final python
    print("Gracias por usar GarciaOS")



inicio()


