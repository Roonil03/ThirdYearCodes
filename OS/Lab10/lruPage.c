#include <stdio.h>
#include <stdlib.h>

int findReplaceIndex(int current, int n, int *pages, int *frames, int frames_count) {
    int max_distance = -1, replace_index = -1;
    for(int i = 0; i < frames_count; i++) {
        int j, found = 0;
        for(j = current + 1; j < n; j++) {
            if(frames[i] == pages[j]) {
                found = 1;
                if(j > max_distance) {
                    max_distance = j;
                    replace_index = i;
                }
                break;
            }
        }
        if(!found){
            return i;
        }
    }
    if(replace_index == -1){
        return 0;
    }
    return replace_index;
}

int main() {
    int n, frames_count, *pages, *frames;
    int i, j, k, is_found, page_faults = 0;
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
            int filled = 0;
            for(j = 0; j < frames_count; j++) {
                if(frames[j] == -1) {
                    frames[j] = pages[i];
                    filled = 1;
                    break;
                }
            }
            if(!filled)
                frames[findReplaceIndex(i, n, pages, frames, frames_count)] = pages[i];
            page_faults++;
        }
        printf("%d\t", pages[i]);
        for(k = 0; k < frames_count; k++)
            if(frames[k] != -1) printf("%d ", frames[k]);
            else printf("- ");
        printf("\n");
    }
    printf("Total Page Faults = %d\n", page_faults);
    free(pages);
    free(frames);
    return EXIT_SUCCESS;
}
