import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


def dropdown_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
style_url = ['https://github.com/STATWORX/blog/blob/master/DashApp/assets/style.css']
headline = [
    html.H2('Dash - STOCK PRICES'),
    html.P('''Visualising time series with Plotly - Dash'''),
    html.P('''Pick one or more stocks from the dropdown below.''')
]
graph1 = dcc.Graph(
    id='timeseries',
    config={'displayModeBar': False}
)
graph2 = dcc.Graph(
    id='change',
    config={'displayModeBar': False}
)
dropdown_menu = [
    html.Div(
        className='div-for-dropdown',
        children=[
            dcc.Dropdown(
                id='stockselector',
                options=dropdown_options(df['stock'].unique()),
                multi=True,
                value=[df['stock'].sort_values()[0]],
                style={'backgroundColor': '#1E1E1E'},
                className='stockselector')
    ],
    style={'color': '#1E1E1E'}
)]

plotting_colors = [
    '#D8B564',
    '#4A79E2',
    '#E24AC1',
    '#4AE25B',
    '#8ED864',

]

app = dash.Dash(__name__)
app.layout = html.Div(
    children= [
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='four columns div-user-controls',
                    children = headline+dropdown_menu
                ),
                html.Div(
                    className='eight columns div-for-charts bg-grey',
                    children=[
                        graph1,
                        graph2
                    ]
                )
            ]
            
            
        )
    ]
)


@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:   
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))  
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=plotting_colors,
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

    }

    return figure


@app.callback(Output('change', 'figure'),
              [Input('stockselector', 'value')])
def update_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    trace = []
    df_sub = df
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['change'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=plotting_colors,
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=250,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Daily Change', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
              ),
              }

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)