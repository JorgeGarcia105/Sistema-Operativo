import pygame
import random

# Inicializar pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Definir la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ahorcado")

# Cargar imágenes
imagenes = []
for i in range(7):
    imagen = pygame.image.load("./Recursos/icon/fondo.png")
    imagenes.append(imagen)

# Definir palabras
PALABRAS = ["PYTHON", "PROGRAMACION", "VIDEOJUEGO", "OPENAI", "IA"]

def seleccionar_palabra():
    return random.choice(PALABRAS)

def dibujar_letras(letras, palabra_secreta):
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

def dibujar_juego(intentos, letras, palabra_secreta):
    pantalla.fill(BLANCO)
    pantalla.blit(imagenes[intentos], (50, 50))
    dibujar_letras(letras, palabra_secreta)
    pygame.display.flip()

def main():
    palabra_secreta = seleccionar_palabra()
    letras_adivinadas = set()
    intentos = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    letra = event.unicode.upper()
                    if letra not in letras_adivinadas:
                        letras_adivinadas.add(letra)
                        if letra not in palabra_secreta:
                            intentos += 1

        dibujar_juego(intentos, letras_adivinadas, palabra_secreta)

        if intentos == 6:
            pantalla.fill(BLANCO)
            mensaje("¡Perdiste! La palabra era: " + palabra_secreta, NEGRO)
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            return

        if all(letra in letras_adivinadas for letra in palabra_secreta):
            pantalla.fill(BLANCO)
            mensaje("¡Ganaste!", NEGRO)
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            return

def mensaje(mensaje, color):
    fuente = pygame.font.Font(None, 48)
    texto_imagen = fuente.render(mensaje, True, color)
    pantalla.blit(texto_imagen, (ANCHO // 2 - texto_imagen.get_width() // 2, ALTO // 2 - texto_imagen.get_height() // 2))

if __name__ == "__main__":
    main()
