import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the dataset
data = pd.read_csv("historical_automobile_sales.csv")

# Task 1.1: Line chart showing yearly automobile sales
sales_by_year = data.groupby('Year')['Automobile_Sales'].sum()
plt.figure(figsize=(10, 6))
plt.plot(sales_by_year.index, sales_by_year.values, marker='o', linestyle='-', color='b')
plt.title('Yearly Automobile Sales Trend', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Automobile Sales', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('task_1_1_line_chart.png')

# Task 1.2: Line chart for different vehicle categories during recession/non-recession
plt.figure(figsize=(12, 6))
for vehicle_type in data['Vehicle_Type'].unique():
    subset = data[data['Vehicle_Type'] == vehicle_type]
    sales_trend = subset.groupby(['Year', 'Recession'])['Automobile_Sales'].sum().unstack()
    plt.plot(sales_trend.index, sales_trend[1], label=f'{vehicle_type} (Recession)')
    plt.plot(sales_trend.index, sales_trend[0], linestyle='--', label=f'{vehicle_type} (Non-Recession)')
plt.title('Sales Trends by Vehicle Type during Recession/Non-Recession', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Automobile Sales', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('task_1_2_vehicle_trends.png')

# Task 1.3: Sales trend comparison using Seaborn
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='Year', y='Automobile_Sales', hue='Recession')
plt.title('Sales Trends: Recession vs Non-Recession', fontsize=14)
plt.tight_layout()
plt.savefig('task_1_3_seaborn_plot.png')

# Task 1.4: GDP variations during recession/non-recession
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='Year', y='GDP', hue='Recession', style='Recession')
plt.title('GDP Variations: Recession vs Non-Recession', fontsize=14)
plt.tight_layout()
plt.savefig('task_1_4_gdp_variations.png')

# Task 1.5: Bubble plot for seasonality impact
plt.figure(figsize=(10, 6))
sizes = data['Seasonality_Weight'] * 100  # Scale for better visualization
plt.scatter(data['Month'], data['Automobile_Sales'], s=sizes, alpha=0.5, c='blue')
plt.title('Seasonality Impact on Automobile Sales', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Automobile Sales', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('task_1_5_bubble_plot.png')

# Task 1.6: Scatter plot for price vs sales during recession
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='Price', y='Automobile_Sales', hue='Recession')
plt.title('Price vs Sales during Recession', fontsize=14)
plt.tight_layout()
plt.savefig('task_1_6_scatter_plot.png')

# Task 1.7 & 1.8: Pie charts for advertising expenditure
ad_expenditure = data.groupby('Recession')['Advertising_Expenditure'].sum()
plt.figure(figsize=(8, 8))
plt.pie(ad_expenditure, labels=['Non-Recession', 'Recession'], autopct='%1.1f%%', colors=['lightblue', 'orange'])
plt.title('Advertising Expenditure during Recession/Non-Recession')
plt.savefig('task_1_7_8_pie_chart.png')

# Task 1.9: Unemployment rate effect on sales
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='Year', y='unemployment_rate', hue='Vehicle_Type', style='Recession')
plt.title('Unemployment Rate Effect on Sales', fontsize=14)
plt.tight_layout()
plt.savefig('task_1_9_line_plot.png')

# Part 2: Dash Application
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Automobile Sales Dashboard", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='vehicle-type-dropdown',
        options=[{'label': vt, 'value': vt} for vt in data['Vehicle_Type'].unique()],
        value=data['Vehicle_Type'].unique()[0],
        placeholder="Select a vehicle type",
    ),
    html.Div(id='output-container', style={'marginTop': '20px'}),
    dcc.Graph(id='recession-stats-graph'),
    dcc.Graph(id='yearly-stats-graph')
])

@app.callback(
    [Output('recession-stats-graph', 'figure'),
     Output('yearly-stats-graph', 'figure')],
    [Input('vehicle-type-dropdown', 'value')]
)
def update_graphs(selected_vehicle):
    filtered_data = data[data['Vehicle_Type'] == selected_vehicle]

    # Recession Report Statistics
    fig1 = px.line(filtered_data, x='Year', y='Automobile_Sales', color='Recession',
                   title=f'Sales Trend for {selected_vehicle} during Recession/Non-Recession')

    # Yearly Report Statistics
    fig2 = px.line(filtered_data, x='Year', y='Automobile_Sales',
                   title=f'Yearly Sales Trend for {selected_vehicle}')

    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)