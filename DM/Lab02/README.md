### Lab Exercise:
1. Consider the hospital dataset with 19 attributes.
    - Remove all the rows which do not have sample data of any patient.
    - Select all the rows with provider number ‘10164’ and store in output.csv
2. 
```SQL
Student (Regno, Name, Major, Bdate)
Course (Course_ID, Cname, dept)
Enroll (RegNo, Course_ID, marks)
Book_Adoption (Course_ID, sem, ISBN)
Text (book_ISBN, title, publisher, author)
```
    - Display the course names taken by students of ICT department.
    - Find whether ICT department has taken up any course which needs books with ISBN=1111.
    - Find names of students who have scored more than 90 in the course of ‘Compilers’
    - Find the departments which provides Major.
    - Find the departments which does not use textbooks of ‘Wiley’ publisher.
    - Display names of the students who have registered for courses for which more than 10 students have registered.
    - Display the departments which uses more than 2 books of author ‘Ken’
    - Find the department which has incorporated textbook by a single publisher.
    - Find course which has maximum number of students.
    - Find the total marks of each student in all courses.

### Additional Exercise
Execute the following SQL queries using data flows in Infosphere
1.
```SQl
PERSON (driver _ id , name, address)
CAR (Regno, model, year)
ACCIDENT (report_number, date, location)
OWNS (driver-id, Regno)
PARTICIPATED (driver-id, Regno , report_number, damage)
```
    - Select registration number of cars which do not come in between the model year 2000 and 2010.
    - Find driver names whose sum of damage amount of all his accidents is less than average
    - damage amount of all accidents in the database.
    - Find driver names whose sum of damage amount of all his accidents is less than average damage amount of
all accidents in database.
    - Find driver ids’ who have met with accident more than once but with different cars owned by him and
damage amount is greater than Rs.50000.
    - Find driver id of persons with name ‘john’.