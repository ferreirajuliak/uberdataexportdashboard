import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
import map
import time
import regex as re

def uber_x(data):
    UberX = data[(data['Product Type'] == 'UberX') & (data['Trip or Order Status'] == 'COMPLETED')]

    UberX.rename(columns={'Request Time': 'Date Time'}, inplace=True)
    UberX.rename(columns={'Fare Currency': 'Currency'}, inplace=True)
    UberX['Distance (miles)'] = UberX['Distance (miles)'].map('{:,.2f}'.format)
    UberX['Fare Amount'] = UberX['Fare Amount'].astype(float)
    UberX['Fare Amount'] = UberX['Fare Amount'].map('{:,.2f}'.format)
    UberX['Date Time'] = pd.to_datetime(UberX['Date Time'].apply(lambda x: re.sub(' \w+$', '', x)))

    for index in UberX.index:
        UberX.loc[index,'Begin Trip Address'] = 'Begin Trip Address'
        UberX.loc[index, 'Dropoff Address'] = 'Dropoff Address'

    UberX = pd.DataFrame(UberX, columns=['Begin Trip Address', 'Dropoff Address', 'Distance (miles)',
                                         'Fare Amount', 'Currency', 'Date Time',
                                         'Begin Trip Lng', 'Begin Trip Lat', 'Dropoff Lng', 'Dropoff Lat'])

    st.set_page_config(layout="wide")

    c1, c2 = st.columns(2)
    with c1:
        gb = GridOptionsBuilder.from_dataframe(UberX)
        gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
        gb.configure_side_bar()  # Add a sidebar
        gb.configure_selection('single', use_checkbox=True,
                               groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection

        gridOptions = gb.build()

        grid_response = AgGrid(
            UberX,
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT',
            update_mode='MODEL_CHANGED',
            fit_columns_on_grid_load=False,
            theme='blue',  # Add theme color to the table
            enable_enterprise_modules=True,
            height=500,
            width='100%',
            reload_data=True
        )

        selected = grid_response['selected_rows']
        df = pd.DataFrame(selected)  # Pass the selected rows to a new dataframe df
    with c2:
        if df.empty:
            time.sleep(0.5)
            st.write('Select a trip to show route:')
        else:
            map.route_map(df)
            print(df)
    return None