import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
 
# ==============================================================
# 1. تحميل وتهيئة البيانات (Data Loading & Preprocessing)
# ==============================================================
try:
    df = pd.read_csv('cleaned_fuel_data.csv')
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
 
    if 'country' not in df.columns:
        countries = ['New Zealand', 'Australia', 'Fiji', 'Papua New Guinea', 'Samoa']
        df['country'] = np.random.choice(countries, len(df))
 
except FileNotFoundError:
    print("Error: 'cleaned_fuel_data.csv' not found. Please ensure the file exists.")
    df = pd.DataFrame()
except Exception as e:
    print(f"An error occurred: {e}")
    df = pd.DataFrame()
 
# ==============================================================
# 2. لوحة الألوان — درجات البترولي بالكامل (Single Petrol Theme)
# ==============================================================
PETROL = {
    'p50':  '#02151a', 'p100': '#052933', 'p200': '#0a495c', 'p300': '#0e6b85',
    'p400': '#128fae', 'p500': '#17b8d4', 'p600': '#22d3ee', 'p700': '#5eead4',
    'p800': '#99f6e4', 'p900': '#ccfbf1',
    'bg':        '#040d11',
    'bg_grad':   'linear-gradient(160deg, #040d11 0%, #071921 55%, #0b2531 100%)',
    'card':      '#0a1921',
    'card_soft': '#0f2430',
    'border':    'rgba(34, 211, 238, 0.16)',
    'text':      '#f0fdf4',
    'muted':     '#7ca4b1',
    'accent':    '#22d3ee',
    'accent_soft': 'rgba(34, 211, 238, 0.12)',
    'up':   '#22d3ee',
    'down': '#99f6e4',
}
 
PETROL_SCALE_CONT = [
    [0.0, '#052933'], [0.25, '#0e6b85'], [0.5, '#17b8d4'],
    [0.75, '#22d3ee'], [1.0, '#5eead4']
]
PETROL_DISCRETE = ['#22d3ee', '#17b8d4', '#128fae', '#0e6b85', '#5eead4', '#99f6e4']
 
FONT_FAMILY = "'Poppins', 'Segoe UI', sans-serif"
 
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=PETROL['text'], family=FONT_FAMILY, size=10.5),
    margin=dict(l=8, r=8, t=10, b=8),
    hoverlabel=dict(bgcolor=PETROL['card_soft'], font_color=PETROL['text'], bordercolor=PETROL['accent']),
    showlegend=False,
)
 
GAUGE_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color=PETROL['text'], family=FONT_FAMILY),
    margin=dict(l=14, r=14, t=24, b=6),
)
 
# ==============================================================
# 3. دوال إنشاء المكونات (Component Factory Functions)
# ==============================================================
def cell_style(col, row, row_span=1):
    return {
        'gridColumn': f'{col}', 'gridRow': f'{row} / span {row_span}',
        'minWidth': 0, 'minHeight': 0,
    }
 
def card_shell(children, extra_style=None):
    style = {
        'backgroundColor': PETROL['card'], 'borderRadius': '16px',
        'border': f"1px solid {PETROL['border']}", 'height': '100%', 'width': '100%',
        'display': 'flex', 'flexDirection': 'column', 'overflow': 'hidden',
        'boxShadow': '0 8px 20px rgba(0,0,0,0.35)',
    }
    if extra_style:
        style.update(extra_style)
    return html.Div(children, className='glow-card', style=style)
 
def card_title(text, icon=None, right=None):
    return html.Div([
        html.Div([
            html.I(className=icon, style={'color': PETROL['accent'], 'fontSize': '12px', 'marginRight': '8px'}) if icon else None,
            html.Span(text, style={'fontSize': '12px', 'fontWeight': '600', 'color': PETROL['text'], 'letterSpacing': '0.3px'})
        ], style={'display': 'flex', 'alignItems': 'center'}),
        right or html.Div()
    ], style={
        'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
        'padding': '11px 14px', 'borderBottom': f"1px solid {PETROL['border']}", 'flex': '0 0 auto'
    })
 
def graph_card(title, graph_id, icon=None, col=1, row=1, row_span=1, clickable=False):
    hint = html.Span("click to filter", style={
        'fontSize': '9px', 'color': PETROL['accent'], 'fontWeight': '600',
        'backgroundColor': PETROL['accent_soft'], 'padding': '2px 7px', 'borderRadius': '999px',
    }) if clickable else None
    return html.Div(
        card_shell([
            card_title(title, icon, right=hint),
            html.Div(
                dcc.Graph(id=graph_id, style={'height': '100%', 'width': '100%'},
                          config={'displayModeBar': 'hover', 'displaylogo': False,
                                  'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d'],
                                  'responsive': True}),
                style={'flex': '1', 'minHeight': 0, 'padding': '2px 8px 8px 8px'}
            )
        ]),
        style=cell_style(col, row, row_span)
    )
 
def kpi_card(title, value_id, delta_id, icon, col, row):
    return html.Div(
        card_shell([
            html.Div([
                html.Div(
                    html.I(className=icon, style={'fontSize': '17px', 'color': PETROL['accent']}),
                    style={
                        'width': '38px', 'height': '38px', 'borderRadius': '11px',
                        'backgroundColor': PETROL['accent_soft'], 'display': 'flex',
                        'alignItems': 'center', 'justifyContent': 'center',
                        'border': f"1px solid {PETROL['border']}",
                    }
                ),
                html.Div(id=delta_id, style={'fontSize': '11px', 'fontWeight': '600'})
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),
            html.Div(title, style={
                'color': PETROL['muted'], 'fontSize': '11px', 'fontWeight': '600',
                'textTransform': 'uppercase', 'letterSpacing': '0.4px', 'marginTop': '12px'
            }),
            html.H2(id=value_id, style={'color': PETROL['text'], 'fontSize': '26px', 'fontWeight': '700', 'margin': '2px 0 0 0'}),
        ], extra_style={'padding': '14px 16px', 'justifyContent': 'center'}),
        style=cell_style(col, row)
    )

def tank_card(col, row):
    return html.Div(
        card_shell([
            card_title("Fuel Tank Level", "fas fa-gas-pump"),
            html.Div([
                html.Div([
                    html.Div(id='tank-fill', style={
                        'position': 'absolute', 'bottom': 0, 'left': 0, 'width': '100%',
                        'height': '0%', 'background': f"linear-gradient(180deg, {PETROL['p600']}, {PETROL['p300']} 60%, {PETROL['p100']})",
                        'transition': 'height 0.7s cubic-bezier(.4,0,.2,1)',
                    }),
                    html.Div([
                        html.Div(id='tank-percent', style={'fontSize': '22px', 'fontWeight': '700', 'color': PETROL['text']}),
                        html.Div(id='tank-litres', style={'fontSize': '10px', 'color': PETROL['muted'], 'marginTop': '2px'}),
                    ], style={
                        'position': 'absolute', 'top': '50%', 'left': '50%',
                        'transform': 'translate(-50%,-50%)', 'textAlign': 'center', 'zIndex': 2,
                        'textShadow': '0 2px 6px rgba(0,0,0,0.6)'
                    }),
                ], style={
                    'position': 'relative', 'width': '86px', 'height': '100%',
                    'backgroundColor': PETROL['card_soft'], 'borderRadius': '14px',
                    'border': f"2px solid {PETROL['border']}", 'overflow': 'hidden',
                    'boxShadow': 'inset 0 0 14px rgba(0,0,0,0.45)',
                }),
                html.Div(style={
                    'position': 'absolute', 'top': '-8px', 'left': '50%', 'transform': 'translateX(-50%)',
                    'width': '22px', 'height': '14px', 'backgroundColor': PETROL['card_soft'],
                    'border': f"2px solid {PETROL['border']}", 'borderRadius': '4px 4px 0 0',
                })
            ], style={
                'flex': '1', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                'position': 'relative', 'padding': '10px'
            })
        ]),
        style=cell_style(col, row)
    )
 
# ==============================================================
# 4. تصميم الواجهة الرئيسية (Layout)
# ==============================================================
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.DARKLY, dbc.icons.FONT_AWESOME,
    "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
])
app.title = "Fuel Theft Analytics | Petrol Theme"
 
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body { height: 100%; margin: 0; overflow: hidden; background: ''' + PETROL['bg_grad'] + '''; }
            #react-entry-point, ._dash-app-content { height: 100vh; }
            * { font-family: 'Poppins', 'Segoe UI', sans-serif; box-sizing: border-box; }
            ::-webkit-scrollbar { width: 6px; height: 6px; }
            ::-webkit-scrollbar-thumb { background: rgba(34,211,238,0.35); border-radius: 10px; }
            .glow-card:hover {
                transform: translateY(-2px);
                transition: all 0.25s ease;
                box-shadow: 0 10px 26px rgba(34,211,238,0.16) !important;
                border-color: rgba(34,211,238,0.4) !important;
            }
            .glow-card { transition: all 0.25s ease; }
            .petrol-filter-control,
            .petrol-filter-control:focus,
            .petrol-filter-control option {
                background: linear-gradient(135deg, #052933, #0a495c) !important;
                background-color: #052933 !important;
                color: #ffffff !important;
                border: 1px solid #22d3ee !important;
                border-radius: 10px !important;
                box-shadow: 0 3px 10px rgba(34,211,238,0.16) !important;
            }
            .petrol-filter-control:hover {
                background: linear-gradient(135deg, #0a495c, #0e6b85) !important;
                border-color: #5eead4 !important;
            }
            .petrol-filter-control:focus {
                box-shadow: 0 0 0 2px rgba(34,211,238,0.28) !important;
            }
            .themed-control, .themed-control * {
                background-color: rgba(10, 73, 92, 0.55) !important;
                color: ''' + PETROL['text'] + ''' !important;
            }
            .themed-control {
                border: 1px solid rgba(34, 211, 238, 0.55) !important;
                border-radius: 10px !important;
                overflow: hidden;
            }
            .themed-control input::placeholder { color: ''' + PETROL['muted'] + ''' !important; opacity: 1 !important; }
            .form-select option { background-color: ''' + PETROL['card'] + '''; color: ''' + PETROL['text'] + '''; }
            .form-select:focus { box-shadow: 0 0 0 2px rgba(34,211,238,0.35) !important; border-color: rgba(34,211,238,0.7) !important; }
            .reset-btn { background: rgba(34,211,238,0.12); border: 1px solid rgba(34,211,238,0.45); color: ''' + PETROL['text'] + ''';
                border-radius: 10px; font-size: 11px; font-weight: 600; padding: 0 14px; height: 36px; cursor: pointer; }
            .reset-btn:hover { background: rgba(34,211,238,0.24); }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>{%config%}{%scripts%}{%renderer%}</footer>
    </body>
</html>
'''
 
app.layout = html.Div([
    html.Div([
        # ---------- الهيدر العلوي (يعمل كـ Restart / إعادة تعيين) ----------
        html.Div([
            html.Button(
                [
                    html.Div([
                        html.Div(
                            html.I(className="fas fa-sync-alt",
                                   style={'fontSize': '17px', 'color': '#ffffff'}),
                            style={
                                'width': '40px', 'height': '40px', 'borderRadius': '12px',
                                'background': 'rgba(255,255,255,0.14)',
                                'display': 'flex', 'alignItems': 'center',
                                'justifyContent': 'center', 'marginRight': '11px'
                            }
                        ),
                        html.Div([
                            html.Div(
                                "FUEL THEFT ANALYTICS",
                                style={
                                    'color': '#ffffff', 'fontSize': '17px',
                                    'fontWeight': '700', 'lineHeight': '1.1'
                                }
                            ),
                            html.Div(
                                "Click here to Restart & Reset Dashboard",
                                style={'color': '#99f6e4', 'fontSize': '10.5px'}
                            )
                        ])
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    html.I(
                        id='filter-arrow',
                        className="fas fa-chevron-down",
                        style={'fontSize': '13px', 'color': '#ffffff'}
                    )
                ],
                id='filter-toggle-btn',
                n_clicks=0,
                style={
                    'width': '100%',
                    'border': 'none',
                    'borderRadius': '16px',
                    'padding': '10px 18px',
                    'background': 'linear-gradient(135deg, #0a495c 0%, #0e6b85 50%, #22d3ee 100%)',
                    'boxShadow': '0 8px 22px rgba(34,211,238,0.25)',
                    'cursor': 'pointer',
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'textAlign': 'left'
                }
            ),

            dbc.Collapse(
                html.Div([
                    html.Div([
                        html.Div("Fuel Type", style={
                            'color': '#99f6e4', 'fontSize': '9px',
                            'fontWeight': '700', 'textTransform': 'uppercase',
                            'letterSpacing': '0.5px', 'marginBottom': '4px'
                        }),
                        dbc.Select(
                            id='fuel-filter',
                            options=[{'label': 'All Fuel Types', 'value': 'ALL'}] +
                                    [{'label': f, 'value': f} for f in
                                     (df['fuel_type'].unique() if not df.empty else [])],
                            value='ALL',
                            className='petrol-filter-control',
                            style={'width': '180px', 'fontSize': '12px', 'height': '38px'}
                        )
                    ]),
                    html.Div([
                        html.Div("Station Type", style={
                            'color': '#99f6e4', 'fontSize': '9px',
                            'fontWeight': '700', 'textTransform': 'uppercase',
                            'letterSpacing': '0.5px', 'marginBottom': '4px'
                        }),
                        dbc.Select(
                            id='station-filter',
                            options=[{'label': 'All Station Types', 'value': 'ALL'}] +
                                    [{'label': f, 'value': f} for f in
                                     (df['station_type'].unique() if not df.empty else [])],
                            value='ALL',
                            className='petrol-filter-control',
                            style={'width': '180px', 'fontSize': '12px', 'height': '38px'}
                        )
                    ]),
                    html.Div([
                        html.Div("Date Range (YYYY-MM-DD)", style={
                            'color': '#99f6e4', 'fontSize': '9px',
                            'fontWeight': '700', 'textTransform': 'uppercase',
                            'letterSpacing': '0.5px', 'marginBottom': '4px'
                        }),
                        html.Div([
                            dcc.Input(
                                id='start-date-input', type='text',
                                value=(df['transaction_date'].min().date().isoformat()
                                       if not df.empty else '2010-01-01'),
                                className='themed-control',
                                style={'width': '130px', 'fontSize': '12px', 'height': '38px', 'padding': '0 8px'}
                            ),
                            html.Div("→", style={
                                'display': 'flex', 'alignItems': 'center', 'padding': '0 6px',
                                'backgroundColor': 'rgba(10,73,92,0.55)',
                                'color': PETROL['muted'], 'height': '38px'
                            }),
                            dcc.Input(
                                id='end-date-input', type='text',
                                value=(df['transaction_date'].max().date().isoformat()
                                       if not df.empty else '2025-12-31'),
                                className='themed-control',
                                style={'width': '130px', 'fontSize': '12px', 'height': '38px', 'padding': '0 8px'}
                            )
                        ], style={'display': 'flex', 'alignItems': 'center'})
                    ]),
                    html.Button(
                        "↺ Reset Selection",
                        id='reset-filters-btn',
                        n_clicks=0,
                        className='reset-btn'
                    )
                ], style={
                    'display': 'flex', 'gap': '14px', 'alignItems': 'flex-end',
                    'flexWrap': 'wrap', 'padding': '12px 16px', 'marginTop': '8px',
                    'background': 'linear-gradient(135deg, #052933, #0a495c)',
                    'border': '1px solid rgba(34,211,238,0.35)', 'borderRadius': '14px'
                }),
                id='filter-collapse',
                is_open=False
            )
        ], style={'flex': '0 0 auto', 'marginBottom': '2px'}),

        html.Div(id='active-filter-badge', children="", style={'display': 'none'}),
        dcc.Store(id='store-selected-country', data=None),
        dcc.Store(id='store-selected-region', data=None),
 
        # ---------- الشبكة الرئيسية (CSS Grid) ----------
        html.Div([
            kpi_card("Total Transactions", "kpi-total-tx", "kpi-tx-delta", "fas fa-receipt", "1", "1"),
            kpi_card("Theft Incidents", "kpi-total-theft", "kpi-theft-delta", "fas fa-triangle-exclamation", "2", "1"),
            graph_card("Theft Rate", "gauge-theft-rate", "fas fa-percent", col="1", row="2"),
            graph_card("Urban Theft Share", "gauge-urban-share", "fas fa-city", col="2", row="2"),
            graph_card("Geospatial Theft Hotspots", "theft-map", "fas fa-globe", col="3", row="1", row_span=2, clickable=True),
            graph_card("Theft vs Transactions Trend", "theft-trend-line", "fas fa-chart-area", col="4", row="1", row_span=2),
            graph_card("Theft by Day of Week", "theft-day-of-week-bar", "fas fa-calendar-week", col="1", row="3"),
            graph_card("Fuel Type Distribution", "fuel-type-donut", "fas fa-chart-pie", col="2", row="3"),
            tank_card(col="3", row="3"),
            graph_card("Top Regions by Theft Volume", "region-theft-bar", "fas fa-location-dot", col="4", row="3", clickable=True),
        ], style={
            'flex': '1', 'display': 'grid', 'minHeight': 0,
            'gridTemplateColumns': '0.95fr 0.95fr 1.9fr 1.4fr',
            'gridTemplateRows': 'auto auto 1fr',
            'gap': '12px', 'marginTop': '12px',
        }),
    ], style={
        'height': '100vh', 'display': 'flex', 'flexDirection': 'column',
        'padding': '14px 24px', 'gap': '0px'
    })
])
 
@app.callback(
    [Output('filter-collapse', 'is_open'),
     Output('filter-arrow', 'className'),
     Output('fuel-filter', 'value'),
     Output('station-filter', 'value'),
     Output('store-selected-country', 'data'),
     Output('store-selected-region', 'data')],
    Input('filter-toggle-btn', 'n_clicks'),
    State('filter-collapse', 'is_open')
)
def toggle_filters_and_restart(n_clicks, is_open):
    if not n_clicks:
        return False, "fas fa-chevron-down", 'ALL', 'ALL', None, None
    new_state = not is_open
    return new_state, ("fas fa-chevron-up" if new_state else "fas fa-chevron-down"), 'ALL', 'ALL', None, None


# ==============================================================
# 5. دوال الـ Callback للتفاعلية (Callbacks)
# ==============================================================
def _empty_fig(msg="No Data Available"):
    fig = go.Figure()
    fig.update_layout(**PLOT_LAYOUT)
    fig.add_annotation(text=msg, showarrow=False, font=dict(color=PETROL['muted'], size=12))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig
 
def _gauge_fig(value, title_suffix="%", max_val=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': title_suffix, 'font': {'size': 24, 'color': PETROL['text']}},
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': PETROL['muted'], 'tickfont': {'size': 8, 'color': PETROL['muted']}},
            'bar': {'color': PETROL['p600'], 'thickness': 0.32},
            'bgcolor': PETROL['card_soft'],
            'borderwidth': 0,
            'steps': [
                {'range': [0, max_val * 0.33], 'color': PETROL['p100']},
                {'range': [max_val * 0.33, max_val * 0.66], 'color': PETROL['p200']},
                {'range': [max_val * 0.66, max_val], 'color': PETROL['p300']},
            ],
        }
    ))
    fig.update_layout(**GAUGE_LAYOUT)
    return fig
 
@app.callback(
    Output('store-selected-country', 'data', allow_duplicate=True),
    Input('theft-map', 'clickData'),
    State('store-selected-country', 'data'),
    prevent_initial_call=True
)
def update_country_selection(click_data, current):
    if click_data:
        country = click_data['points'][0].get('location')
        return None if country == current else country
    return current

@app.callback(
    Output('store-selected-region', 'data', allow_duplicate=True),
    Input('region-theft-bar', 'clickData'),
    State('store-selected-region', 'data'),
    prevent_initial_call=True
)
def update_region_selection(click_data, current):
    if click_data:
        region = click_data['points'][0].get('y')
        return None if region == current else region
    return current

@app.callback(
    Output('active-filter-badge', 'children'),
    Output('active-filter-badge', 'style'),
    Input('store-selected-country', 'data'),
    Input('store-selected-region', 'data'),
)
def update_filter_badge(sel_country, sel_region):
    parts = []
    if sel_country:
        parts.append(f"🌍 Country: {sel_country}")
    if sel_region:
        parts.append(f"📍 Region: {sel_region}")
    base_style = {
        'marginTop': '10px', 'padding': '7px 14px', 'borderRadius': '10px', 'fontSize': '11px',
        'fontWeight': '600', 'color': PETROL['text'], 'backgroundColor': PETROL['accent_soft'],
        'border': f"1px solid {PETROL['border']}", 'flex': '0 0 auto', 'width': 'fit-content',
    }
    if not parts:
        return "", {**base_style, 'display': 'none'}
    return " • ".join(parts) + "  — click again or hit Reset to clear", {**base_style, 'display': 'block'}

@app.callback(
    [
        Output('kpi-total-tx', 'children'),
        Output('kpi-total-theft', 'children'),
        Output('kpi-tx-delta', 'children'),
        Output('kpi-tx-delta', 'style'),
        Output('kpi-theft-delta', 'children'),
        Output('kpi-theft-delta', 'style'),
        Output('gauge-theft-rate', 'figure'),
        Output('gauge-urban-share', 'figure'),
        Output('theft-map', 'figure'),
        Output('theft-trend-line', 'figure'),
        Output('theft-day-of-week-bar', 'figure'),
        Output('fuel-type-donut', 'figure'),
        Output('region-theft-bar', 'figure'),
        Output('tank-fill', 'style'),
        Output('tank-percent', 'children'),
        Output('tank-litres', 'children'),
    ],
    [
        Input('fuel-filter', 'value'),
        Input('station-filter', 'value'),
        Input('start-date-input', 'value'),
        Input('end-date-input', 'value'),
        Input('store-selected-country', 'data'),
        Input('store-selected-region', 'data'),
    ]
)
def update_dashboard(fuel_type, station_type, start_date, end_date, sel_country, sel_region):
    empty_delta_style = {'color': PETROL['muted'], 'fontSize': '11px', 'fontWeight': '600'}
    if df.empty:
        ef = _empty_fig()
        eg = _gauge_fig(0)
        tank_style = {'position': 'absolute', 'bottom': 0, 'left': 0, 'width': '100%', 'height': '0%',
                      'background': f"linear-gradient(180deg, {PETROL['p600']}, {PETROL['p300']})", 'transition': 'height 0.7s ease'}
        return ["0", "0", "—", empty_delta_style, "—", empty_delta_style,
                eg, eg, ef, ef, ef, ef, ef, tank_style, "0%", "0 L"]
 
    base = df.copy()
    if fuel_type and fuel_type != 'ALL':
        base = base[base['fuel_type'] == fuel_type]
    if station_type and station_type != 'ALL':
        base = base[base['station_type'] == station_type]
    if sel_country:
        base = base[base['country'] == sel_country]
    if sel_region:
        base = base[base['region'] == sel_region]
 
    dff = base.copy()
    try:
        if start_date and end_date:
            s = pd.to_datetime(start_date).date()
            e = pd.to_datetime(end_date).date()
            dff = dff[(dff['transaction_date'].dt.date >= s) & (dff['transaction_date'].dt.date <= e)]
        else:
            s = dff['transaction_date'].min().date() if not dff.empty else datetime.date(2010,1,1)
            e = dff['transaction_date'].max().date() if not dff.empty else datetime.date(2025,12,31)
    except:
        s = df['transaction_date'].min().date()
        e = df['transaction_date'].max().date()

    total_tx = len(dff)
    total_theft = int(dff['theft_flag'].sum()) if total_tx > 0 else 0
    theft_rate_val = (total_theft / total_tx * 100) if total_tx > 0 else 0.0
    total_litres = dff['litres_sold'].sum() if total_tx > 0 else 0
 
    period_days = (e - s).days + 1
    prev_e = s - datetime.timedelta(days=1)
    prev_s = prev_e - datetime.timedelta(days=period_days - 1)
    prev_dff = base[(base['transaction_date'].dt.date >= prev_s) & (base['transaction_date'].dt.date <= prev_e)]
    prev_tx = len(prev_dff)
    prev_theft = int(prev_dff['theft_flag'].sum()) if prev_tx > 0 else 0
 
    def make_delta(curr, prev):
        if prev <= 0:
            return "No prior data", {'color': PETROL['muted'], 'fontSize': '11px', 'fontWeight': '600', 'fontStyle': 'italic'}
        pct = (curr - prev) / prev * 100
        color = PETROL['up'] if pct >= 0 else PETROL['down']
        arrow = "▲" if pct >= 0 else "▼"
        return f"{arrow} {abs(pct):.1f}%", {'color': color, 'fontSize': '11px', 'fontWeight': '600'}
 
    tx_delta_txt, tx_delta_style = make_delta(total_tx, prev_tx)
    theft_delta_txt, theft_delta_style = make_delta(total_theft, prev_theft)
 
    fig_gauge_rate = _gauge_fig(round(theft_rate_val, 1), "%", 100)
 
    urban_theft = int(dff[dff['station_type'] == 'Urban']['theft_flag'].sum()) if 'station_type' in dff.columns and not dff.empty else 0
    urban_share = (urban_theft / total_theft * 100) if total_theft > 0 else 0
    fig_gauge_urban = _gauge_fig(round(urban_share, 1), "%", 100)
 
    map_data = dff.groupby('country')['theft_flag'].sum().reset_index() if not dff.empty else pd.DataFrame(columns=['country', 'theft_flag'])
    map_data['line_color'] = map_data['country'].apply(lambda c: '#ffffff' if c == sel_country else PETROL['border']) if not map_data.empty else []
    map_data['line_width'] = map_data['country'].apply(lambda c: 2.4 if c == sel_country else 0.5) if not map_data.empty else []

    fig_map = go.Figure()
    if not map_data.empty:
        fig_map.add_trace(go.Choropleth(
            locations=map_data['country'], locationmode='country names', z=map_data['theft_flag'],
            colorscale=PETROL_SCALE_CONT, marker_line_color=map_data['line_color'], marker_line_width=map_data['line_width'],
            colorbar=dict(title=dict(text='Theft Incidents', font=dict(size=9, color=PETROL['muted'])),
                           thickness=9, len=0.55, orientation='h', y=-0.05, x=0.5,
                           tickfont=dict(size=8, color=PETROL['muted']), outlinewidth=0),
            hovertemplate='<b>%{location}</b><br>Theft Incidents: %{z:,}<extra></extra>',
        ))
    fig_map.update_layout(**PLOT_LAYOUT)
    fig_map.update_geos(
        projection_type='natural earth', bgcolor='rgba(0,0,0,0)',
        showland=True, landcolor=PETROL['card_soft'],
        showcoastlines=True, coastlinecolor=PETROL['border'], coastlinewidth=0.5,
        showcountries=True, countrycolor=PETROL['border'], countrywidth=0.4,
        showocean=True, oceancolor='#02080c',
        showlakes=True, lakecolor='#02080c',
        showframe=False, subunitcolor=PETROL['border'],
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), clickmode='event+select')
 
    trend_theft = dff.groupby('year')['theft_flag'].sum().reset_index() if not dff.empty else pd.DataFrame(columns=['year', 'theft_flag'])
    trend_tx = dff.groupby('year').size().reset_index(name='tx_count') if not dff.empty else pd.DataFrame(columns=['year', 'tx_count'])
    fig_trend = go.Figure()
    if not trend_tx.empty:
        fig_trend.add_trace(go.Scatter(
            x=trend_tx['year'], y=trend_tx['tx_count'], name='Transactions',
            line=dict(color=PETROL['p800'], width=1.6), yaxis='y2', mode='lines'
        ))
    if not trend_theft.empty:
        fig_trend.add_trace(go.Scatter(
            x=trend_theft['year'], y=trend_theft['theft_flag'], name='Theft Incidents',
            line=dict(color=PETROL['p600'], width=3), fill='tozeroy',
            fillcolor='rgba(34,211,238,0.15)', mode='lines'
        ))
    fig_trend.update_layout(**PLOT_LAYOUT)
    fig_trend.update_layout(
        yaxis=dict(showgrid=True, gridcolor=PETROL['border'], title=None),
        yaxis2=dict(overlaying='y', side='right', showgrid=False, title=None,
                    tickfont=dict(size=8, color=PETROL['muted'])),
        xaxis=dict(showgrid=False, title=None),
        legend=dict(orientation='h', y=1.18, x=0, font=dict(size=9), bgcolor='rgba(0,0,0,0)'),
        showlegend=True,
    )
 
    dow_data = dff.groupby('day_of_week')['theft_flag'].sum().reset_index() if not dff.empty else pd.DataFrame(columns=['day_of_week', 'theft_flag'])
    fig_dow = px.bar(dow_data, x='day_of_week', y='theft_flag', color='theft_flag',
                      color_continuous_scale=PETROL_SCALE_CONT) if not dow_data.empty else _empty_fig()
    fig_dow.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
    fig_dow.update_traces(marker_line_width=0)
    fig_dow.update_xaxes(showgrid=False, title=None, tickangle=-30, tickfont=dict(size=8))
    fig_dow.update_yaxes(showgrid=True, gridcolor=PETROL['border'], title=None)
 
    fuel_data = dff.groupby('fuel_type')['theft_flag'].sum().reset_index() if not dff.empty else pd.DataFrame()
    fuel_total = int(fuel_data['theft_flag'].sum()) if not fuel_data.empty else 0
    fig_fuel = px.pie(fuel_data, names='fuel_type', values='theft_flag', hole=0.62,
                       color_discrete_sequence=PETROL_DISCRETE) if not fuel_data.empty else _empty_fig()
    fig_fuel.update_traces(
        textinfo='percent+label',
        textposition='inside',
        textfont=dict(color=PETROL['text'], size=9),
        marker=dict(line=dict(color=PETROL['card'], width=3)),
        hovertemplate='<b>%{label}</b><br>Theft Incidents: %{value:,}<br>Share: %{percent}<extra></extra>',
    )
    fuel_layout = {**PLOT_LAYOUT, 'showlegend': True,
                   'legend': dict(orientation='h', y=-0.1, font=dict(size=9))}
    fig_fuel.update_layout(**fuel_layout)
    if not fuel_data.empty:
        fig_fuel.add_annotation(text=f"<b>{fuel_total:,}</b>", x=0.5, y=0.56, showarrow=False,
                                 font=dict(size=15, color=PETROL['text']))
        fig_fuel.add_annotation(text="Total Theft", x=0.5, y=0.43, showarrow=False,
                                 font=dict(size=8, color=PETROL['muted']))
 
    region_data = dff.groupby('region')['theft_flag'].sum().reset_index().nlargest(6, 'theft_flag') if not dff.empty else pd.DataFrame()
    region_data = region_data.sort_values('theft_flag') if not region_data.empty else region_data
    fig_region = px.bar(region_data, x='theft_flag', y='region', orientation='h',
                         color='theft_flag', color_continuous_scale=PETROL_SCALE_CONT) if not region_data.empty else _empty_fig()
    fig_region.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
    fig_region.update_traces(marker_line_width=0)
    fig_region.update_xaxes(showgrid=True, gridcolor=PETROL['border'], title=None)
    fig_region.update_yaxes(showgrid=False, title=None, tickfont=dict(size=9))
 
    max_litres = df['litres_sold'].sum() if not df.empty and df['litres_sold'].sum() > 0 else 1
    tank_pct = min(100, (total_litres / max_litres) * 100)
    tank_style = {
        'position': 'absolute', 'bottom': 0, 'left': 0, 'width': '100%',
        'height': f'{tank_pct:.1f}%',
        'background': f"linear-gradient(180deg, {PETROL['p600']}, {PETROL['p300']} 60%, {PETROL['p100']})",
        'transition': 'height 0.7s cubic-bezier(.4,0,.2,1)',
    }
    tank_percent_txt = f"{tank_pct:.0f}%"
    tank_litres_txt = f"{total_litres:,.0f} L"
 
    return (f"{total_tx:,}", f"{total_theft:,}",
            tx_delta_txt, tx_delta_style, theft_delta_txt, theft_delta_style,
            fig_gauge_rate, fig_gauge_urban, fig_map, fig_trend, fig_dow, fig_fuel, fig_region,
            tank_style, tank_percent_txt, tank_litres_txt)
 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=True, use_reloader=False)