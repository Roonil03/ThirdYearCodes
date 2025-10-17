#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, frames_count, *pages, *frames;
    int i, j, k, is_found, page_faults = 0, next = 0;
    printf("Enter number of pages: ");
    scanf("%d", &n);
    pages = (int*)malloc(n * sizeof(int));
    printf("Enter the page sequence: ");
    for(i = 0; i < n; i++){
        scanf("%d", &pages[i]);
    }
    printf("Enter number of frames: ");
    scanf("%d", &frames_count);
    frames = (int*)malloc(frames_count * sizeof(int));
    for(i = 0; i < frames_count; i++){
        frames[i] = -1;
    }
    printf("\nPage\tFrames\n");
    for(i = 0; i < n; i++) {
        is_found = 0;
        for(j = 0; j < frames_count; j++) {
            if(frames[j] == pages[i]) {
                is_found = 1;
                break;
            }
        }
        if(!is_found) {
            frames[next] = pages[i];
            next = (next + 1) % frames_count;
            page_faults++;
        }
        printf("%d\t", pages[i]);
        for(k = 0; k < frames_count; k++)
            if(frames[k] != -1) {
                printf("%d ", frames[k]);
            } else{
                printf("- ");
            }
        printf("\n");
    }
    printf("Total Page Faults = %d\n", page_faults);
    free(pages);
    free(frames);
    return EXIT_SUCCESS;
}
