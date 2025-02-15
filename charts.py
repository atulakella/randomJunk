import plotly.express as px

def create_bar_figure(df, title):
    if df.empty:
        return {}
    frequencies = df.iloc[0].to_dict()
    return px.bar(
        x=list(frequencies.keys()),
        y=list(frequencies.values()),
        labels={'x': 'Frequency Band', 'y': 'Value'},
        title=title,
        color=list(frequencies.keys()),
        color_discrete_sequence=['#F84BAE', '#C47300', '#F0EEE9', '#231630','#5700AE'],
    ).update_layout(
        plot_bgcolor='#2E1A47',
        paper_bgcolor='#2E1A47',
        font=dict(color='#F0EEE9')
    )

def create_pie_figure(df, title):
    if df.empty:
        return {}
    frequencies = df.iloc[0].to_dict()
    return px.pie(
        names=list(frequencies.keys()),
        values=list(frequencies.values()),
        title=title,
        color=list(frequencies.keys()),
        color_discrete_sequence=['#F84BAE', '#C47300', '#F0EEE9', '#231630','#5700AE'],
    ).update_layout(
        plot_bgcolor='#2E1A47',
        paper_bgcolor='#2E1A47',
        font=dict(color='#F0EEE9')
    )