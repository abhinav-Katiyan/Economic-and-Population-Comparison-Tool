import streamlit as st
import wbgapi as wb
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

COUNTRY_CODES = {
    'BRA': 'Brazil', 'RUS': 'Russia', 'IND': 'India', 'CHN': 'China', 'ZAF': 'South Africa',
    'USA': 'United States', 'GBR': 'United Kingdom', 'CAN': 'Canada', 'AUS': 'Australia',
    'JPN': 'Japan', 'FRA': 'France', 'DEU': 'Germany', 'ITA': 'Italy', 'ESP': 'Spain',
    'MEX': 'Mexico', 'ARG': 'Argentina', 'SAU': 'Saudi Arabia', 'KOR': 'South Korea',
    'TUR': 'Turkey', 'NGA': 'Nigeria', 'EGY': 'Egypt', 'PAK': 'Pakistan', 'BGD': 'Bangladesh',
    'VNM': 'Vietnam', 'IRN': 'Iran', 'IDN': 'Indonesia', 'PHL': 'Philippines', 'THA': 'Thailand',
    'NLD': 'Netherlands', 'BEL': 'Belgium', 'SWE': 'Sweden', 'CHE': 'Switzerland',
    'AUT': 'Austria', 'NOR': 'Norway', 'DNK': 'Denmark', 'FIN': 'Finland', 'POL': 'Poland',
    'GRC': 'Greece', 'HUN': 'Hungary', 'PRT': 'Portugal', 'IRL': 'Ireland', 'CZE': 'Czech Republic',
    'SVK': 'Slovakia', 'ROU': 'Romania', 'BGR': 'Bulgaria', 'HRV': 'Croatia', 'SRB': 'Serbia',
    'UKR': 'Ukraine', 'BLR': 'Belarus', 'KAZ': 'Kazakhstan', 'UZB': 'Uzbekistan', 'TJK': 'Tajikistan',
    'KGZ': 'Kyrgyzstan', 'AFG': 'Afghanistan', 'IRQ': 'Iraq', 'SYR': 'Syria', 'JOR': 'Jordan',
    'ISR': 'Israel', 'LBN': 'Lebanon', 'OMN': 'Oman', 'YEM': 'Yemen', 'QAT': 'Qatar',
    'BHR': 'Bahrain', 'KWT': 'Kuwait', 'ARE': 'United Arab Emirates', 'SGP': 'Singapore',
    'MYS': 'Malaysia', 'MMR': 'Myanmar', 'LKA': 'Sri Lanka', 'KHM': 'Cambodia', 'LAO': 'Laos',
    'BRN': 'Brunei', 'TLS': 'Timor-Leste', 'NPL': 'Nepal', 'BTN': 'Bhutan', 'MDV': 'Maldives',
    'MNG': 'Mongolia', 'PRY': 'Paraguay', 'URY': 'Uruguay', 'BOL': 'Bolivia', 'VEN': 'Venezuela',
    'COL': 'Colombia', 'PER': 'Peru', 'CHL': 'Chile', 'ECU': 'Ecuador', 'GUY': 'Guyana',
    'SUR': 'Suriname', 'DZA': 'Algeria', 'MAR': 'Morocco', 'TUN': 'Tunisia', 'LBY': 'Libya',
    'SDN': 'Sudan', 'SSD': 'South Sudan', 'ETH': 'Ethiopia', 'KEN': 'Kenya', 'UGA': 'Uganda',
    'TZA': 'Tanzania', 'RWA': 'Rwanda', 'BDI': 'Burundi', 'MWI': 'Malawi', 'MOZ': 'Mozambique',
    'ZMB': 'Zambia', 'ZWE': 'Zimbabwe', 'BWA': 'Botswana', 'NAM': 'Namibia', 'AGO': 'Angola',
    'COD': 'Democratic Republic of the Congo', 'COG': 'Republic of the Congo', 'GAB': 'Gabon',
    'GNQ': 'Equatorial Guinea', 'CMR': 'Cameroon', 'GHA': 'Ghana', 'CIV': 'Ivory Coast',
    'LBR': 'Liberia', 'SLE': 'Sierra Leone', 'GIN': 'Guinea', 'GMB': 'Gambia', 'SEN': 'Senegal',
    'MRT': 'Mauritania', 'MLI': 'Mali', 'NER': 'Niger', 'TCD': 'Chad', 'CAF': 'Central African Republic',
    'STP': 'Sao Tome and Principe', 'CPV': 'Cape Verde', 'MDG': 'Madagascar', 'SYC': 'Seychelles',
    'MUS': 'Mauritius', 'COM': 'Comoros', 'FJI': 'Fiji', 'PNG': 'Papua New Guinea', 'SLB': 'Solomon Islands',
    'VUT': 'Vanuatu', 'WSM': 'Samoa', 'TON': 'Tonga', 'KIR': 'Kiribati', 'NRU': 'Nauru',
    'TUV': 'Tuvalu', 'FSM': 'Micronesia', 'MHL': 'Marshall Islands', 'PLW': 'Palau'
}

GROUPS = {
    'BRICS': ['BRA', 'RUS', 'IND', 'CHN', 'ZAF'],
    'NATO': ['USA', 'GBR', 'CAN', 'AUS', 'JPN', 'FRA', 'DEU', 'ITA', 'ESP', 'TUR'],
    'G7': ['USA', 'GBR', 'CAN', 'FRA', 'DEU', 'ITA', 'JPN'],
    'G20': ['ARG', 'AUS', 'BRA', 'CAN', 'CHN', 'FRA', 'DEU', 'IND', 'IDN', 'ITA', 'JPN', 'MEX', 'RUS', 'SAU', 'ZAF', 'KOR', 'TUR', 'GBR', 'USA', 'EU'],
    'EU': ['AUT', 'BEL', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK', 'SVN', 'ESP', 'SWE'],
    'ASEAN': ['BRN', 'KHM', 'IDN', 'LAO', 'MYS', 'MMR', 'PHL', 'SGP', 'THA', 'VNM'],
    'MERCOSUR': ['ARG', 'BRA', 'PRY', 'URY', 'VEN'],
    'APEC': ['AUS', 'BRN', 'CAN', 'CHL', 'CHN', 'HKG', 'IDN', 'JPN', 'KOR', 'MYS', 'MEX', 'NZL', 'PNG', 'PER', 'PHL', 'RUS', 'SGP', 'THA', 'USA', 'VNM'],
    'OPEC': ['DZA', 'AGO', 'GAB', 'IRN', 'IRQ', 'KWT', 'LBY', 'NGA', 'SAU', 'ARE', 'VEN']
}





def fetch_data(indicator, years, countries):
    try:
        if isinstance(years, list):
            data = wb.data.DataFrame(indicator, economy=countries, time=years)
            global_data = wb.data.DataFrame(indicator, economy="WLD", time=years)
        else:
            data = wb.data.DataFrame(indicator, economy=countries, time=f"YR{years}")
            global_data = wb.data.DataFrame(indicator, economy="WLD", time=f"YR{years}")
        if data.empty:
            st.warning(f"No data found for indicator {indicator} for countries {countries} and years {years}.")
            return pd.DataFrame(), pd.DataFrame()
        if global_data.empty:
            st.warning(f"No global data found for indicator {indicator} for years {years}.")
            return data, pd.DataFrame()

        if 'economy' not in data.index.names:
            data = data.set_index('economy')
        if 'economy' not in global_data.index.names:
            global_data = global_data.set_index('economy')

        return data, global_data

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame(), pd.DataFrame()

def plot_comparison(selected_code, data, global_data, metric_name, chart_type):
    if selected_code in GROUPS:
        group_name = selected_code
        try:
            if 'economy' not in data.index.names:
                data = data.set_index('economy')

            available_countries = data.index.intersection(GROUPS[group_name])
            if available_countries.empty:
                st.error(f"No data available for group: {group_name}")
                return

            group_data = data.loc[available_countries].sum()
        except KeyError:
            st.error(f"Some of the group codes {GROUPS[group_name]} are not present in the data index.")
            return

        world_value = global_data.loc['WLD'].values[0]
        selected_value = group_data.values[0]

        labels = [group_name, 'World - Other']
        sizes = [selected_value, world_value - selected_value]
    else:
        if selected_code not in data.index:
            st.error(f"Data for {selected_code} not available.")
            return

        selected_value = data.loc[selected_code].values[0]
        world_value = global_data.loc['WLD'].values[0]

        if selected_value < 0 or world_value < 0:
            st.warning(f"Negative values detected for {metric_name}. Showing bar chart instead.")
            chart_type = 'bar'

        labels = [COUNTRY_CODES[selected_code], 'World - Other']
        sizes = [selected_value, world_value - selected_value]

    if chart_type == 'pie':
        colors = ['#636EFA', '#EF553B']
        fig = px.pie(values=sizes, names=labels, title=f'{metric_name} Comparison',
                     color_discrete_sequence=colors)
    elif chart_type == 'bar':
        fig = go.Figure(data=[
            go.Bar(name=labels[0], x=[labels[0]], y=[sizes[0]], marker_color='#636EFA'),
            go.Bar(name=labels[1], x=[labels[1]], y=[sizes[1]], marker_color='#EF553B')
        ])
        fig.update_layout(title=f'{metric_name} Comparison', barmode='stack')
    elif chart_type == 'line':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=labels, y=sizes,
                                 mode='lines+markers', name=metric_name, marker_color='#636EFA'))
        fig.update_layout(title=f'{metric_name} Comparison', xaxis_title='Category', yaxis_title=metric_name)
    elif chart_type == 'scatter':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[labels[0]], y=[sizes[0]], mode='markers', name=labels[0],
                                 marker_color='#636EFA'))
        fig.add_trace(go.Scatter(x=[labels[1]], y=[sizes[1]], mode='markers', name=labels[1],
                                 marker_color='#EF553B'))
        fig.update_layout(title=f'{metric_name} Comparison', xaxis_title='Category', yaxis_title=metric_name)
    else:
        st.error("Unsupported chart type.")
        return

    st.plotly_chart(fig)

def plot_country_vs_country(country_code_1, country_code_2, country_data_1, country_data_2, metric, chart_type):
    # Check and standardize column names (remove leading/trailing spaces)
    country_data_1.columns = country_data_1.columns.str.strip()
    country_data_2.columns = country_data_2.columns.str.strip()

    # Inspect the data structure
    st.write("Data for Country 1:", country_data_1.head())
    st.write("Data for Country 2:", country_data_2.head())

    if 'Country Code' in country_data_1.columns:
        is_column = True
    else:
        is_column = False

    if is_column:
        # Filter the data for the selected countries if 'Country Code' is a column
        if country_code_1 not in country_data_1['Country Code'].values or country_code_2 not in country_data_2[
            'Country Code'].values:
            st.error(f"No data found for the country codes: {country_code_1} or {country_code_2}")
            return

        data_1 = country_data_1[country_data_1['Country Code'] == country_code_1]
        data_2 = country_data_2[country_data_2['Country Code'] == country_code_2]
    else:
        # Assuming 'Country Code' might be an index or different column
        if country_code_1 not in country_data_1.index or country_code_2 not in country_data_2.index:
            st.error(f"No data found for the country codes: {country_code_1} or {country_code_2}")
            return

        data_1 = country_data_1.loc[country_code_1]
        data_2 = country_data_2.loc[country_code_2]

    if isinstance(data_1, pd.Series):
        data_1 = data_1.to_frame().T
    if isinstance(data_2, pd.Series):
        data_2 = data_2.to_frame().T


    if data_1.empty or data_2.empty:
        st.error("No data available for the selected countries.")
        return
    years_1 = [col for col in data_1.columns if col.startswith('YR')]
    years_2 = [col for col in data_2.columns if col.startswith('YR')]

    if not years_1 or not years_2:
        st.error("No valid year columns found in the data.")
        return

    values_1 = [data_1[year].values[0] for year in years_1]
    values_2 = [data_2[year].values[0] for year in years_2]

    if len(years_1) != len(values_1) or len(years_2) != len(values_2):
        st.error("Mismatch in the number of years and values.")
        return

    import plotly.graph_objects as go

    fig = go.Figure()

    if chart_type == 'line':
        fig.add_trace(go.Scatter(x=years_1, y=values_1, mode='lines', name=country_code_1))
        fig.add_trace(go.Scatter(x=years_2, y=values_2, mode='lines', name=country_code_2))
    elif chart_type == 'bar':
        fig.add_trace(go.Bar(x=years_1, y=values_1, name=country_code_1))
        fig.add_trace(go.Bar(x=years_2, y=values_2, name=country_code_2))

    fig.update_layout(title=f"Comparison of {metric} between {country_code_1} and {country_code_2}",
                      xaxis_title='Year',
                      yaxis_title=metric,
                      barmode='group' if chart_type == 'bar' else None)

    st.plotly_chart(fig)


def plot_group_vs_group(group_name_1, group_name_2, data_1, data_2, metric_name, chart_type):
    st.write(f'Comparing {group_name_1} with {group_name_2} for {metric_name}')

    data_1_df = pd.DataFrame(data_1)
    data_2_df = pd.DataFrame(data_2)

    data_1_df = data_1_df.sort_index()
    data_2_df = data_2_df.sort_index()
    data_1_df.columns = [f"{group_name_1}_{col}" for col in data_1_df.columns]
    data_2_df.columns = [f"{group_name_2}_{col}" for col in data_2_df.columns]

    combined_data = pd.concat([data_1_df, data_2_df], axis=1)

 
    combined_data = combined_data.loc[:, ~combined_data.columns.duplicated()]



    # Plot based on chart type
    if chart_type == 'line':
        st.line_chart(combined_data)
    elif chart_type == 'bar':
        # Grouped bar chart
        fig = go.Figure()

        # Add bars for each group
        for col in combined_data.columns:
            group_name = col.split('_')[0]  # Extract group name
            fig.add_trace(go.Bar(
                x=combined_data.index,
                y=combined_data[col],
                name=col,
                marker=dict(line=dict(width=1.5, color='black'))
            ))

        fig.update_layout(
            title=f'{metric_name} Comparison',
            xaxis_title='Year',
            yaxis_title=metric_name,
            barmode='group',  # Grouped bar chart
            xaxis_tickangle=-45,  # Angle x-axis labels for readability
            legend_title='Groups'
        )

        st.plotly_chart(fig)
    elif chart_type == 'histogram':
        fig = go.Figure()
        for col in combined_data.columns:
            fig.add_trace(go.Histogram(x=combined_data[col], name=col))
        fig.update_layout(title=f'{metric_name} Comparison',
                          xaxis_title=metric_name,
                          yaxis_title='Frequency')
        st.plotly_chart(fig)
    elif chart_type == 'pie':
        # Aggregated data for pie chart
        data_sum = combined_data.sum()
        fig = px.pie(values=data_sum, names=data_sum.index, title=f'{metric_name} Comparison')
        st.plotly_chart(fig)
    else:
        st.error("Unsupported chart type")



def fetch_data(indicator, years, countries):
    if isinstance(years, list):
        data = wb.data.DataFrame(indicator, economy=countries, time=years)
        global_data = wb.data.DataFrame(indicator, economy="WLD", time=years)
    else:
        data = wb.data.DataFrame(indicator, economy=countries, time=f"YR{years}")
        global_data = wb.data.DataFrame(indicator, economy="WLD", time=f"YR{years}")

    return data, global_data
def fetch_group_data(indicator, years, countries):
    return wb.data.DataFrame(indicator, economy=countries, time=years)


def aggregate_group_data(group, indicator, year):
    # Ensure GROUPS is defined and contains the necessary data
    if group not in GROUPS:
        st.error(f"Group {group} is not defined in GROUPS.")
        return pd.Series(dtype=float)

    countries = GROUPS[group]
    data, _ = fetch_data(indicator, year, countries)

    if data.empty:
        st.error(f"No data available for group: {group}")
        return pd.Series(dtype=float)

    try:
        # Filter the data to include only available countries
        available_countries = data.index.intersection(countries)

        if available_countries.empty:
            st.warning(f"No available data for the countries in group {group}.")
            return pd.Series(dtype=float)

        # Aggregate data for available countries
        aggregated_data = data.loc[available_countries].sum()
        return aggregated_data
    except KeyError as e:
        st.error(f"KeyError during aggregation: {e}")
        return pd.Series(dtype=float)
    except Exception as e:
        st.error(f"Error during aggregation: {e}")
        return pd.Series(dtype=float)


def main():
    st.title('Economic and Population Comparison Tool')

    # Sidebar selection
    analysis_type = st.sidebar.radio('Select Analysis Type', ['Country Comparison', 'Country vs. Country', 'Group vs. Group'])
    chart_type = st.sidebar.selectbox('Select Chart Type:', ['bar', 'pie', 'line', 'scatter'])

    # User input for metric
    metric = st.sidebar.selectbox('Select Metric:', ['Population', 'GDP',  'GDP Growth Rate'])

    # Map metric names to World Bank API indicators
    metric_indicators = {
        'Population': 'SP.POP.TOTL',
        'GDP': 'NY.GDP.MKTP.CD',
        'Inflation': 'FP.CPI.TOTL',
        'GDP Growth Rate': 'NY.GDP.MKTP.KD.ZG'
    }
    selected_indicator = metric_indicators[metric]

    if analysis_type == 'Country Comparison':
        # Country comparison
        selected_country_code = st.sidebar.selectbox('Select Country:', list(COUNTRY_CODES.keys()),
                                                     format_func=lambda code: COUNTRY_CODES.get(code, code))
        year = st.sidebar.selectbox('Select Year:', list(range(1990, 2024)))
        country_data, global_data = fetch_data(selected_indicator, year, list(COUNTRY_CODES.keys()))

        st.subheader(f'{metric} Comparison')
        plot_comparison(selected_country_code, country_data, global_data, metric, chart_type)

    elif analysis_type == 'Group Comparison':
        # Group comparison
        selected_group_name = st.sidebar.selectbox('Select Group:', list(GROUPS.keys()))
        group_countries = GROUPS[selected_group_name]
        year = st.sidebar.selectbox('Select Year:', list(range(1990, 2024)))

        group_data, global_group_data = fetch_data(selected_indicator, year, group_countries)

        # Aggregate group data
        group_aggregated_data = aggregate_group_data(selected_group_name, selected_indicator, year)
        global_group_data.loc[selected_group_name] = group_aggregated_data

        st.subheader(f'{metric} Comparison with the World for {selected_group_name}')
        plot_comparison(selected_group_name, global_group_data, global_group_data, metric, chart_type)

        st.subheader(f'{metric} Comparison within {selected_group_name}')
        plot_comparison(selected_group_name, group_data, global_group_data, metric, chart_type)

    elif analysis_type == 'Country vs. Country':
        # Country vs. Country comparison
        selected_country_code_1 = st.sidebar.selectbox('Select First Country:', list(COUNTRY_CODES.keys()),
                                                       format_func=lambda code: COUNTRY_CODES.get(code, code))
        selected_country_code_2 = st.sidebar.selectbox('Select Second Country:', list(COUNTRY_CODES.keys()),
                                                       format_func=lambda code: COUNTRY_CODES.get(code, code))
        year_range = st.sidebar.slider('Select Year Range:', 1990, 2023, (2020, 2023))

        country_data_1, _ = fetch_data(selected_indicator, list(range(year_range[0], year_range[1] + 1)), [selected_country_code_1])
        country_data_2, _ = fetch_data(selected_indicator, list(range(year_range[0], year_range[1] + 1)), [selected_country_code_2])

        st.subheader(f'{metric} Comparison between {COUNTRY_CODES[selected_country_code_1]} and {COUNTRY_CODES[selected_country_code_2]}')
        plot_country_vs_country(selected_country_code_1, selected_country_code_2, country_data_1, country_data_2, metric, chart_type)

    elif analysis_type == 'Group vs. Group':
        # Group vs. Group comparison
        selected_group_name_1 = st.sidebar.selectbox('Select First Group:', list(GROUPS.keys()))
        selected_group_name_2 = st.sidebar.selectbox('Select Second Group:', list(GROUPS.keys()))
        year_range = st.sidebar.slider('Select Year Range:', 1990, 2023, (2020, 2023))

        group_data_1 = fetch_group_data(selected_indicator, list(range(year_range[0], year_range[1] + 1)), GROUPS[selected_group_name_1])
        group_data_2 = fetch_group_data(selected_indicator, list(range(year_range[0], year_range[1] + 1)), GROUPS[selected_group_name_2])

        st.subheader(f'{metric} Comparison between {selected_group_name_1} and {selected_group_name_2}')
        plot_group_vs_group(selected_group_name_1, selected_group_name_2, group_data_1, group_data_2, metric, chart_type)

if __name__ == "__main__":
    main()
