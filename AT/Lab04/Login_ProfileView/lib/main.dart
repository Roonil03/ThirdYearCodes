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
      home: LoginProfileDemo(),
    );
  }
}

class LoginProfileDemo extends StatefulWidget {
  const LoginProfileDemo({super.key});

  @override
  State<LoginProfileDemo> createState() => _LoginProfileDemoState();
}

class _LoginProfileDemoState extends State<LoginProfileDemo> {
  bool _loggedIn = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login ↔ Profile View'),
      ),
      body: Center(
        child: AnimatedCrossFade(
          duration: const Duration(seconds: 1),
          crossFadeState: _loggedIn
              ? CrossFadeState.showSecond
              : CrossFadeState.showFirst,
          firstChild: ElevatedButton(
            onPressed: () {
              setState(() {
                _loggedIn = true;
              });
            },
            child: const Text('Login'),
          ),
          secondChild: _buildProfileCard(),
        ),
      ),
    );
  }

  Widget _buildProfileCard() {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const CircleAvatar(
              radius: 30,
              child: Icon(Icons.person),
            ),
            const SizedBox(height: 10),
            const Text(
              'John Doe',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  _loggedIn = false;
                });
              },
              child: const Text('Logout'),
            ),
          ],
        ),
      ),
    );
  }
}
