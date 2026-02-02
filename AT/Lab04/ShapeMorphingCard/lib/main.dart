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
      home: ShapeMorphingCard(),
    );
  }
}

class ShapeMorphingCard extends StatefulWidget {
  const ShapeMorphingCard({super.key});

  @override
  State<ShapeMorphingCard> createState() => _ShapeMorphingCardState();
}

class _ShapeMorphingCardState extends State<ShapeMorphingCard> {
  bool _toggled = false;

  EdgeInsets _animatedMargin() {
    return _toggled
        ? const EdgeInsets.symmetric(horizontal: 40)
        : const EdgeInsets.symmetric(horizontal: 10);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Shape Morphing Card'),
      ),
      body: Center(
        child: AnimatedContainer(
          duration: const Duration(seconds: 1),
          curve: Curves.easeInOut,
          alignment:
          _toggled ? Alignment.centerRight : Alignment.centerLeft,
          margin: _animatedMargin(),
          child: GestureDetector(
            onTap: () {
              setState(() {
                _toggled = !_toggled;
              });
            },
            child: AnimatedContainer(
              duration: const Duration(seconds: 1),
              curve: Curves.easeInOut,
              width: 150,
              height: 100,
              decoration: BoxDecoration(
                color: Colors.blue,
                borderRadius: BorderRadius.circular(_toggled ? 30 : 0),
                boxShadow: _toggled
                    ? [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.3),
                    blurRadius: 10,
                    offset: const Offset(0, 5),
                  )
                ]
                    : [],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
