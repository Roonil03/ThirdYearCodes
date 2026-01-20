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
      home: const ProfilePage(),
    );
  }
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Stack(
            clipBehavior: Clip.none,
            children: [
              Container(
                height: 200,
                width: double.infinity,
                color: Colors.grey[800],
              ),
              const Positioned(
                bottom: -40,
                left: 20,
                child: CircleAvatar(
                  radius: 40,
                  backgroundImage: AssetImage('profile.png'),
                ),
              ),
            ],
          ),
          const SizedBox(height: 60),
          const ListTile(
            leading: Icon(Icons.person),
            title: Text('John Doe'),
            subtitle: Text('Software Engineer'),
          ),
          const ListTile(
            leading: Icon(Icons.work),
            title: Text('Company'),
            subtitle: Text('Tech Corp'),
          ),
          const ListTile(
            leading: Icon(Icons.email),
            title: Text('Email'),
            subtitle: Text('john.doe@example.com'),
          ),
        ],
      ),
    );
  }
}
