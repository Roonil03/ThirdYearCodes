import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData.dark(),
      home: const FeedbackFormPage(),
    );
  }
}

class FeedbackFormPage extends StatefulWidget {
  const FeedbackFormPage({super.key});

  @override
  State<FeedbackFormPage> createState() => _FeedbackFormPageState();
}

class _FeedbackFormPageState extends State<FeedbackFormPage> {
  final TextEditingController _movieController = TextEditingController();
  int _rating = 3;
  bool _recommend = false;

  bool get _isFormValid => _movieController.text.trim().isNotEmpty;

  @override
  void initState() {
    super.initState();
    // Enable/disable recommend switch based on movie name
    _movieController.addListener(() {
      setState(() {}); // rebuild to update switch enabled state
    });
  }

  @override
  void dispose() {
    _movieController.dispose();
    super.dispose();
  }

  void _submit() {
    if (!_isFormValid) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter a movie name')),
      );
      return;
    }

    // Print to terminal/console
    print('Movie: ${_movieController.text.trim()}, '
        'Rating: $_rating stars, '
        'Recommend: ${_recommend ? "Yes" : "No"}');

    // Show feedback to user
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          'Submitted: ${_movieController.text.trim()} - $_rating ★ - '
              '${_recommend ? "Recommended" : "Not recommended"}',
        ),
      ),
    );

    // Reset form
    setState(() {
      _movieController.clear();
      _rating = 3;
      _recommend = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Movie Feedback')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: _movieController,
              decoration: const InputDecoration(
                labelText: 'Movie Name',
                border: OutlineInputBorder(),
              ),
              textCapitalization: TextCapitalization.words,
            ),
            const SizedBox(height: 24),

            const Text('Rating:', style: TextStyle(fontSize: 16)),
            Column(
              children: List.generate(5, (index) {
                int value = index + 1;
                return RadioListTile<int>(
                  dense: true,
                  contentPadding: EdgeInsets.zero,
                  title: Text('$value Star${value > 1 ? "s" : ""}'),
                  value: value,
                  groupValue: _rating,
                  onChanged: (val) => setState(() => _rating = val!),
                );
              }),
            ),

            const SizedBox(height: 16),

            SwitchListTile(
              title: const Text('Recommend to others?'),
              value: _recommend,
              onChanged: _isFormValid
                  ? (val) => setState(() => _recommend = val)
                  : null, // null = disabled
              activeColor: Colors.green,
            ),

            const SizedBox(height: 32),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _submit,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: const Text('Submit', style: TextStyle(fontSize: 16)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}