from dash import Dash
from layouts import create_layout
from callbacks import register_callbacks
from data_loader import load_data
from api import configure_genai

def main():
    # Configure AI
    configure_genai()
    
    # Load data
    relaxed_df = load_data("EEG_Relaxed.csv")
    stressed_df = load_data("EEG_Stressed.csv")
    active_df = load_data("EEG_Active.csv")
    
    # Create app
    app = Dash(__name__)
    app.title = "EEG Frequency Dashboard"
    
    # Setup layout
    app.layout = create_layout(relaxed_df)
    
    # Register callbacks
    register_callbacks(app, relaxed_df, stressed_df, active_df)
    
    # Run server
    app.run_server(debug=True)

if __name__ == '__main__':
    main()