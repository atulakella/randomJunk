import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import io

# Gemini API setup
genai.configure(api_key='AIzaSyD5HvoyjOQMIBNJRrFK3O4sxDap--BVU_Q')

def generate_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.replace('*', '') if response.text else "No response available."
    except Exception as e:
        return f"Error: {str(e)}"

# Load data
RELAXED_CSV_PATH = "EEG_Relaxed.csv"
STRESSED_CSV_PATH = "EEG_Stressed.csv"
ACTIVE_CSV_PATH = "EEG_Active.csv"

def load_data(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return pd.DataFrame()

relaxed_df = load_data(RELAXED_CSV_PATH)
stressed_df = load_data(STRESSED_CSV_PATH)
active_df = load_data(ACTIVE_CSV_PATH)

# Generate default frequency content
if not relaxed_df.empty:
    relaxed_freq = relaxed_df.iloc[0].to_dict()
    frequency_output_content = html.Ul([html.Li(f"{band}: {value:.4f}") for band, value in relaxed_freq.items()])
else:
    frequency_output_content = html.Div("Data not available.")

# Function to create charts
def create_bar_figure(df):
    if df.empty:
        return {}
    frequencies = df.iloc[0].to_dict()
    return px.bar(
        x=list(frequencies.keys()),
        y=list(frequencies.values()),
        labels={'x': 'Frequency Band', 'y': 'Value'},
        title='Frequency Bands (Relaxed State)',
        color=list(frequencies.keys()),
        color_discrete_sequence=['#F84BAE', '#C47300', '#F0EEE9', '#231630','#5700AE'],
    ).update_layout(
        plot_bgcolor='#2E1A47',
        paper_bgcolor='#2E1A47',
        font=dict(color='#F0EEE9')
    )

def create_pie_figure(df):
    if df.empty:
        return {}
    frequencies = df.iloc[0].to_dict()
    return px.pie(
        names=list(frequencies.keys()),
        values=list(frequencies.values()),
        title='Distribution of Frequency Bands (Relaxed State)',
        color=list(frequencies.keys()),
        color_discrete_sequence=['#F84BAE', '#C47300', '#F0EEE9', '#231630','#5700AE'],
    ).update_layout(
        plot_bgcolor='#2E1A47',
        paper_bgcolor='#2E1A47',
        font=dict(color='#F0EEE9')
    )

# Generate PDF report
def generate_pdf(name, age, relaxed_freq, stressed_freq, active_freq, bar_fig, pie_fig):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "TEST REPORTS")
    c.drawString(50, height - 80, "COGNILIFT.AI")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 120, f"Name: {name}")
    c.drawString(50, height - 140, f"Age: {age}")
    c.drawString(50, height - 160, f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.drawString(50, height - 200, "Frequency Analysis:")
    y = height - 220
    for state, freq in [("Relaxed", relaxed_freq), ("Stressed", stressed_freq), ("Active", active_freq)]:
        c.drawString(70, y, f"{state} State:")
        y -= 20
        for band, value in freq.items():
            c.drawString(90, y, f"{band}: {value:.4f}")
            y -= 20
        y -= 10

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y - 40, "cognilift")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "EEG Frequency Dashboard"

app.layout = html.Div(
    style={'backgroundColor': '#231630', 'padding': '28px', 'fontFamily': 'Trebuchet MS, sans-serif'},
    children=[
        # Navigation Bar
        html.Div(
            [
                html.A(
                    "Dashboard",
                    href="/",
                    style={
                        "color": "#F0EEE9",
                        "textDecoration": "none",
                        "padding": "10px 20px",
                        "backgroundColor": "#F84BAE",
                        "borderRadius": "5px",
                        "fontWeight": "bold",
                    },
                ),
                html.A(
                    "Life Analysis",
                    href="/life-analysis",
                    style={
                        "color": "#F0EEE9",
                        "textDecoration": "none",
                        "padding": "10px 20px",
                        "backgroundColor": "#3A2A4A",
                        "borderRadius": "5px",
                        "fontWeight": "bold",
                    },
                ),
            ],
            style={
                "display": "flex",
                "gap": "20px",
                "padding": "10px 20px",
                "backgroundColor": "#2E1A47",
                "borderRadius": "5px",
                "marginBottom": "20px",
            },
        ),

        
        dcc.Download(id="download-pdf"),
        html.Div([
            html.H1(
                "EEG Frequency Dashboard",
                style={
                    'textAlign': 'center',
                    'color': '#F84BAE',
                    'fontWeight': '700',
                    'fontSize': '36px',
                    'marginBottom': '20px'
                }
            ),
            html.Button(
                'Generate Report',
                id='generate-report-button',
                style={
                    'position': 'absolute',
                    'top': '20px',
                    'left': '20px',
                    'padding': '10px 20px',
                    'backgroundColor': '#F84BAE',
                    'color': '#231630',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer',
                    'fontWeight': 'bold'
                }
            ),
        ], style={'position': 'relative'}),

        html.Div(
            id='frequency-output',
            children=frequency_output_content,
            style={
                'margin': '20px',
                'fontSize': '18px',
                'color': '#F0EEE9',
                'textAlign': 'center'
            }
        ),

        html.Div([
            dcc.Graph(
                id='frequency-bar-chart',
                figure=create_bar_figure(relaxed_df),
                style={'width': '50%'}
            ),
            dcc.Graph(
                id='frequency-pie-chart',
                figure=create_pie_figure(relaxed_df),
                style={'width': '50%'}
            ),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'backgroundColor': '#2E1A47',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'
        }),

        html.Div([
            html.H3(
                "Chatbot",
                style={
                    'color': '#F84BAE',
                    'fontSize': '24px',
                    'marginBottom': '10px',
                    'marginTop': '30px'
                }
            ),
            dcc.Input(
                id='chat-input',
                type='text',
                placeholder='Ask me anything...',
                style={
                    'width': '80%',
                    'padding': '10px',
                    'borderRadius': '5px',
                    'border': '1px solid #F84BAE',
                    'marginRight': '10px',
                    'backgroundColor': '#2E1A47',
                    'color': '#F0EEE9'
                }
            ),
            html.Button(
                'Send',
                id='chat-submit',
                n_clicks=0,
                style={
                    'padding': '10px 20px',
                    'backgroundColor': '#F84BAE',
                    'color': '#231630',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer',
                    'fontWeight': 'bold'
                }
            ),
            html.Div(
                id='chat-response',
                style={
                    'marginTop': '20px',
                    'padding': '15px',
                    'backgroundColor': '#2E1A47',
                    'borderRadius': '10px',
                    'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
                    'fontSize': '16px',
                    'color': '#F0EEE9'
                }
            )
        ], style={
            'marginTop': '30px',
            'padding': '20px',
            'backgroundColor': '#2E1A47',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'
        }),

        html.Div([
            html.Div([
                html.Label("Name:", style={'fontSize': '18px', 'color': '#F0EEE9'}),
                dcc.Input(id='name-input', type='text', style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}),
                html.Label("Age:", style={'fontSize': '18px', 'color': '#F0EEE9'}),
                dcc.Input(id='age-input', type='number', style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}),
                html.Button(
                    'Generate PDF',
                    id='generate-pdf-button',
                    style={
                        'padding': '10px 20px',
                        'backgroundColor': '#F84BAE',
                        'color': '#231630',
                        'border': 'none',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'fontWeight': 'bold'
                    }
                ),
            ], style={
                'backgroundColor': '#2E1A47',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'
            }),
        ], id='modal', style={
            'display': 'none',
            'position': 'fixed',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'zIndex': '1000',
            'width': '300px'
        }),

        html.Script('''
            document.getElementById("chat-input").addEventListener("keyup", function(event) {
                if (event.key === "Enter") {
                    document.getElementById("chat-submit").click();
                }
            });
        ''', type="text/javascript")
    ]
)

# Chatbot Callback
@app.callback(
    [Output('chat-response', 'children'),
     Output('chat-input', 'value')],
    [Input('chat-submit', 'n_clicks')],
    [State('chat-input', 'value')]
)
def chat_response(n_clicks, user_input):
    if n_clicks > 0 and user_input:
        frequencies = relaxed_df.iloc[0].to_dict() if not relaxed_df.empty else {}
        prompt = f"The current EEG frequency values (Relaxed State) are: {frequencies}. {user_input}"
        response = generate_gemini_response(prompt)
        styled_response = html.Div(
            response,
            style={
                'fontFamily': 'Trebuchet MS, sans-serif',
                'fontSize': '16px',
                'lineHeight': '1.6',
                'color': '#F0EEE9',
                'padding': '10px',
                'borderRadius': '5px',
                'backgroundColor': '#3A2A4A',
                'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
            }
        )
        return styled_response, ""
    return "", ""

# Report Generation Callback
@app.callback(
    [Output('modal', 'style'),
     Output('download-pdf', 'data')],
    [Input('generate-report-button', 'n_clicks'),
     Input('generate-pdf-button', 'n_clicks')],
    [State('modal', 'style'),
     State('name-input', 'value'),
     State('age-input', 'value'),
     State('frequency-bar-chart', 'figure'),
     State('frequency-pie-chart', 'figure')]
)
def handle_report_generation(report_clicks, pdf_clicks, modal_style, name, age, bar_fig, pie_fig):
    ctx = dash.callback_context
    if not ctx.triggered:
        return modal_style, None

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'generate-report-button':
        return {'display': 'block'}, None
    elif button_id == 'generate-pdf-button':
        if not name or not age:
            return modal_style, None

        relaxed_freq = relaxed_df.iloc[0].to_dict() if not relaxed_df.empty else {}
        stressed_freq = stressed_df.iloc[0].to_dict() if not stressed_df.empty else {}
        active_freq = active_df.iloc[0].to_dict() if not active_df.empty else {}

        pdf_buffer = generate_pdf(name, age, relaxed_freq, stressed_freq, active_freq, bar_fig, pie_fig)
        return {'display': 'none'}, dcc.send_bytes(pdf_buffer.getvalue(), f"EEG_Report_{name}.pdf")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)