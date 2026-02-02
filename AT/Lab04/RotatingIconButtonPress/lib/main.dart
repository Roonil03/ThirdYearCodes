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
      home: RotateIconPage(),
    );
  }
}

class RotateIconPage extends StatefulWidget {
  const RotateIconPage({super.key});

  @override
  State<RotateIconPage> createState() => _RotateIconPageState();
}

class _RotateIconPageState extends State<RotateIconPage>
    with SingleTickerProviderStateMixin {

  late AnimationController _controller;

  @override
  void initState() {
    super.initState();

    // AnimationController (0 → 1 = one full rotation)
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    );
  }

  void _rotateIcon() {
    // Start rotation from beginning
    _controller.forward(from: 0.0);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Rotating Icon'),
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            RotationTransition(
              turns: _controller,
              child: const Icon(
                Icons.refresh,
                size: 100,
                color: Colors.blue,
              ),
            ),
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: _rotateIcon,
              child: const Text('Rotate Icon'),
            ),
          ],
        ),
      ),
    );
  }
}
