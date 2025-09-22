#include <stdio.h>

struct Process {
    int pid;
    int arrival_time;
    int burst_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
    int response_time;
};

void non_preemptive_sjf_different_arrival(struct Process processes[], int n) {
    int current_time = 0;
    int completed = 0;
    int is_completed[100] = {0};    
    printf("\nNon-Preemptive SJF with Different Arrival Times:\n");
    printf("Execution Order and Timeline:\n");    
    while (completed < n) {
        int shortest_job_idx = -1;
        int min_burst = 999999;
        for (int i = 0; i < n; i++) {
            if (processes[i].arrival_time <= current_time && 
                !is_completed[i] && 
                processes[i].burst_time < min_burst) {
                min_burst = processes[i].burst_time;
                shortest_job_idx = i;
            }
        }        
        if (shortest_job_idx == -1) {
            current_time++;
            continue;
        }
        printf("Time %d-%d: Process P%d (Burst: %d)\n", 
               current_time, current_time + processes[shortest_job_idx].burst_time,
               processes[shortest_job_idx].pid, processes[shortest_job_idx].burst_time);
        processes[shortest_job_idx].response_time = current_time - processes[shortest_job_idx].arrival_time;
        current_time += processes[shortest_job_idx].burst_time;
        processes[shortest_job_idx].completion_time = current_time;
        processes[shortest_job_idx].turnaround_time = 
            processes[shortest_job_idx].completion_time - processes[shortest_job_idx].arrival_time;
        processes[shortest_job_idx].waiting_time = 
            processes[shortest_job_idx].turnaround_time - processes[shortest_job_idx].burst_time;        
        is_completed[shortest_job_idx] = 1;
        completed++;
    }
}

void print_sjf_results(struct Process processes[], int n) {
    printf("\nNon-Preemptive SJF Results:\n");
    printf("PID\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\tResponse\n");    
    float avg_turnaround = 0, avg_waiting = 0, avg_response = 0;    
    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t%d\t%d\t\t%d\t\t%d\t%d\n",
               processes[i].pid, processes[i].arrival_time, processes[i].burst_time,
               processes[i].completion_time, processes[i].turnaround_time,
               processes[i].waiting_time, processes[i].response_time);        
        avg_turnaround += processes[i].turnaround_time;
        avg_waiting += processes[i].waiting_time;
        avg_response += processes[i].response_time;
    }    
    printf("\nAverage Turnaround Time: %.2f\n", avg_turnaround / n);
    printf("Average Waiting Time: %.2f\n", avg_waiting / n);
    printf("Average Response Time: %.2f\n", avg_response / n);
}

int main() {
    int n;    
    printf("Non-Preemptive SJF with Different Arrival Times\n");
    printf("Enter number of processes: ");
    scanf("%d", &n);    
    struct Process processes[n];    
    printf("Enter process details:\n");
    for (int i = 0; i < n; i++) {
        processes[i].pid = i + 1;
        printf("Process P%d:\n", i + 1);
        printf("  Arrival Time: ");
        scanf("%d", &processes[i].arrival_time);
        printf("  Burst Time: ");
        scanf("%d", &processes[i].burst_time);
    }    
    non_preemptive_sjf_different_arrival(processes, n);
    print_sjf_results(processes, n);    
    return 0;
}
