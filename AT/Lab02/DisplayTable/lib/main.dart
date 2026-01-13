import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: TableExample(),
    );
  }
}

class TableExample extends StatelessWidget {
  const TableExample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Student Details Table'),
      ),
      body: Center(
        child: Table(
          border: TableBorder.all(),
          columnWidths: const {
            0: FlexColumnWidth(),
            1: FlexColumnWidth(),
            2: FlexColumnWidth(),
          },
          children: const [
            // Header Row
            TableRow(
              decoration: BoxDecoration(color: Colors.grey),
              children: [
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text(
                    'Name',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text(
                    'Age',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text(
                    'Department',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),

            // Data Rows
            TableRow(
              children: [
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('A'),
                ),
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('20'),
                ),
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('CSE'),
                ),
              ],
            ),
            TableRow(
              children: [
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('B'),
                ),
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('21'),
                ),
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('IT'),
                ),
              ],
            ),
            TableRow(
              children: [
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('C'),
                ),
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('22'),
                ),
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('ECE'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
