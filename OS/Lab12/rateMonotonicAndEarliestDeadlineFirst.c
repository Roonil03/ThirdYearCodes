#include <stdio.h>
#include <limits.h>

#define MAX 10
#define TIME 20

typedef struct {
    int id;
    int burst;
    int period;
    int deadline;
    int next_arrival;
    int remaining;
} task;

void simulate_RM(task a[], int n, int time) {
    printf("RM Scheduling Simulation:\n");
    for (int t = 0; t < time; t++) {
        int high_prio = -1;
        for (int i = 0; i < n; i++) {
            if (t == a[i].next_arrival) {
                a[i].remaining = a[i].burst;
                a[i].deadline = t + a[i].period;
            }
        }
        for (int i = 0; i < n; i++) {
            if (a[i].remaining > 0) {
                if (high_prio == -1 || a[i].period < a[high_prio].period) {
                    high_prio = i;
                }
            }
        }
        if (high_prio != -1) {
            printf("Time %2d: Task %d\n", t, a[high_prio].id);
            a[high_prio].remaining--;
        } else {
            printf("Time %2d: Idle\n", t);
        }
        for (int i = 0; i < n; i++) {
            if (a[i].remaining == 0 && t + 1 == a[i].deadline) {
                a[i].next_arrival += a[i].period;
            }
        }
    }
}

void simulate_EDF(task b[], int n, int time) {
    printf("\nEDF Scheduling Simulation:\n");
    for (int t = 0; t < time; t++) {
        int min_deadline = INT_MAX, idx = -1;
        for (int i = 0; i < n; i++) {
            if (t == b[i].next_arrival) {
                b[i].remaining = b[i].burst;
                b[i].deadline = t + b[i].period;
            }
        }
        for (int i = 0; i < n; i++) {
            if (b[i].remaining > 0 && b[i].deadline < min_deadline) {
                min_deadline = b[i].deadline;
                idx = i;
            }
        }
        if (idx != -1) {
            printf("Time %2d: Task %d\n", t, b[idx].id);
            b[idx].remaining--;
        } else {
            printf("Time %2d: Idle\n", t);
        }
        for (int i = 0; i < n; i++) {
            if (b[i].remaining == 0 && t + 1 == b[i].deadline) {
                b[i].next_arrival += b[i].period;
            }
        }
    }
}

int main() {
    int n, time, burst, period;
    task a[MAX], b[MAX];
    printf("Enter number of tasks: ");
    scanf("%d", &n);
    printf("Enter simulation time: ");
    scanf("%d", &time);
    for (int i = 0; i < n; i++) {
        printf("Task %d burst time: ", i+1);
        scanf("%d", &burst);
        printf("Task %d period: ", i+1);
        scanf("%d", &period);
        a[i] = (task){i+1, burst, period, 0, 0, 0};
        b[i] = (task){i+1, burst, period, 0, 0, 0};
    }
    simulate_RM(a, n, time);
    simulate_EDF(b, n, time);
    return 0;
}
