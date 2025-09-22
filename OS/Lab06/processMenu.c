#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Process {
    int pid;
    int arrival_time;
    int burst_time;
    int priority;
    int remaining_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
    int response_time;
    int first_response;
};

void preemptive_sjf(struct Process processes[], int n) {
    int current_time = 0;
    int completed = 0;
    int shortest = -1;
    int min_burst = 999999;
    for (int i = 0; i < n; i++) {
        processes[i].remaining_time = processes[i].burst_time;
        processes[i].first_response = -1;
    }    
    printf("\nPreemptive SJF Scheduling:\n");
    printf("Time\tProcess\n");    
    while (completed < n) {
        shortest = -1;
        min_burst = 999999;        
        for (int i = 0; i < n; i++) {
            if (processes[i].arrival_time <= current_time && 
                processes[i].remaining_time > 0 && 
                processes[i].remaining_time < min_burst) {
                min_burst = processes[i].remaining_time;
                shortest = i;
            }
        }        
        if (shortest == -1) {
            current_time++;
            continue;
        }
        if (processes[shortest].first_response == -1) {
            processes[shortest].first_response = current_time;
            processes[shortest].response_time = current_time - processes[shortest].arrival_time;
        }        
        printf("%d\tP%d\n", current_time, processes[shortest].pid);
        processes[shortest].remaining_time--;
        current_time++;
        if (processes[shortest].remaining_time == 0) {
            completed++;
            processes[shortest].completion_time = current_time;
            processes[shortest].turnaround_time = processes[shortest].completion_time - processes[shortest].arrival_time;
            processes[shortest].waiting_time = processes[shortest].turnaround_time - processes[shortest].burst_time;
        }
    }
}

void round_robin(struct Process processes[], int n, int time_quantum) {
    int current_time = 0;
    int completed = 0;
    int queue[100];
    int front = 0, rear = 0;
    int in_queue[100] = {0};
    for (int i = 0; i < n; i++) {
        processes[i].remaining_time = processes[i].burst_time;
        processes[i].first_response = -1;
    }
    for (int i = 0; i < n; i++) {
        if (processes[i].arrival_time == 0) {
            queue[rear++] = i;
            in_queue[i] = 1;
        }
    }    
    printf("\nRound Robin Scheduling (Time Quantum = %d):\n", time_quantum);
    printf("Time\tProcess\n");    
    while (completed < n) {
        if (front == rear) {
            current_time++;
            for (int i = 0; i < n; i++) {
                if (processes[i].arrival_time == current_time && !in_queue[i] && processes[i].remaining_time > 0) {
                    queue[rear++] = i;
                    in_queue[i] = 1;
                }
            }
            continue;
        }        
        int current_process = queue[front++];
        in_queue[current_process] = 0;
        if (processes[current_process].first_response == -1) {
            processes[current_process].first_response = current_time;
            processes[current_process].response_time = current_time - processes[current_process].arrival_time;
        }        
        int execution_time = (processes[current_process].remaining_time > time_quantum) ? 
                            time_quantum : processes[current_process].remaining_time;        
        for (int i = 0; i < execution_time; i++) {
            printf("%d\tP%d\n", current_time, processes[current_process].pid);
            current_time++;
            for (int j = 0; j < n; j++) {
                if (processes[j].arrival_time == current_time && !in_queue[j] && processes[j].remaining_time > 0) {
                    queue[rear++] = j;
                    in_queue[j] = 1;
                }
            }
        }        
        processes[current_process].remaining_time -= execution_time;        
        if (processes[current_process].remaining_time == 0) {
            completed++;
            processes[current_process].completion_time = current_time;
            processes[current_process].turnaround_time = processes[current_process].completion_time - processes[current_process].arrival_time;
            processes[current_process].waiting_time = processes[current_process].turnaround_time - processes[current_process].burst_time;
        } else {
            queue[rear++] = current_process;
            in_queue[current_process] = 1;
        }
    }
}

void non_preemptive_priority(struct Process processes[], int n) {
    int current_time = 0;
    int completed = 0;
    int is_completed[100] = {0};    
    printf("\nNon-Preemptive Priority Scheduling:\n");
    printf("Time\tProcess\n");    
    while (completed < n) {
        int highest_priority_idx = -1;
        int highest_priority = 999999;
        for (int i = 0; i < n; i++) {
            if (processes[i].arrival_time <= current_time && 
                !is_completed[i] && 
                processes[i].priority < highest_priority) {
                highest_priority = processes[i].priority;
                highest_priority_idx = i;
            }
        }        
        if (highest_priority_idx == -1) {
            current_time++;
            continue;
        }
        processes[highest_priority_idx].response_time = current_time - processes[highest_priority_idx].arrival_time;        
        for (int i = 0; i < processes[highest_priority_idx].burst_time; i++) {
            printf("%d\tP%d\n", current_time, processes[highest_priority_idx].pid);
            current_time++;
        }        
        is_completed[highest_priority_idx] = 1;
        completed++;        
        processes[highest_priority_idx].completion_time = current_time;
        processes[highest_priority_idx].turnaround_time = processes[highest_priority_idx].completion_time - processes[highest_priority_idx].arrival_time;
        processes[highest_priority_idx].waiting_time = processes[highest_priority_idx].turnaround_time - processes[highest_priority_idx].burst_time;
    }
}

void print_results(struct Process processes[], int n, char* algorithm_name) {
    printf("\n%s Results:\n", algorithm_name);
    printf("PID\tArrival\tBurst\tPriority\tCompletion\tTurnaround\tWaiting\tResponse\n");    
    float avg_turnaround = 0, avg_waiting = 0, avg_response = 0;    
    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t%d\t%d\t\t%d\t\t%d\t\t%d\t%d\n",
               processes[i].pid, processes[i].arrival_time, processes[i].burst_time,
               processes[i].priority, processes[i].completion_time,
               processes[i].turnaround_time, processes[i].waiting_time, processes[i].response_time);        
        avg_turnaround += processes[i].turnaround_time;
        avg_waiting += processes[i].waiting_time;
        avg_response += processes[i].response_time;
    }    
    printf("\nAverage Turnaround Time: %.2f\n", avg_turnaround / n);
    printf("Average Waiting Time: %.2f\n", avg_waiting / n);
    printf("Average Response Time: %.2f\n", avg_response / n);
}

int main() {
    int n, choice, time_quantum;    
    printf("Enter number of processes: ");
    scanf("%d", &n);    
    struct Process processes[n];
    struct Process temp_processes[n];    
    printf("Enter process details:\n");
    for (int i = 0; i < n; i++) {
        printf("Process %d:\n", i + 1);
        processes[i].pid = i + 1;
        printf("  Arrival Time: ");
        scanf("%d", &processes[i].arrival_time);
        printf("  Burst Time: ");
        scanf("%d", &processes[i].burst_time);
        printf("  Priority (lower number = higher priority): ");
        scanf("%d", &processes[i].priority);
    }    
    do {
        printf("\nProcess Scheduling Algorithms:\n");
        printf("1. Preemptive SJF\n");
        printf("2. Round Robin\n");
        printf("3. Non-Preemptive Priority\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        memcpy(temp_processes, processes, sizeof(processes));        
        switch (choice) {
            case 1:
                preemptive_sjf(temp_processes, n);
                print_results(temp_processes, n, "Preemptive SJF");
                break;
            case 2:
                printf("Enter time quantum: ");
                scanf("%d", &time_quantum);
                round_robin(temp_processes, n, time_quantum);
                print_results(temp_processes, n, "Round Robin");
                break;
            case 3:
                non_preemptive_priority(temp_processes, n);
                print_results(temp_processes, n, "Non-Preemptive Priority");
                break;
            case 4:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice!\n");
        }
    } while (choice != 4);    
    return EXIT_SUCCESS;
}
