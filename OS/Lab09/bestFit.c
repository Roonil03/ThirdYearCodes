#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void firstFit(int *blockSize, int blocks, int *processSize, int processes) {
    int *allocation = (int *)malloc(processes * sizeof(int));
    memset(allocation, -1, processes * sizeof(int));
    int *tempBlocks = (int *)malloc(blocks * sizeof(int));
    memcpy(tempBlocks, blockSize, blocks * sizeof(int));
    for (int i = 0; i < processes; i++) {
        for (int j = 0; j < blocks; j++) {
            if (tempBlocks[j] >= processSize[i]) {
                allocation[i] = j;
                tempBlocks[j] -= processSize[i];
                break;
            }
        }
    }
    printf("First Fit Result:\nProcess No.\tProcess Size\tBlock No.\n");
    for (int i = 0; i < processes; i++) {
        printf("%d\t\t%d\t\t", i + 1, processSize[i]);
        if (allocation[i] != -1)
            printf("%d\n", allocation[i] + 1);
        else
            printf("Not Allocated\n");
    }
    free(allocation);
    free(tempBlocks);
}

void bestFit(int *blockSize, int blocks, int *processSize, int processes) {
    int *allocation = (int *)malloc(processes * sizeof(int));
    memset(allocation, -1, processes * sizeof(int));
    int *tempBlocks = (int *)malloc(blocks * sizeof(int));
    memcpy(tempBlocks, blockSize, blocks * sizeof(int));
    for (int i = 0; i < processes; i++) {
        int bestIdx = -1;
        for (int j = 0; j < blocks; j++) {
            if (tempBlocks[j] >= processSize[i]) {
                if (bestIdx == -1 || tempBlocks[j] < tempBlocks[bestIdx])
                    bestIdx = j;
            }
        }
        if (bestIdx != -1) {
            allocation[i] = bestIdx;
            tempBlocks[bestIdx] -= processSize[i];
        }
    }
    printf("Best Fit Result:\nProcess No.\tProcess Size\tBlock No.\n");
    for (int i = 0; i < processes; i++) {
        printf("%d\t\t%d\t\t", i + 1, processSize[i]);
        if (allocation[i] != -1){
            printf("%d\n", allocation[i] + 1);
        } else{
            printf("Not Allocated\n");
        }
    }
    free(allocation);
    free(tempBlocks);
}

int main() {
    int blocks, processes;
    printf("Enter number of blocks: ");
    scanf("%d", &blocks);
    int *blockSize = (int *)malloc(blocks * sizeof(int));
    printf("Enter block sizes: ");
    for (int i = 0; i < blocks; i++){
        scanf("%d", &blockSize[i]);
    }
    printf("Enter number of processes: ");
    scanf("%d", &processes);
    int *processSize = (int *)malloc(processes * sizeof(int));
    printf("Enter process sizes: ");
    for (int i = 0; i < processes; i++){
        scanf("%d", &processSize[i]);
    }
    firstFit(blockSize, blocks, processSize, processes);
    bestFit(blockSize, blocks, processSize, processes);
    free(blockSize);
    free(processSize);
    return EXIT_SUCCESS;
}
