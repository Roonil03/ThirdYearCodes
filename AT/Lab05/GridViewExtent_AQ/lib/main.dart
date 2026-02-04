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
          title: const Text('GridView.extent Example'),
        ),
        body: GridView.extent(
          maxCrossAxisExtent: 150, // maximum width of each cell
          crossAxisSpacing: 10,
          mainAxisSpacing: 10,
          padding: const EdgeInsets.all(10),
          children: List.generate(8, (index) {
            return Container(
              color: Colors.teal[100 * ((index % 8) + 1)],
              child: Center(
                child: Text(
                  'Item $index',
                  style: const TextStyle(fontSize: 16, color: Colors.white),
                ),
              ),
            );
          }),
        ),
      ),
    );
  }
}
