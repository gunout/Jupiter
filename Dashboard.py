import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import base64
from io import BytesIO
import hashlib

# Configuration de la page
st.set_page_config(
    page_title="♃ Jupiter Data Dashboard",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec thème "Jupiter - Le Roi des Planètes"
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #D8CA9D;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #2C1810, #4A3729, #2C1810);
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 2px solid #B8A86D;
        text-shadow: 0 0 20px #FFD700, 0 0 40px #B8A86D;
        animation: royalGlow 4s ease-in-out infinite;
    }
    @keyframes royalGlow {
        0% { text-shadow: 0 0 20px #FFD700; }
        50% { text-shadow: 0 0 40px #B8A86D, 0 0 60px #D8CA9D; }
        100% { text-shadow: 0 0 20px #FFD700; }
    }
    .metric-card {
        background: linear-gradient(135deg, #2C1810, #4A3729);
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #B8A86D;
        text-align: center;
        box-shadow: 0 0 30px rgba(184, 168, 109, 0.3);
    }
    .metric-label {
        color: #D8CA9D;
        font-size: 1rem;
        font-weight: 600;
    }
    .metric-value {
        color: #FFD700;
        font-size: 2rem;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }
    .info-box {
        background: linear-gradient(135deg, #2C1810, #3E2B1F);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #B8A86D;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(184, 168, 109, 0.2);
    }
    .event-marker {
        background: linear-gradient(135deg, #3E2B1F, #5A4535);
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #B8A86D;
        margin: 0.2rem 0;
        transition: all 0.3s ease;
    }
    .event-marker:hover {
        transform: translateX(5px);
        box-shadow: 0 0 20px rgba(184, 168, 109, 0.5);
        border-color: #FFD700;
    }
    .storm-high {
        color: #FF4500;
        font-weight: bold;
        text-shadow: 0 0 10px #FF4500;
    }
    .storm-moderate {
        color: #FFA500;
        font-weight: bold;
    }
    .mission-badge {
        background: linear-gradient(135deg, #B8A86D, #D8CA9D);
        color: #2C1810;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
        border: 1px solid #FFD700;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1A0F0A;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #2C1810;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: #D8CA9D;
        border: 1px solid #B8A86D;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #B8A86D, #D8CA9D);
        color: #2C1810;
        font-weight: bold;
    }
    .royal-badge {
        background: linear-gradient(135deg, #B8A86D, #FFD700);
        color: #2C1810;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
        font-weight: bold;
        border: 1px solid #FFD700;
    }
</style>
""", unsafe_allow_html=True)

class JupiterDataAnalyzer:
    def __init__(self, data_type):
        self.data_type = data_type
        self.colors = ['#D8CA9D', '#B8A86D', '#9B8E64', '#C9B27C', '#E0D0A8',
                      '#A8996D', '#D4C49E', '#F0E6C8', '#8C7C5E', '#B5A885']
        
        self.start_year = 1610
        self.end_year = 2025
        
        self.config = self._get_jupiter_config()
        
    def _get_jupiter_config(self):
        configs = {
            "atmospheric_temperature": {
                "base_value": -145,
                "cycle_years": 11.86,
                "amplitude": 20,
                "trend": "stable",
                "unit": "°C",
                "description": "🌡️ Température atmosphérique",
                "icon": "🌡️",
                "color": "#B8A86D",
                "range": [-165, -125]
            },
            "wind_speeds": {
                "base_value": 150,
                "cycle_years": 11.86,
                "amplitude": 100,
                "trend": "jet_streams",
                "unit": "km/h",
                "description": "💨 Vitesse des vents",
                "icon": "💨",
                "color": "#C9B27C",
                "range": [50, 600]
            },
            "great_red_spot": {
                "base_value": 16000,
                "cycle_years": 11.86,
                "amplitude": 2000,
                "trend": "shrinking",
                "unit": "km",
                "description": "🔴 Grande Tache Rouge",
                "icon": "🔴",
                "color": "#FF4500",
                "range": [14000, 18000]
            },
            "magnetic_field": {
                "base_value": 4200000,
                "cycle_years": 11.86,
                "amplitude": 100000,
                "trend": "stable",
                "unit": "nT",
                "description": "🧲 Champ magnétique",
                "icon": "🧲",
                "color": "#9B8E64",
                "range": [4000000, 4300000]
            },
            "radiation_belts": {
                "base_value": 3500,
                "cycle_years": 11.86,
                "amplitude": 500,
                "trend": "variable",
                "unit": "rads/h",
                "description": "☢️ Ceintures de radiation",
                "icon": "☢️",
                "color": "#FFD700",
                "range": [3000, 4000]
            },
            "auroral_activity": {
                "base_value": 80,
                "cycle_years": 11.86,
                "amplitude": 40,
                "trend": "solar_dependent",
                "unit": "intensité",
                "description": "✨ Activité aurorale",
                "icon": "✨",
                "color": "#00CED1",
                "range": [40, 120]
            },
            "ring_system": {
                "base_value": 30,
                "cycle_years": 11.86,
                "amplitude": 5,
                "trend": "stable",
                "unit": "albédo",
                "description": "💫 Système d'anneaux",
                "icon": "💫",
                "color": "#E0D0A8",
                "range": [25, 35]
            },
            "moons_activity": {
                "base_value": 65,
                "cycle_years": 11.86,
                "amplitude": 20,
                "trend": "volcanic",
                "unit": "index",
                "description": "🌕 Activité des lunes",
                "icon": "🌕",
                "color": "#DA70D6",
                "range": [45, 85]
            },
            "atmospheric_composition": {
                "base_value": 90,
                "cycle_years": 11.86,
                "amplitude": 5,
                "trend": "stable",
                "unit": "% H₂",
                "description": "🧪 Composition H₂",
                "icon": "🧪",
                "color": "#A8996D",
                "range": [85, 95]
            },
            "orbital_parameters": {
                "base_value": 5.20,
                "cycle_years": 11.86,
                "amplitude": 0.20,
                "trend": "stable",
                "unit": "UA",
                "description": "🛸 Distance au Soleil",
                "icon": "🛸",
                "color": "#B5A885",
                "range": [5.00, 5.40]
            }
        }
        return configs.get(self.data_type, configs["wind_speeds"])
    
    def generate_jupiter_data(self):
        years = list(range(self.start_year, self.end_year + 1))
        
        data = {'Earth_Year': years}
        data['Jupiter_Year'] = self._earth_to_jupiter_years(years)
        data['Solar_Distance'] = self._simulate_solar_distance(years)
        
        # Données principales
        data['Base_Value'] = self._simulate_jupiter_cycle(years)
        data['Seasonal_Variation'] = self._simulate_seasonal_variation(years)
        data['Atmospheric_Storms'] = self._simulate_atmospheric_storms(years)
        data['Magnetic_Activity'] = self._simulate_magnetic_activity(years)
        data['Great_Red_Spot_Evolution'] = self._simulate_great_red_spot(years)
        data['Radiation_Variations'] = self._simulate_radiation_variations(years)
        data['Moon_Influences'] = self._simulate_moon_influences(years)
        data['Smoothed_Value'] = self._simulate_smoothed_data(years)
        data['Short_Term_Variation'] = self._simulate_short_term_variation(years)
        data['Long_Term_Trend'] = self._simulate_long_term_trend(years)
        data['Jupiter_Index'] = self._simulate_jupiter_index(years)
        data['Observation_Quality'] = self._simulate_observation_quality(years)
        data['Future_Prediction'] = self._simulate_future_prediction(years)
        data['Storm_Intensity'] = self._simulate_storm_intensity(years)
        data['Auroral_Power'] = self._simulate_auroral_power(years)
        
        df = pd.DataFrame(data)
        self._add_jupiter_events(df)
        
        return df
    
    def _earth_to_jupiter_years(self, years):
        jupiter_years = []
        jupiter_year_duration = 11.86
        
        for earth_year in years:
            jupiter_year = (earth_year - self.start_year) / jupiter_year_duration
            jupiter_years.append(jupiter_year)
        return jupiter_years
    
    def _simulate_solar_distance(self, years):
        distances = []
        for earth_year in years:
            base_distance = 5.20
            variation = 0.05 * np.sin(2 * np.pi * (earth_year - self.start_year) / 11.86)
            distance = base_distance + variation
            distances.append(distance)
        return distances
    
    def _simulate_jupiter_cycle(self, years):
        base_value = self.config["base_value"]
        cycle_years = self.config["cycle_years"]
        amplitude = self.config["amplitude"]
        
        values = []
        for earth_year in years:
            jupiter_phase = (earth_year - self.start_year) % cycle_years
            seasonal_cycle = np.sin(2 * np.pi * jupiter_phase / cycle_years)
            
            spot_cycle_years = 12.5
            spot_phase = (earth_year - self.start_year) % spot_cycle_years
            spot_cycle = np.cos(2 * np.pi * spot_phase / spot_cycle_years)
            
            solar_cycle_years = 11.0
            solar_phase = (earth_year - self.start_year) % solar_cycle_years
            solar_cycle = np.sin(2 * np.pi * solar_phase / solar_cycle_years)
            
            if self.config["trend"] == "jet_streams":
                value = base_value + amplitude * (0.6 * seasonal_cycle + 0.4 * spot_cycle)
            elif self.config["trend"] == "shrinking":
                years_since_start = earth_year - self.start_year
                shrinkage = -0.01 * years_since_start
                value = base_value + amplitude * seasonal_cycle + shrinkage
            elif self.config["trend"] == "solar_dependent":
                value = base_value + amplitude * (0.7 * solar_cycle + 0.3 * seasonal_cycle)
            elif self.config["trend"] == "volcanic":
                volcanic_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 7.3)
                value = base_value + amplitude * volcanic_cycle
            else:
                value = base_value + amplitude * seasonal_cycle
            
            noise = np.random.normal(0, amplitude * 0.1)
            values.append(value + noise)
        return values
    
    def _simulate_seasonal_variation(self, years):
        variations = []
        for earth_year in years:
            seasonal_variation = 0.1 * np.sin(2 * np.pi * (earth_year - self.start_year) / 11.86)
            variations.append(1 + seasonal_variation)
        return variations
    
    def _simulate_atmospheric_storms(self, years):
        storm_activities = []
        for earth_year in years:
            short_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 3.2)
            medium_cycle = np.cos(2 * np.pi * (earth_year - self.start_year) / 7.5)
            long_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 15.8)
            
            storm_activity = 1.0 + 0.3 * short_cycle + 0.2 * medium_cycle + 0.1 * long_cycle
            storm_activities.append(storm_activity)
        return storm_activities
    
    def _simulate_storm_intensity(self, years):
        intensities = []
        base_intensity = self._simulate_atmospheric_storms(years)
        for i, val in enumerate(base_intensity):
            intensity = val * 100 + np.random.normal(0, 10)
            intensities.append(max(0, intensity))
        return intensities
    
    def _simulate_magnetic_activity(self, years):
        magnetic_activities = []
        for earth_year in years:
            magnetic_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 9.7)
            magnetic_activity = 1.0 + 0.2 * magnetic_cycle
            magnetic_activities.append(magnetic_activity)
        return magnetic_activities
    
    def _simulate_great_red_spot(self, years):
        spot_evolutions = []
        for earth_year in years:
            years_since_start = earth_year - self.start_year
            
            if earth_year < 1800:
                size_factor = 1.8
            elif earth_year < 1900:
                size_factor = 1.5
            elif earth_year < 2000:
                size_factor = 1.2
            else:
                size_factor = 1.0 - 0.001 * (earth_year - 2000)
            
            short_term = 0.1 * np.sin(2 * np.pi * (earth_year - self.start_year) / 5.3)
            spot_evolution = size_factor * (1 + short_term)
            spot_evolutions.append(spot_evolution)
        return spot_evolutions
    
    def _simulate_radiation_variations(self, years):
        radiation_levels = []
        for earth_year in years:
            solar_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 11.0)
            magnetic_cycle = np.cos(2 * np.pi * (earth_year - self.start_year) / 9.7)
            
            radiation_level = 1.0 + 0.3 * solar_cycle + 0.2 * magnetic_cycle
            radiation_levels.append(radiation_level)
        return radiation_levels
    
    def _simulate_moon_influences(self, years):
        moon_influences = []
        for earth_year in years:
            io_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 1.77)
            europa_cycle = np.cos(2 * np.pi * (earth_year - self.start_year) / 3.55)
            ganymede_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 7.15)
            callisto_cycle = np.cos(2 * np.pi * (earth_year - self.start_year) / 16.69)
            
            moon_influence = 1.0 + 0.15 * io_cycle + 0.1 * europa_cycle + 0.05 * ganymede_cycle + 0.03 * callisto_cycle
            moon_influences.append(moon_influence)
        return moon_influences
    
    def _simulate_smoothed_data(self, years):
        base_cycle = self._simulate_jupiter_cycle(years)
        smoothed = []
        window_size = 5
        
        for i in range(len(base_cycle)):
            start_idx = max(0, i - window_size//2)
            end_idx = min(len(base_cycle), i + window_size//2 + 1)
            window = base_cycle[start_idx:end_idx]
            smoothed.append(np.mean(window))
        return smoothed
    
    def _simulate_short_term_variation(self, years):
        variations = []
        for earth_year in years:
            rapid_variation = 0.05 * np.sin(2 * np.pi * (earth_year - self.start_year) / 0.1)
            variations.append(1 + rapid_variation)
        return variations
    
    def _simulate_long_term_trend(self, years):
        trends = []
        for earth_year in years:
            years_since_start = earth_year - self.start_year
            
            if self.config["trend"] == "shrinking":
                trend = 1.0 - 0.0005 * years_since_start
            else:
                trend = 1.0 + 0.0001 * years_since_start
            
            trends.append(trend)
        return trends
    
    def _simulate_auroral_power(self, years):
        powers = []
        for earth_year in years:
            base_power = 100
            solar_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 11.0)
            magnetic_cycle = np.cos(2 * np.pi * (earth_year - self.start_year) / 9.7)
            
            power = base_power * (1 + 0.3 * solar_cycle + 0.2 * magnetic_cycle)
            powers.append(power)
        return powers
    
    def _simulate_jupiter_index(self, years):
        indices = []
        base_cycle = self._simulate_jupiter_cycle(years)
        storm_activity = self._simulate_atmospheric_storms(years)
        magnetic_activity = self._simulate_magnetic_activity(years)
        
        for i in range(len(years)):
            index = (base_cycle[i] * 0.4 + storm_activity[i] * 30 * 0.3 + magnetic_activity[i] * 1000 * 0.3)
            indices.append(index)
        return indices
    
    def _simulate_observation_quality(self, years):
        qualities = []
        for earth_year in years:
            if earth_year < 1700:
                quality = 10
            elif earth_year < 1800:
                quality = 20
            elif earth_year < 1900:
                quality = 40
            elif earth_year < 1970:
                quality = 60
            elif earth_year < 1990:
                quality = 80
            else:
                quality = 95
            
            orbital_variation = 5 * np.sin(2 * np.pi * (earth_year - self.start_year) / 11.86)
            qualities.append(min(100, quality + orbital_variation))
        return qualities
    
    def _simulate_future_prediction(self, years):
        predictions = []
        base_cycle = self._simulate_jupiter_cycle(years)
        long_term_trend = self._simulate_long_term_trend(years)
        
        for i, earth_year in enumerate(years):
            current_value = base_cycle[i]
            trend_factor = long_term_trend[i]
            
            if earth_year > 2020:
                years_since_2020 = earth_year - 2020
                uncertainty = 0.02 * years_since_2020
                prediction = current_value * trend_factor * (1 + np.random.normal(0, uncertainty))
            else:
                prediction = current_value
            predictions.append(prediction)
        return predictions
    
    def _add_jupiter_events(self, df):
        events = []
        for i, row in df.iterrows():
            earth_year = row['Earth_Year']
            
            mission_events = {
                1610: ("Galilée - Découverte des lunes galiléennes", "discovery", "historique"),
                1665: ("Première observation de la Grande Tache Rouge", "observation", "majeur"),
                1831: ("Observations détaillées des bandes", "observation", "majeur"),
                1973: ("Pioneer 10 - Premier survol", "flyby", "historique"),
                1979: ("Voyager 1/2 - Découvertes majeures", "flyby", "historique"),
                1995: ("Galileo - Première orbite", "orbiter", "historique"),
                2000: ("Cassini - Survol vers Saturne", "flyby", "majeur"),
                2007: ("New Horizons - Survol vers Pluton", "flyby", "majeur"),
                2016: ("Juno - Arrivée en orbite polaire", "orbiter", "historique"),
                2021: ("James Webb - Observations", "telescope", "majeur")
            }
            
            if earth_year in mission_events:
                event_name, event_type, severity = mission_events[earth_year]
                events.append({
                    "year": earth_year,
                    "event": event_name,
                    "type": event_type,
                    "severity": severity,
                    "jupiter_year": row['Jupiter_Year']
                })
                df.loc[i, 'Observation_Quality'] = min(100, df.loc[i, 'Observation_Quality'] + 5)
            
            # Grandes tempêtes documentées
            storm_years = [1990, 2006, 2012, 2016, 2020]
            if earth_year in storm_years:
                events.append({
                    "year": earth_year,
                    "event": "🌪️ Grande tempête atmosphérique",
                    "type": "storm",
                    "severity": "majeur",
                    "jupiter_year": row['Jupiter_Year']
                })
                df.loc[i, 'Atmospheric_Storms'] *= 1.5
        
        self.events = events

# Fonctions de visualisation avec des IDs uniques
@st.cache_data
def create_plotly_visualizations(df, analyzer, chart_id):
    """Crée des visualisations Plotly interactives avec ID unique"""
    
    fig_main = make_subplots(
        rows=3, cols=2,
        subplot_titles=('♃ Cycle Jovien Principal', '🔴 Grande Tache Rouge',
                       '🌪️ Activité des Tempêtes', '🧲 Activité Magnétique',
                       '📊 Données Brutes vs Lissées', '🔮 Projections Futures'),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Cycle principal
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'], y=df['Base_Value'],
                  mode='lines', name='Valeur observée',
                  line=dict(color=analyzer.config['color'], width=2),
                  hovertemplate='Année: %{x}<br>Valeur: %{y:.2f} ' + analyzer.config['unit']),
        row=1, col=1
    )
    
    # Grande Tache Rouge
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'], y=df['Great_Red_Spot_Evolution'],
                  mode='lines', name='Taille relative',
                  line=dict(color='#FF4500', width=2),
                  fill='tozeroy'),
        row=1, col=2
    )
    
    # Tendance de la GTR
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'], y=[1.0] * len(df),
                  mode='lines', name='Référence (1665)',
                  line=dict(color='yellow', width=1, dash='dash')),
        row=1, col=2
    )
    
    # Activité des tempêtes
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'], y=df['Storm_Intensity'],
                  mode='lines', name='Intensité des tempêtes',
                  line=dict(color='#FFA500', width=2)),
        row=2, col=1
    )
    
    # Activité magnétique
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'], y=df['Magnetic_Activity'],
                  mode='lines', name='Champ magnétique',
                  line=dict(color='#1E90FF', width=2)),
        row=2, col=2
    )
    
    # Aurores
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'], y=df['Auroral_Power'],
                  mode='lines', name='Aurores',
                  line=dict(color='#00CED1', width=2, dash='dot')),
        row=2, col=2
    )
    
    # Données brutes vs lissées
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'], y=df['Base_Value'],
                  mode='lines', name='Données brutes',
                  line=dict(color=analyzer.config['color'], width=1, dash='dot')),
        row=3, col=1
    )
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'], y=df['Smoothed_Value'],
                  mode='lines', name='Données lissées',
                  line=dict(color='#00FF7F', width=3)),
        row=3, col=1
    )
    
    # Projections futures
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'][df['Earth_Year'] <= 2020], 
                  y=df['Base_Value'][df['Earth_Year'] <= 2020],
                  mode='lines', name='Historique',
                  line=dict(color=analyzer.config['color'], width=2)),
        row=3, col=2
    )
    fig_main.add_trace(
        go.Scatter(x=df['Earth_Year'][df['Earth_Year'] >= 2020], 
                  y=df['Future_Prediction'][df['Earth_Year'] >= 2020],
                  mode='lines', name='Projections',
                  line=dict(color='#00FFFF', width=2, dash='dash')),
        row=3, col=2
    )
    
    fig_main.update_layout(
        height=900,
        showlegend=True,
        template='plotly_dark',
        title_text=f"♃ Analyse Interactive des Données Joviennes - {analyzer.config['description']}",
        title_font_size=18,
        title_font_color='#D8CA9D',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    for i in range(1, 4):
        for j in range(1, 3):
            fig_main.update_xaxes(title_text="Année Terrestre", row=i, col=j, gridcolor='#333333')
            fig_main.update_yaxes(gridcolor='#333333', row=i, col=j)
    
    fig_main.update_yaxes(title_text=analyzer.config['unit'], row=1, col=1)
    fig_main.update_yaxes(title_text="Taille relative", row=1, col=2)
    fig_main.update_yaxes(title_text="Intensité", row=2, col=1)
    fig_main.update_yaxes(title_text="Activité", row=2, col=2)
    fig_main.update_yaxes(title_text=analyzer.config['unit'], row=3, col=1)
    fig_main.update_yaxes(title_text=analyzer.config['unit'], row=3, col=2)
    
    return fig_main

@st.cache_data
def create_jupiter_atmosphere_visualization(df, analyzer, chart_id):
    """Crée une visualisation de l'atmosphère de Jupiter avec ID unique"""
    
    # Couches atmosphériques
    layers = ['Haute atmosphère', 'Nuages d\'ammoniac', 'Nuages d\'hydrosulfure', 'Nuages d\'eau', 'Profondeur']
    altitudes = [100, 70, 50, 30, 0]  # km
    
    if analyzer.data_type == "atmospheric_temperature":
        values = [-120, -100, -50, 0, 20000]
    elif analyzer.data_type == "wind_speeds":
        values = [400, 300, 200, 100, 0]
    else:
        values = [100, 80, 60, 40, 20]
    
    fig_atmo = go.Figure()
    
    fig_atmo.add_trace(go.Scatter(
        x=values,
        y=altitudes,
        mode='lines+markers',
        name='Profil atmosphérique',
        line=dict(color='#D8CA9D', width=3),
        marker=dict(size=10, color='#FFD700')
    ))
    
    for i, (layer, alt) in enumerate(zip(layers, altitudes)):
        fig_atmo.add_annotation(x=values[i] + 50, y=alt, text=layer, 
                               showarrow=True, arrowhead=1, ax=-30, ay=0,
                               font=dict(color='#D8CA9D'))
    
    fig_atmo.update_layout(
        title="🌪️ Structure Atmosphérique de Jupiter",
        template='plotly_dark',
        xaxis_title=analyzer.config['unit'],
        yaxis_title="Altitude (km)",
        height=500
    )
    
    return fig_atmo

@st.cache_data
def create_moon_orbits_visualization(chart_id):
    """Crée une visualisation des orbites des lunes galiléennes avec ID unique"""
    
    moons = ['Io', 'Europa', 'Ganymède', 'Callisto']
    colors = ['#FF4500', '#1E90FF', '#32CD32', '#FFD700']
    radii = [421800, 671100, 1070400, 1882700]  # km
    periods = [1.77, 3.55, 7.15, 16.69]  # jours
    
    fig_moons = go.Figure()
    
    for i, (moon, color, radius) in enumerate(zip(moons, colors, radii)):
        theta = np.linspace(0, 2*np.pi, 100)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        fig_moons.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            name=moon,
            line=dict(color=color, width=2),
            showlegend=True
        ))
        
        angle = 2 * np.pi * (datetime.now().timestamp() / (periods[i] * 86400))
        fig_moons.add_trace(go.Scatter(
            x=[radius * np.cos(angle)],
            y=[radius * np.sin(angle)],
            mode='markers',
            marker=dict(size=10, color=color, line=dict(color='white', width=1)),
            showlegend=False,
            hovertext=moon
        ))
    
    fig_moons.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        marker=dict(size=30, color='#D8CA9D', symbol='star'),
        name='Jupiter',
        hovertext='Jupiter'
    ))
    
    fig_moons.update_layout(
        title="🌕 Système des Lunes Galiléennes",
        template='plotly_dark',
        xaxis_title="Distance (km)",
        yaxis_title="Distance (km)",
        xaxis=dict(scaleanchor="y", scaleratio=1),
        yaxis=dict(scaleanchor="x", scaleratio=1),
        height=600,
        showlegend=True
    )
    
    return fig_moons

@st.cache_data
def create_mission_timeline(events, chart_id):
    """Crée une timeline des missions joviennes avec ID unique"""
    if not events:
        return None
    
    df_events = pd.DataFrame(events)
    
    fig_timeline = go.Figure()
    
    color_map = {
        'discovery': '#FFD700',
        'observation': '#B8A86D',
        'flyby': '#1E90FF',
        'orbiter': '#32CD32',
        'telescope': '#FFA07A',
        'storm': '#FF4500'
    }
    
    for event_type in df_events['type'].unique():
        df_type = df_events[df_events['type'] == event_type]
        
        fig_timeline.add_trace(go.Scatter(
            x=df_type['year'],
            y=[1] * len(df_type),
            mode='markers+text',
            name=event_type.capitalize(),
            marker=dict(
                size=15,
                color=color_map.get(event_type, '#808080'),
                symbol='diamond' if event_type == 'storm' else 'circle',
                line=dict(color='white', width=1)
            ),
            text=df_type['event'],
            textposition="top center",
            hoverinfo='text',
            showlegend=True
        ))
    
    fig_timeline.update_layout(
        title="🚀 Chronologie des Missions et Découvertes Joviennes",
        template='plotly_dark',
        height=300,
        xaxis=dict(title="Année Terrestre", gridcolor='#333333', dtick=20),
        yaxis=dict(showticklabels=False, gridcolor='#333333'),
        hovermode='x',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig_timeline

@st.cache_data
def create_gtr_evolution_chart(df, chart_id):
    """Crée un graphique d'évolution de la Grande Tache Rouge avec ID unique"""
    
    fig_gtr = go.Figure()
    
    fig_gtr.add_trace(go.Scatter(
        x=df['Earth_Year'],
        y=df['Great_Red_Spot_Evolution'] * 16000,
        mode='lines',
        name='Diamètre',
        line=dict(color='#FF4500', width=3),
        fill='tozeroy'
    ))
    
    fig_gtr.update_layout(
        template='plotly_dark',
        xaxis_title="Année Terrestre",
        yaxis_title="Diamètre (km)",
        height=400
    )
    
    return fig_gtr

@st.cache_data
def create_moon_influence_chart(df, chart_id):
    """Crée un graphique d'influence des lunes avec ID unique"""
    
    fig_moon_influence = go.Figure()
    fig_moon_influence.add_trace(go.Scatter(
        x=df['Earth_Year'],
        y=df['Moon_Influences'],
        mode='lines',
        name='Influence combinée',
        line=dict(color='#DA70D6', width=2)
    ))
    
    fig_moon_influence.update_layout(
        template='plotly_dark',
        xaxis_title="Année Terrestre",
        yaxis_title="Influence relative",
        height=300
    )
    
    return fig_moon_influence

def get_storm_class(intensity):
    """Retourne la classe CSS pour l'intensité des tempêtes"""
    if intensity < 150:
        return "storm-moderate"
    else:
        return "storm-high"

def main():
    st.markdown('<h1 class="main-header">♃ Jupiter - Le Roi des Planètes</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e2/Jupiter.jpg", 
                 use_column_width=True)
        
        st.markdown("## 🎯 Configuration")
        
        jupiter_data_types = {
            "atmospheric_temperature": "🌡️ Température atmosphérique",
            "wind_speeds": "💨 Vitesse des vents",
            "great_red_spot": "🔴 Grande Tache Rouge",
            "magnetic_field": "🧲 Champ magnétique",
            "radiation_belts": "☢️ Ceintures de radiation",
            "auroral_activity": "✨ Activité aurorale",
            "ring_system": "💫 Système d'anneaux",
            "moons_activity": "🌕 Activité des lunes",
            "atmospheric_composition": "🧪 Composition H₂",
            "orbital_parameters": "🛸 Distance orbitale"
        }
        
        selected_type = st.selectbox(
            "Type de données joviennes",
            options=list(jupiter_data_types.keys()),
            format_func=lambda x: jupiter_data_types[x],
            key="data_type_selector"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            start_year = st.number_input("Début", min_value=1600, max_value=2000, value=1610, key="start_year")
        with col2:
            end_year = st.number_input("Fin", min_value=1611, max_value=2030, value=2025, key="end_year")
        
        show_missions = st.checkbox("Afficher les missions", value=True, key="show_missions")
        show_moons = st.checkbox("Afficher les lunes", value=True, key="show_moons")
        
        viz_mode = st.radio(
            "Mode de visualisation",
            ["Standard", "Atmosphère", "Système lunaire"],
            key="viz_mode"
        )
        
        if st.button("♃ Générer l'analyse", use_container_width=True, key="generate_button"):
            st.session_state['generate'] = True
            # Clear cache when generating new data
            st.cache_data.clear()
        
        st.markdown("---")
        st.markdown("### 👑 Faits royaux")
        
        st.markdown("""
        <div class="info-box">
            • Diamètre: 11 × Terre<br>
            • Masse: 318 × Terre<br>
            • Rotation: 9.9 heures<br>
            • Lunes: 95 connues<br>
            • GTR: plus grande tempête
        </div>
        """, unsafe_allow_html=True)
    
    # Initialisation de l'analyseur
    analyzer = JupiterDataAnalyzer(selected_type)
    analyzer.start_year = start_year
    analyzer.end_year = end_year
    
    # Génération des données avec cache
    @st.cache_data
    def load_data(analyzer, start_year, end_year, selected_type):
        analyzer.start_year = start_year
        analyzer.end_year = end_year
        return analyzer.generate_jupiter_data()
    
    if 'generate' in st.session_state and st.session_state['generate']:
        with st.spinner("♃ Génération des données joviennes en cours..."):
            df = load_data(analyzer, start_year, end_year, selected_type)
            st.session_state['df'] = df
            st.session_state['generate'] = False
    elif 'df' not in st.session_state:
        with st.spinner("♃ Chargement des données joviennes..."):
            df = load_data(analyzer, start_year, end_year, selected_type)
            st.session_state['df'] = df
    else:
        df = st.session_state['df']
    
    # Métriques principales avec IDs uniques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_jupiter_year = df['Jupiter_Year'].iloc[-1]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">♃ Année jovienne</div>
            <div class="metric-value">{current_jupiter_year:.1f}</div>
            <div style="color: #D8CA9D;">depuis 1610</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        current_value = df['Base_Value'].iloc[-1]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{analyzer.config['icon']} Valeur actuelle</div>
            <div class="metric-value">{current_value:.1f}</div>
            <div style="color: #D8CA9D;">{analyzer.config['unit']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        storm_current = df['Storm_Intensity'].iloc[-1] if 'Storm_Intensity' in df.columns else 100
        storm_class = get_storm_class(storm_current)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🌪️ Tempêtes actuelles</div>
            <div class="metric-value {storm_class}">{storm_current:.0f}</div>
            <div style="color: #D8CA9D;">intensité</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        moons_value = df['Moon_Influences'].iloc[-1] if 'Moon_Influences' in df.columns else 1.0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🌕 Influence lunaire</div>
            <div class="metric-value">{moons_value:.2f}</div>
            <div style="color: #D8CA9D;">relative</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs avec clés uniques
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Analyse Principale", "🌪️ Atmosphère", "🌕 Lunes", 
        "🚀 Missions", "📊 Statistiques", "🔮 Projections"
    ])
    
    with tab1:
        st.markdown("## Visualisation Interactive")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            year_range = st.slider(
                "Période d'affichage",
                min_value=int(df['Earth_Year'].min()),
                max_value=int(df['Earth_Year'].max()),
                value=(1900, 2025),
                key="year_range_slider"
            )
        
        df_filtered = df[(df['Earth_Year'] >= year_range[0]) & (df['Earth_Year'] <= year_range[1])]
        
        # Générer un ID unique basé sur les paramètres
        chart_id = f"main_{selected_type}_{year_range[0]}_{year_range[1]}_{viz_mode}"
        
        if viz_mode == "Standard":
            fig_main = create_plotly_visualizations(df_filtered, analyzer, chart_id)
            st.plotly_chart(fig_main, use_container_width=True, key=f"plot_main_{chart_id}")
        elif viz_mode == "Atmosphère":
            fig_atmo = create_jupiter_atmosphere_visualization(df_filtered, analyzer, chart_id)
            st.plotly_chart(fig_atmo, use_container_width=True, key=f"plot_atmo_{chart_id}")
        else:
            fig_moons = create_moon_orbits_visualization(chart_id)
            st.plotly_chart(fig_moons, use_container_width=True, key=f"plot_moons_{chart_id}")
        
        with st.expander("ℹ️ À propos de Jupiter", expanded=False):
            st.markdown(f"""
            <div class="info-box">
                <h4>{analyzer.config['description']}</h4>
                <p><strong>Unité:</strong> {analyzer.config['unit']}</p>
                <p><strong>Plage typique:</strong> {analyzer.config['range'][0]} - {analyzer.config['range'][1]} {analyzer.config['unit']}</p>
                <p><strong>Année jovienne:</strong> 11.86 années terrestres</p>
                <p><strong>Période de rotation:</strong> 9.9 heures (la plus rapide)</p>
                <p><strong>Distance au Soleil:</strong> 5.20 UA</p>
                <p><strong>Atmosphère:</strong> 90% H₂, 10% He</p>
                <p><strong>Lunes galiléennes:</strong> Io, Europe, Ganymède, Callisto</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("## 🌪️ Atmosphère et Météo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Structure atmosphérique")
            fig_atmo = create_jupiter_atmosphere_visualization(df, analyzer, f"atmo_{selected_type}")
            st.plotly_chart(fig_atmo, use_container_width=True, key="plot_atmo_detail")
        
        with col2:
            st.markdown("### Caractéristiques")
            st.markdown("""
            <div class="info-box">
                <h4>🌡️ Température par couche</h4>
                <ul>
                    <li><strong>Nuages d'ammoniac:</strong> -145°C</li>
                    <li><strong>Nuages d'hydrosulfure:</strong> -100°C</li>
                    <li><strong>Nuages d'eau:</strong> -50°C</li>
                    <li><strong>Profondeur:</strong> +20,000°C (noyau)</li>
                </ul>
                <h4>💨 Vents</h4>
                <ul>
                    <li>Courants-jets: jusqu'à 600 km/h</li>
                    <li>Super-rotation: atmosphère tourne plus vite</li>
                    <li>Structure en bandes alternées</li>
                </ul>
                <h4>🔴 Grande Tache Rouge</h4>
                <ul>
                    <li>Dimensions: ~16,000 km</li>
                    <li>Vitesse du vent: 430 km/h</li>
                    <li>Âge: >350 ans</li>
                    <li>Rétrécissement: ~0.1%/an</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Évolution de la GTR
        st.markdown("### 📈 Évolution de la Grande Tache Rouge")
        
        fig_gtr = create_gtr_evolution_chart(df, "gtr_evolution")
        st.plotly_chart(fig_gtr, use_container_width=True, key="plot_gtr")
    
    with tab3:
        st.markdown("## 🌕 Système Lunaire")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Orbites des lunes galiléennes")
            fig_moons = create_moon_orbits_visualization("moons_orbit")
            st.plotly_chart(fig_moons, use_container_width=True, key="plot_moons_detail")
        
        with col2:
            st.markdown("### Caractéristiques des lunes")
            
            moons_data = {
                "Io": {
                    "icon": "🌋",
                    "diameter": "3,642 km",
                    "distance": "421,800 km",
                    "period": "1.77 jours",
                    "feature": "Volcans actifs"
                },
                "Europa": {
                    "icon": "🌊",
                    "diameter": "3,122 km",
                    "distance": "671,100 km",
                    "period": "3.55 jours",
                    "feature": "Océan sous-glaciaire"
                },
                "Ganymède": {
                    "icon": "🪨",
                    "diameter": "5,268 km",
                    "distance": "1,070,400 km",
                    "period": "7.15 jours",
                    "feature": "Plus grande lune du SS"
                },
                "Callisto": {
                    "icon": "❄️",
                    "diameter": "4,821 km",
                    "distance": "1,882,700 km",
                    "period": "16.69 jours",
                    "feature": "Surface cratérisée"
                }
            }
            
            for moon, data in moons_data.items():
                st.markdown(f"""
                <div class="event-marker">
                    <span class="mission-badge">{data['icon']} {moon}</span><br>
                    <strong>Diamètre:</strong> {data['diameter']}<br>
                    <strong>Distance:</strong> {data['distance']}<br>
                    <strong>Période:</strong> {data['period']}<br>
                    <strong>Caractéristique:</strong> {data['feature']}
                </div>
                """, unsafe_allow_html=True)
        
        # Influence des lunes
        st.markdown("### 📊 Influence gravitationnelle")
        
        fig_moon_influence = create_moon_influence_chart(df, "moon_influence")
        st.plotly_chart(fig_moon_influence, use_container_width=True, key="plot_moon_influence")
    
    with tab4:
        st.markdown("## 🚀 Exploration Jovienne")
        
        if hasattr(analyzer, 'events') and analyzer.events:
            fig_timeline = create_mission_timeline(analyzer.events, "mission_timeline")
            if fig_timeline:
                st.plotly_chart(fig_timeline, use_container_width=True, key="plot_timeline")
            
            col1, col2, col3 = st.columns(3)
            
            df_events = pd.DataFrame(analyzer.events)
            missions_df = df_events[df_events['type'] != 'storm']
            
            with col1:
                st.markdown("### Types de missions")
                mission_counts = missions_df['type'].value_counts()
                fig_pie = go.Figure(data=[go.Pie(
                    labels=mission_counts.index,
                    values=mission_counts.values,
                    hole=.3,
                    marker_colors=['#FFD700', '#B8A86D', '#1E90FF', '#32CD32', '#FFA07A']
                )])
                fig_pie.update_layout(template='plotly_dark', height=300)
                st.plotly_chart(fig_pie, use_container_width=True, key="plot_pie_missions")
            
            with col2:
                st.markdown("### Missions clés")
                key_missions = missions_df[missions_df['severity'] == 'historique'].sort_values('year')
                for _, mission in key_missions.iterrows():
                    st.markdown(f"**{int(mission['year'])}:** {mission['event']}")
            
            with col3:
                st.markdown("### Missions futures")
                st.markdown("""
                - **Europa Clipper** (2024) : étude d'Europe
                - **JUICE** (2023) : orbiteur de Ganymède
                - **Concepts avancés** : sonde atmosphérique
                """)
            
            st.markdown("### 📋 Chronologie détaillée")
            
            filtered_events = missions_df.sort_values('year')
            for _, event in filtered_events.iterrows():
                severity_color = {
                    'historique': '#FFD700',
                    'majeur': '#B8A86D'
                }.get(event['severity'], '#808080')
                
                st.markdown(f"""
                <div class="event-marker">
                    <span class="mission-badge">Année {event['jupiter_year']:.1f}</span>
                    <strong style="color: {severity_color};">{int(event['year'])}</strong> - 
                    {event['event']}
                </div>
                """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("## 📊 Statistiques Joviennes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Résumé statistique")
            stats_df = df[['Base_Value', 'Jupiter_Index', 'Storm_Intensity', 
                          'Magnetic_Activity', 'Observation_Quality']].describe()
            st.dataframe(stats_df.style.format("{:.2f}"), use_container_width=True)
        
        with col2:
            fig_dist = make_subplots(rows=2, cols=1, 
                                     subplot_titles=('Distribution', 'Box Plot'))
            
            fig_dist.add_trace(
                go.Histogram(x=df['Base_Value'], nbinsx=20,
                            marker_color=analyzer.config['color']),
                row=1, col=1
            )
            
            fig_dist.add_trace(
                go.Box(y=df['Base_Value'], name='Box Plot',
                      marker_color=analyzer.config['color'],
                      boxmean=True),
                row=2, col=1
            )
            
            fig_dist.update_layout(template='plotly_dark', height=500)
            st.plotly_chart(fig_dist, use_container_width=True, key="plot_distribution")
        
        df['Century'] = (df['Earth_Year'] // 100) * 100
        century_stats = df.groupby('Century').agg({
            'Base_Value': 'mean',
            'Observation_Quality': 'mean',
            'Storm_Intensity': 'mean'
        }).round(2)
        
        century_stats.columns = ['Moyenne', 'Qualité obs.', 'Intensité tempêtes']
        st.markdown("### Analyse par siècle")
        st.dataframe(century_stats, use_container_width=True)
    
    with tab6:
        st.markdown("## 🔮 Missions Futures et Exploration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Missions planifiées")
            st.markdown("""
            <div class="info-box">
                <h4>🚀 Europa Clipper (2024-2030)</h4>
                <p>Étude détaillée d'Europe, recherche d'océans</p>
                
                <h4>🛰️ JUICE (2023-2033)</h4>
                <p>Exploration de Ganymède, Callisto, Europe</p>
                
                <h4>🎈 Sondes atmosphériques</h4>
                <p>Étude in-situ de l'atmosphère profonde</p>
                
                <h4>🤖 Lander lunaire</h4>
                <p>Atterrisseur sur Europe ou Ganymède (concept)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Défis technologiques")
            
            challenges = [
                ("Radiation intense", "Ceintures radiatives", 95),
                ("Distance", "Communication ~40-50 min", 80),
                ("Atmosphère", "Pression inconnue", 60),
                ("Température", "-145°C à surface", 70),
                ("Propulsion", "Durée du voyage", 75)
            ]
            
            for challenge, desc, value in challenges:
                st.progress(value/100, text=f"**{challenge}:** {desc}")
        
        st.markdown("### 🔬 Recherche scientifique")
        
        research_areas = [
            ("🌊 Océans souterrains", "Europa et Ganymède pourraient abriter la vie"),
            ("🌋 Volcanisme", "Io, lune la plus volcanique"),
            ("🌪️ Météo", "Comprendre les tempêtes séculaires"),
            ("🧲 Magnétosphère", "Laboratoire naturel unique")
        ]
        
        for area, desc in research_areas:
            st.markdown(f"**{area}:** {desc}")
        
        st.markdown("""
        <div class="info-box">
            <h4>🎯 Objectifs scientifiques</h4>
            <ul>
                <li>Comprendre la formation du système jovien</li>
                <li>Rechercher des environnements habitables</li>
                <li>Étudier la dynamique atmosphérique</li>
                <li>Analyser le champ magnétique</li>
                <li>Préparer l'exploration future</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer avec téléchargement
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="jupiter_data.csv" style="text-decoration: none; color: #D8CA9D;">📥 Télécharger CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    with col2:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Jupiter Data')
        excel_data = output.getvalue()
        b64_excel = base64.b64encode(excel_data).decode()
        href_excel = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="jupiter_data.xlsx" style="text-decoration: none; color: #D8CA9D;">📊 Télécharger Excel</a>'
        st.markdown(href_excel, unsafe_allow_html=True)
    
    with col3:
        st.markdown('<a href="#" style="text-decoration: none; color: #D8CA9D;">📑 Rapport PDF</a>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<span class="royal-badge">♃ Roi des Planètes</span>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
