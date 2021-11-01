# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='id',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="place holder here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `success-pie-chart` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='id', component_property='value'))


def get_graph(site):
    # Select 2019 data
    filtered_df = spacex_df
    if site == 'ALL':
        fig = px.pie(filtered_df, values=filtered_df['Mission Outcome'].value_counts(),names=filtered_df['Mission Outcome'].value_counts().index, title='title')

        return fig
    else:
        df =  filtered_df[filtered_df['Launch Site']==site]
        fig = px.pie(df, values=df['Mission Outcome'].value_counts(),names=df['Mission Outcome'].value_counts().index, title='title')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='id', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_graph_scatter(site,slider):
    # Select 2019 data
    filtered_df = spacex_df
    filtered_df=filtered_df.loc[filtered_df['Payload Mass (kg)'] > slider[0]]
    filtered_df=filtered_df.loc[slider[1] > filtered_df['Payload Mass (kg)']]
    print(filtered_df)

    if site == 'ALL':
        fig = px.scatter(y=filtered_df['Mission Outcome'], x=filtered_df['Payload Mass (kg)'] )

        return fig
    else:
        df =  filtered_df[filtered_df['Launch Site']==site]
        fig=px.scatter(y=df['Mission Outcome'], x=df['Payload Mass (kg)'] )
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
