
class Crop {
  final String name;
  final CropRequirements requirements;
  final String season;
  final String duration;

  Crop({
    required this.name,
    required this.requirements,
    required this.season,
    required this.duration,
  });
}

class CropRequirements {
  final Range nRange;
  final Range pRange;
  final Range kRange;
  final Range phRange;
  final Range tempRange;
  final Range humidityRange;
  final Range rainfallRange;
  final List<String> soilTypes;

  CropRequirements({
    required this.nRange,
    required this.pRange,
    required this.kRange,
    required this.phRange,
    required this.tempRange,
    required this.humidityRange,
    required this.rainfallRange,
    required this.soilTypes,
  });
}

class Range {
  final double min;
  final double max;

  Range(this.min, this.max);
}
