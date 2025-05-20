import math
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

from config import *


def clamp(value, lower, upper):
    return max(lower, min(value, upper))

def calculate_sell_price_logistic(buy_price, supply_ratio, factor, center_point=1.0, min_discount=0.4, max_discount=0.985):
    discount = min_discount + (max_discount - min_discount) / (1 + math.exp(-factor * (center_point - supply_ratio)))
    return buy_price * discount

def calculate_buy_price_logistic_impl(floor, ceil, supply_ratio, deviation, factor, center_point=1.0, base_price=1):
    new_floor = floor - deviation
    new_ceil = ceil + deviation
    temp = new_floor + (new_ceil - new_floor) / (1 + math.exp(-factor * (center_point - supply_ratio)))
    return base_price * clamp(temp, floor, ceil)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Buy & Sell Price Logistic Curve", style={"textAlign": "center"}),

    dcc.Graph(id='combined-graph', style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '80vh', 'height': '40vh'}),

    html.Div([
        html.Div([
            html.Label('Floor'),
            dcc.Slider(0, 0.95, 0.05, value=0.5, marks={0: '0', 0.95: '0.95'}, tooltip={"placement": "bottom", "always_visible": False}, id='floor-slider'),

            html.Label('Ceil'),
            dcc.Slider(1.05, 2, 0.05, value=1.5, marks={1.05: '1.05', 2: '2'}, tooltip={"placement": "bottom", "always_visible": False}, id='ceil-slider'),

            html.Label('Buy Cut-off'),
            dcc.Slider(-0.5, 0.5, 0.01, value=LOGISTIC_CUTOFF, marks={-0.5: '-0.5', 0.5: '0.5'}, tooltip={"placement": "bottom", "always_visible": False}, id='deviation-slider'),
        ], style={"flex": 1, "padding": "10px"}),

        html.Div([
            html.Label('Buy Center Point'),
            dcc.Slider(0, 2, 0.05, value=1.0, marks={0: '0', 2: '2'},
                       tooltip={"placement": "bottom", "always_visible": False}, id='buy-center-point'),

            html.Label('Buy Logistic Factor'),
            dcc.Slider(0.1, 10, 0.1, value=BUY_LOGISTIC_FACTOR, marks={0: '1', 10: '10'}, tooltip={"placement": "bottom", "always_visible": False}, id='factor-slider'),

            html.Label('Base Price Multiplier'),
            dcc.Slider(1, 500, 1, value=1, marks={1: '1', 500: '500'}, tooltip={"placement": "bottom", "always_visible": False},
                       id='base-price-slider'),        ], style={"flex": 1, "padding": "10px"}),

        html.Div([
            html.Label('Sell Center Point'),
            dcc.Slider(0    , 2, 0.05, value=SELL_CENTER_SHIFT, marks={0: '0', 2: '2'}, tooltip={"placement": "bottom", "always_visible": False}, id='sell-center-point'),

            html.Label('Sell Logistic Factor'),
            dcc.Slider(0.1, 10, 0.1, value=SELL_LOGISTIC_FACTOR, marks={0: '0', 10: '10'}, tooltip={"placement": "bottom", "always_visible": False}, id='sell-factor-slider'),

            html.Label('Min Sell Discount'),
            dcc.Slider(0.1, 0.9, 0.01, value=SELL_MIN_DISCOUNT, marks={0.1: '0', 0.9: '0.9'}, tooltip={"placement": "bottom", "always_visible": False}, id='min-sell-discount-slider'),

            html.Label('Max Sell Discount'),
            dcc.Slider(0.9, 1.0, 0.001, value=SELL_MAX_DISCOUNT, marks={0.9: '0.9', 1.00: '1.0'}, tooltip={"placement": "bottom", "always_visible": False}, id='max-sell-discount-slider'),
        ], style={"flex": 1, "padding": "10px"}),
    ], style={"display": "flex", "flexWrap": "wrap", "maxWidth": "1000px", "margin": "0 auto"}),
])

@app.callback(
    Output('combined-graph', 'figure'),
    Input('floor-slider', 'value'),
    Input('ceil-slider', 'value'),
    Input('deviation-slider', 'value'),
    Input('factor-slider', 'value'),
    Input('base-price-slider', 'value'),
    Input('sell-factor-slider', 'value'),
    Input('min-sell-discount-slider', 'value'),
    Input('max-sell-discount-slider', 'value'),
    Input('buy-center-point', 'value'),
    Input('sell-center-point', 'value'),
)
def update_combined_graph(floor, ceil, deviation, factor, base_price, sell_factor, min_discount, max_discount, buy_center_point, sell_center_point):
    supply_ratios = np.linspace(0, 2, 100)

    buy_prices = [calculate_buy_price_logistic_impl(floor, ceil, r, deviation, factor, buy_center_point, base_price) for r in supply_ratios]
    sell_prices = [calculate_sell_price_logistic(buy, r, sell_factor, sell_center_point, min_discount, max_discount) for buy, r in zip(buy_prices, supply_ratios)]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=supply_ratios, y=buy_prices, mode='lines', name='Buy Price', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=supply_ratios, y=sell_prices, mode='lines', name='Sell Price', line=dict(color='orange')))

    # Asymptote Lines for Buy Prices
    fig.add_trace(go.Scatter(x=supply_ratios, y=[base_price * floor] * len(supply_ratios), mode='lines', name='Buy Floor', line=dict(dash='dash', color='green')))
    fig.add_trace(go.Scatter(x=supply_ratios, y=[base_price * ceil] * len(supply_ratios), mode='lines', name='Buy Ceil', line=dict(dash='dash', color='red')))

    fig.update_layout(
        title='Buy & Sell Price vs Supply Ratio',
        xaxis_title='Supply Ratio',
        yaxis_title='Price',
        legend=dict(x=0.99, y=0.99),
        template='plotly_white'
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
