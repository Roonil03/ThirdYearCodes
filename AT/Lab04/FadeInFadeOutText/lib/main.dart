import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: FadeTextDemo(),
    );
  }
}

class FadeTextDemo extends StatefulWidget {
  const FadeTextDemo({super.key});

  @override
  State<FadeTextDemo> createState() => _FadeTextDemoState();
}

class _FadeTextDemoState extends State<FadeTextDemo> {
  bool _visible = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Fade In / Fade Out Text'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AnimatedOpacity(
              opacity: _visible ? 1.0 : 0.0,
              duration: const Duration(milliseconds: 800),
              child: const Text(
                'Welcome to Flutter Animations',
                style: TextStyle(fontSize: 22),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  _visible = !_visible;
                });
              },
              child: const Text('Toggle Fade'),
            ),
          ],
        ),
      ),
    );
  }
}
