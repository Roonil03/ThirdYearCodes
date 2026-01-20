import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(useMaterial3: true),
      home: const CategoryScreen(),
    );
  }
}

class CategoryScreen extends StatelessWidget {
  const CategoryScreen({super.key});

  // Sample categories - you can expand this list
  static const List<Map<String, dynamic>> categories = [
    {'name': 'Electronics', 'icon': Icons.devices_other},
    {'name': 'Fashion', 'icon': Icons.checkroom},
    {'name': 'Home & Kitchen', 'icon': Icons.kitchen},
    {'name': 'Books', 'icon': Icons.menu_book},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Categories'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: GridView.count(
          crossAxisCount: 2,              // 2 columns
          mainAxisSpacing: 16,            // vertical spacing between cards
          crossAxisSpacing: 16,           // horizontal spacing between cards
          childAspectRatio: 1.1,          // slightly taller than square
          children: categories.map((category) {
            return _CategoryCard(
              icon: category['icon'] as IconData,
              label: category['name'] as String,
              onTap: () {
                // You can navigate or show feedback here
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('${category['name']} selected')),
                );
              },
            );
          }).toList(),
        ),
      ),
    );
  }
}

class _CategoryCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  const _CategoryCard({
    required this.icon,
    required this.label,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      clipBehavior: Clip.hardEdge,
      child: InkWell(
        onTap: onTap,
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                size: 48,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(height: 12),
              Text(
                label,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w500,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}