import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Student Details'),
        ),
        body: ListView(
          children: const [
            ListTile(
              leading: Icon(Icons.person),
              title: Text('Student 1'),
              subtitle: Text('Computer Science'),
            ),
            Divider(),

            ListTile(
              leading: Icon(Icons.person),
              title: Text('Student 2'),
              subtitle: Text('Information Technology'),
            ),
            Divider(),

            ListTile(
              leading: Icon(Icons.person),
              title: Text('Student 3'),
              subtitle: Text('Electronics'),
            ),
            Divider(),

            ListTile(
              leading: Icon(Icons.person),
              title: Text('Student 4'),
              subtitle: Text('Mechanical'),
            ),
          ],
        ),
      ),
    );
  }
}
