#include <stdio.h>
#include <stdlib.h>

#define MAX 100

void SSTF(int req[], int n, int head) {
    int done[MAX]= {0}, cnt = 0, total = 0, idx, min, i;
    printf("SSTF Order: %d ", head);
    while(cnt < n) {
        min = 1e9;
        idx = -1;
        for(i = 0; i < n; i++) {
            if(!done[i] && abs(head - req[i]) < min) {
                min = abs(head - req[i]);
                idx = i;
            }
        }
        printf("-> %d ", req[idx]);
        total += abs(head - req[idx]);
        head = req[idx];
        done[idx] = 1;
        cnt++;
    }
    printf("\nTotal head movement: %d\n", total);
}

void SCAN(int req[], int n, int head, int disk_size) {
    int arr[MAX], i, j, total = 0, direction, temp;
    printf("Enter direction (1: higher, 0: lower): ");
    scanf("%d", &direction);
    for(i = 0; i < n; i++) arr[i] = req[i];
    arr[n++] = head;
    arr[n++] = direction ? disk_size - 1 : 0;
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
    printf("SCAN Order: %d ", head);
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

void CSCAN(int req[], int n, int head, int disk_size) {
    int arr[MAX], i, j, total = 0, temp;
    for(i = 0; i < n; i++) arr[i] = req[i];
    arr[n++] = head;
    arr[n++] = 0;
    arr[n++] = disk_size - 1;
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
    printf("C-SCAN Order: %d ", head);
    for(j = i+1; j < n; j++) {
        printf("-> %d ", arr[j]);
        total += abs(head - arr[j]);
        head = arr[j];
    }
    head = 0;
    printf("-> 0 ");
    for(j = 1; j < i; j++) {
        printf("-> %d ", arr[j]);
        total += abs(head - arr[j]);
        head = arr[j];
    }
    printf("\nTotal head movement: %d\n", total);
}

void CLOOK(int req[], int n, int head) {
    int arr[MAX], i, j, total = 0, temp;
    for(i = 0; i < n; i++){
        arr[i] = req[i];
    }
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
    printf("C-LOOK Order: %d ", head);
    for(j = i+1; j < n; j++) {
        printf("-> %d ", arr[j]);
        total += abs(head - arr[j]);
        head = arr[j];
    }
    for(j = 0; j < i; j++) { 
        printf("-> %d ", arr[j]);
        total += abs(head - arr[j]);
        head = arr[j];
    }
    printf("\nTotal head movement: %d\n", total);
}

int main() {
    int req[MAX], n, i, head, disk_size, ch;
    printf("Enter disk size (max cylinder number): ");
    scanf("%d", &disk_size);
    printf("Enter number of requests: ");
    scanf("%d", &n);
    printf("Enter request array:\n");
    for(i=0;i<n;i++) scanf("%d",&req[i]);
    printf("Enter initial head position: ");
    scanf("%d", &head);
    do {
        printf("\nMenu:\n1. SSTF\n2. SCAN\n3. CSCAN\n4. CLOOK\n5. Exit\nEnter choice: ");
        scanf("%d", &ch);
        switch(ch) {
            case 1: SSTF(req, n, head); break;
            case 2: SCAN(req, n, head, disk_size); break;
            case 3: CSCAN(req, n, head, disk_size); break;
            case 4: CLOOK(req, n, head); break;
        }
    } while(ch!=5);
    return EXIT_SUCCESS;
}
