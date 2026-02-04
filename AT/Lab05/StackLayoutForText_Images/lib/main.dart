import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Stack Example'),
        ),
        body: Center(
          child: Stack(
            alignment: Alignment.center,
            children: [
              Image.network(
                // 'https://picsum.photos/300/200',
                'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSLdsC9B3CKTDk9E5LiKMMlqGqk8J1YOU71g&s',
                width: 300,
                height: 200,
                fit: BoxFit.cover,
              ),

              // Text over image
              Container(
                padding: const EdgeInsets.all(8),
                color: Colors.black54,
                child: const Text(
                  'Haru Urara!',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
