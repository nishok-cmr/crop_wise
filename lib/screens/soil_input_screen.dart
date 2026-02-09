
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/crop_provider.dart';
import 'results_screen.dart';

class SoilInputScreen extends StatefulWidget {
  const SoilInputScreen({super.key});

  @override
  State<SoilInputScreen> createState() => _SoilInputScreenState();
}

class _SoilInputScreenState extends State<SoilInputScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nController = TextEditingController(text: '40');
  final _pController = TextEditingController(text: '35');
  final _kController = TextEditingController(text: '30');
  final _phController = TextEditingController(text: '6.5');

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Soil Analysis'),
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildTextField(_nController, 'Nitrogen (N) - kg/ha'),
              const SizedBox(height: 16),
              _buildTextField(_pController, 'Phosphorus (P) - kg/ha'),
              const SizedBox(height: 16),
              _buildTextField(_kController, 'Potassium (K) - kg/ha'),
              const SizedBox(height: 16),
              _buildTextField(_phController, 'pH Level (4-9)'),
              const SizedBox(height: 24),
              _buildSoilTypeSelector(context),
              const SizedBox(height: 24),
              _buildAnalyzeButton(context),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(
      TextEditingController controller, String label) {
    return TextFormField(
      controller: controller,
      decoration: InputDecoration(
        labelText: label,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
        ),
      ),
      keyboardType: TextInputType.number,
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Please enter a value';
        }
        if (double.tryParse(value) == null) {
          return 'Please enter a valid number';
        }
        return null;
      },
    );
  }

  Widget _buildSoilTypeSelector(BuildContext context) {
    final cropProvider = Provider.of<CropProvider>(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Soil Type', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 10),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: ['clay', 'sandy', 'loamy'].map((type) {
            return ChoiceChip(
              label: Text(type.capitalize()),
              selected: cropProvider.selectedSoilType == type,
              onSelected: (selected) {
                if (selected) {
                  cropProvider.selectSoilType(type);
                }
              },
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildAnalyzeButton(BuildContext context) {
    return ElevatedButton(
      onPressed: () {
        if (_formKey.currentState!.validate()) {
          final n = double.parse(_nController.text);
          final p = double.parse(_pController.text);
          final k = double.parse(_kController.text);
          final ph = double.parse(_phController.text);

          Provider.of<CropProvider>(context, listen: false)
              .analyzeAndRecommend(n, p, k, ph);

          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const ResultsScreen()),
          );
        }
      },
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 16.0),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(15),
        ),
      ),
      child: const Text('Get Crop Recommendations'),
    );
  }
}
