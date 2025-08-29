import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pybaseball import *
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class BlueJaysAnalysis:
    def __init__(self):
        self.team_code = 'TOR'
        self.current_season = 2024
        self.seasons = list(range(2000, 2025))  # Last 24 seasons
        
    def get_team_batting_stats(self, season):
        #Get team batting statistics for a given season
        try:
            data = team_batting(season, league='AL')
            return data[data['Team'] == self.team_code]
        except Exception as e:
            print(f"Error fetching batting data for {season}: {e}")
            return None
    
    def get_team_pitching_stats(self, season):
        #Get team pitching statistics for a given season
        try:
            data = team_pitching(season, league='AL')
            return data[data['Team'] == self.team_code]
        except Exception as e:
            print(f"Error fetching pitching data for {season}: {e}")
            return None
    
    def get_player_stats(self, season, min_pa=100):
        #Get individual player statistics for Blue Jays
        try:
            # Get all AL batting stats and filter for Blue Jays
            batting_data = batting_stats(season, qual=min_pa)
            # Filter for Blue Jays players (this might need adjustment based on data structure)
            blue_jays_batting = batting_data[batting_data['Team'] == self.team_code]
            return blue_jays_batting
        except Exception as e:
            print(f"Error fetching player data for {season}: {e}")
            return None
    
    def analyze_offensive_performance(self):
        #Analyze Blue Jays offensive performance over multiple seasons
        batting_data = []
        
        for season in self.seasons:
            team_stats = self.get_team_batting_stats(season)
            if team_stats is not None and not team_stats.empty:
                team_stats['Season'] = season
                batting_data.append(team_stats)
        
        if not batting_data:
            print("No batting data available")
            return None
            
        combined_batting = pd.concat(batting_data, ignore_index=True)
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Toronto Blue Jays Offensive Performance Trends', fontsize=16, fontweight='bold')
        
        # Key offensive metrics
        metrics = [
            ('AVG', 'Batting Average'),
            ('OBP', 'On-Base Percentage'), 
            ('SLG', 'Slugging Percentage'),
            ('HR', 'Home Runs')
        ]
        
        for i, (metric, title) in enumerate(metrics):
            ax = axes[i//2, i%2]
            if metric in combined_batting.columns:
                ax.plot(combined_batting['Season'], combined_batting[metric], 
                       marker='o', linewidth=2, markersize=8)
                ax.set_title(title, fontweight='bold')
                ax.set_xlabel('Season')
                ax.set_ylabel(metric)
                ax.grid(True, alpha=0.3)
                
                # Add trend line
                z = np.polyfit(combined_batting['Season'], combined_batting[metric], 1)
                p = np.poly1d(z)
                ax.plot(combined_batting['Season'], p(combined_batting['Season']), 
                       "--", alpha=0.7, color='red')
        
        plt.tight_layout()
        plt.show()
        
        return combined_batting
    
    def analyze_pitching_performance(self):
        #Analyze Blue Jays pitching performance over multiple seasons
        pitching_data = []
        
        for season in self.seasons:
            team_stats = self.get_team_pitching_stats(season)
            if team_stats is not None and not team_stats.empty:
                team_stats['Season'] = season
                pitching_data.append(team_stats)
        
        if not pitching_data:
            print("No pitching data available")
            return None
            
        combined_pitching = pd.concat(pitching_data, ignore_index=True)
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Toronto Blue Jays Pitching Performance Trends', fontsize=16, fontweight='bold')
        
        # Key pitching metrics
        metrics = [
            ('ERA', 'Earned Run Average'),
            ('WHIP', 'Walks + Hits per Inning Pitched'),
            ('K/9', 'Strikeouts per 9 Innings'),
            ('BB/9', 'Walks per 9 Innings')
        ]
        
        for i, (metric, title) in enumerate(metrics):
            ax = axes[i//2, i%2]
            if metric in combined_pitching.columns:
                ax.plot(combined_pitching['Season'], combined_pitching[metric], 
                       marker='o', linewidth=2, markersize=8, color='orange')
                ax.set_title(title, fontweight='bold')
                ax.set_xlabel('Season')
                ax.set_ylabel(metric)
                ax.grid(True, alpha=0.3)
                
                # Add trend line
                z = np.polyfit(combined_pitching['Season'], combined_pitching[metric], 1)
                p = np.poly1d(z)
                ax.plot(combined_pitching['Season'], p(combined_pitching['Season']), 
                       "--", alpha=0.7, color='red')
        
        plt.tight_layout()
        plt.show()
        
        return combined_pitching
    
    def player_performance_analysis(self, season=2024):
        #Analyze individual player performance
        player_data = self.get_player_stats(season)
        
        if player_data is None or player_data.empty:
            print(f"No player data available for {season}")
            return None
        
        # Top performers analysis
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Toronto Blue Jays Top Performers - {season}', fontsize=16, fontweight='bold')
        
        # Top 10 by different metrics
        metrics = [
            ('AVG', 'Batting Average'),
            ('HR', 'Home Runs'),
            ('RBI', 'RBIs'),
            ('OPS', 'OPS')
        ]
        
        for i, (metric, title) in enumerate(metrics):
            ax = axes[i//2, i%2]
            if metric in player_data.columns:
                top_players = player_data.nlargest(10, metric)
                bars = ax.barh(range(len(top_players)), top_players[metric])
                ax.set_yticks(range(len(top_players)))
                ax.set_yticklabels(top_players['Name'])
                ax.set_title(f'Top 10 - {title}', fontweight='bold')
                ax.set_xlabel(metric)
                
                # Add value labels on bars
                for j, bar in enumerate(bars):
                    width = bar.get_width()
                    ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                           f'{width:.3f}' if metric in ['AVG', 'OPS'] else f'{int(width)}',
                           ha='left', va='center', fontsize=8)
        
        plt.tight_layout()
        plt.show()
        
        return player_data
    
    def run_comprehensive_analysis(self):
        #Run a comprehensive analysis of Blue Jays performance
        print("Toronto Blue Jays Baseball Operations Analysis")
        print("=" * 50)
        
        # Offensive Analysis
        print("\n Analyzing Offensive Performance...")
        batting_trends = self.analyze_offensive_performance()
        
        if batting_trends is not None:
            print("\nOffensive Performance Summary (Latest Season):")
            latest_batting = batting_trends[batting_trends['Season'] == batting_trends['Season'].max()]
            key_stats = ['AVG', 'OBP', 'SLG', 'HR', 'RBI', 'R']
            for stat in key_stats:
                if stat in latest_batting.columns:
                    value = latest_batting[stat].iloc[0]
                    print(f"  {stat}: {value}")
        
        # Pitching Analysis
        print("\n Analyzing Pitching Performance...")
        pitching_trends = self.analyze_pitching_performance()
        
        if pitching_trends is not None:
            print("\nPitching Performance Summary (Latest Season):")
            latest_pitching = pitching_trends[pitching_trends['Season'] == pitching_trends['Season'].max()]
            key_stats = ['ERA', 'WHIP', 'K/9', 'BB/9', 'SV']
            for stat in key_stats:
                if stat in latest_pitching.columns:
                    value = latest_pitching[stat].iloc[0]
                    print(f"  {stat}: {value:.3f}" if isinstance(value, (int, float)) else f"  {stat}: {value}")
        
        # Player Analysis
        print("\n Analyzing Individual Player Performance...")
        player_stats = self.player_performance_analysis()
        
        if player_stats is not None:
            print(f"\nTop 3 Players by OPS:")
            if 'OPS' in player_stats.columns:
                top_ops = player_stats.nlargest(3, 'OPS')[['Name', 'OPS', 'AVG', 'HR', 'RBI']]
                for idx, player in top_ops.iterrows():
                    print(f"  {player['Name']}: OPS {player['OPS']:.3f}, AVG {player['AVG']:.3f}, HR {player['HR']}, RBI {player['RBI']}")
        
        print("\n Analysis Complete")

# Example usage
if __name__ == "__main__":
    # Initialize the analysis
    blue_jays = BlueJaysAnalysis()
    
    # Run comprehensive analysis
    blue_jays.run_comprehensive_analysis()
    
    # You can also run individual analyses:
    # batting_data = blue_jays.analyze_offensive_performance()
    # pitching_data = blue_jays.analyze_pitching_performance()

    # player_data = blue_jays.player_performance_analysis(2024)
