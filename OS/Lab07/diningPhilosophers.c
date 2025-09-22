#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define N 5
#define EAT_TIMES 3

sem_t chopstick[N];
pthread_t phil[N];

void* philosopher(void* arg) {
    int id = *(int*)arg;
    int left = id;
    int right = (id + 1) % N;
    for (int i = 0; i < EAT_TIMES; i++) {
        printf("Philosopher %d is thinking.\n", id);
        usleep(rand() % 200000);
        if (left < right) {
            sem_wait(&chopstick[left]);
            sem_wait(&chopstick[right]);
        } else {
            sem_wait(&chopstick[right]);
            sem_wait(&chopstick[left]);
        }
        printf("Philosopher %d is eating (%d/%d).\n", id, i+1, EAT_TIMES);
        usleep(rand() % 200000);
        sem_post(&chopstick[left]);
        sem_post(&chopstick[right]);
    }
    return NULL;
}

int main() {
    int ids[N];
    srand(time(NULL));
    for (int i = 0; i < N; i++)
        sem_init(&chopstick[i], 0, 1);
    for (int i = 0; i < N; i++) {
        ids[i] = i;
        pthread_create(&phil[i], NULL, philosopher, &ids[i]);
    }
    for (int i = 0; i < N; i++){
        pthread_join(phil[i], NULL);
    }
    for (int i = 0; i < N; i++){
        sem_destroy(&chopstick[i]);
    }
    return EXIT_SUCCESS;
}
