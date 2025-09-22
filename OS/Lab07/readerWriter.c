#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define READERS 5
#define WRITERS 2
#define READS_PER_READER 5
#define WRITES_PER_WRITER 5

int shared_data = 0;
int read_count = 0;
sem_t mutex_rc;
sem_t rw_mutex;

void* reader(void* arg) {
    int id = *(int*)arg;
    for (int i = 0; i < READS_PER_READER; i++) {
        sem_wait(&mutex_rc);
        read_count++;
        if (read_count == 1)
            sem_wait(&rw_mutex);
        sem_post(&mutex_rc);
        printf("Reader %d reads data = %d\n", id, shared_data);
        usleep(rand() % 100000);
        sem_wait(&mutex_rc);
        read_count--;
        if (read_count == 0)
            sem_post(&rw_mutex);
        sem_post(&mutex_rc);

        usleep(rand() % 150000);
    }
    return NULL;
}

void* writer(void* arg) {
    int id = *(int*)arg;
    for (int i = 0; i < WRITES_PER_WRITER; i++) {
        sem_wait(&rw_mutex);
        shared_data += id;
        printf("Writer %d updates data to %d\n", id, shared_data);
        usleep(rand() % 200000);
        sem_post(&rw_mutex);
        usleep(rand() % 200000);
    }
    return NULL;
}

int main() {
    pthread_t rthr[READERS], wthr[WRITERS];
    int ids[READERS > WRITERS ? READERS : WRITERS];
    sem_init(&mutex_rc, 0, 1);
    sem_init(&rw_mutex, 0, 1);
    srand(time(NULL));
    for (int i = 0; i < READERS; i++) {
        ids[i] = i + 1;
        pthread_create(&rthr[i], NULL, reader, &ids[i]);
    }
    for (int i = 0; i < WRITERS; i++) {
        ids[i] = i + 1;
        pthread_create(&wthr[i], NULL, writer, &ids[i]);
    }
    for (int i = 0; i < READERS; i++){
        pthread_join(rthr[i], NULL);
    }
    for (int i = 0; i < WRITERS; i++){
        pthread_join(wthr[i], NULL);
    }
    sem_destroy(&mutex_rc);
    sem_destroy(&rw_mutex);
    return EXIT_SUCCESS;
}
