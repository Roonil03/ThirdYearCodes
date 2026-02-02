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
      home: PulsingCircle(),
    );
  }
}

class PulsingCircle extends StatefulWidget {
  const PulsingCircle({super.key});

  @override
  State<PulsingCircle> createState() => _PulsingCircleState();
}

class _PulsingCircleState extends State<PulsingCircle>
    with SingleTickerProviderStateMixin {

  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();

    // AnimationController
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    );

    // Tween<double> for scaling
    _scaleAnimation = Tween<double>(
      begin: 0.8,
      end: 1.2,
    ).animate(
      CurvedAnimation(
        parent: _controller,
        curve: Curves.easeInOut,
      ),
    );

    // Loop animation (grow & shrink)
    _controller.repeat(reverse: true);
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
        title: const Text('Pulsing Circle'),
        centerTitle: true,
      ),
      body: Center(
        child: ScaleTransition(
          scale: _scaleAnimation,
          child: Container(
            width: 150,
            height: 150,
            decoration: const BoxDecoration(
              color: Colors.blue,
              shape: BoxShape.circle,
            ),
          ),
        ),
      ),
    );
  }
}
