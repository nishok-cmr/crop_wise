
import 'package:flutter/material.dart';
import '../models/crop_model.dart';

class CropCard extends StatelessWidget {
  final Map<String, dynamic> recommendation;

  const CropCard({super.key, required this.recommendation});

  @override
  Widget build(BuildContext context) {
    final Crop crop = recommendation['crop'];
    final String suitability = recommendation['suitability'];
    final Color suitabilityColor = _getSuitabilityColor(suitability);

    return Card(
      elevation: 4,
      margin: const EdgeInsets.symmetric(vertical: 8.0),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  crop.name,
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                Chip(
                  label: Text(suitability),
                  backgroundColor: suitabilityColor,
                  labelStyle: const TextStyle(color: Colors.white),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              'Season: ${crop.season} | Duration: ${crop.duration}',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const Divider(height: 20),
            _buildRequirementRow(
                'N-P-K (kg/ha)', _formatNPK(crop.requirements)),
            _buildRequirementRow('pH', _formatRange(crop.requirements.phRange)),
            _buildRequirementRow(
                'Temperature', '${_formatRange(crop.requirements.tempRange)}°C'),
            _buildRequirementRow(
                'Humidity', '${_formatRange(crop.requirements.humidityRange)}%'),
            _buildRequirementRow(
                'Rainfall', '${_formatRange(crop.requirements.rainfallRange)}mm'),
            _buildRequirementRow('Soil Types', crop.requirements.soilTypes.join(', ')),
          ],
        ),
      ),
    );
  }

  Color _getSuitabilityColor(String suitability) {
    switch (suitability) {
      case 'Highly Suitable':
        return Colors.green.shade600;
      case 'Suitable':
        return Colors.orange.shade600;
      case 'Moderately Suitable':
        return Colors.amber.shade800;
      default:
        return Colors.grey;
    }
  }

  String _formatNPK(CropRequirements req) {
    return '${_formatRange(req.nRange)} - ${_formatRange(req.pRange)} - ${_formatRange(req.kRange)}';
  }

  String _formatRange(Range range) {
    return '${range.min.toInt()}-${range.max.toInt()}';
  }

  Widget _buildRequirementRow(String title, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [Text(title), Text(value)],
      ),
    );
  }
}
