class Student {
    constructor(name, age, grade, subjects) {
        this.name = name;
        this.age = age;
        this.grade = grade;
        this.subjects = subjects;
    }

    greet() {
        console.log(`Hello! My name is ${this.name}.\n`);
    }

    getDetails() {
        console.log(`Name: ${this.name},\nAge: ${this.age},\nGrade: ${this.grade}\n`);
    }

    addSubject(subject) {
        this.subjects.push(subject);
        console.log(`${subject} added to subjects...\n`);
    }

    listSubjects() {
        console.log(`${this.name}'s subjects: ${this.subjects.join(", ")}\n`);
    }
}

// Creating an object
const student = new Student("Roonil03", 20, "A+", ["Math", "Databases", "Physics"]);

// Calling methods
student.greet();
student.getDetails();
student.addSubject("Computer Science");
student.listSubjects();
