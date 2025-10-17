#include <stdio.h>
#include <stdlib.h>

#define MAX 100

void FCFS(int req[], int n, int head) {
    int total = 0, i;
    printf("FCFS Order: %d ", head);
    for(i = 0; i < n; i++) {
        printf("-> %d ", req[i]);
        total += abs(head - req[i]);
        head = req[i];
    }
    printf("\nTotal head movement: %d\n", total);
}

void LOOK(int req[], int n, int head) {
    int arr[MAX], i, j, total = 0, direction, temp;
    printf("Enter direction (1: towards higher, 0: towards lower): ");
    scanf("%d", &direction);
    for(i = 0; i < n; i++) arr[i] = req[i];
    arr[n++] = head;
    for(i = 0; i < n-1; i++){
        for(j = i+1; j < n; j++){
            if(arr[j] < arr[i]) {
                temp=arr[i];
                arr[i]=arr[j];
                arr[j]=temp;
            }
        }
    }
    for(i = 0; i < n; i++){
        if(arr[i]==head){
            break;
        }
    }
    printf("LOOK Order: %d ", head);
    if(direction) {
        for(j = i+1; j < n; j++) {
            printf("-> %d ", arr[j]);
            total += abs(head - arr[j]);
            head = arr[j];
        }
        for(j = i-1; j >= 0; j--) {
            printf("-> %d ", arr[j]);
            total += abs(head - arr[j]);
            head = arr[j];
        }
    } else {
        for(j = i-1; j >= 0; j--) {
            printf("-> %d ", arr[j]);
            total += abs(head - arr[j]);
            head = arr[j];
        }
        for(j = i+1; j < n; j++) {
            printf("-> %d ", arr[j]);
            total += abs(head - arr[j]);
            head = arr[j];
        }
    }
    printf("\nTotal head movement: %d\n", total);
}

int main() {
    int req[MAX], n, i, head, ch;
    printf("Enter number of requests: ");
    scanf("%d", &n);
    printf("Enter request array:\n");
    for(i=0;i<n;i++) scanf("%d",&req[i]);
    printf("Enter initial head position: ");
    scanf("%d", &head);
    do {
        printf("\nMenu:\n1. FCFS\n2. LOOK\n3. Exit\nEnter choice: ");
        scanf("%d", &ch);
        switch(ch){
            case 1: FCFS(req, n, head); break;
            case 2: LOOK(req, n, head); break;
        }
    } while(ch!=3);
    return EXIT_SUCCESS;
}
