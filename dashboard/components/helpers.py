import plotly.graph_objects as go

def plot_gauge(title, value, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value * 100,
        number={'suffix': " %", "font": {"size": 18}},
        title={'text': title, "font": {"size": 14}},
        gauge={
            'axis': {'range': [0, 100], "tickwidth": 1, "tickcolor": "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 1,
            'steps': [
                {'range': [0, 20], 'color': "#f2f2f2"},
                {'range': [20, 40], 'color': "#e6e6e6"},
                {'range': [40, 60], 'color': "#cccccc"},
                {'range': [60, 80], 'color': "#b3b3b3"},
                {'range': [80, 100], 'color': "#999999"},
            ],
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75,
                'value': value * 100
            }
        }
    ))

    fig.update_layout(
        width=250,   # Smaller width
        height=180,  # Smaller height
        margin=dict(t=20, b=20, l=10, r=10)
    )
    return fig