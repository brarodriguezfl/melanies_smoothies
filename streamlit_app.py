import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

# Input de nombre
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

# Conexión Snowflake
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

# Convertir a lista para el multiselect
fruit_names = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

# Selección de ingredientes
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , fruit_names
    , max_selections=5
    )

if ingredients_list and name_on_order:
    ingredients_string = ', '.join(ingredients_list)

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+ ' '
        st.subheader(fruit_chosen+ 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
        sf_df= st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Botón para insertar
    if st.button('Submit Order'):
        # Uso de parámetros para evitar inyección
        session.sql(
            "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (?, ?)",
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success('Your Smoothie is ordered!', icon="✅")

