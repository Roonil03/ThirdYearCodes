import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final int itemCount = 20; // Number of grid items

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Les couleurs'),
        ),
        body: GridView.builder(
          padding: const EdgeInsets.all(10),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2, // 2 columns
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
            childAspectRatio: 1, // width = height
          ),
          itemCount: itemCount,
          itemBuilder: (context, index) {
            return Card(
              elevation: 5,
              color: Colors.blue[100 * ((index % 8) + 1)],
              child: Center(
                child: Text(
                  'Item $index',
                  style: const TextStyle(fontSize: 18),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
