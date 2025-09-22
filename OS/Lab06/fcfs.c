#include <stdio.h>
#include <stdlib.h>

struct Process {
    int pid;
    int burst_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
};

void fcfs_same_arrival(struct Process processes[], int n) {
    int current_time = 0;    
    printf("\nFCFS Scheduling (All processes arrive at time 0):\n");
    printf("Execution Order: ");    
    for (int i = 0; i < n; i++) {
        printf("P%d ", processes[i].pid);
        current_time += processes[i].burst_time;
        processes[i].completion_time = current_time;
        processes[i].turnaround_time = processes[i].completion_time;
        processes[i].waiting_time = processes[i].turnaround_time - processes[i].burst_time;
    }
    printf("\n");
}

void print_fcfs_results(struct Process processes[], int n) {
    printf("\nFCFS Results:\n");
    printf("PID\tBurst Time\tCompletion Time\tTurnaround Time\tWaiting Time\n");    
    float avg_turnaround = 0, avg_waiting = 0;    
    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t\t%d\t\t%d\t\t%d\n",
               processes[i].pid, processes[i].burst_time,
               processes[i].completion_time, processes[i].turnaround_time,
               processes[i].waiting_time);
        
        avg_turnaround += processes[i].turnaround_time;
        avg_waiting += processes[i].waiting_time;
    }    
    printf("\nAverage Turnaround Time: %.2f\n", avg_turnaround / n);
    printf("Average Waiting Time: %.2f\n", avg_waiting / n);
}

int main() {
    int n;    
    printf("FCFS Scheduling (All processes arrive at same time)\n");
    printf("Enter number of processes: ");
    scanf("%d", &n);    
    struct Process processes[n];    
    printf("Enter burst times for each process:\n");
    for (int i = 0; i < n; i++) {
        processes[i].pid = i + 1;
        printf("Process P%d burst time: ", i + 1);
        scanf("%d", &processes[i].burst_time);
    }    
    fcfs_same_arrival(processes, n);
    print_fcfs_results(processes, n);    
    return EXIT_SUCCESS;
}
