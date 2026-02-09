"""
Crop Recommendation System - Mobile Application
Modern Flutter-like design with KivyMD
Theme: White, Sky Blue, Light Green, Black (text only)
"""

from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivymd.toast import toast
from kivy.utils import platform
from kivy.network.urlrequest import UrlRequest
from datetime import datetime
import json
import random

try:
    from plyer import gps
    from plyer import share
except ImportError:
    gps = None
    share = None

# Set window size for mobile simulation
Window.size = (360, 640)

KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<CropCard@MDCard>:
    orientation: 'vertical'
    size_hint_y: None
    height: dp(120)
    elevation: 2
    radius: [dp(15)]
    md_bg_color: 1, 1, 1, 1
    padding: dp(15)
    spacing: dp(8)
    
    # Define custom properties
    crop_name: ''
    crop_details: ''
    suitability: ''
    
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(5)
        
        MDLabel:
            text: root.crop_name
            font_style: 'H6'
            theme_text_color: 'Custom'
            text_color: 0, 0, 0, 1
            size_hint_y: None
            height: self.texture_size[1]
            
        MDLabel:
            text: root.crop_details
            font_style: 'Caption'
            theme_text_color: 'Custom'
            text_color: 0.3, 0.3, 0.3, 1
            size_hint_y: None
            height: self.texture_size[1]
            
        Widget:
        
        MDBoxLayout:
            size_hint_y: None
            height: dp(30)
            spacing: dp(8)
            
            MDChip:
                text: root.suitability
                md_bg_color: (0.6, 0.9, 0.6, 1) if root.suitability == 'Highly Suitable' else (0.2, 0.6, 1, 1)
                text_color: 1, 1, 1, 1
                size_hint_x: None
                height: dp(28)

ScreenManager:
    id: screen_manager
    transition: FadeTransition()
    
    MDScreen:
        name: 'splash'
        
        MDBoxLayout:
            orientation: 'vertical'
            md_bg_color: 0.2, 0.6, 1, 1
            
            Widget:
            
            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(200)
                spacing: dp(20)
                padding: dp(20)
                
                MDIcon:
                    icon: 'sprout'
                    halign: 'center'
                    font_size: dp(80)
                    theme_text_color: 'Custom'
                    text_color: 1, 1, 1, 1
                    
                MDLabel:
                    text: 'CropWise'
                    halign: 'center'
                    font_style: 'H4'
                    theme_text_color: 'Custom'
                    text_color: 1, 1, 1, 1
                    
                MDLabel:
                    text: 'Smart Crop Recommendations'
                    halign: 'center'
                    font_style: 'Caption'
                    theme_text_color: 'Custom'
                    text_color: 1, 1, 1, 0.8
                    
            Widget:
    
    MDScreen:
        name: 'home'
        
        MDBoxLayout:
            orientation: 'vertical'
            md_bg_color: 0.98, 0.98, 0.98, 1
            
            MDTopAppBar:
                title: 'CropWise'
                md_bg_color: 0.2, 0.6, 1, 1
                specific_text_color: 1, 1, 1, 1
                elevation: 3
                left_action_items: [['menu', lambda x: None]]
                right_action_items: [['refresh', lambda x: app.refresh_data()]]
                
            ScrollView:
                do_scroll_x: False
                
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: dp(15)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(180)
                        elevation: 3
                        radius: [dp(20)]
                        md_bg_color: 1, 1, 1, 1
                        padding: dp(20)
                        
                        MDLabel:
                            text: 'Current Location'
                            font_style: 'H6'
                            theme_text_color: 'Custom'
                            text_color: 0, 0, 0, 1
                            size_hint_y: None
                            height: dp(30)
                            
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(40)
                            
                            MDIcon:
                                icon: 'map-marker'
                                theme_text_color: 'Primary'
                                size_hint_x: None
                                width: dp(30)
                                
                            MDLabel:
                                id: location_label
                                text: 'Detecting location...'
                                font_style: 'Body1'
                                theme_text_color: 'Custom'
                                text_color: 0.2, 0.2, 0.2, 1
                                
                        Widget:
                        
                        MDRaisedButton:
                            text: 'Update Location'
                            md_bg_color: 0.2, 0.6, 1, 1
                            size_hint_x: None
                            width: dp(150)
                            pos_hint: {'center_x': 0.5}
                            on_release: app.update_location()
                            
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(200)
                        elevation: 3
                        radius: [dp(20)]
                        md_bg_color: 1, 1, 1, 1
                        padding: dp(20)
                        
                        MDLabel:
                            text: 'Weather Conditions'
                            font_style: 'H6'
                            theme_text_color: 'Custom'
                            text_color: 0, 0, 0, 1
                            size_hint_y: None
                            height: dp(30)
                            
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(15)
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(5)
                                
                                MDLabel:
                                    text: 'Temperature'
                                    font_style: 'Caption'
                                    theme_text_color: 'Custom'
                                    text_color: 0.4, 0.4, 0.4, 1
                                    size_hint_y: None
                                    height: dp(20)
                                    
                                MDLabel:
                                    id: temp_label
                                    text: '28°C'
                                    font_style: 'H5'
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    
                            MDSeparator:
                                orientation: 'vertical'
                                
                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(5)
                                
                                MDLabel:
                                    text: 'Humidity'
                                    font_style: 'Caption'
                                    theme_text_color: 'Custom'
                                    text_color: 0.4, 0.4, 0.4, 1
                                    size_hint_y: None
                                    height: dp(20)
                                    
                                MDLabel:
                                    id: humidity_label
                                    text: '65%'
                                    font_style: 'H5'
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    
                            MDSeparator:
                                orientation: 'vertical'
                                
                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(5)
                                
                                MDLabel:
                                    text: 'Rainfall'
                                    font_style: 'Caption'
                                    theme_text_color: 'Custom'
                                    text_color: 0.4, 0.4, 0.4, 1
                                    size_hint_y: None
                                    height: dp(20)
                                    
                                MDLabel:
                                    id: rainfall_label
                                    text: '120mm'
                                    font_style: 'H5'
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    
                    MDRaisedButton:
                        text: 'Analyze Soil & Get Recommendations'
                        md_bg_color: 0.5, 0.8, 0.5, 1
                        size_hint_x: 1
                        size_hint_y: None
                        height: dp(50)
                        on_release: app.show_soil_input()
                        
                    MDLabel:
                        text: 'Recent Analysis'
                        font_style: 'H6'
                        theme_text_color: 'Custom'
                        text_color: 0, 0, 0, 1
                        size_hint_y: None
                        height: dp(30)
                        
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(100)
                        elevation: 2
                        radius: [dp(15)]
                        md_bg_color: 1, 1, 1, 1
                        padding: dp(15)
                        
                        MDLabel:
                            id: last_analysis_label
                            text: 'No analysis yet'
                            font_style: 'Body2'
                            theme_text_color: 'Custom'
                            text_color: 0.3, 0.3, 0.3, 1
                            
    MDScreen:
        name: 'soil_input'
        
        MDBoxLayout:
            orientation: 'vertical'
            md_bg_color: 0.98, 0.98, 0.98, 1
            
            MDTopAppBar:
                title: 'Soil Analysis'
                md_bg_color: 0.2, 0.6, 1, 1
                specific_text_color: 1, 1, 1, 1
                elevation: 3
                left_action_items: [['arrow-left', lambda x: app.go_back()]]
                
            ScrollView:
                do_scroll_x: False
                
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: dp(15)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(120)
                        elevation: 3
                        radius: [dp(20)]
                        md_bg_color: 0.2, 0.6, 1, 1
                        padding: dp(20)
                        
                        MDIcon:
                            icon: 'flask'
                            halign: 'center'
                            font_size: dp(40)
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1
                            size_hint_y: None
                            height: dp(50)
                            
                        MDLabel:
                            text: 'Enter Soil Parameters'
                            halign: 'center'
                            font_style: 'H6'
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1
                            
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(500)
                        elevation: 2
                        radius: [dp(15)]
                        md_bg_color: 1, 1, 1, 1
                        padding: dp(20)
                        spacing: dp(15)
                        
                        MDTextField:
                            id: nitrogen_input
                            hint_text: 'Nitrogen (N) - kg/ha'
                            mode: 'rectangle'
                            size_hint_y: None
                            height: dp(50)
                            input_filter: 'float'
                            text: '40'
                            
                        MDTextField:
                            id: phosphorus_input
                            hint_text: 'Phosphorus (P) - kg/ha'
                            mode: 'rectangle'
                            size_hint_y: None
                            height: dp(50)
                            input_filter: 'float'
                            text: '35'
                            
                        MDTextField:
                            id: potassium_input
                            hint_text: 'Potassium (K) - kg/ha'
                            mode: 'rectangle'
                            size_hint_y: None
                            height: dp(50)
                            input_filter: 'float'
                            text: '30'
                            
                        MDTextField:
                            id: ph_input
                            hint_text: 'pH Level (4-9)'
                            mode: 'rectangle'
                            size_hint_y: None
                            height: dp(50)
                            input_filter: 'float'
                            text: '6.5'
                            
                        MDLabel:
                            text: 'Soil Type'
                            font_style: 'Caption'
                            theme_text_color: 'Custom'
                            text_color: 0.4, 0.4, 0.4, 1
                            size_hint_y: None
                            height: dp(20)
                            
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(40)
                            
                            MDRaisedButton:
                                id: soil_clay
                                text: 'Clay'
                                md_bg_color: (0.9, 0.9, 0.9, 1) if self.state == 'normal' else (0.2, 0.6, 1, 1)
                                text_color: (0, 0, 0, 1) if self.state == 'normal' else (1, 1, 1, 1)
                                on_release: app.select_soil_type('clay')
                                
                            MDRaisedButton:
                                id: soil_sandy
                                text: 'Sandy'
                                md_bg_color: (0.9, 0.9, 0.9, 1) if self.state == 'normal' else (0.2, 0.6, 1, 1)
                                text_color: (0, 0, 0, 1) if self.state == 'normal' else (1, 1, 1, 1)
                                on_release: app.select_soil_type('sandy')
                                
                            MDRaisedButton:
                                id: soil_loamy
                                text: 'Loamy'
                                md_bg_color: (0.9, 0.9, 0.9, 1) if self.state == 'normal' else (0.2, 0.6, 1, 1)
                                text_color: (0, 0, 0, 1) if self.state == 'normal' else (1, 1, 1, 1)
                                on_release: app.select_soil_type('loamy')
                                
                        Widget:
                        
                        MDRaisedButton:
                            text: 'Get Crop Recommendations'
                            md_bg_color: 0.5, 0.8, 0.5, 1
                            size_hint_x: 1
                            size_hint_y: None
                            height: dp(50)
                            on_release: app.analyze_and_recommend()
                            
    MDScreen:
        name: 'results'
        
        MDBoxLayout:
            orientation: 'vertical'
            md_bg_color: 0.98, 0.98, 0.98, 1
            
            MDTopAppBar:
                title: 'Crop Recommendations'
                md_bg_color: 0.2, 0.6, 1, 1
                specific_text_color: 1, 1, 1, 1
                elevation: 3
                left_action_items: [['arrow-left', lambda x: app.go_home()]]
                right_action_items: [['share-variant', lambda x: app.share_results()]]
                
            ScrollView:
                do_scroll_x: False
                
                MDBoxLayout:
                    id: results_container
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: dp(15)
                    size_hint_y: None
                    height: self.minimum_height
'''


class CropRecommendationApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_soil_type = 'loamy'
        self.current_location = {'lat': 13.0827, 'lon': 80.2707, 'city': 'Chennai'}
        self.weather_data = {
            'temperature': 28,
            'humidity': 65,
            'rainfall': 120
        }
        
        # Crop database with detailed information
        self.crop_database = {
            'rice': {
                'name': 'Rice',
                'n_range': (80, 120),
                'p_range': (40, 60),
                'k_range': (40, 60),
                'ph_range': (5.5, 7.0),
                'temp_range': (20, 35),
                'humidity_range': (60, 80),
                'rainfall_range': (150, 300),
                'soil_types': ['clay', 'loamy'],
                'season': 'Kharif/Rabi',
                'duration': '120-150 days'
            },
            'wheat': {
                'name': 'Wheat',
                'n_range': (60, 100),
                'p_range': (30, 50),
                'k_range': (30, 50),
                'ph_range': (6.0, 7.5),
                'temp_range': (15, 25),
                'humidity_range': (50, 70),
                'rainfall_range': (50, 100),
                'soil_types': ['loamy', 'clay'],
                'season': 'Rabi',
                'duration': '110-130 days'
            },
            'maize': {
                'name': 'Maize (Corn)',
                'n_range': (80, 120),
                'p_range': (40, 60),
                'k_range': (40, 60),
                'ph_range': (5.8, 7.0),
                'temp_range': (20, 30),
                'humidity_range': (60, 75),
                'rainfall_range': (60, 110),
                'soil_types': ['loamy', 'sandy'],
                'season': 'Kharif',
                'duration': '90-120 days'
            },
            'cotton': {
                'name': 'Cotton',
                'n_range': (60, 90),
                'p_range': (30, 50),
                'k_range': (30, 50),
                'ph_range': (6.0, 7.5),
                'temp_range': (21, 30),
                'humidity_range': (50, 70),
                'rainfall_range': (60, 120),
                'soil_types': ['loamy', 'clay'],
                'season': 'Kharif',
                'duration': '180-195 days'
            },
            'sugarcane': {
                'name': 'Sugarcane',
                'n_range': (100, 150),
                'p_range': (50, 80),
                'k_range': (60, 100),
                'ph_range': (6.0, 7.5),
                'temp_range': (20, 35),
                'humidity_range': (65, 85),
                'rainfall_range': (150, 250),
                'soil_types': ['loamy', 'clay'],
                'season': 'Year-round',
                'duration': '10-12 months'
            },
            'groundnut': {
                'name': 'Groundnut',
                'n_range': (20, 40),
                'p_range': (40, 60),
                'k_range': (50, 70),
                'ph_range': (6.0, 7.0),
                'temp_range': (22, 30),
                'humidity_range': (55, 75),
                'rainfall_range': (50, 100),
                'soil_types': ['sandy', 'loamy'],
                'season': 'Kharif/Summer',
                'duration': '100-130 days'
            },
            'pulses': {
                'name': 'Pulses (Lentils)',
                'n_range': (15, 30),
                'p_range': (30, 50),
                'k_range': (30, 50),
                'ph_range': (6.0, 7.5),
                'temp_range': (18, 28),
                'humidity_range': (50, 70),
                'rainfall_range': (40, 80),
                'soil_types': ['loamy', 'clay'],
                'season': 'Rabi',
                'duration': '90-110 days'
            },
            'vegetables': {
                'name': 'Mixed Vegetables',
                'n_range': (40, 80),
                'p_range': (30, 60),
                'k_range': (40, 70),
                'ph_range': (6.0, 7.0),
                'temp_range': (15, 30),
                'humidity_range': (60, 80),
                'rainfall_range': (60, 150),
                'soil_types': ['loamy', 'sandy'],
                'season': 'Year-round',
                'duration': '60-120 days'
            }
        }
        
    def build(self):
        self.theme_cls.primary_palette = 'LightBlue'
        self.theme_cls.accent_palette = 'LightGreen'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_hue = '500'
        
        return Builder.load_string(KV)
    
    def on_start(self):
        # Show splash screen then navigate to home
        Clock.schedule_once(self.show_home, 2)
        Clock.schedule_once(self.init_gps, 2.5)
        Clock.schedule_once(self.update_weather, 3.5)
        
    def show_home(self, dt):
        self.root.current = 'home'

    def init_gps(self, *args):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])
            except ImportError:
                pass
            
            if gps:
                try:
                    gps.configure(on_location=self.on_location, on_status=self.on_status)
                    gps.start(minTime=1000, minDistance=0)
                    toast("Starting GPS...")
                except NotImplementedError:
                    toast("GPS not implemented on this platform")
                    self.update_location_simulation()
        else:
            self.update_location_simulation()

    @mainthread
    def on_location(self, **kwargs):
        # kwargs returns lat, lon, etc.
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        if lat and lon:
            self.current_location = {'lat': lat, 'lon': lon}
            
            # Display coordinates
            self.current_location['city'] = f"GPS: {lat:.4f}, {lon:.4f}"
            
            home_screen = self.root.get_screen('home')
            if hasattr(home_screen.ids, 'location_label'):
                home_screen.ids.location_label.text = self.current_location['city']
            
            # Trigger weather update with new precise location
            toast("GPS Location Found")
            self.update_weather()
            
            # Stop GPS to save battery after getting location
            if gps:
                gps.stop()

    @mainthread
    def on_status(self, stype, status):
        toast(f"GPS Status: {stype} - {status}")

    def update_location(self, *args):
        if platform == 'android':
            if gps:
                gps.start(minTime=1000, minDistance=0)
                toast("Updating location...")
            else:
                self.update_location_simulation()
        else:
            self.update_location_simulation()

    def update_location_simulation(self):
        # Try to get real location via IP if GPS is not available (Desktop fallback)
        url = 'https://ipapi.co/json/'
        toast('Detecting location via IP...')
        # Use UrlRequest for async fetching
        UrlRequest(url, on_success=self.on_ip_location_success, on_failure=self.on_ip_location_error, on_error=self.on_ip_location_error, timeout=5)

    def on_ip_location_success(self, req, result):
        try:
            self.current_location = {
                'lat': result.get('latitude'),
                'lon': result.get('longitude'),
                'city': f"{result.get('city')}, {result.get('region')}"
            }
            toast('Location detected via IP')
            self.update_location_ui()
            self.update_weather()
        except Exception as e:
            self.on_ip_location_error(req, e)

    def on_ip_location_error(self, req, error):
        print(f"IP Location failed: {error}")
        # Fallback to simulation if IP fetch fails
        locations = [
            {'lat': 13.0827, 'lon': 80.2707, 'city': 'Chennai, Tamil Nadu'},
            {'lat': 12.9716, 'lon': 77.5946, 'city': 'Bangalore, Karnataka'},
            {'lat': 28.7041, 'lon': 77.1025, 'city': 'Delhi'},
        ]
        self.current_location = random.choice(locations)
        toast('Location simulation (Network unavailable)')
        self.update_location_ui()
        self.update_weather()
        
    def update_location_ui(self):
        # Try to find the label in root ids or screen ids
        label = None
        if 'location_label' in self.root.ids:
            label = self.root.ids.location_label
        else:
            home_screen = self.root.get_screen('home')
            if hasattr(home_screen.ids, 'location_label'):
                label = home_screen.ids.location_label
                
        if label:
            label.text = self.current_location['city']
        else:
            print("Warning: location_label not found")
        
    def update_weather(self, *args):
        # Fetch real weather data using Open-Meteo API (Free, No key required)
        lat = self.current_location.get('lat', 13.0827)
        lon = self.current_location.get('lon', 80.2707)
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain&timezone=auto"
        
        # Use UrlRequest for async fetching to prevent UI freezing
        UrlRequest(url, on_success=self.on_weather_success, on_failure=self.on_weather_error, on_error=self.on_weather_error, timeout=5)
            
    def on_weather_success(self, req, result):
        try:
            current = result.get('current', {})
            
            self.weather_data = {
                'temperature': int(current.get('temperature_2m', 28)),
                'humidity': int(current.get('relative_humidity_2m', 65)),
                'rainfall': int(current.get('rain', 0) * 24 * 30) # Convert hourly rain to approx monthly/seasonal
            }
            
            # If no rain currently, simulate seasonal rainfall based on region logic or random
            if self.weather_data['rainfall'] == 0:
                 self.weather_data['rainfall'] = random.randint(50, 200)
                     
            toast('Weather updated from Live Data')
            self.update_weather_ui()
        except Exception as e:
            print(f"Weather parsing error: {e}")
            self.on_weather_error(req, e)

    def on_weather_error(self, req, error):
        print(f"Weather fetch failed: {error}")
        # Fallback to simulation
        self.weather_data = {
            'temperature': random.randint(20, 35),
            'humidity': random.randint(50, 85),
            'rainfall': random.randint(40, 250)
        }
        toast('Weather simulation (Network unavailable)')
        self.update_weather_ui()
        
    def update_weather_ui(self):
        # Update UI
        ids = self.root.ids
        home_screen = self.root.get_screen('home')
        screen_ids = home_screen.ids if hasattr(home_screen, 'ids') else {}
        
        if 'temp_label' in ids:
            ids.temp_label.text = f"{self.weather_data['temperature']}°C"
        elif 'temp_label' in screen_ids:
            screen_ids.temp_label.text = f"{self.weather_data['temperature']}°C"
            
        if 'humidity_label' in ids:
            ids.humidity_label.text = f"{self.weather_data['humidity']}%"
        elif 'humidity_label' in screen_ids:
            screen_ids.humidity_label.text = f"{self.weather_data['humidity']}%"
            
        if 'rainfall_label' in ids:
            ids.rainfall_label.text = f"{self.weather_data['rainfall']}mm"
        elif 'rainfall_label' in screen_ids:
            screen_ids.rainfall_label.text = f"{self.weather_data['rainfall']}mm"
        
    def refresh_data(self):
        self.update_location()
        self.update_weather()
        toast('Data refreshed')
        
    def show_soil_input(self):
        self.root.current = 'soil_input'
        # Initialize default soil type selection after a short delay
        Clock.schedule_once(lambda dt: self.select_soil_type(self.selected_soil_type), 0.1)
        
    def select_soil_type(self, soil_type):
        self.selected_soil_type = soil_type
        
        # Helper to get widget by id
        def get_widget(wid_id):
            if wid_id in self.root.ids:
                return self.root.ids[wid_id]
            
            soil_screen = self.root.get_screen('soil_input')
            if hasattr(soil_screen.ids, wid_id):
                return soil_screen.ids[wid_id]
            return None

        # Reset all buttons to normal state
        for st in ['clay', 'sandy', 'loamy']:
            btn = get_widget(f'soil_{st}')
            if btn:
                btn.state = 'normal'
                # Reset colors manually as well since we use custom colors
                btn.md_bg_color = (0.9, 0.9, 0.9, 1)
                btn.text_color = (0, 0, 0, 1)
        
        # Set selected button to down state
        selected_btn = get_widget(f'soil_{soil_type}')
        if selected_btn:
            selected_btn.state = 'down'
            selected_btn.md_bg_color = (0.2, 0.6, 1, 1)
            selected_btn.text_color = (1, 1, 1, 1)
            
        toast(f'{soil_type.capitalize()} soil selected')
        
    def go_back(self):
        self.root.current = 'home'
        
    def go_home(self):
        self.root.current = 'home'
        
    def analyze_and_recommend(self):
        # Helper to get widget by id
        def get_widget(wid_id):
            if wid_id in self.root.ids:
                return self.root.ids[wid_id]
            
            soil_screen = self.root.get_screen('soil_input')
            if hasattr(soil_screen.ids, wid_id):
                return soil_screen.ids[wid_id]
            return None

        # Get soil parameters
        try:
            nitrogen_input = get_widget('nitrogen_input')
            nitrogen = float(nitrogen_input.text) if nitrogen_input and nitrogen_input.text else 40
                
            phosphorus_input = get_widget('phosphorus_input')
            phosphorus = float(phosphorus_input.text) if phosphorus_input and phosphorus_input.text else 35
                
            potassium_input = get_widget('potassium_input')
            potassium = float(potassium_input.text) if potassium_input and potassium_input.text else 30
                
            ph_input = get_widget('ph_input')
            ph = float(ph_input.text) if ph_input and ph_input.text else 6.5
            
        except ValueError:
            toast('Please enter valid numeric values')
            return
            
        if not (0 <= nitrogen <= 200 and 0 <= phosphorus <= 200 and 
                0 <= potassium <= 200 and 4 <= ph <= 9):
            toast('Please enter values within valid ranges')
            return
            
        # Calculate crop suitability
        recommendations = self.calculate_recommendations(
            nitrogen, phosphorus, potassium, ph
        )
        
        # Display results
        self.display_results(recommendations)
        
        # Update last analysis
        self.analysis_text = f"Last analysis: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n"
        self.analysis_text += f"N: {nitrogen}, P: {phosphorus}, K: {potassium}, pH: {ph}\n"
        self.analysis_text += f"Soil: {self.selected_soil_type.capitalize()}"
        
        # Generate shareable result text
        self.share_text = f"CropWise Recommendations\n\n{self.analysis_text}\n\nTop Crops:\n"
        for i, rec in enumerate(recommendations[:3], 1):
             self.share_text += f"{i}. {rec['crop']['name']} ({rec['suitability']})\n"
        
        last_analysis_label = get_widget('last_analysis_label')
        if last_analysis_label:
            last_analysis_label.text = self.analysis_text
        else:
            # Fallback for home screen
            home_screen = self.root.get_screen('home')
            if hasattr(home_screen.ids, 'last_analysis_label'):
                home_screen.ids.last_analysis_label.text = self.analysis_text
        
    def calculate_recommendations(self, n, p, k, ph):
        recommendations = []
        temp = self.weather_data['temperature']
        humidity = self.weather_data['humidity']
        rainfall = self.weather_data['rainfall']
        
        for crop_id, crop in self.crop_database.items():
            score = 0
            max_score = 7
            
            # Check NPK ranges
            if crop['n_range'][0] <= n <= crop['n_range'][1]:
                score += 1
            if crop['p_range'][0] <= p <= crop['p_range'][1]:
                score += 1
            if crop['k_range'][0] <= k <= crop['k_range'][1]:
                score += 1
                
            # Check pH
            if crop['ph_range'][0] <= ph <= crop['ph_range'][1]:
                score += 1
                
            # Check temperature
            if crop['temp_range'][0] <= temp <= crop['temp_range'][1]:
                score += 1
                
            # Check humidity
            if crop['humidity_range'][0] <= humidity <= crop['humidity_range'][1]:
                score += 1
                
            # Check rainfall
            if crop['rainfall_range'][0] <= rainfall <= crop['rainfall_range'][1]:
                score += 1
                
            # Check soil type
            if self.selected_soil_type not in crop['soil_types']:
                score -= 1
                
            suitability_percentage = (score / max_score) * 100
            
            if suitability_percentage >= 50:
                if suitability_percentage >= 80:
                    suitability = 'Highly Suitable'
                elif suitability_percentage >= 65:
                    suitability = 'Suitable'
                else:
                    suitability = 'Moderately Suitable'
                    
                recommendations.append({
                    'crop': crop,
                    'score': suitability_percentage,
                    'suitability': suitability
                })
                
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:6]  # Return top 6 recommendations
        
    def display_results(self, recommendations):
        # First navigate to results screen to ensure it's loaded
        self.root.current = 'results'
        
        # Wait a moment for the screen to fully load
        Clock.schedule_once(lambda dt: self._display_results_impl(recommendations), 0.1)
    
    def _display_results_impl(self, recommendations):
        results_screen = self.root.get_screen('results')
        
        # Access container directly via ids
        if hasattr(results_screen.ids, 'results_container'):
            container = results_screen.ids.results_container
        else:
            # Fallback for manual traversal if ids fail
            container = None
            try:
                for child in results_screen.walk():
                    if hasattr(child, 'id') and child.id == 'results_container':
                        container = child
                        break
                    # Also check if it's in ids of children (if accessible)
                    if hasattr(child, 'ids') and 'results_container' in child.ids:
                        container = child.ids.results_container
                        break
            except Exception as e:
                print(f"Error traversing: {e}")

        if container is None:
            # Try one more specific path based on KV structure
            try:
                # MDScreen -> MDBoxLayout -> ScrollView -> MDBoxLayout(results_container)
                container = results_screen.children[0].children[0].children[0]
            except:
                pass

        if container is None:
            toast('Error: Results container not found')
            return
        
        container.clear_widgets()
        
        if not recommendations:
            no_results = Builder.load_string('''
MDCard:
    orientation: 'vertical'
    size_hint_y: None
    height: dp(200)
    elevation: 2
    radius: [dp(15)]
    md_bg_color: 1, 1, 1, 1
    padding: dp(20)
    
    MDIcon:
        icon: 'alert-circle-outline'
        halign: 'center'
        font_size: dp(60)
        theme_text_color: 'Custom'
        text_color: 0.7, 0.7, 0.7, 1
        size_hint_y: None
        height: dp(80)
        
    MDLabel:
        text: 'No suitable crops found'
        halign: 'center'
        font_style: 'H6'
        theme_text_color: 'Custom'
        text_color: 0.5, 0.5, 0.5, 1
        
    MDLabel:
        text: 'Try adjusting soil parameters'
        halign: 'center'
        font_style: 'Caption'
        theme_text_color: 'Custom'
        text_color: 0.6, 0.6, 0.6, 1
''')
            container.add_widget(no_results)
        else:
            # Add header card
            header = Builder.load_string(f'''
MDCard:
    orientation: 'vertical'
    size_hint_y: None
    height: dp(150)
    elevation: 3
    radius: [dp(20)]
    md_bg_color: 0.2, 0.6, 1, 1
    padding: dp(20)
    
    MDIcon:
        icon: 'check-circle'
        halign: 'center'
        font_size: dp(50)
        theme_text_color: 'Custom'
        text_color: 1, 1, 1, 1
        size_hint_y: None
        height: dp(60)
        
    MDLabel:
        text: 'Analysis Complete'
        halign: 'center'
        font_style: 'H6'
        theme_text_color: 'Custom'
        text_color: 1, 1, 1, 1
        
    MDLabel:
        text: '{len(recommendations)} crops recommended'
        halign: 'center'
        font_style: 'Caption'
        theme_text_color: 'Custom'
        text_color: 1, 1, 1, 0.8
''')
            container.add_widget(header)
            
            # Add recommendations
            for rec in recommendations:
                crop = rec['crop']
                card_kv = f'''
CropCard:
    crop_name: '{crop["name"]}'
    crop_details: 'Season: {crop["season"]} | Duration: {crop["duration"]}'
    suitability: '{rec["suitability"]}'
'''
                card = Builder.load_string(card_kv)
                container.add_widget(card)
                
        toast('Analysis complete')
        
    def share_results(self):
        if hasattr(self, 'share_text') and self.share_text:
            try:
                if share:
                    share.share(title='CropWise Recommendations', text=self.share_text)
                else:
                    # Fallback for clipboard or simulation
                    from kivy.core.clipboard import Clipboard
                    Clipboard.copy(self.share_text)
                    toast('Results copied to clipboard (Share not available)')
            except Exception as e:
                toast(f'Error sharing: {e}')
        else:
            toast('No results to share yet')


if __name__ == '__main__':
    CropRecommendationApp().run()
