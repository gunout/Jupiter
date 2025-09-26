import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class JupiterDataAnalyzer:
    def __init__(self, data_type):
        self.data_type = data_type
        self.colors = ['#D8CA9D', '#B8A86D', '#9B8E64', '#C9B27C', '#E0D0A8',
                      '#A8996D', '#D4C49E', '#F0E6C8', '#8C7C5E', '#B5A885']
        
        self.start_year = 1610  # Découverte des lunes galiléennes
        self.end_year = 2025
        
        # Configuration spécifique pour chaque type de données joviennes
        self.config = self._get_jupiter_config()
        
    def _get_jupiter_config(self):
        """Retourne la configuration spécifique pour chaque type de données joviennes"""
        configs = {
            "atmospheric_temperature": {
                "base_value": -145,
                "cycle_years": 11.86,  # Année jovienne
                "amplitude": 20,
                "trend": "stable",
                "unit": "°C",
                "description": "Température atmosphérique"
            },
            "wind_speeds": {
                "base_value": 150,
                "cycle_years": 11.86,
                "amplitude": 100,
                "trend": "jet_streams",
                "unit": "km/h",
                "description": "Vitesse des vents"
            },
            "great_red_spot": {
                "base_value": 16000,
                "cycle_years": 11.86,
                "amplitude": 2000,
                "trend": "shrinking",
                "unit": "km diamètre",
                "description": "Grande Tache Rouge"
            },
            "magnetic_field": {
                "base_value": 4200000,
                "cycle_years": 11.86,
                "amplitude": 100000,
                "trend": "stable",
                "unit": "nT",
                "description": "Champ magnétique"
            },
            "radiation_belts": {
                "base_value": 3500,
                "cycle_years": 11.86,
                "amplitude": 500,
                "trend": "variable",
                "unit": "rads/h",
                "description": "Ceintures de radiation"
            },
            "auroral_activity": {
                "base_value": 80,
                "cycle_years": 11.86,
                "amplitude": 40,
                "trend": "solar_dependent",
                "unit": "intensité",
                "description": "Activité aurorale"
            },
            "ring_system": {
                "base_value": 30,
                "cycle_years": 11.86,
                "amplitude": 5,
                "trend": "stable",
                "unit": "albédo",
                "description": "Système d'anneaux"
            },
            "moons_activity": {
                "base_value": 65,
                "cycle_years": 11.86,
                "amplitude": 20,
                "trend": "volcanic",
                "unit": "index",
                "description": "Activité des lunes"
            },
            "atmospheric_composition": {
                "base_value": 90,
                "cycle_years": 11.86,
                "amplitude": 5,
                "trend": "stable",
                "unit": "% hydrogène",
                "description": "Composition atmosphérique"
            },
            "orbital_parameters": {
                "base_value": 5.20,
                "cycle_years": 11.86,
                "amplitude": 0.20,
                "trend": "stable",
                "unit": "UA",
                "description": "Distance au Soleil"
            },
            # Configuration par défaut
            "default": {
                "base_value": 100,
                "cycle_years": 11.86,
                "amplitude": 20,
                "trend": "stable",
                "unit": "Unités",
                "description": "Données joviennes génériques"
            }
        }
        
        return configs.get(self.data_type, configs["default"])
    
    def generate_jupiter_data(self):
        """Génère des données joviennes simulées basées sur les caractéristiques uniques de Jupiter"""
        print(f"♃ Génération des données joviennes pour {self.config['description']}...")
        
        # Créer une base de données annuelle (en années terrestres) - CORRIGÉ
        # Utiliser des années directement au lieu de dates pandas pour éviter l'overflow
        years = list(range(self.start_year, self.end_year + 1))
        
        data = {'Earth_Year': years}
        data['Jupiter_Year'] = self._earth_to_jupiter_years(years)
        data['Solar_Distance'] = self._simulate_solar_distance(years)
        
        # Données principales basées sur les cycles joviens
        data['Base_Value'] = self._simulate_jupiter_cycle(years)
        data['Seasonal_Variation'] = self._simulate_seasonal_variation(years)
        data['Atmospheric_Storms'] = self._simulate_atmospheric_storms(years)
        data['Magnetic_Activity'] = self._simulate_magnetic_activity(years)
        
        # Variations spécifiques à Jupiter
        data['Great_Red_Spot_Evolution'] = self._simulate_great_red_spot(years)
        data['Radiation_Variations'] = self._simulate_radiation_variations(years)
        data['Moon_Influences'] = self._simulate_moon_influences(years)
        
        # Données dérivées
        data['Smoothed_Value'] = self._simulate_smoothed_data(years)
        data['Short_Term_Variation'] = self._simulate_short_term_variation(years)
        data['Long_Term_Trend'] = self._simulate_long_term_trend(years)
        
        # Indices joviens complémentaires
        data['Jupiter_Index'] = self._simulate_jupiter_index(years)
        data['Observation_Quality'] = self._simulate_observation_quality(years)
        data['Future_Prediction'] = self._simulate_future_prediction(years)
        
        df = pd.DataFrame(data)
        
        # Ajouter des événements joviens historiques
        self._add_jupiter_events(df)
        
        return df
    
    def _earth_to_jupiter_years(self, years):
        """Convertit les années terrestres en années joviennes"""
        jupiter_years = []
        jupiter_year_duration = 11.86  # Années terrestres
        
        for earth_year in years:
            jupiter_year = (earth_year - self.start_year) / jupiter_year_duration
            jupiter_years.append(jupiter_year)
        
        return jupiter_years
    
    def _simulate_solar_distance(self, years):
        """Simule la distance au Soleil"""
        distances = []
        for earth_year in years:
            # Distance moyenne de Jupiter : 5.20 UA
            base_distance = 5.20
            # Légère variation due à l'excentricité orbitale
            variation = 0.05 * np.sin(2 * np.pi * (earth_year - self.start_year) / 11.86)
            distance = base_distance + variation
            distances.append(distance)
        
        return distances
    
    def _simulate_jupiter_cycle(self, years):
        """Simule le cycle jovien principal"""
        base_value = self.config["base_value"]
        cycle_years = self.config["cycle_years"]
        amplitude = self.config["amplitude"]
        
        values = []
        for earth_year in years:
            # Cycle saisonnier jovien (11.86 années terrestres)
            jupiter_phase = (earth_year - self.start_year) % cycle_years
            seasonal_cycle = np.sin(2 * np.pi * jupiter_phase / cycle_years)
            
            # Cycle des taches (environ 10-15 ans terrestres)
            spot_cycle_years = 12.5
            spot_phase = (earth_year - self.start_year) % spot_cycle_years
            spot_cycle = np.cos(2 * np.pi * spot_phase / spot_cycle_years)
            
            # Cycle solaire influençant Jupiter
            solar_cycle_years = 11.0
            solar_phase = (earth_year - self.start_year) % solar_cycle_years
            solar_cycle = np.sin(2 * np.pi * solar_phase / solar_cycle_years)
            
            if self.config["trend"] == "jet_streams":
                value = base_value + amplitude * (0.6 * seasonal_cycle + 0.4 * spot_cycle)
            elif self.config["trend"] == "shrinking":
                # Tendance à la réduction pour la Grande Tache Rouge
                years_since_start = earth_year - self.start_year
                shrinkage = -0.01 * years_since_start
                value = base_value + amplitude * seasonal_cycle + shrinkage
            elif self.config["trend"] == "solar_dependent":
                value = base_value + amplitude * (0.7 * solar_cycle + 0.3 * seasonal_cycle)
            elif self.config["trend"] == "volcanic":
                # Activité volcanique des lunes (cycle irrégulier)
                volcanic_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 7.3)
                value = base_value + amplitude * volcanic_cycle
            else:
                value = base_value + amplitude * seasonal_cycle
            
            # Bruit naturel jovien
            noise = np.random.normal(0, amplitude * 0.1)
            values.append(value + noise)
        
        return values
    
    def _simulate_seasonal_variation(self, years):
        """Simule les variations saisonnières (faibles sur Jupiter)"""
        variations = []
        for earth_year in years:
            # Variation saisonnière faible (axe peu incliné)
            seasonal_variation = 0.1 * np.sin(2 * np.pi * (earth_year - self.start_year) / 11.86)
            variations.append(1 + seasonal_variation)
        
        return variations
    
    def _simulate_atmospheric_storms(self, years):
        """Simule l'activité des tempêtes atmosphériques"""
        storm_activities = []
        for earth_year in years:
            # Cycles de tempêtes multiples
            short_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 3.2)
            medium_cycle = np.cos(2 * np.pi * (earth_year - self.start_year) / 7.5)
            long_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 15.8)
            
            storm_activity = 1.0 + 0.3 * short_cycle + 0.2 * medium_cycle + 0.1 * long_cycle
            storm_activities.append(storm_activity)
        
        return storm_activities
    
    def _simulate_magnetic_activity(self, years):
        """Simule l'activité magnétique"""
        magnetic_activities = []
        for earth_year in years:
            # Cycle magnétique lié à la rotation rapide
            magnetic_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 9.7)
            magnetic_activity = 1.0 + 0.2 * magnetic_cycle
            magnetic_activities.append(magnetic_activity)
        
        return magnetic_activities
    
    def _simulate_great_red_spot(self, years):
        """Simule l'évolution de la Grande Tache Rouge"""
        spot_evolutions = []
        for earth_year in years:
            years_since_start = earth_year - self.start_year
            
            # Réduction graduelle documentée
            if earth_year < 1800:
                size_factor = 1.8  # Plus grande historiquement
            elif earth_year < 1900:
                size_factor = 1.5
            elif earth_year < 2000:
                size_factor = 1.2
            else:
                size_factor = 1.0 - 0.001 * (earth_year - 2000)
            
            # Variations à court terme
            short_term = 0.1 * np.sin(2 * np.pi * (earth_year - self.start_year) / 5.3)
            spot_evolution = size_factor * (1 + short_term)
            spot_evolutions.append(spot_evolution)
        
        return spot_evolutions
    
    def _simulate_radiation_variations(self, years):
        """Simule les variations des ceintures de radiation"""
        radiation_levels = []
        for earth_year in years:
            # Influencé par le vent solaire et l'activité magnétique
            solar_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 11.0)
            magnetic_cycle = np.cos(2 * np.pi * (earth_year - self.start_year) / 9.7)
            
            radiation_level = 1.0 + 0.3 * solar_cycle + 0.2 * magnetic_cycle
            radiation_levels.append(radiation_level)
        
        return radiation_levels
    
    def _simulate_moon_influences(self, years):
        """Simule les influences des lunes galiléennes"""
        moon_influences = []
        for earth_year in years:
            # Cycles des principales lunes
            io_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 1.77)  # Io
            europa_cycle = np.cos(2 * np.pi * (earth_year - self.start_year) / 3.55)  # Europe
            ganymede_cycle = np.sin(2 * np.pi * (earth_year - self.start_year) / 7.15)  # Ganymède
            callisto_cycle = np.cos(2 * np.pi * (earth_year - self.start_year) / 16.69)  # Callisto
            
            moon_influence = 1.0 + 0.15 * io_cycle + 0.1 * europa_cycle + 0.05 * ganymede_cycle + 0.03 * callisto_cycle
            moon_influences.append(moon_influence)
        
        return moon_influences
    
    def _simulate_smoothed_data(self, years):
        """Simule des données lissées"""
        base_cycle = self._simulate_jupiter_cycle(years)
        
        smoothed = []
        window_size = 5  # 5 années terrestres
        
        for i in range(len(base_cycle)):
            start_idx = max(0, i - window_size//2)
            end_idx = min(len(base_cycle), i + window_size//2 + 1)
            window = base_cycle[start_idx:end_idx]
            smoothed.append(np.mean(window))
        
        return smoothed
    
    def _simulate_short_term_variation(self, years):
        """Simule les variations à court terme"""
        variations = []
        for earth_year in years:
            # Variation rapide due à la rotation (9.9 heures) - ajustée pour l'échelle annuelle
            rapid_variation = 0.05 * np.sin(2 * np.pi * (earth_year - self.start_year) / 0.1)  # Ajusté
            variations.append(1 + rapid_variation)
        
        return variations
    
    def _simulate_long_term_trend(self, years):
        """Simule les tendances à long terme"""
        trends = []
        for earth_year in years:
            years_since_start = earth_year - self.start_year
            
            if self.config["trend"] == "shrinking":
                trend = 1.0 - 0.0005 * years_since_start  # Réduction lente
            else:
                trend = 1.0 + 0.0001 * years_since_start  # Stabilité générale
            
            trends.append(trend)
        
        return trends
    
    def _simulate_jupiter_index(self, years):
        """Simule un indice jovien composite"""
        indices = []
        base_cycle = self._simulate_jupiter_cycle(years)
        storm_activity = self._simulate_atmospheric_storms(years)
        magnetic_activity = self._simulate_magnetic_activity(years)
        
        for i in range(len(years)):
            # Indice composite pondéré
            index = (base_cycle[i] * 0.4 + 
                    storm_activity[i] * 30 * 0.3 +
                    magnetic_activity[i] * 1000 * 0.3)
            indices.append(index)
        
        return indices
    
    def _simulate_observation_quality(self, years):
        """Simule la qualité d'observation (0-100)"""
        qualities = []
        for earth_year in years:
            # Amélioration progressive des techniques d'observation
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
            
            # Variation due à la position orbitale
            orbital_variation = 5 * np.sin(2 * np.pi * (earth_year - self.start_year) / 11.86)
            qualities.append(min(100, quality + orbital_variation))
        
        return qualities
    
    def _simulate_future_prediction(self, years):
        """Simule des prédictions futures"""
        predictions = []
        base_cycle = self._simulate_jupiter_cycle(years)
        long_term_trend = self._simulate_long_term_trend(years)
        
        for i, earth_year in enumerate(years):
            current_value = base_cycle[i]
            trend_factor = long_term_trend[i]
            
            if earth_year > 2020:  # Période de prédiction
                # Ajouter une incertitude croissante
                years_since_2020 = earth_year - 2020
                uncertainty = 0.02 * years_since_2020
                prediction = current_value * trend_factor * (1 + np.random.normal(0, uncertainty))
            else:
                prediction = current_value
            
            predictions.append(prediction)
        
        return predictions
    
    def _add_jupiter_events(self, df):
        """Ajoute des événements joviens historiques significatifs"""
        for i, row in df.iterrows():
            earth_year = row['Earth_Year']
            
            # Événements d'observation de Jupiter
            if earth_year == 1610:
                # Galilée découvre les lunes galiléennes
                df.loc[i, 'Observation_Quality'] = 15
                df.loc[i, 'Moons_Activity'] = 50  # Découverte majeure
            
            elif earth_year == 1665:
                # Première observation de la Grande Tache Rouge
                df.loc[i, 'Great_Red_Spot_Evolution'] = 1.8  # Taille initiale
            
            elif earth_year == 1831:
                # Observations détaillées des bandes atmosphériques
                df.loc[i, 'Observation_Quality'] = 30
            
            elif earth_year == 1973:
                # Pioneer 10 - premier survol
                df.loc[i, 'Observation_Quality'] = 70
                df.loc[i, 'Radiation_Variations'] = 1.5  # Découverte des ceintures
            
            elif earth_year == 1979:
                # Voyager 1 et 2
                df.loc[i, 'Observation_Quality'] = 85
                df.loc[i, 'Atmospheric_Storms'] = 1.8  # Tempêtes détaillées
                df.loc[i, 'Moons_Activity'] = 80  # Volcans sur Io
            
            elif earth_year == 1995:
                # Galileo - insertion orbitale
                df.loc[i, 'Observation_Quality'] = 95
                df.loc[i, 'Base_Value'] *= 1.3  # Données approfondies
            
            elif earth_year == 2000:
                # Cassini survole Jupiter
                df.loc[i, 'Observation_Quality'] = 90
            
            elif earth_year == 2007:
                # New Horizons survole Jupiter
                df.loc[i, 'Observation_Quality'] = 92
            
            elif earth_year == 2016:
                # Juno arrive en orbite
                df.loc[i, 'Observation_Quality'] = 98
                df.loc[i, 'Magnetic_Activity'] = 1.4  # Champ magnétique complexe
                df.loc[i, 'Base_Value'] *= 1.5
            
            elif earth_year == 2021:
                # James Webb Telescope observations
                df.loc[i, 'Observation_Quality'] = 99
            
            # Grandes tempêtes documentées
            if earth_year in [1990, 2006, 2012, 2016, 2020]:
                df.loc[i, 'Atmospheric_Storms'] *= 1.5
                df.loc[i, 'Jupiter_Index'] *= 1.2
    
    def create_jupiter_analysis(self, df):
        """Crée une analyse complète des données joviennes"""
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(20, 28))
        
        # 1. Cycle jovien principal
        ax1 = plt.subplot(5, 2, 1)
        self._plot_jupiter_cycle(df, ax1)
        
        # 2. Qualité d'observation historique
        ax2 = plt.subplot(5, 2, 2)
        self._plot_observation_quality(df, ax2)
        
        # 3. Activité des tempêtes
        ax3 = plt.subplot(5, 2, 3)
        self._plot_storm_activity(df, ax3)
        
        # 4. Évolution de la Grande Tache Rouge
        ax4 = plt.subplot(5, 2, 4)
        self._plot_great_red_spot(df, ax4)
        
        # 5. Activité magnétique
        ax5 = plt.subplot(5, 2, 5)
        self._plot_magnetic_activity(df, ax5)
        
        # 6. Données lissées
        ax6 = plt.subplot(5, 2, 6)
        self._plot_smoothed_data_plot(df, ax6)
        
        # 7. Niveaux de radiation
        ax7 = plt.subplot(5, 2, 7)
        self._plot_radiation_levels(df, ax7)
        
        # 8. Influences des lunes
        ax8 = plt.subplot(5, 2, 8)
        self._plot_moon_influences(df, ax8)
        
        # 9. Indice jovien
        ax9 = plt.subplot(5, 2, 9)
        self._plot_jupiter_index(df, ax9)
        
        # 10. Prédictions futures
        ax10 = plt.subplot(5, 2, 10)
        self._plot_future_predictions(df, ax10)
        
        plt.suptitle(f'Analyse des Données Joviennes: {self.config["description"]} ({self.start_year}-{self.end_year})', 
                    fontsize=16, fontweight='bold', color='#D8CA9D')
        plt.tight_layout()
        plt.savefig(f'jupiter_{self.data_type}_analysis.png', dpi=300, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.show()
        
        # Générer les insights
        self._generate_jupiter_insights(df)
    
    def _plot_jupiter_cycle(self, df, ax):
        """Plot du cycle jovien principal"""
        ax.plot(df['Earth_Year'], df['Base_Value'], label='Valeur de base', 
               linewidth=2, color='#D8CA9D', alpha=0.9)
        
        ax.set_title(f'Cycle Jovien Principal - {self.config["description"]}', 
                    fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel(self.config["unit"], color='#D8CA9D')
        ax.tick_params(axis='y', labelcolor='#D8CA9D')
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        
        # Ajouter des annotations pour les missions
        missions = {
            1610: 'Galilée\nlunes',
            1973: 'Pioneer 10\n1er survol',
            1979: 'Voyager\n1&2',
            1995: 'Galileo\norbite',
            2016: 'Juno\norbite polaire'
        }
        
        for year, label in missions.items():
            if year in df['Earth_Year'].values:
                y_val = df.loc[df['Earth_Year'] == year, 'Base_Value'].values[0]
                ax.annotate(label, xy=(year, y_val), xytext=(year, y_val*1.1),
                           arrowprops=dict(arrowstyle='->', color='yellow'),
                           color='yellow', fontsize=8, ha='center')
    
    def _plot_observation_quality(self, df, ax):
        """Plot de la qualité d'observation"""
        ax.fill_between(df['Earth_Year'], df['Observation_Quality'], alpha=0.7, 
                       color='#B8A86D', label='Qualité d\'observation')
        
        ax.set_title('Qualité d\'Observation Historique', fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel('Qualité (%)', color='#B8A86D')
        ax.set_xlabel('Année Terrestre', color='white')
        ax.set_ylim(0, 100)
        ax.tick_params(axis='y', labelcolor='#B8A86D')
        ax.tick_params(axis='x', labelcolor='white')
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
    
    def _plot_storm_activity(self, df, ax):
        """Plot de l'activité des tempêtes"""
        ax.plot(df['Earth_Year'], df['Atmospheric_Storms'], label='Activité des tempêtes', 
               color='#FF6347', alpha=0.7, linewidth=2)
        
        ax.set_title('Activité des Tempêtes Atmosphériques', fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel('Intensité relative', color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_great_red_spot(self, df, ax):
        """Plot de l'évolution de la Grande Tache Rouge"""
        ax.plot(df['Earth_Year'], df['Great_Red_Spot_Evolution'], label='Grande Tache Rouge', 
               linewidth=2, color='#FF4500')
        
        ax.set_title('Évolution de la Grande Tache Rouge', fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel('Taille relative', color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_magnetic_activity(self, df, ax):
        """Plot de l'activité magnétique"""
        ax.plot(df['Earth_Year'], df['Magnetic_Activity'], label='Activité magnétique', 
               linewidth=2, color='#1E90FF')
        
        ax.set_title('Activité Magnétique Jovienne', fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel('Intensité relative', color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_smoothed_data_plot(self, df, ax):
        """Plot des données lissées"""
        ax.plot(df['Earth_Year'], df['Base_Value'], label='Données brutes', 
               alpha=0.5, color='#B8A86D')
        ax.plot(df['Earth_Year'], df['Smoothed_Value'], label='Données lissées (5 ans)', 
               linewidth=2, color='#00FF7F')
        
        ax.set_title('Données Brutes vs Lissées', fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel(self.config["unit"], color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_radiation_levels(self, df, ax):
        """Plot des niveaux de radiation"""
        ax.fill_between(df['Earth_Year'], df['Radiation_Variations'], alpha=0.6, 
                       color='#FFD700', label='Ceintures de radiation')
        
        ax.set_title('Niveaux de Radiation Joviens', fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel('Intensité relative', color='white')
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_moon_influences(self, df, ax):
        """Plot des influences des lunes"""
        ax.plot(df['Earth_Year'], df['Moon_Influences'], label='Influences des lunes', 
               linewidth=2, color='#DA70D6')
        
        ax.set_title('Influences des Lunes Galiléennes', fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel('Influence relative', color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_jupiter_index(self, df, ax):
        """Plot de l'indice jovien composite"""
        ax.plot(df['Earth_Year'], df['Jupiter_Index'], label='Indice jovien composite', 
               linewidth=2, color='#00CED1')
        
        ax.set_title('Indice Jovien Composite', fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel('Valeur de l\'indice', color='white')
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_future_predictions(self, df, ax):
        """Plot des prédictions futures"""
        ax.plot(df['Earth_Year'], df['Base_Value'], label='Données historiques', 
               color='#B8A86D', alpha=0.7)
        ax.plot(df['Earth_Year'], df['Future_Prediction'], label='Projections', 
               linewidth=2, color='#00FFFF', linestyle='--')
        
        ax.axvline(x=2020, color='yellow', linestyle=':', alpha=0.7, label='Début des prédictions')
        
        ax.set_title('Données Historiques et Projections Futures', fontsize=12, fontweight='bold', color='#D8CA9D')
        ax.set_ylabel(self.config["unit"], color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _generate_jupiter_insights(self, df):
        """Génère des insights analytiques sur les données joviennes"""
        print(f"♃ INSIGHTS ANALYTIQUES - {self.config['description']}")
        print("=" * 70)
        
        # 1. Statistiques de base
        print("\n1. 📊 STATISTIQUES FONDAMENTALES:")
        avg_value = df['Base_Value'].mean()
        max_value = df['Base_Value'].max()
        min_value = df['Base_Value'].min()
        current_value = df['Base_Value'].iloc[-1]
        
        print(f"Valeur moyenne: {avg_value:.2f} {self.config['unit']}")
        print(f"Valeur maximale: {max_value:.2f} {self.config['unit']}")
        print(f"Valeur minimale: {min_value:.2f} {self.config['unit']}")
        print(f"Valeur actuelle: {current_value:.2f} {self.config['unit']}")
        
        # 2. Caractéristiques physiques
        print("\n2. 🪐 CARACTÉRISTIQUES PHYSIQUES:")
        print("• Masse: 317.8 × Terre (1.898 × 10²⁷ kg)")
        print("• Diamètre: 139,820 km (11 × Terre)")
        print("• Gravité: 24.79 m/s² (2.5 × Terre)")
        print("• Période de rotation: 9.9 heures (la plus rapide)")
        print("• Période orbitale: 11.86 années terrestres")
        
        # 3. Atmosphère et climat
        print("\n3. 🌪️ ATMOSPHÈRE ET CLIMAT:")
        print("• Composition: 90% H₂, 10% He (+ traces)")
        print("• Température: -145°C (niveau des nuages)")
        print("• Vents: jusqu'à 600 km/h (courants-jets)")
        print("• Pression: très élevée (noyau à 100 millions bars)")
        
        # 4. Système magnétique
        print("\n4. 🧲 SYSTÈME MAGNÉTIQUE:")
        print("• Champ magnétique: 20,000 × Terre (le plus puissant)")
        print("• Magnétosphère: plus grande structure du système solaire")
        print("• Aurores: les plus intenses observées")
        print("• Ceintures de radiation: dangereuses pour l'électronique")
        
        # 5. Lunes et anneaux
        print("\n5. 🌕 SYSTÈME DE LUNES ET ANNEAUX:")
        print("• Lunes connues: 95 (dont 4 galiléennes)")
        print("• Io: volcans les plus actifs du système solaire")
        print("• Europe: océan souterrain potentiellement habitable")
        print("• Anneaux: ténus, découverts par Voyager 1")
        
        # 6. Exploration historique
        print("\n6. 🚀 HISTORIQUE D'EXPLORATION:")
        print("• 1610: Galilée découvre les 4 lunes principales")
        print("• 1973: Pioneer 10 - premier survol")
        print("• 1979: Voyager 1 et 2 - découvertes majeures")
        print("• 1995-2003: Galileo - première mission en orbite")
        print("• 2016-présent: Juno - étude de la structure interne")
        
        # 7. Découvertes scientifiques majeures
        print("\n7. 🔍 DÉCOUVERTES MAJEURES:")
        print("• Grande Tache Rouge: tempête anticyclonique séculaire")
        print("• Anneaux joviens: système d'anneaux ténu")
        print("• Volcanisme sur Io: alimenté par les forces de marée")
        print("• Océan sur Europe: sous une couche de glace")
        print("• Champ magnétique complexe: asymétrique et puissant")
        
        # 8. Défis et perspectives
        print("\n8. 🔮 DÉFIS ET PERSPECTIVES:")
        print("• Radiation intense: défi pour les missions")
        print("• Mission Europa Clipper: étude de l'habitabilité")
        print("• JUICE (ESA): étude de Ganymède, Callisto, Europe")
        print("• Recherche de vie: dans les lunes océaniques")
        print("• Exploration humaine: lointaine mais envisagée")

def main():
    """Fonction principale pour l'analyse des données joviennes"""
    # Types de données joviennes disponibles
    jupiter_data_types = [
        "atmospheric_temperature", "wind_speeds", "great_red_spot", "magnetic_field",
        "radiation_belts", "auroral_activity", "ring_system", "moons_activity",
        "atmospheric_composition", "orbital_parameters"
    ]
    
    print("♃ ANALYSE DES DONNÉES NUMÉRIQUES DE JUPITER (1610-2025)")
    print("=" * 65)
    
    # Demander à l'utilisateur de choisir un type de données
    print("Types de données joviennes disponibles:")
    for i, data_type in enumerate(jupiter_data_types, 1):
        analyzer_temp = JupiterDataAnalyzer(data_type)
        print(f"{i}. {analyzer_temp.config['description']}")
    
    try:
        choix = int(input("\nChoisissez le numéro du type de données à analyser: "))
        if choix < 1 or choix > len(jupiter_data_types):
            raise ValueError
        selected_type = jupiter_data_types[choix-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection des vents atmosphériques par défaut.")
        selected_type = "wind_speeds"
    
    # Initialiser l'analyseur
    analyzer = JupiterDataAnalyzer(selected_type)
    
    # Générer les données
    jupiter_data = analyzer.generate_jupiter_data()
    
    # Sauvegarder les données
    output_file = f'jupiter_{selected_type}_data_1610_2025.csv'
    jupiter_data.to_csv(output_file, index=False)
    print(f"💾 Données sauvegardées: {output_file}")
    
    # Aperçu des données
    print("\n👀 Aperçu des données:")
    print(jupiter_data[['Earth_Year', 'Jupiter_Year', 'Base_Value', 'Observation_Quality', 'Jupiter_Index']].head())
    
    # Créer l'analyse
    print("\n📈 Création de l'analyse des données joviennes...")
    analyzer.create_jupiter_analysis(jupiter_data)
    
    print(f"\n✅ Analyse des données {analyzer.config['description']} terminée!")
    print(f"📊 Période: {analyzer.start_year}-{analyzer.end_year} (années terrestres)")
    print(f"♃ Couverture: ~{(2025-1610)/11.86:.1f} années joviennes")
    print("🌪️ Données: Atmosphère, magnétosphère, lunes, exploration")

if __name__ == "__main__":
    main()