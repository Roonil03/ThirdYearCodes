import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.network(
                'https://juststickers.in/wp-content/uploads/2019/01/flutter-264x264.png',
                height: 100,
              ),
              const SizedBox(height: 16),
              const Text(
                "Welcome to Flutter Lab",
                style: TextStyle(fontSize: 20),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () => print("Elevated Button Clicked"),
                child: const Text("Submit"),
              ),
              OutlinedButton(
                onPressed: () => print("Outlined Button Clicked"),
                child: const Text("Secondary Action"),
              ),
              TextButton(
                onPressed: () => print("Text Button Clicked"),
                child: const Text("Text Action"),
              ),
              IconButton(
                onPressed: () => print("Icon Button Clicked"),
                icon: const Icon(Icons.thumb_up),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
