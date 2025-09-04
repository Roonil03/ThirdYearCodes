echo "Enter Basic Salary:"
read basics

echo "Enter Travel Allowance (TA):"
read ta

if ! [[ "$basics" =~ ^[0-9]+\.?[0-9]*$ ]] || ! [[ "$ta" =~ ^[0-9]+\.?[0-9]*$ ]]; then
    echo "Error: Please enter valid numeric values."
    exit 1
fi

ten_percent=$(echo "scale=2; $basics * 0.10" | bc)

gross_salary=$(echo "scale=2; $basics + $ta + $ten_percent" | bc)

echo "Basic Salary: $basics"
echo "Travel Allowance: $ta"
echo "10% of Basic Salary: $ten_percent"
echo "Gross Salary: $gross_salary"