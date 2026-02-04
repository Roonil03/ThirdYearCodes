import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final List<Map<String, String>> students = [
    {'name': 'Student 1', 'department': 'CSE'},
    {'name': 'Student 2', 'department': 'IT'},
    {'name': 'Student 3', 'department': 'ECE'},
    {'name': 'Student 4', 'department': 'ME'},
    {'name': 'Student 5', 'department': 'CE'},
  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Student List'),
        ),
        body: ListView.builder(
          itemCount: students.length,
          itemBuilder: (context, index) {
            final student = students[index];
            return ListTile(
              leading: const Icon(Icons.person),
              title: Text(student['name']!),
              subtitle: Text(student['department']!),
            );
          },
        ),
      ),
    );
  }
}
