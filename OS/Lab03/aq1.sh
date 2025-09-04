#!/bin/bash
# Script to check if a number is prime or not

echo "Enter a number:"
read number

# Validate input - check if it's a positive integer
if ! [[ "$number" =~ ^[0-9]+$ ]] || [ "$number" -le 0 ]; then
    echo "Error: Please enter a valid positive integer."
    exit 1
fi

# Handle special cases
if [ "$number" -eq 1 ]; then
    echo "$number is neither prime nor composite."
    exit 0
elif [ "$number" -eq 2 ]; then
    echo "$number is a prime number."
    exit 0
fi

# Check if number is even (and greater than 2)
if [ $((number % 2)) -eq 0 ]; then
    echo "$number is not a prime number."
    exit 0
fi

# Check for odd divisors from 3 to sqrt(number)
is_prime=1
i=3

while [ $((i * i)) -le "$number" ]; do
    if [ $((number % i)) -eq 0 ]; then
        is_prime=0
        break
    fi
    i=$((i + 2))
done

if [ $is_prime -eq 1 ]; then
    echo "$number is a prime number."
else
    echo "$number is not a prime number."
fi
