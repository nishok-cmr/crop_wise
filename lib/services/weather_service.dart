
import 'dart:convert';
import 'package:http/http.dart' as http;

class WeatherService {
  Future<Map<String, int>> getWeather(double lat, double lon) async {
    try {
      final url = 'https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lon&current=temperature_2m,relative_humidity_2m,rain&timezone=auto';
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final current = data['current'];
        return {
          'temperature': current['temperature_2m'].round(),
          'humidity': current['relative_humidity_2m'].round(),
          'rainfall': (current['rain'] * 24 * 30).round(), // Approx. monthly
        };
      } else {
        return _defaultWeather();
      }
    } catch (e) {
      return _defaultWeather();
    }
  }

  Map<String, int> _defaultWeather() {
    return {
      'temperature': 28,
      'humidity': 65,
      'rainfall': 120,
    };
  }
}
