import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Create a Dash web application
app = dash.Dash(__name__)

# Layout of the application
app.layout = html.Div([
    # Title of the Dashboard
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center'}),
    
    # Task 1: Launch Site Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    # Task 2: Success Pie Chart
    dcc.Graph(id='success-pie-chart'),

    # Title above the Payload Range Slider
    html.H3("Payload range (Kg):", style={'textAlign': 'left'}),
    
    # Task 3: Payload Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0',
               2500: '2500',
               5000: '5000',
               7500: '7500',
               10000: '10000'},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),

    # Task 4: Success Payload Scatter Chart
    dcc.Graph(id='success-payload-scatter-chart')
])

# Task 2: Callback function for Success Pie Chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
                     names='Launch Site', 
                     title='Success Rate for All Launch Sites')
    else:
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        success_rate = site_filtered_df.groupby('class').size() / len(site_filtered_df) * 100
        fig = px.pie(names=success_rate.index, values=success_rate.values, 
                     title=f'Success Rate for {entered_site}', 
                     labels={'1': 'Success', '0': 'Failure'})
    
    return fig

# Task 4: Callback function for Success Payload Scatter Chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(selected_site, selected_payload):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload[0]) &
                             (spacex_df['Payload Mass (kg)'] <= selected_payload[1])]
    
    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs Success/Failure for All Launch Sites')
    else:
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(site_filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs Success/Failure for {selected_site}')
    # Update the x-axis range title and marks
    fig.update_xaxes(title_text='Payload Mass (kg)', range=[selected_payload[0], selected_payload[1]])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
