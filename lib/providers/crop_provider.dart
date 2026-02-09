
import 'package:flutter/material.dart';
import '../models/crop_model.dart';
import '../services/location_service.dart';
import '../services/weather_service.dart';

class CropProvider with ChangeNotifier {
  final LocationService _locationService = LocationService();
  final WeatherService _weatherService = WeatherService();

  Map<String, dynamic> _currentLocation = {};
  Map<String, int> _weatherData = {};
  List<Map<String, dynamic>> _recommendations = [];
  String _selectedSoilType = 'loamy';
  String _analysisText = 'No analysis yet';

  Map<String, dynamic> get currentLocation => _currentLocation;
  Map<String, int> get weatherData => _weatherData;
  List<Map<String, dynamic>> get recommendations => _recommendations;
  String get selectedSoilType => _selectedSoilType;
  String get analysisText => _analysisText;

  final Map<String, Crop> _cropDatabase = {
    'rice': Crop(
        name: 'Rice',
        requirements: CropRequirements(
          nRange: Range(80, 120),
          pRange: Range(40, 60),
          kRange: Range(40, 60),
          phRange: Range(5.5, 7.0),
          tempRange: Range(20, 35),
          humidityRange: Range(60, 80),
          rainfallRange: Range(150, 300),
          soilTypes: ['clay', 'loamy'],
        ),
        season: 'Kharif/Rabi',
        duration: '120-150 days'),
    'wheat': Crop(
        name: 'Wheat',
        requirements: CropRequirements(
          nRange: Range(60, 100),
          pRange: Range(30, 50),
          kRange: Range(30, 50),
          phRange: Range(6.0, 7.5),
          tempRange: Range(15, 25),
          humidityRange: Range(50, 70),
          rainfallRange: Range(50, 100),
          soilTypes: ['loamy', 'clay'],
        ),
        season: 'Rabi',
        duration: '110-130 days'),
    'maize': Crop(
        name: 'Maize (Corn)',
        requirements: CropRequirements(
          nRange: Range(80, 120),
          pRange: Range(40, 60),
          kRange: Range(40, 60),
          phRange: Range(5.8, 7.0),
          tempRange: Range(20, 30),
          humidityRange: Range(60, 75),
          rainfallRange: Range(60, 110),
          soilTypes: ['loamy', 'sandy'],
        ),
        season: 'Kharif',
        duration: '90-120 days'),
    'cotton': Crop(
        name: 'Cotton',
        requirements: CropRequirements(
          nRange: Range(60, 90),
          pRange: Range(30, 50),
          kRange: Range(30, 50),
          phRange: Range(6.0, 7.5),
          tempRange: Range(21, 30),
          humidityRange: Range(50, 70),
          rainfallRange: Range(60, 120),
          soilTypes: ['loamy', 'clay'],
        ),
        season: 'Kharif',
        duration: '180-195 days'),
    'sugarcane': Crop(
        name: 'Sugarcane',
        requirements: CropRequirements(
          nRange: Range(100, 150),
          pRange: Range(50, 80),
          kRange: Range(60, 100),
          phRange: Range(6.0, 7.5),
          tempRange: Range(20, 35),
          humidityRange: Range(65, 85),
          rainfallRange: Range(150, 250),
          soilTypes: ['loamy', 'clay'],
        ),
        season: 'Year-round',
        duration: '10-12 months'),
    'groundnut': Crop(
        name: 'Groundnut',
        requirements: CropRequirements(
          nRange: Range(20, 40),
          pRange: Range(40, 60),
          kRange: Range(50, 70),
          phRange: Range(6.0, 7.0),
          tempRange: Range(22, 30),
          humidityRange: Range(55, 75),
          rainfallRange: Range(50, 100),
          soilTypes: ['sandy', 'loamy'],
        ),
        season: 'Kharif/Summer',
        duration: '100-130 days'),
    'pulses': Crop(
        name: 'Pulses (Lentils)',
        requirements: CropRequirements(
          nRange: Range(15, 30),
          pRange: Range(30, 50),
          kRange: Range(30, 50),
          phRange: Range(6.0, 7.5),
          tempRange: Range(18, 28),
          humidityRange: Range(50, 70),
          rainfallRange: Range(40, 80),
          soilTypes: ['loamy', 'clay'],
        ),
        season: 'Rabi',
        duration: '90-110 days'),
    'vegetables': Crop(
        name: 'Mixed Vegetables',
        requirements: CropRequirements(
          nRange: Range(40, 80),
          pRange: Range(30, 60),
          kRange: Range(40, 70),
          phRange: Range(6.0, 7.0),
          tempRange: Range(15, 30),
          humidityRange: Range(60, 80),
          rainfallRange: Range(60, 150),
          soilTypes: ['loamy', 'sandy'],
        ),
        season: 'Year-round',
        duration: '60-120 days'),
  };

  Future<void> init() async {
    await refreshData();
  }

  Future<void> refreshData() async {
    _currentLocation = await _locationService.getLocation();
    _weatherData = await _weatherService.getWeather(
        _currentLocation['lat'], _currentLocation['lon']);
    notifyListeners();
  }

  void selectSoilType(String soilType) {
    _selectedSoilType = soilType;
    notifyListeners();
  }

  void analyzeAndRecommend(
      double n, double p, double k, double ph) {
    _recommendations =
        _calculateRecommendations(n, p, k, ph);
    _analysisText =
        'Last analysis: ${DateTime.now().toString().substring(0, 16)}\nN: $n, P: $p, K: $k, pH: $ph\nSoil: ${_selectedSoilType.capitalize()}';
    notifyListeners();
  }

  List<Map<String, dynamic>> _calculateRecommendations(
      double n, double p, double k, double ph) {
    List<Map<String, dynamic>> recommendations = [];
    final temp = _weatherData['temperature']?.toDouble() ?? 28.0;
    final humidity = _weatherData['humidity']?.toDouble() ?? 65.0;
    final rainfall = _weatherData['rainfall']?.toDouble() ?? 120.0;

    _cropDatabase.forEach((key, crop) {
      double score = 0;
      const maxScore = 7.0;

      if (n >= crop.requirements.nRange.min &&
          n <= crop.requirements.nRange.max) score++;
      if (p >= crop.requirements.pRange.min &&
          p <= crop.requirements.pRange.max) score++;
      if (k >= crop.requirements.kRange.min &&
          k <= crop.requirements.kRange.max) score++;
      if (ph >= crop.requirements.phRange.min &&
          ph <= crop.requirements.phRange.max) score++;
      if (temp >= crop.requirements.tempRange.min &&
          temp <= crop.requirements.tempRange.max) score++;
      if (humidity >= crop.requirements.humidityRange.min &&
          humidity <= crop.requirements.humidityRange.max) score++;
      if (rainfall >= crop.requirements.rainfallRange.min &&
          rainfall <= crop.requirements.rainfallRange.max) score++;

      if (!crop.requirements.soilTypes.contains(_selectedSoilType)) {
        score--;
      }

      final suitabilityPercentage = (score / maxScore) * 100;

      if (suitabilityPercentage >= 50) {
        String suitability;
        if (suitabilityPercentage >= 80) {
          suitability = 'Highly Suitable';
        } else if (suitabilityPercentage >= 65) {
          suitability = 'Suitable';
        } else {
          suitability = 'Moderately Suitable';
        }
        recommendations.add({
          'crop': crop,
          'score': suitabilityPercentage,
          'suitability': suitability,
        });
      }
    });

    recommendations.sort((a, b) => b['score'].compareTo(a['score']));
    return recommendations.take(6).toList();
  }
}

extension StringExtension on String {
  String capitalize() {
    return '${this[0].toUpperCase()}${substring(1)}';
  }
}
