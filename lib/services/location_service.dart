
import 'dart:convert';
import 'package:http/http.dart' as http;

class LocationService {
  Future<Map<String, dynamic>> getLocation() async {
    try {
      final response = await http.get(Uri.parse('https://ipapi.co/json/'));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {
          'lat': data['latitude'],
          'lon': data['longitude'],
          'city': '${data['city']}, ${data['region']}',
        };
      } else {
        return _defaultLocation();
      }
    } catch (e) {
      return _defaultLocation();
    }
  }

  Map<String, dynamic> _defaultLocation() {
    return {
      'lat': 13.0827,
      'lon': 80.2707,
      'city': 'Chennai, Tamil Nadu',
    };
  }
}
