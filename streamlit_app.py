import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

# Input de nombre
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

# Conexión Snowflake
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

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

    # Botón para insertar
    if st.button('Submit Order'):
        # Uso de parámetros para evitar inyección
        session.sql(
            "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (?, ?)",
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
