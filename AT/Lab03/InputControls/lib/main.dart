import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: PreferencePage());
  }
}

class PreferencePage extends StatefulWidget {
  const PreferencePage({super.key});

  @override
  State<PreferencePage> createState() => _PreferencePageState();
}

class _PreferencePageState extends State<PreferencePage> {
  bool _isAccepted = false;
  int _selectedGender = 1;
  double _genderValue = 0.0;
  String get genderLabel {
    if (_genderValue <= 0.2) return 'Male';
    if (_genderValue <= 0.4) return 'Mostly Male';
    if (_genderValue <= 0.6) return 'Non-binary';
    if (_genderValue <= 0.8) return 'Mostly Female';
    return 'Female';
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Preferences')),
      body: Column(
        children: [
          CheckboxListTile(
            title: const Text('I accept terms'),
            value: _isAccepted,
            onChanged: (val) => setState(() => _isAccepted = val!),
          ),
          const SizedBox(height: 20),
          Text(genderLabel),
          Slider(
            value: _genderValue,
            min: 0,
            max: 1,
            divisions: 10,
            label: genderLabel,
            onChanged: (val) => setState(() => _genderValue = val),
          ),
          RadioListTile(
            title: const Text('Male'),
            value: 1,
            groupValue: _selectedGender,
            onChanged: (val) =>
                setState(() => _selectedGender = val as int),
          ),
          RadioListTile(
            title: const Text('Female'),
            value: 2,
            groupValue: _selectedGender,
            onChanged: (val) =>
                setState(() => _selectedGender = val as int),
          ),
        ],
      ),
    );
  }
}
