import math
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

def clamp(value, lower, upper):
    return max(lower, min(value, upper))

def calculate_buy_price_logistic_impl(floor, ceil, supply_ratio, deviation, factor, base_price=1):
    new_floor = floor - deviation
    new_ceil = ceil + deviation
    temp = new_floor + (new_ceil - new_floor) / (1 + math.exp(-factor * (1 - supply_ratio)))
    return base_price * clamp(temp, floor, ceil)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Logistic Buy Price Visualizer"),

    dcc.Graph(id='logistic-graph'),

    html.Div([
        html.Label('Floor'),
        dcc.Slider(0, 0.95, 0.05, value=0.5, id='floor-slider'),
    ], style={"margin": "10px"}),

    html.Div([
        html.Label('Ceil'),
        dcc.Slider(1.05, 2, 0.05, value=1.5, id='ceil-slider'),
    ], style={"margin": "10px"}),

    html.Div([
        html.Label('Deviation'),
        dcc.Slider(0.01, 0.5, 0.01, value=0.1, id='deviation-slider'),
    ], style={"margin": "10px"}),

    html.Div([
        html.Label('Logistic Factor'),
        dcc.Slider(0.1, 10, 0.1, value=2, id='factor-slider'),
    ], style={"margin": "10px"}),

    html.Div([
        html.Label('Base Price Multiplier'),
        dcc.Slider(1, 500, 1, value=1, marks=None, tooltip={"placement": "bottom", "always_visible": True}, id='base-price-slider'),
    ], style={"margin": "10px"}),
])

@app.callback(
    Output('logistic-graph', 'figure'),
    Input('floor-slider', 'value'),
    Input('ceil-slider', 'value'),
    Input('deviation-slider', 'value'),
    Input('factor-slider', 'value'),
    Input('base-price-slider', 'value'),
)
def update_graph(floor, ceil, deviation, factor, base_price):
    supply_ratios = np.linspace(0.0, 2, 100)
    prices = [calculate_buy_price_logistic_impl(floor, ceil, r, deviation, factor, base_price) for r in supply_ratios]

    fig = go.Figure()

    # Main logistic price curve
    fig.add_trace(go.Scatter(x=supply_ratios, y=prices, mode='lines', name='Price Curve', line=dict(color='blue')))

    # Asymptote lines for floor and ceil
    fig.add_trace(go.Scatter(
        x=supply_ratios, y=[base_price * floor] * len(supply_ratios),
        mode='lines', name='Floor (min)',
        line=dict(dash='dash', color='green')
    ))
    fig.add_trace(go.Scatter(
        x=supply_ratios, y=[base_price * ceil] * len(supply_ratios),
        mode='lines', name='Ceil (max)',
        line=dict(dash='dash', color='red')
    ))

    fig.update_layout(
        title='Supply Ratio vs. Adjusted Buy Price',
        xaxis_title='Supply Ratio',
        yaxis_title='Buy Price',
        legend_title='Legend'
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
