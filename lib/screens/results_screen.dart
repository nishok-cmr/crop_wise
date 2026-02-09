
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/crop_provider.dart';
import '../widgets/crop_card.dart';

class ResultsScreen extends StatelessWidget {
  const ResultsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final cropProvider = Provider.of<CropProvider>(context);
    final recommendations = cropProvider.recommendations;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Crop Recommendations'),
        actions: [
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              // TODO: Implement sharing
            },
          ),
        ],
      ),
      body: recommendations.isEmpty
          ? const Center(
              child: Text('No suitable crops found for the given conditions.'),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: recommendations.length,
              itemBuilder: (context, index) {
                final recommendation = recommendations[index];
                return CropCard(recommendation: recommendation);
              },
            ),
    );
  }
}
