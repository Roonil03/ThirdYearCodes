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
      home: FaqDemo(),
    );
  }
}

class FaqDemo extends StatefulWidget {
  const FaqDemo({super.key});

  @override
  State<FaqDemo> createState() => _FaqDemoState();
}

class _FaqDemoState extends State<FaqDemo>
    with SingleTickerProviderStateMixin {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Expandable FAQ Tile'),
      ),
      body: Center(
        child: GestureDetector(
          onTap: () {
            setState(() {
              _expanded = !_expanded;
            });
          },
          child: _buildAnimatedFaq(),
        ),
      ),
    );
  }

  /// BONUS: Wraps crossfade with AnimatedSize for smoother height change.
  /// You can comment out AnimatedSize and return AnimatedCrossFade directly.
  Widget _buildAnimatedFaq() {
    return AnimatedSize(
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
      child: AnimatedCrossFade(
        duration: const Duration(milliseconds: 300),
        crossFadeState: _expanded
            ? CrossFadeState.showSecond
            : CrossFadeState.showFirst,
        firstChild: _buildQuestionOnly(),
        secondChild: _buildQuestionWithAnswer(),
      ),
    );
  }

  Widget _buildQuestionOnly() {
    return _cardWrapper(
      const Text(
        'What is Flutter?',
        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _buildQuestionWithAnswer() {
    return _cardWrapper(
      Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: const [
          Text(
            'What is Flutter?',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          Text(
            'Flutter is an open-source UI framework by Google '
                'used to build natively compiled applications for '
                'mobile, web, and desktop from a single codebase.',
          ),
        ],
      ),
    );
  }

  Widget _cardWrapper(Widget child) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: child,
      ),
    );
  }
}
