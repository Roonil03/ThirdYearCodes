#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
    pid_t pid = fork();
    if (pid < 0) {
        perror("Fork failed");
        exit(1);
    } else if (pid == 0) {
        printf("This is the child process.\n");
        printf("Child PID: %d\n", getpid());
        printf("Child PPID: %d\n", getppid());
    } else {
        printf("This is the parent process.\n");
        printf("Parent PID: %d\n", getpid());
        printf("Parent PPID: %d\n", getppid());
    }
    return EXIT_SUCCESS;
}
