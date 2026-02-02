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
      home: AnimatedThemeSwitcher(),
    );
  }
}

class AnimatedThemeSwitcher extends StatefulWidget {
  const AnimatedThemeSwitcher({super.key});

  @override
  State<AnimatedThemeSwitcher> createState() => _AnimatedThemeSwitcherState();
}

class _AnimatedThemeSwitcherState extends State<AnimatedThemeSwitcher>
    with SingleTickerProviderStateMixin {

  bool _isDark = false;

  late AnimationController _rotationController;

  @override
  void initState() {
    super.initState();

    // Explicit animation for icon rotation
    _rotationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 500),
    );
  }

  void _toggleTheme() {
    setState(() {
      _isDark = !_isDark;
    });

    // Rotate icon on toggle
    _rotationController.forward(from: 0.0);
  }

  @override
  void dispose() {
    _rotationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AnimatedContainer(
        duration: const Duration(milliseconds: 600),
        curve: Curves.easeInOut,
        color: _isDark ? Colors.black : Colors.white,
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              RotationTransition(
                turns: _rotationController,
                child: AnimatedOpacity(
                  duration: const Duration(milliseconds: 400),
                  opacity: 1.0,
                  child: Icon(
                    _isDark ? Icons.dark_mode : Icons.light_mode,
                    size: 100,
                    color: _isDark ? Colors.white : Colors.black,
                  ),
                ),
              ),
              const SizedBox(height: 30),
              ElevatedButton(
                onPressed: _toggleTheme,
                child: Text(
                  _isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode',
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
