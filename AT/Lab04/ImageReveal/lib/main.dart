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
      home: ImageRevealDemo(),
    );
  }
}

class ImageRevealDemo extends StatefulWidget {
  const ImageRevealDemo({super.key});

  @override
  State<ImageRevealDemo> createState() => _ImageRevealDemoState();
}

class _ImageRevealDemoState extends State<ImageRevealDemo> {
  bool _showImage = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Image Reveal'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Stack(
              alignment: Alignment.center,
              children: [
                AnimatedOpacity(
                  opacity: _showImage ? 1.0 : 0.0,
                  duration: const Duration(milliseconds: 800),
                  child: Image.network(
                    'https://i.etsystatic.com/27743352/r/il/4917d3/4031314436/il_570xN.4031314436_1xfr.jpg',
                    width: 200,
                    height: 200,
                    fit: BoxFit.cover,
                  ),
                ),
                AnimatedOpacity(
                  opacity: _showImage ? 0.0 : 1.0,
                  duration: const Duration(milliseconds: 800),
                  child: const Icon(
                    Icons.image,
                    size: 100,
                    color: Colors.grey,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  _showImage = !_showImage;
                });
              },
              child: const Text('Reveal Image'),
            ),
          ],
        ),
      ),
    );
  }
}
