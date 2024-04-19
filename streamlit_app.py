import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

st.title(":cup_with_straw: Customize Your Smoothie!  :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

name = st.text_input('Name on the Smoothie', '')
st.write('The name on your Smoothie will be: ', name)

options = st.multiselect(
    'What are your fruit choices ?',
    my_dataframe,max_selections=6)
if options:
    # st.text(options)
    ingredients_string = ''

    for i in options:
        ingredients_string += i + ' '


    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order,ingredients)
                values ('"""+name+ """','""" + ingredients_string + """')"""
    
    st.write(my_insert_stmt)
    # st.stop()
    
    submitbutton = st.button("Submit Order")
    
    if submitbutton:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+name+' !', icon="✅")
