#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define BUFFER_SIZE 5
#define PRODUCERS 2
#define CONSUMERS 2
#define ITEMS_PER_PRODUCER 10

int buffer[BUFFER_SIZE];
int in = 0, out = 0;
sem_t empty;
sem_t full;
pthread_mutex_t mutex;

void* producer(void* arg) {
    int id = *(int*)arg;
    for (int i = 0; i < ITEMS_PER_PRODUCER; i++) {
        int item = id * 100 + i;
        sem_wait(&empty);
        pthread_mutex_lock(&mutex);
        buffer[in] = item;
        printf("Producer %d produced %d at %d\n", id, item, in);
        in = (in + 1) % BUFFER_SIZE;
        pthread_mutex_unlock(&mutex);
        sem_post(&full);
        usleep(rand() % 100000);
    }
    return NULL;
}

void* consumer(void* arg) {
    int id = *(int*)arg;
    for (int i = 0; i < (PRODUCERS * ITEMS_PER_PRODUCER) / CONSUMERS; i++) {
        sem_wait(&full);
        pthread_mutex_lock(&mutex);
        int item = buffer[out];
        printf("Consumer %d consumed %d from %d\n", id, item, out);
        out = (out + 1) % BUFFER_SIZE;
        pthread_mutex_unlock(&mutex);
        sem_post(&empty);
        usleep(rand() % 150000);
    }
    return NULL;
}

int main() {
    pthread_t prod[PRODUCERS], cons[CONSUMERS];
    int ids[PRODUCERS > CONSUMERS ? PRODUCERS : CONSUMERS];
    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);
    pthread_mutex_init(&mutex, NULL);
    srand(time(NULL));
    for (int i = 0; i < PRODUCERS; i++) {
        ids[i] = i + 1;
        pthread_create(&prod[i], NULL, producer, &ids[i]);
    }
    for (int i = 0; i < CONSUMERS; i++) {
        ids[i] = i + 1;
        pthread_create(&cons[i], NULL, consumer, &ids[i]);
    }
    for (int i = 0; i < PRODUCERS; i++){
        pthread_join(prod[i], NULL);
    }
    for (int i = 0; i < CONSUMERS; i++){
        pthread_join(cons[i], NULL);
    }
    sem_destroy(&empty);
    sem_destroy(&full);
    pthread_mutex_destroy(&mutex);
    return EXIT_SUCCESS;
}
