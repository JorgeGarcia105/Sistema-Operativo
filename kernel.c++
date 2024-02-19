#include <stdio.h>
#include <string.h>

// Definición de funciones
int sum(int arr[], int num) {
    int result = 0;
    for (int i = 0; i < num; i++) {
        result += arr[i];
    }
    return result;
}

int resta(int arr[], int num) {
    int result = arr[0];
    for (int i = 1; i < num; i++) {
        result -= arr[i];
    }
    return result;
}

int multiplicacion(int arr[], int num) {
    int result = 1;
    for (int i = 0; i < num; i++) {
        result *= arr[i];
    }
    return result;
}

int division(int arr[], int num) {
    int result = arr[0];
    for (int i = 1; i < num; i++) {
        if (arr[i] == 0) {
            printf("Error: división por cero.\n");
            return 0;
        }
        result /= arr[i];
    }
    return result;
}

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
            //opcion 1: calculadora cientifica
            printf("Has seleccionado la calculadora cientifica.\n");

            //crear menu de la calculadora
            printf("1. Suma\n");
            printf("2. Resta\n");
            printf("3. Multiplicación\n");
            printf("4. División\n");
            printf("Elige una opción: ");

            scanf("%d", &option);

            // Variables para operaciones matemáticas
            int num;
            int arr[50];

            //crear opciones de la calculadora
            switch(option) {
                case 1:
                    //opcion 1: sumar
                    num = 0;
                    printf("Ingrese el número de elementos: ");
                    scanf("%d", &num);
                    printf("Ingrese los números: ");
                    for (int i = 0; i < num; i++) {
                        scanf("%d", &arr[i]);
                    }
                    printf("La suma es: %d\n", sum(arr, num));

                    break;
                case 2:
                    //opcion 2: resta
                    
                    num = 0;
                    printf("Ingrese el número de elementos: ");
                    scanf("%d", &num);
                    printf("Ingrese los números: ");
                    for (int i = 0; i < num; i++) {
                        scanf("%d", &arr[i]);
                    }
                    printf("La resta es: %d\n", resta(arr, num));

                    break;
                case 3:
                    //opcion 3: multiplicación
                    

                    num = 0;
                    printf("Ingrese el número de elementos: ");
                    scanf("%d", &num);
                    printf("Ingrese los números: ");
                    for (int i = 0; i < num; i++) {
                        scanf("%d", &arr[i]);
                    }
                    printf("La multiplicación es: %d\n", multiplicacion(arr, num));
                    break;
                case 4:
                    //opcion 4: división

                    num = 0;
                    printf("Ingrese el número de elementos: ");
                    scanf("%d", &num);
                    printf("Ingrese los números: ");
                    for (int i = 0; i < num; i++) {
                        scanf("%d", &arr[i]);
                    }
                    printf("La división es: %d\n", division(arr, num));

                    break;
                default:
                    printf("Opción no válida.\n");
            }
            break;
        default:
            printf("Opción no válida.\n");
    }

    return 0;
}
