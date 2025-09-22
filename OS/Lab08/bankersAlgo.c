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
    int Max[MAX_PROCESSES][MAX_RESOURCES];
    int Need[MAX_PROCESSES][MAX_RESOURCES];
    int Available[MAX_RESOURCES];
    bool Finish[MAX_PROCESSES] = {false};
    int SafeSequence[MAX_PROCESSES];
    printf("Enter allocation matrix:\n");
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &Allocation[i][j]);
    printf("Enter max matrix:\n");
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &Max[i][j]);
    printf("Enter available resources:\n");
    for (int j = 0; j < m; j++)
        scanf("%d", &Available[j]);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            Need[i][j] = Max[i][j] - Allocation[i][j];
    int count = 0;
    while (count < n) {
        bool found = false;
        for (int i = 0; i < n; i++) {
            if (!Finish[i]) {
                bool canAllocate = true;
                for (int j = 0; j < m; j++) {
                    if (Need[i][j] > Available[j]) {
                        canAllocate = false;
                        break;
                    }
                }
                if (canAllocate) {
                    for (int j = 0; j < m; j++)
                        Available[j] += Allocation[i][j];
                    SafeSequence[count++] = i;
                    Finish[i] = true;
                    found = true;
                }
            }
        }
        if (!found) {
            printf("System is not in a safe state.\n");
            return 0;
        }
    }
    printf("System is in a safe state.\nSafe sequence is: ");
    for (int i = 0; i < n; i++) {
        printf("P%d", SafeSequence[i]);
        if (i != n-1) printf(" -> ");
    }
    printf("\n");
    char ans;
    printf("Do you want to make a resource request? (y/n): ");
    scanf(" %c", &ans);
    if (ans == 'y' || ans == 'Y') {
        int pid;
        int Request[MAX_RESOURCES];
        printf("Enter process number making request: ");
        scanf("%d", &pid);
        printf("Enter request vector:\n");
        for (int j = 0; j < m; j++)
            scanf("%d", &Request[j]);
        for (int j = 0; j < m; j++) {
            if (Request[j] > Need[pid][j]) {
                printf("Error: Process has exceeded its maximum claim.\n");
                return 0;
            }
        }
        for (int j = 0; j < m; j++) {
            if (Request[j] > Available[j]) {
                printf("Resources not available. Process must wait.\n");
                return 0;
            }
        }
        for (int j = 0; j < m; j++) {
            Available[j] -= Request[j];
            Allocation[pid][j] += Request[j];
            Need[pid][j] -= Request[j];
        }
        for (int i = 0; i < n; i++) {
            Finish[i] = false;
        }
        count = 0;
        while (count < n) {
            bool found2 = false;
            for (int i = 0; i < n; i++) {
                if (!Finish[i]) {
                    bool canAll2 = true;
                    for (int j = 0; j < m; j++) {
                        if (Need[i][j] > Available[j]) {
                            canAll2 = false;
                            break;
                        }
                    }
                    if (canAll2) {
                        for (int j = 0; j < m; j++)
                            Available[j] += Allocation[i][j];
                        SafeSequence[count++] = i;
                        Finish[i] = true;
                        found2 = true;
                    }
                }
            }
            if (!found2) {
                printf("After allocation, system is NOT in safe state. Request denied.\n");
                return 0;
            }
        }
        printf("After allocation, system is still safe.\nNew safe sequence: ");
        for (int i = 0; i < n; i++) {
            printf("P%d", SafeSequence[i]);
            if (i != n-1) printf(" -> ");
        }
        printf("\n");
    }
    return EXIT_SUCCESS;
}
