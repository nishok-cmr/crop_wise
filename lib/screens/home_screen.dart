
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/crop_provider.dart';
import 'soil_input_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final cropProvider = Provider.of<CropProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('CropWise'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              cropProvider.refreshData();
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildLocationCard(context, cropProvider),
            const SizedBox(height: 20),
            _buildWeatherCard(context, cropProvider),
            const SizedBox(height: 20),
            _buildAnalysisButton(context),
            const SizedBox(height: 20),
            _buildLastAnalysisCard(context, cropProvider),
          ],
        ),
      ),
    );
  }

  Widget _buildLocationCard(
      BuildContext context, CropProvider cropProvider) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Current Location',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                const Icon(Icons.location_on, color: Colors.blueAccent),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    cropProvider.currentLocation['city'] ?? 'Detecting...',
                    style: Theme.of(context).textTheme.bodyLarge,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWeatherCard(BuildContext context, CropProvider cropProvider) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Weather Conditions',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildWeatherItem(
                    context,
                    'Temperature',
                    '${cropProvider.weatherData['temperature'] ?? 'N/A'}°C',
                    Icons.thermostat),
                _buildWeatherItem(
                    context,
                    'Humidity',
                    '${cropProvider.weatherData['humidity'] ?? 'N/A'}%',
                    Icons.water_drop),
                _buildWeatherItem(
                    context,
                    'Rainfall',
                    '${cropProvider.weatherData['rainfall'] ?? 'N/A'}mm',
                    Icons.umbrella),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWeatherItem(
      BuildContext context, String title, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: Colors.blueAccent, size: 30),
        const SizedBox(height: 5),
        Text(title, style: Theme.of(context).textTheme.bodyMedium),
        const SizedBox(height: 5),
        Text(value, style: Theme.of(context).textTheme.titleMedium),
      ],
    );
  }

  Widget _buildAnalysisButton(BuildContext context) {
    return ElevatedButton(
      onPressed: () {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const SoilInputScreen()),
        );
      },
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 16.0),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(15),
        ),
      ),
      child: const Center(
        child: Text(
          'Analyze Soil & Get Recommendations',
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  Widget _buildLastAnalysisCard(
      BuildContext context, CropProvider cropProvider) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Recent Analysis',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 10),
            Text(
              cropProvider.analysisText,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }
}
