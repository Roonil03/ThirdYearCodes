import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: InputScreen(),
    );
  }
}
//Input Screen
class InputScreen extends StatefulWidget {
  const InputScreen({super.key});

  @override
  State<InputScreen> createState() => _InputScreenState();
}

class _InputScreenState extends State<InputScreen> {
  final TextEditingController nameController = TextEditingController();
  final TextEditingController designationController = TextEditingController();
  final TextEditingController companyController = TextEditingController();
  final TextEditingController experienceController = TextEditingController();

  void submitDetails() {
    if (nameController.text.isEmpty ||
        designationController.text.isEmpty ||
        companyController.text.isEmpty ||
        experienceController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please fill all fields')),
      );
      return;
    }

    List<Map<String, String>> userDetails = [
      {'title': 'Name', 'value': nameController.text},
      {'title': 'Designation', 'value': designationController.text},
      {'title': 'Company', 'value': companyController.text},
      {'title': 'Experience', 'value': experienceController.text},
    ];

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => DisplayScreen(details: userDetails),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Enter User Details'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: nameController,
              decoration: const InputDecoration(
                labelText: 'Name',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: designationController,
              decoration: const InputDecoration(
                labelText: 'Designation',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: companyController,
              decoration: const InputDecoration(
                labelText: 'Company',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: experienceController,
              decoration: const InputDecoration(
                labelText: 'Experience',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: submitDetails,
              child: const Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}

// Display Screen
class DisplayScreen extends StatelessWidget {
  final List<Map<String, String>> details;

  const DisplayScreen({super.key, required this.details});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('User Profile'),
      ),
      body: ListView.builder(
        itemCount: details.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(details[index]['title']!),
            subtitle: Text(details[index]['value']!),
            trailing: const Icon(Icons.arrow_forward_ios),
            onTap: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                    '${details[index]['title']}: ${details[index]['value']}',
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}