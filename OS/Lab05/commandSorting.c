#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>

void sort_strings(char *arr[], int n) {
    char *temp;
    for (int i = 0; i < n-1; i++) {
        for (int j = i+1; j < n; j++) {
            if (strcmp(arr[i], arr[j]) > 0) {
                temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Please provide some strings as command line arguments.\n");
        return 1;
    }
    pid_t pid = fork();
    if (pid < 0) {
        perror("Fork failed");
        return 1;
    } else if (pid == 0) {
        sort_strings(argv + 1, argc - 1);
        printf("Sorted strings in child process:\n");
        for (int i = 1; i < argc; i++) {
            printf("%s\n", argv[i]);
        }
        exit(0);
    } else {
        wait(NULL);
        printf("Unsorted strings in parent process after child completes:\n");
        for (int i = 1; i < argc; i++) {
            printf("%s\n", argv[i]);
        }
    }
    return EXIT_SUCCESS;
}
