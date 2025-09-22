#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#define MAX_PROCESSES 10
#define MAX_RESOURCES 10

int main() {
    int n, m;
    printf("Enter number of processes: ");
    scanf("%d", &n);
    printf("Enter number of resource types: ");
    scanf("%d", &m);
    int Allocation[MAX_PROCESSES][MAX_RESOURCES];
    int Request[MAX_PROCESSES][MAX_RESOURCES];
    int Available[MAX_RESOURCES];
    bool Finish[MAX_PROCESSES] = {false};
    int Work[MAX_RESOURCES];
    printf("Enter allocation matrix:\n");
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &Allocation[i][j]);
    printf("Enter request matrix:\n");
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &Request[i][j]);
    printf("Enter available resources:\n");
    for (int j = 0; j < m; j++)
        scanf("%d", &Available[j]);
    for (int j = 0; j < m; j++)
        Work[j] = Available[j];
    bool progress = true;
    while (progress) {
        progress = false;
        for (int i = 0; i < n; i++) {
            if (!Finish[i]) {
                bool canSatisfy = true;
                for (int j = 0; j < m; j++) {
                    if (Request[i][j] > Work[j]) {
                        canSatisfy = false;
                        break;
                    }
                }
                if (canSatisfy) {
                    for (int j = 0; j < m; j++)
                        Work[j] += Allocation[i][j];
                    Finish[i] = true;
                    progress = true;
                }
            }
        }
    }
    bool deadlock = false;
    for (int i = 0; i < n; i++) {
        if (!Finish[i]) {
            if (!deadlock) {
                printf("Deadlock detected! Processes involved:\n");
                deadlock = true;
            }
            printf("P%d\n", i);
        }
    }
    if (!deadlock) {
        printf("No deadlock detected. All processes can complete.\n");
    }
    return EXIT_SUCCESS;
}
