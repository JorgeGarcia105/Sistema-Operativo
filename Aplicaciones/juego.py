import pygame
import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt5.QtCore import QTimer
import sys
import time

# Inicializar pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Definir la pantalla
ANCHO = 800
ALTO = 600

# Cargar imágenes
imagenes = []
for i in range(6):
    imagen = pygame.image.load(f"./Recursos/icon/ahorcado{i}.png")
    imagenes.append(imagen)

# Definir palabras
PALABRAS = ["PYTHON", "PROGRAMACION", "VIDEOJUEGO", "OPENAI","GARCIAOS", "LINUX", "WINDOWS", "MACOS", "ANDROID", "IOS", "UBUNTU", "DEBIAN", "FEDORA", "CENTOS", "REDHAT", "CHROMEOS"]


def seleccionar_palabra():
    return random.choice(PALABRAS)

def dibujar_letras(letras, palabra_secreta, pantalla):
    letra_pos_x = 50
    letra_pos_y = ALTO - 100
    for letra in palabra_secreta:
        if letra in letras:
            texto = letra
        else:
            texto = "_"
        fuente = pygame.font.Font(None, 36)
        texto_imagen = fuente.render(texto, True, NEGRO)
        pantalla.blit(texto_imagen, (letra_pos_x, letra_pos_y))
        letra_pos_x += 30

def dibujar_juego(intentos, letras, palabra_secreta, pantalla):
    pantalla.fill(BLANCO)
    if intentos < len(imagenes):  # Verificar si el número de intentos es válido
        pantalla.blit(imagenes[intentos], (50, 50))
    dibujar_letras(letras, palabra_secreta, pantalla)
    pygame.display.flip()

def mensaje(mensaje, color, pantalla):
    fuente = pygame.font.Font(None, 48)
    texto_imagen = fuente.render(mensaje, True, color)
    pantalla.blit(texto_imagen, (ANCHO // 2 - texto_imagen.get_width() // 2, ALTO // 2 - texto_imagen.get_height() // 2))

class JuegoAhorcado(QWidget):
    def __init__(self, pantalla):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.main_loop)
        self.timer.start(100)
        self.pantalla = pantalla

    def initUI(self):
        self.setWindowTitle('Ahorcado')
        self.setGeometry(100, 100, ANCHO, ALTO)

        layout = QVBoxLayout()
        self.setLayout(layout)

        boton_reiniciar = QPushButton('Reiniciar', self)
        boton_reiniciar.clicked.connect(self.reiniciar_juego)
        layout.addWidget(boton_reiniciar)

        self.reiniciar_juego()

    def reiniciar_juego(self):
        self.palabra_secreta = seleccionar_palabra()
        self.letras_adivinadas = set()
        self.intentos = 0

    def main_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()  # Cerrar solo la ventana del juego

            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    letra = event.unicode.upper()
                    if letra not in self.letras_adivinadas:
                        self.letras_adivinadas.add(letra)
                        if letra not in self.palabra_secreta:
                            self.intentos += 1

        self.dibujar_juego()

        if self.intentos == 6:
            mensaje(f"¡Perdiste! La palabra era: {self.palabra_secreta}", NEGRO, self.pantalla)
            pygame.time.delay(3000)
            self.reiniciar_juego()

        if all(letra in self.letras_adivinadas for letra in self.palabra_secreta):
            mensaje("¡Ganaste!", NEGRO, self.pantalla)
            pygame.time.delay(3000)
            self.reiniciar_juego()

    def dibujar_juego(self):
        dibujar_juego(self.intentos, self.letras_adivinadas, self.palabra_secreta, self.pantalla)


class Escritorio(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Escritorio")
        self.setObjectName("mainWindow")

        # Configurar el layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Ajustar la ventana para que ocupe toda la pantalla
        self.setGeometry(0, 0, ANCHO, ALTO)

        # Crear un nuevo QVBoxLayout para el layout de la parte superior izquierda
        layout_superior_izquierda = QVBoxLayout()

        # Añadir el layout de la parte superior izquierda al layout principal
        layout.addLayout(layout_superior_izquierda)

        # Crear una instancia de la pantalla de Pygame
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))

        # Crear una instancia del juego de ahorcado
        self.juego = JuegoAhorcado(self.pantalla)

def main():
    app = QApplication(sys.argv)
    escritorio = Escritorio()
    escritorio.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
