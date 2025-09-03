grep ":ICT:" studentInformation.txt | grep -v "RegistrationNo" | wc -l
echo ""

sed 's/:IT:/:Information Technology:/g' studentInformation.txt > ITStudents.txt
cat ITStudents.txt
echo ""

student_data=$(grep "^0001:" studentInformation.txt)
sub1=$(echo $student_data | cut -d':' -f6)
sub2=$(echo $student_data | cut -d':' -f7)
sub3=$(echo $student_data | cut -d':' -f8)
average=$(echo "($sub1 + $sub2 + $sub3) / 3" | bc)
echo "Student: $(echo $student_data | cut -d':' -f2)"
echo "Marks: $sub1, $sub2, $sub3"
echo "Average: $average"
echo ""

head -n 1 studentInformation.txt | tr '[:lower:]' '[:upper:]'
tail -n +2 studentInformation.txt
echo ""