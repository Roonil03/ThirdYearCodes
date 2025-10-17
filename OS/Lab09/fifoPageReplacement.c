#include <stdio.h>
#include <stdlib.h>

int main() {
    int pageCount, frameCount;
    printf("Enter number of pages: ");
    scanf("%d", &pageCount);
    int *pages = (int *)malloc(pageCount * sizeof(int));
    printf("Enter page numbers: ");
    for (int i = 0; i < pageCount; i++){
        scanf("%d", &pages[i]);
    }
    printf("Enter number of frames: ");
    scanf("%d", &frameCount);
    int *frames = (int *)malloc(frameCount * sizeof(int));
    for (int i = 0; i < frameCount; i++){
        frames[i] = -1;
    }
    int faults = 0, j = 0;
    printf("\nRef String\tPage Frames\n");
    for (int i = 0; i < pageCount; i++) {
        printf("%d\t\t", pages[i]);
        int available = 0;
        for (int k = 0; k < frameCount; k++) {
            if (frames[k] == pages[i]) {
                available = 1;
                break;
            }
        }
        if (!available) {
            frames[j] = pages[i];
            j = (j + 1) % frameCount;
            faults++;
        }
        for (int k = 0; k < frameCount; k++)
            printf("%d\t", frames[k]);
        printf("\n");
    }
    printf("\nPage Faults = %d\n", faults);
    free(pages);
    free(frames);
    return EXIT_SUCCESS;
}
