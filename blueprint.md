
# CropWise Application Blueprint

## Overview

CropWise is a Flutter application designed to provide intelligent crop recommendations to farmers based on real-time environmental data and soil conditions. The app fetches the user's location, retrieves current weather data, and allows users to input soil nutrient information (Nitrogen, Phosphorus, Potassium, and pH levels) to generate a list of suitable crops.

## Style, Design, and Features

### Architecture

*   **Provider State Management**: The application uses the `provider` package for state management, centralizing the application's state in the `CropProvider` class.
*   **Service-Oriented Architecture**: Services like `LocationService` and `WeatherService` are used to fetch data from external APIs, separating data fetching logic from the UI.
*   **Model-View-Provider (MVP)**: The architecture resembles an MVP pattern, with:
    *   **Models**: `Crop` and `CropRequirements` define the data structure.
    *   **Views**: The UI is built with Flutter widgets, organized into different screens (`SplashScreen`, `HomeScreen`, `SoilInputScreen`, `ResultsScreen`).
    *   **Provider**: `CropProvider` acts as the presenter, handling business logic and managing the state.

### UI and Design

*   **Theme**: The application uses a custom theme defined in `main.dart` with `google_fonts` for typography (`Lato` and `Merriweather`). The color scheme is based on `Colors.blue`.
*   **Splash Screen**: A simple splash screen is displayed while the initial data (location and weather) is being fetched.
*   **Home Screen**:
    *   Displays the user's current location and weather information in cards.
    *   Provides a button to navigate to the soil analysis screen.
    *   Shows the details of the last analysis performed.
*   **Soil Input Screen**:
    *   A form for users to input soil nutrient values (N, P, K, pH).
    *   A `ChoiceChip` for selecting the soil type.
*   **Results Screen**:
    *   Displays a list of recommended crops in `CropCard` widgets.
    *   Each card shows the crop's name, suitability, and detailed requirements.
    *   The suitability is color-coded for easy identification (Green for 'Highly Suitable', Orange for 'Suitable', Amber for 'Moderately Suitable').

### Features

*   **Automatic Location Detection**: Fetches the user's current location to provide localized weather data.
*   **Real-time Weather Data**: Retrieves current temperature, humidity, and rainfall from the Open-Meteo API.
*   **Soil Analysis**: Allows users to input soil nutrient data.
*   **Crop Recommendations**:
    *   A sophisticated scoring algorithm in `CropProvider` calculates the suitability of different crops based on soil and weather conditions.
    *   The recommendations are sorted by suitability score.
*   **Offline Data**: The app has default values for weather and location, allowing it to function even if the APIs are unreachable.

## Current Plan

The current plan was to build the CropWise application from scratch. This involved:

1.  **Project Setup**:
    *   Creating the folder structure (`models`, `services`, `providers`, `screens`, `widgets`).
    *   Adding necessary dependencies (`provider`, `google_fonts`, `http`).
2.  **Model Definition**:
    *   Creating the `Crop` and `CropRequirements` models in `lib/models/crop_model.dart`.
3.  **Service Implementation**:
    *   Implementing `LocationService` to fetch the user's location.
    *   Implementing `WeatherService` to fetch weather data.
4.  **State Management**:
    *   Creating `CropProvider` to manage the application's state, including location, weather, soil data, and crop recommendations.
    *   Implementing the crop recommendation logic.
5.  **UI Development**:
    *   Building the splash screen to handle initial data loading.
    *   Designing the home screen to display location and weather.
    *   Creating the soil input form.
    *   Developing the results screen to display the crop recommendations.
    *   Creating a reusable `CropCard` widget.
6.  **Theming**:
    *   Applying a consistent theme using `ThemeData` and `google_fonts`.
7.  **Finalization**:
    *   Adding a `blueprint.md` file to document the project.
    *   Formatting the code.
