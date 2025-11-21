import dash
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
from statsmodels.tsa.holtwinters import ExponentialSmoothing  # For predictive analysis

# Load and preprocess data
raw_data_path = 'data/Updated_Sales_Records.csv'
df = pd.read_csv(raw_data_path)

# Ensure the Date column is datetime
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Initialize the Dash app with suppress_callback_exceptions
app = Dash(__name__, suppress_callback_exceptions=True)

# Define the layout of the dashboard
app.layout = html.Div(style={'backgroundColor': 'beige', 'padding': '20px'}, children=[
    dcc.Location(id='url', refresh=False),  # For navigation
    html.H1("Interactive Sales Analysis Platform for E-commerce Optimization", style={'textAlign': 'center', 'color': '#343a40', 'fontSize': '36px'}),
    
    # Navigation Bar
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '20px'}, children=[
        dcc.Link('Home', href='/home', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff', 'fontSize': '20px'}),
        dcc.Link('About', href='/about', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff', 'fontSize': '20px'}),
        dcc.Link('Contact', href='/contact', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff', 'fontSize': '20px'}),
    ]),
    
    # Content Area
    html.Div(id='page-content')
])

# Sales Analysis Layout
def create_analysis_layout():
    return html.Div([
        # Dropdown for selecting product categories
        html.Div([
            html.Label("Select Product Category:", style={'fontWeight': 'bold', 'fontSize': '20px'}),
            dcc.Dropdown(
                id='product-category',
                options=[{'label': cat, 'value': cat} for cat in df['Category'].unique()],
                value=df['Category'].unique()[0],
                style={'width': '50%', 'margin': 'auto', 'fontSize': '18px'}
            ),
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Date Range Selector
        html.Div([
            html.Label("Select Date Range:", style={'fontWeight': 'bold', 'fontSize': '20px'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['Date'].min(),
                end_date=df['Date'].max(),
                display_format='DD-MM-YYYY',
                style={'margin': 'auto', 'fontSize': '18px'}
            ),
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Graphs
        dcc.Graph(id='sales-trend'),
        dcc.Graph(id='revenue-category'),
        dcc.Graph(id='customer-segmentation'),
        dcc.Graph(id='sales-prediction'),
        dcc.Graph(id='top-products'),
        dcc.Graph(id='sales-distribution'),
        dcc.Graph(id='region-sales-map'),  # New: Region-wise Sales Map
        dcc.Graph(id='product-sales-revenue'),  # New: Product Sales and Revenue Graph
    ], style={'marginTop': '20px'})

# Home Page Layout
home_layout = html.Div([
    html.H2("Welcome to the Sales Analysis Platform", style={'textAlign': 'center', 'fontSize': '28px'}),
    html.Div([
        html.Label("Login or Sign Up", style={'fontWeight': 'bold', 'fontSize': '20px'}),
        dcc.Input(id='username', type='text', placeholder='Username', style={'margin': '10px', 'width': '300px', 'padding': '10px', 'fontSize': '18px'}),
        dcc.Input(id='password', type='password', placeholder='Password', style={'margin': '10px', 'width': '300px', 'padding': '10px', 'fontSize': '18px'}),
        html.Button('Login', id='login-button', n_clicks=0, style={'margin': '10px', 'backgroundColor': '#007bff', 'color': 'white', 'padding': '10px', 'fontSize': '18px'}),
        html.Button('Sign Up', id='signup-button', n_clicks=0, style={'margin': '10px', 'backgroundColor': '#28a745', 'color': 'white', 'padding': '10px', 'fontSize': '18px'}),
        html.Div(id='login-output', style={'marginTop': '20px', 'fontSize': '18px'})
    ], style={'textAlign': 'center', 
              'backgroundImage': 'url(https://t4.ftcdn.net/jpg/01/19/11/55/360_F_119115529_mEnw3lGpLdlDkfLgRcVSbFRuVl6sMDty.jpg)',  
              'backgroundSize': 'cover',  
              'backgroundPosition': 'center',  
              'color': 'black', 
              'padding': '50px', 
              'borderRadius': '10px'})])
 

# About Page Layout
about_layout = html.Div([
    html.H2("About This Platform", style={'textAlign': 'center', 'fontSize': '28px'}),
    html.P("In the era of digital commerce, businesses generate a wealth of data that, when properly analysed, can offer valuable insights into customer behaviour, sales performance, and market trends. To help organizations harness the power of this data, we present an Interactive Sales Analysis Platform for E-commerce Optimization. This platform is a comprehensive dashboard built using Python, Dash, Pandas, and Plotly, aiming to provide actionable insights into e-commerce sales data through interactive visualizations and advanced analytics.", style={'textAlign': 'center', 'fontSize': '18px'}),
    html.P("This platform integrates essential functionalities, such as sales trend analysis, revenue breakdowns, customer segmentation, predictive analytics, and region-based performance mapping. The goal is to empower decision-makers with a tool that not only showcases historical performance but also enables them to forecast future trends and make data-driven decisions.", style={'textAlign': 'center', 'fontSize': '18px'}),
    
    html.H3("Key Features of the Dashboard", style={'textAlign': 'center', 'fontSize': '24px', 'bold': 'bold'}),
    html.Ul([
        html.Li("Sales Trend Analysis: Understanding how sales evolve over time is crucial for recognizing patterns and planning strategies. This feature visualizes revenue trends for a selected product category over a specified date range. Users can easily explore how seasonal changes or specific events influence sales performance, enabling more precise inventory and marketing planning."),
        html.Li("Revenue Breakdown by Product: Businesses often need to identify their top-performing products within a specific category. The dashboard includes a bar chart visualization that breaks down revenue contributions from different products, making it easy to spot best-sellers and underperformers within a selected category."),
        html.Li("Customer Segmentation: Knowing your customers is as important as knowing your products. By displaying a pie chart of customer types for a selected category, the platform helps businesses understand which customer segments generate the most revenue. This information is invaluable for tailoring marketing campaigns and optimizing customer experience."),
        html.Li("Sales Prediction Using Time-Series Analysis: Predicting future sales is a cornerstone of effective e-commerce management. By employing the Holt-Winters Exponential Smoothing model, the dashboard forecasts future sales trends for a selected category. This feature provides a 12-month sales projection, helping businesses anticipate demand and adjust their strategies accordingly."),
        html.Li("Top 10 Products by Revenue: Identifying the most profitable products is essential for optimizing inventory and marketing efforts. This feature generates a bar chart of the top 10 products based on revenue, giving businesses a clear picture of their strongest revenue drivers."),
        html.Li("Sales Distribution Analysis: Understanding the distribution of sales data can highlight variations in customer purchases. A histogram visualization displays the frequency distribution of revenue, allowing users to spot trends, outliers, and anomalies in the data."),
        html.Li("Region-Wise Sales Analysis: Geographic performance analysis is crucial for businesses operating in multiple regions. A choropleth map visualizes revenue contributions from different regions, providing insights into location-based sales patterns. This information can guide decisions on regional marketing, logistics, and product availability."),
        html.Li("Product Sales and Revenue Analysis: To complement revenue analysis, the platform also provides insights into the number of units sold per product alongside revenue. A grouped bar chart displays these metrics, offering a dual perspective on product performance."),
    ], style={'textAlign': 'left', 'marginLeft': '20px', 'fontSize': '18px', 'bold': 'bold'}),
    
    html.H3("Technical Overview", style={'textAlign': 'center', 'fontSize': '24px', 'bold': 'bold'}),
    html.P("The platform is implemented in Python, leveraging the following libraries and frameworks:", style={'textAlign': 'center', 'fontSize': '18px'}),
    html.Ul([
        html.Li("Dash: A powerful web application framework for building interactive dashboards."),
        html.Li("Pandas: Used for efficient data manipulation and preprocessing."),
        html.Li("Plotly: Enables the creation of interactive and visually appealing charts."),
        html.Li("Statsmodels: Provides advanced statistical models, such as the Holt-Winters Exponential Smoothing, for predictive analytics."),
    ], style={'textAlign': 'left', 'marginLeft': '20px', 'fontSize': '18px', 'bold': 'bold'}),
    
    html.H3("Data Preprocessing", style={'textAlign': 'center', 'fontSize': '24px',  'bold': 'bold'}),
    html.P("The dataset (Updated_Sales_Records.csv) is loaded using Pandas, and necessary preprocessing steps are applied:", style={'textAlign': 'center', 'fontSize': '18px'}),
    html.Ul([
        html.Li("Converting the Date column to datetime format ensures proper handling of time-series data."),
        html.Li("Grouping data by Region and Product provides summaries required for various visualizations."),
    ], style={'textAlign': 'left', 'marginLeft': '20px', 'fontSize': '18px', 'bold': 'bold'}),
    
    html.H3("Dashboard Layout", style={'textAlign': 'center', 'fontSize': '24px',  'bold': 'bold'}),
    html.P("The dashboard's layout is defined using Dash's html and dcc components, organized into sections for:", style={'textAlign': 'center', 'fontSize': '18px'}),
    html.Ul([
        html.Li("Dropdown selection for product categories."),
        html.Li("Date range selection."),
        html.Li("Multiple interactive graphs for sales and revenue analysis."),
    ], style={'textAlign': 'left', 'marginLeft': '20px', 'fontSize': '18px', 'bold': 'bold'}),
    
    html.H3("Interactivity with Callbacks", style={'textAlign': 'center', 'fontSize': '24px'}),
    html.P("Dash's callback mechanism allows the application to update visualizations dynamically based on user inputs. For instance:", style={'textAlign': 'center', 'fontSize': '18px'}),
    html.Ul([
        html.Li("Selecting a different product category updates the sales trend, revenue breakdown, and other graphs."),
        html.Li("Adjusting the date range dynamically filters the data to display relevant trends and patterns."),
    ], style={'textAlign': 'left', 'marginLeft': '20px', 'fontSize': '18px', 'bold': 'bold'}),
    
    html.H3("Predictive Analytics", style={'textAlign': 'center', 'fontSize': '24px'}),
    html.P("The sales prediction feature uses the Holt-Winters Exponential Smoothing model from the statsmodels library. This model considers seasonality and trends to forecast future revenue for a selected product category. The predictions are visualized as an interactive line chart.", style={'textAlign': 'center', 'fontSize': '18px'}),
    
    html.H3("Benefits of the Platform", style={'textAlign': 'center', 'fontSize': '24px'}),
    html.Ul([
        html.Li("Data-Driven Decision Making: The platform enables businesses to identify strengths and weaknesses in their sales strategy by analyzing detailed visualizations of revenue, sales trends, and customer segmentation."),
        html.Li("Actionable Insights: Interactive visualizations provide actionable insights, such as the most profitable regions, products, and customer segments. These insights can guide marketing, inventory, and operational decisions."),
        html.Li("Forecasting and Planning: By predicting future sales trends, the platform empowers businesses to plan effectively for upcoming seasons, promotional campaigns, and product launches."),
        html.Li("Enhanced User Experience: The platform’s interactivity and intuitive design ensure that users can explore data without needing technical expertise, making advanced analytics accessible to decision-makers across departments."),
        html.Li("Scalability and Customization: Built on Python and Dash, the platform is highly scalable and can be customized to accommodate additional features, such as integrating real-time data or incorporating machine learning models for deeper analysis."),
    ], style={'textAlign': 'left', 'marginLeft': '20px', 'fontSize': '18px', 'bold': 'bold'}),
], style={'textAlign': 'center', 
          'backgroundImage': 'url(https://t4.ftcdn.net/jpg/03/01/98/59/360_F_301985997_w5OZVg27eKFVQ7BuYKu4ybJJbVIRxx7k.webp)',  
          'backgroundSize': 'cover', 
          'color': 'black', 
          'padding': '50px', 
          'borderRadius': '10px'})

# Contact Page Layout
contact_layout = html.Div([
    html.H2("Contact Us\n", style={'textAlign': 'center'}),
    html.P("Name: Varun Gangadhari\n", style={'textAlign': 'center'}),
    html.P("Phone Number: 9491200841\n", style={'textAlign': 'center'}),
    html.P("Email: 217y1a67j2@mlritm.ac.in\n", style={'textAlign': 'center'}),
    html.P("LinkedIn: https://www.linkedin.com/in/gangadhari-varun-485a95141/\n", style={'textAlign': 'center'}),
],  style={'textAlign': 'center', 
          'backgroundImage': 'url(https://t3.ftcdn.net/jpg/05/30/96/04/360_F_530960431_c8fPd3HansYvrSJ4fJxZqp9OhjQmYoll.jpg)',  
          'backgroundSize': 'cover', 
          'color': 'black', 
          'padding': '50px', 
          'borderRadius': '10px'})

# Callback to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/home':
        return home_layout
    elif pathname == '/about':
        return about_layout
    elif pathname == '/contact':
        return contact_layout
    else:
        return create_analysis_layout()  # Default to sales analysis layout

# Callback for login/signup actions
@app.callback(
    Output('login-output', 'children'),
    [Input('login-button', 'n_clicks'),
     Input('signup-button', 'n_clicks')],
    [State('username', 'value'),
     State('password', 'value')]
)
def handle_login_signup(login_clicks, signup_clicks, username, password):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    try:
        if button_id == 'login-button':
            if username and password:
                return f"Logged in as {username}!"
            else:
                return "Please enter both username and password."
        elif button_id == 'signup-button':
            if username and password:
                return f"Signed up with username {username}!"
            else:
                return "Please enter both username and password."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Callbacks for interactive updates
@app.callback(
    Output('sales-trend', 'figure'),
    [Input('product-category', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_sales_trend(selected_category, start_date, end_date):
    filtered_df = df[(df['Category'] == selected_category) & 
                     (df['Date'] >= start_date) & 
                     (df['Date'] <= end_date)]
    sales_trend = filtered_df.groupby('Date')['Revenue'].sum().reset_index()
    return px.line(sales_trend, x='Date', y='Revenue', title=f'Sales Trend for {selected_category}', template='plotly_dark')

@app.callback(
    Output('revenue-category', 'figure'),
    [Input('product-category', 'value')]
)
def update_revenue_category(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    revenue_by_product = filtered_df.groupby('Product')['Revenue'].sum().reset_index()
    return px.bar(revenue_by_product, x='Product', y='Revenue', title=f'Revenue by Product for {selected_category}', template='plotly_dark')

@app.callback(
    Output('customer-segmentation', 'figure'),
    [Input('product-category', 'value')]
)
def update_customer_segmentation(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    customer_segments = filtered_df['Customer Type'].value_counts().reset_index()
    customer_segments.columns = ['Customer Type', 'Count']  # Rename the columns for clarity
    return px.pie(customer_segments, names='Customer Type', values='Count', title='Customer Segmentation', template='plotly_dark')

@app.callback(
    Output('sales-prediction', 'figure'),
    [Input('product-category', 'value')]
)
def predict_sales(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    
    if filtered_df.empty:
        return px.line(title='No data available for this category', template='plotly_dark')
    
    sales_trend = filtered_df.groupby('Date')['Revenue'].sum()
    
    if len(sales_trend) < 2:
        return px.line(title='Not enough data to make predictions', template='plotly_dark')
    
    try:
        model = ExponentialSmoothing(sales_trend, seasonal='add', seasonal_periods=12).fit()
        future_dates = pd.date_range(start=sales_trend.index[-1], periods=12, freq='M')
        prediction = model.forecast(12)
        
        prediction_df = pd.DataFrame({'Date': future_dates, 'Revenue': prediction})
        return px.line(prediction_df, x='Date', y='Revenue', title='Sales Prediction for Next 12 Months', template='plotly_dark')
    
    except Exception as e:
        return px.line(title='Error in prediction', template='plotly_dark')

@app.callback(
    Output('top-products', 'figure'),
    [Input('product-category', 'value')]
)
def update_top_products(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    top_n = filtered_df.groupby('Product')['Revenue'].sum().nlargest(10).reset_index()
    return px.bar(top_n, x='Product', y='Revenue', title='Top 10 Products by Revenue', template='plotly_dark')

@app.callback(
    Output('sales-distribution', 'figure'),
    [Input('product-category', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_sales_distribution(selected_category, start_date, end_date):
    filtered_df = df[(df['Category'] == selected_category) & 
                     (df['Date'] >= start_date) & 
                     (df['Date'] <= end_date)]
    
    if filtered_df.empty:
        return px.histogram(title='No data available for this category and date range', template='plotly_dark')
    
    return px.histogram(filtered_df, x='Revenue', title='Sales Distribution', nbins=30, template='plotly_dark')

@app.callback(
    Output('region-sales-map', 'figure'),
    [Input('product-category', 'value')]
)
def update_region_sales_map(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    region_sales = filtered_df.groupby('Region')['Revenue'].sum().reset_index()
    
    fig = px.choropleth(
        region_sales,
        locations='Region',
        locationmode='country names',
        color='Revenue',
        title=f'Region-wise Sales for {selected_category}',
        color_continuous_scale=px.colors.sequential.Plasma,
        template='plotly_dark'
    )
    
    return fig

@app.callback(
    Output('product-sales-revenue', 'figure'),
    [Input('product-category', 'value')]
)
def update_product_sales_revenue(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    product_sales = filtered_df.groupby('Product').agg({'Revenue': 'sum', 'Product': 'count'}).rename(columns={'Product': 'Units Sold'}).reset_index()
    
    fig = px.bar(product_sales, x='Product', y=['Revenue', 'Units Sold'], barmode='group',
                  title=f'Sales Revenue and Units Sold for {selected_category}', template='plotly_dark')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)