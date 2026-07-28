import streamlit as st
import pandas as pd
import plotly.express as px

company = st.text_input('Company Name')
st.title(f'{company} Employee Performance Dashboard')

st.markdown('''
**Welcome to the Employee Performance Dashboard.**

Upload your sales data to instantly generate performance insights across your team with finanical modeling & KPI metrics. 
Track individual sales attainment, profit margins, and department breakdowns.

**Your CSV must include the following columns:**
- Employee
- Region  
- Sales
- Target
- Expenses

Don't have a CSV? Download a sample dataset below to see the dashboard in action.
''')

#Sample Data
st.subheader('Try a Sample Dataset')
col1, col2 = st.columns(2)
with col1:
    with open('MOCK_DATA (12).csv', 'rb') as f:
        st.download_button('Download Sample Dataset 1', f, 'sample_employee_data1.csv')

with col2:
    with open('MOCK_DATA (13).csv', 'rb') as f:
        st.download_button('Download Sample Dataset 2', f, 'sample_employee_data2.csv')


st.divider()

#File Uploader
uploaded_file = st.file_uploader('Upload CSV', type='csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.title()

    #Error Message
    required_columns = ['Employee', 'Region', 'Sales', 'Target', 'Expenses']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f'Missing required columns: {", ".join(missing_columns)}. Please check your CSV and try again.')
        st.stop()
    
    df['Profit'] = df['Sales'] - df['Expenses']
    df['Profit Margin %'] = (df['Profit'] / df['Sales'])*100
    df['Attainment %'] = (df['Sales']/df['Target'])*100

    st.subheader('KPI Metrics')
    col1, col2, col3 = st.columns(3)
    col1.metric('Total Sales', f'${df['Sales'].sum():,.0f}')
    col2.metric('Total Profit', f'${df['Profit'].sum():,.0f}')
    col3.metric('Average Attainment %', f'{df['Attainment %'].mean():.2f}%')

    with st.sidebar:
        st.header('Filters')
        region = st.selectbox('Select Region', ['All'] + list(df['Region'].unique()))

    if region != 'All':
        df = df[df['Region'] == region]

    st.subheader('Region Summary')
    region_summary = df.groupby('Region')[['Sales', 'Profit', 'Attainment %']].mean().round(2)
    st.dataframe(region_summary)

    st.subheader('Employee Data')
    st.dataframe(df)

    fig1 = px.bar(df, x = 'Employee', y = 'Sales', title = 'Sales by Employee',
                  color = 'Region')
    st.plotly_chart(fig1)
    
    fig2 = px.bar(df, x = 'Employee', y = 'Attainment %', title = 'Attainment % by Employee',
                    color = 'Attainment %',
                    color_continuous_scale=['red', 'green'],
                    color_continuous_midpoint=100)
    st.plotly_chart(fig2)

    fig3 = px.bar(df, x='Region', y='Profit', title = 'Profit By Region',
                  color = 'Region')
    st.plotly_chart(fig3)

    st.download_button('Download Processed Data', df.to_csv(index=False), 'processed_data.csv')