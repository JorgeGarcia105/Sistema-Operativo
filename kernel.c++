#include <stdio.h>
#include <string.h>

int main() {
    char name[50];
    char password[50];
    char correct_password[] = "password123";
    int option;

    //bienvenida
    printf("Hello, World!\n");

    printf("Por favor, ingresa tu nombre: ");
    fgets(name, sizeof(name), stdin);

    printf("Hola, %s", name);

    //validar usuario
    printf("Por favor, ingresa tu contraseña: ");
    fgets(password, sizeof(password), stdin);
    password[strcspn(password, "\n")] = 0; // remove newline character

    if(strcmp(password, correct_password) != 0) {
        printf("Contraseña incorrecta. Inténtalo de nuevo.\n");
        return 0;
    }

    //crear menu del sistema operativo
    printf("1. Calculadora\n");
    printf("Elige una opción: ");
    scanf("%d", &option);

    //crear opciones del menu
    switch(option) {
        case 1:
            //opcion 1: calculadora
            printf("Has seleccionado la calculadora.\n");
            break;
        default:
            printf("Opción no válida.\n");
    }

    return 0;
}
