"""
Traild Customer Onboarding Analysis Dashboard
RevOps Case Study | Paarth Arora
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd

# =============================================================================
# COLOR SCHEME
# =============================================================================
COLORS = {
    'blue': '#1f77b4',      # Live
    'orange': '#ff7f0e',    # At Risk
    'gray': '#7f7f7f',      # On Hold
    'green': '#2ca02c',     # Low Risk
    'red': '#d62728',       # Churned
    'light_blue': '#aec7e8',
    'light_orange': '#ffbb78',
    'purple': '#9467bd',
    'teal': '#17becf',
}

# =============================================================================
# HARD-CODED DATA FROM REPORT
# =============================================================================

# KPI Data
kpi_data = {
    'avg_onboarding': 73,
    'median_onboarding': 49,
    'pct_under_20': 29,
    'pct_20_to_40': 11,
    'at_risk_customers': 72,
    'at_risk_acv': 1.3,  # in millions
}

# Segmentation Data (for treemap)
segmentation_data = pd.DataFrame([
    {'Live Status': 'Live', 'Status': 'Active', 'Category': 'Live-Active', 'N': 96, 'ACV': 1.7},
    {'Live Status': 'Live', 'Status': 'Churned', 'Category': 'Live-Churned', 'N': 1, 'ACV': 0.02},
    {'Live Status': 'Not Live', 'Status': 'Active', 'Category': 'Never Onboarded', 'N': 2, 'ACV': 0.02},
    {'Live Status': 'Not Live', 'Status': 'Active', 'Category': 'On Hold', 'N': 90, 'ACV': 2.3},
    {'Live Status': 'Not Live', 'Status': 'Active', 'Category': 'At Risk', 'N': 72, 'ACV': 1.3},
    {'Live Status': 'Not Live', 'Status': 'Active', 'Category': 'Low Risk', 'N': 97, 'ACV': 3.3},
    {'Live Status': 'Not Live', 'Status': 'Churned', 'Category': 'Not Live-Churned', 'N': 11, 'ACV': 0.3},
])

# ERP Onboarding Data (Top 5 ERPs)
erp_data = pd.DataFrame([
    {'ERP': 'mb (MYOB)', 'N': 45, 'Average': 79, 'Median': 43},
    {'ERP': 'so (Syspro)', 'N': 23, 'Average': 96, 'Median': 75},
    {'ERP': 'at (Acumatica)', 'N': 11, 'Average': 19, 'Median': 10},
    {'ERP': 'xo (Xero)', 'N': 6, 'Average': 29, 'Median': 29},
    {'ERP': 'eo', 'N': 5, 'Average': 60, 'Median': 48},
])

# Cohort Trend Data
cohort_data = pd.DataFrame([
    {'Month': 'Oct-24', 'Avg_Days': 65},
    {'Month': 'Nov-24', 'Avg_Days': 68},
    {'Month': 'Dec-24', 'Avg_Days': 74},
    {'Month': 'Jan-25', 'Avg_Days': 88},
])

# Distribution Data (Histogram bins)
distribution_data = pd.DataFrame([
    {'Bin': '0-20', 'Count': 28, 'Pct': 29},
    {'Bin': '20-40', 'Count': 10, 'Pct': 11},
    {'Bin': '40-60', 'Count': 15, 'Pct': 16},
    {'Bin': '60-80', 'Count': 8, 'Pct': 8},
    {'Bin': '80-100', 'Count': 6, 'Pct': 6},
    {'Bin': '100+', 'Count': 28, 'Pct': 29},
])

# ACV vs Onboarding (for scatter approximation)
acv_onboarding_data = pd.DataFrame([
    {'ACV_Band': '<$5K', 'Avg_Days': 42, 'N': 11, 'Avg_ACV': 3864},
    {'ACV_Band': '$5K-$10K', 'Avg_Days': 62, 'N': 21, 'Avg_ACV': 6911},
    {'ACV_Band': '$10K-$25K', 'Avg_Days': 68, 'N': 44, 'Avg_ACV': 15294},
    {'ACV_Band': '$25K-$50K', 'Avg_Days': 115, 'N': 14, 'Avg_ACV': 36667},
    {'ACV_Band': '$50K+', 'Avg_Days': 116, 'N': 5, 'Avg_ACV': 69058},
])

# Non-Live Category Data
non_live_data = pd.DataFrame([
    {'Category': 'Never Onboarded', 'ACV': 0.023, 'N': 2},
    {'Category': 'On Hold', 'ACV': 2.3, 'N': 90},
    {'Category': 'At Risk', 'ACV': 1.3, 'N': 72},
    {'Category': 'Low Risk', 'ACV': 3.3, 'N': 97},
])

# At Risk Breakdown
at_risk_breakdown = pd.DataFrame([
    {'Reason': 'No incoming comms', 'Count': 54},
    {'Reason': 'Low response / other risk', 'Count': 18},
])

# =============================================================================
# INITIALIZE DASH APP
# =============================================================================
app = Dash(__name__)
app.title = "Traild Customer Onboarding Analysis"

# =============================================================================
# CHART CREATION FUNCTIONS
# =============================================================================

def create_kpi_cards():
    """Create KPI indicator cards"""
    fig = go.Figure()

    # Create 5 indicators in a row
    indicators = [
        {'value': 73, 'title': 'Avg Onboarding', 'suffix': ' days'},
        {'value': 49, 'title': 'Median Onboarding', 'suffix': ' days'},
        {'value': 29, 'title': '% Onboarded <20 Days', 'suffix': '%'},
        {'value': 11, 'title': '% Onboarded 20-40 Days', 'suffix': '%'},
        {'value': 72, 'title': 'At Risk Customers', 'suffix': ' ($1.3M)'},
    ]

    for i, ind in enumerate(indicators):
        fig.add_trace(go.Indicator(
            mode="number",
            value=ind['value'],
            title={'text': ind['title'], 'font': {'size': 14}},
            number={'suffix': ind['suffix'], 'font': {'size': 32, 'color': COLORS['blue']}},
            domain={'x': [i/5, (i+1)/5], 'y': [0, 1]}
        ))

    fig.update_layout(
        height=120,
        margin=dict(l=20, r=20, t=30, b=10),
        paper_bgcolor='white',
    )
    return fig


def create_segmentation_chart():
    """Create treemap for customer segmentation"""
    # Build hierarchical data for treemap
    labels = [
        'All Customers',
        'Live (N=97, $1.7M)', 'Not Live (N=272, $7.3M)',
        'Live-Active (N=96)', 'Live-Churned (N=1)',
        'Not Live-Active (N=261)', 'Not Live-Churned (N=11)',
        'Never Onboarded (N=2)', 'On Hold (N=90)', 'At Risk (N=72)', 'Low Risk (N=97)'
    ]
    parents = [
        '',
        'All Customers', 'All Customers',
        'Live (N=97, $1.7M)', 'Live (N=97, $1.7M)',
        'Not Live (N=272, $7.3M)', 'Not Live (N=272, $7.3M)',
        'Not Live-Active (N=261)', 'Not Live-Active (N=261)', 'Not Live-Active (N=261)', 'Not Live-Active (N=261)'
    ]
    values = [9.0, 1.72, 7.28, 1.7, 0.02, 6.98, 0.3, 0.02, 2.3, 1.3, 3.3]
    colors_list = [
        'white',
        COLORS['blue'], COLORS['gray'],
        COLORS['blue'], COLORS['red'],
        COLORS['light_blue'], COLORS['red'],
        COLORS['gray'], COLORS['gray'], COLORS['orange'], COLORS['green']
    ]

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=colors_list, line=dict(width=2, color='white')),
        textinfo='label+value',
        texttemplate='%{label}<br>$%{value}M',
        hovertemplate='<b>%{label}</b><br>ACV: $%{value}M<extra></extra>',
        root_color='white',
    ))

    fig.update_layout(
        title={'text': 'Customer Segmentation by ACV ($M)', 'font': {'size': 16}},
        template='plotly_white',
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


def create_erp_chart():
    """Create horizontal bar chart for ERP onboarding days with avg bars and median markers"""
    # Reverse order so top ERP appears at top
    erp_reversed = erp_data.iloc[::-1].reset_index(drop=True)
    erp_labels = [f"{row['ERP']} N={row['N']}" for _, row in erp_reversed.iterrows()]

    fig = go.Figure()

    # Average bars
    fig.add_trace(go.Bar(
        y=erp_labels,
        x=erp_reversed['Average'],
        name='Average',
        orientation='h',
        marker_color=COLORS['blue'],
        text=erp_reversed['Average'],
        textposition='inside',
        insidetextanchor='middle',
    ))

    # Median markers (diamond shapes)
    fig.add_trace(go.Scatter(
        y=erp_labels,
        x=erp_reversed['Median'],
        name='Median',
        mode='markers',
        marker=dict(symbol='diamond', size=14, color=COLORS['orange'], line=dict(width=2, color='white')),
    ))

    fig.update_layout(
        title={'text': 'Onboarding Days by ERP (Live & Active, N=96)', 'font': {'size': 16}},
        xaxis_title='Days',
        yaxis_title='',
        template='plotly_white',
        height=320,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=20, r=40, t=70, b=40),
        xaxis=dict(range=[0, 110]),
    )

    return fig


def create_cohort_trend():
    """Create line chart for onboarding trend by cohort"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=cohort_data['Month'],
        y=cohort_data['Avg_Days'],
        mode='lines+markers+text',
        line=dict(color=COLORS['orange'], width=3),
        marker=dict(size=12),
        text=cohort_data['Avg_Days'],
        textposition='top center',
        textfont=dict(size=12, color=COLORS['orange']),
    ))

    fig.update_layout(
        title={'text': 'Avg Onboarding Days by Created Cohort', 'font': {'size': 16}},
        xaxis_title='Created Month',
        yaxis_title='Average Days',
        template='plotly_white',
        height=320,
        margin=dict(l=20, r=20, t=70, b=40),
        yaxis=dict(range=[50, 100]),
    )

    return fig


def create_distribution_chart():
    """Create histogram for onboarding distribution"""
    fig = go.Figure()

    colors = [COLORS['green'] if b in ['0-20', '20-40'] else
              (COLORS['red'] if b == '100+' else COLORS['blue'])
              for b in distribution_data['Bin']]

    fig.add_trace(go.Bar(
        x=distribution_data['Bin'],
        y=distribution_data['Pct'],
        marker_color=colors,
        text=[f"{p}%" for p in distribution_data['Pct']],
        textposition='outside',
    ))

    fig.update_layout(
        title={'text': 'Onboarding Days Distribution (N=95)', 'font': {'size': 16}},
        xaxis_title='Days to Onboard',
        yaxis_title='% of Customers',
        template='plotly_white',
        height=320,
        margin=dict(l=20, r=20, t=70, b=40),
        yaxis=dict(range=[0, 38]),
    )

    return fig


def create_acv_chart():
    """Create bar chart for ACV bands showing % of customer distribution"""
    # Calculate percentages
    total_customers = acv_onboarding_data['N'].sum()
    acv_onboarding_data['Pct'] = (acv_onboarding_data['N'] / total_customers * 100).round(0).astype(int)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=acv_onboarding_data['ACV_Band'],
        y=acv_onboarding_data['Pct'],
        marker_color=COLORS['blue'],
        text=[f"{p}%<br>({d} days)" for p, d in zip(acv_onboarding_data['Pct'], acv_onboarding_data['Avg_Days'])],
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Customers: %{customdata[0]}<br>Avg Days: %{customdata[1]}<extra></extra>",
        customdata=list(zip(acv_onboarding_data['N'], acv_onboarding_data['Avg_Days'])),
    ))

    # Add correlation annotation
    fig.add_annotation(
        x='$10K-$25K', y=55,
        text="r = 0.25 (weak positive correlation)",
        showarrow=False,
        font=dict(size=11, color=COLORS['gray']),
        bgcolor='rgba(255,255,255,0.8)',
    )

    fig.update_layout(
        title={'text': 'Customer Distribution by ACV Band (with Avg Onboarding Days)', 'font': {'size': 16}},
        xaxis_title='ACV Band',
        yaxis_title='% of Customers',
        template='plotly_white',
        height=320,
        margin=dict(l=20, r=20, t=70, b=40),
        yaxis=dict(range=[0, 60]),
    )

    return fig


def create_non_live_chart():
    """Create horizontal bar chart for non-live categories"""
    # Sort by ACV
    df_sorted = non_live_data.sort_values('ACV', ascending=True)

    colors_map = {
        'Never Onboarded': COLORS['gray'],
        'On Hold': COLORS['gray'],
        'At Risk': COLORS['orange'],
        'Low Risk': COLORS['green'],
    }

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=[f"{row['Category']} (N={row['N']})" for _, row in df_sorted.iterrows()],
        x=df_sorted['ACV'],
        orientation='h',
        marker_color=[colors_map[cat] for cat in df_sorted['Category']],
        text=[f"${row['ACV']}M" for _, row in df_sorted.iterrows()],
        textposition='outside',
    ))

    fig.update_layout(
        title={'text': 'Non-Live Pipeline by Category (N=261, $7.0M ACV)', 'font': {'size': 16}},
        xaxis_title='ACV ($M)',
        yaxis_title='',
        template='plotly_white',
        height=300,
        margin=dict(l=20, r=80, t=70, b=40),
        xaxis=dict(range=[0, 4.2]),
    )

    return fig


def create_at_risk_breakdown():
    """Create stacked bar chart for At Risk breakdown"""
    fig = go.Figure()

    # Stacked horizontal bar
    fig.add_trace(go.Bar(
        y=['At Risk (N=72)'],
        x=[54],
        name='No incoming comms',
        orientation='h',
        marker_color=COLORS['orange'],
        text=['54 (75%)'],
        textposition='inside',
        insidetextanchor='middle',
    ))

    fig.add_trace(go.Bar(
        y=['At Risk (N=72)'],
        x=[18],
        name='Low response / other',
        orientation='h',
        marker_color=COLORS['light_orange'],
        text=['18 (25%)'],
        textposition='inside',
        insidetextanchor='middle',
    ))

    fig.update_layout(
        title={'text': 'At Risk Breakdown (N=72)', 'font': {'size': 16}},
        xaxis_title='Customer Count',
        yaxis_title='',
        template='plotly_white',
        height=200,
        barmode='stack',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        margin=dict(l=20, r=20, t=80, b=40),
    )

    return fig


# =============================================================================
# INSIGHT BOX STYLE (reusable)
# =============================================================================
INSIGHT_STYLE = {
    'fontSize': '14px',
    'color': '#555',
    'marginBottom': '10px',
    'fontStyle': 'italic',
    'backgroundColor': '#f8f9fa',
    'padding': '10px 15px',
    'borderRadius': '5px',
    'borderLeft': '3px solid #1f77b4',
}

# =============================================================================
# DASHBOARD LAYOUT
# =============================================================================

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Traild Customer Onboarding Analysis",
                style={'marginBottom': '5px', 'color': '#333', 'fontSize': '28px'}),
        html.P("RevOps Case Study | CRM data extract for records created Oct 2024 – Jan 2025",
               style={'color': '#666', 'fontSize': '16px', 'marginTop': '0'}),
    ], style={'textAlign': 'center', 'padding': '25px', 'backgroundColor': '#f8f9fa'}),

    # Main content
    html.Div([
        # Executive Summary Section
        html.Div([
            html.H2("Executive Summary", style={'fontSize': '20px', 'marginBottom': '15px'}),
            dcc.Graph(figure=create_kpi_cards(), config={'displayModeBar': False}),
            html.Div([
                html.P([
                    html.Strong("Key Finding: "),
                    "Onboarding performance is underperforming and deteriorating: average days increased from 65 (Oct-24) to 88 (Jan-25). ",
                    "$3.6M ACV is 'At Risk' or 'On Hold'. Delays are likely to have negative impacts on customer satisfaction and net revenue retention."
                ], style={'backgroundColor': '#fff3cd', 'padding': '15px', 'borderRadius': '5px',
                         'borderLeft': '4px solid #ffc107', 'fontSize': '14px', 'margin': '15px 0'})
            ]),
        ], style={'marginBottom': '40px'}),

        # Segmentation Overview
        html.Div([
            html.H2("Customer Segmentation Overview", style={'fontSize': '20px', 'marginBottom': '15px'}),
            dcc.Graph(figure=create_segmentation_chart(), config={'displayModeBar': False}),
        ], style={'marginBottom': '40px'}),

        html.Hr(style={'margin': '40px 0'}),

        # Part 1: Live & Active Client Onboarding
        html.Div([
            html.H2("Part 1: Live & Active Client Onboarding",
                    style={'fontSize': '20px', 'marginBottom': '25px', 'color': COLORS['blue']}),

            # Row 1: ERP Chart + Cohort Trend
            html.Div([
                html.Div([
                    html.P("Insight: Significant variance in avg onboarding days – MYOB=79, Syspro=96, Acumatica=19, Xero=29",
                           style=INSIGHT_STYLE),
                    dcc.Graph(figure=create_erp_chart(), config={'displayModeBar': False}),
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),

                html.Div([
                    html.P("Insight: 35% increase in onboarding time over 4 months (65 → 88 days)",
                           style=INSIGHT_STYLE),
                    dcc.Graph(figure=create_cohort_trend(), config={'displayModeBar': False}),
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            ], style={'marginBottom': '30px'}),

            # Row 2: Distribution + ACV Correlation
            html.Div([
                html.Div([
                    html.P("Insight: Bimodal pattern – 29% onboard in <20 days, but 29% take 100+ days",
                           style=INSIGHT_STYLE),
                    dcc.Graph(figure=create_distribution_chart(), config={'displayModeBar': False}),
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),

                html.Div([
                    html.P("Insight: Higher-value clients ($25K+) take 115+ days vs 42 days for <$5K",
                           style=INSIGHT_STYLE),
                    dcc.Graph(figure=create_acv_chart(), config={'displayModeBar': False}),
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            ]),
        ], style={'marginBottom': '40px'}),

        html.Hr(style={'margin': '40px 0'}),

        # Part 2: Non-Live Pipeline Risk
        html.Div([
            html.H2("Part 2: Non-Live Pipeline Risk",
                    style={'fontSize': '20px', 'marginBottom': '25px', 'color': COLORS['orange']}),

            html.Div([
                html.P("Insight: $2.3M stuck in 'On Hold'; $1.3M 'At Risk' needs urgent intervention",
                       style={**INSIGHT_STYLE, 'borderLeft': '3px solid #ff7f0e'}),
                dcc.Graph(figure=create_non_live_chart(), config={'displayModeBar': False}),
            ], style={'marginBottom': '30px'}),

            html.Div([
                html.P("Insight: 75% of At Risk clients (54 of 72) have never responded to outreach",
                       style={**INSIGHT_STYLE, 'borderLeft': '3px solid #ff7f0e'}),
                dcc.Graph(figure=create_at_risk_breakdown(), config={'displayModeBar': False}),
            ]),
        ]),

        # Footer
        html.Div([
            html.Hr(),
            html.P("Dashboard built with Plotly Dash | Data source: Traild CRM Export (Oct 2024 - Jan 2025)",
                   style={'textAlign': 'center', 'color': '#999', 'fontSize': '12px'}),
        ], style={'marginTop': '40px'}),

    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '30px'}),

], style={'backgroundColor': 'white', 'minHeight': '100vh', 'fontFamily': 'Arial, sans-serif'})


# =============================================================================
# RUN SERVER
# =============================================================================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("Traild Customer Onboarding Analysis Dashboard")
    print("="*60)
    print("\nStarting server... Open http://127.0.0.1:8050 in your browser")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True)
