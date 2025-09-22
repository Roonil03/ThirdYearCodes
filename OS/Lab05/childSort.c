#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>

void bubble_sort(char *arr[], int n) {
    char *temp;
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (strcmp(arr[j], arr[j+1]) > 0) {
                temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

void selection_sort(char *arr[], int n) {
    char *temp;
    int min_idx;
    for (int i = 0; i < n-1; i++) {
        min_idx = i;
        for (int j = i+1; j < n; j++) {
            if (strcmp(arr[j], arr[min_idx]) < 0) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            temp = arr[i];
            arr[i] = arr[min_idx];
            arr[min_idx] = temp;
        }
    }
}

int main() {
    int n;
    printf("Enter number of strings: ");
    scanf("%d", &n);
    char *arr[n];
    char buffer[100];
    printf("Enter %d strings:\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%s", buffer);
        arr[i] = strdup(buffer);
    }
    pid_t pid1 = fork();
    if (pid1 < 0) {
        perror("Fork failed");
        return EXIT_FAILURE;
    }
    if (pid1 == 0) {
        bubble_sort(arr, n);
        printf("Sorted with bubble sort (child 1):\n");
        for (int i = 0; i < n; i++) {
            printf("%s\n", arr[i]);
        }
        return EXIT_SUCCESS;
    }
    pid_t pid2 = fork();
    if (pid2 < 0) {
        perror("Fork failed");
        return EXIT_FAILURE;
    }
    if (pid2 == 0) {
        selection_sort(arr, n);
        printf("Sorted with selection sort (child 2):\n");
        for (int i = 0; i < n; i++) {
            printf("%s\n", arr[i]);
        }
        return EXIT_SUCCESS;
    }
    wait(NULL);
    printf("One child process finished, parent terminates now.\n");
    return EXIT_SUCCESS;
}
