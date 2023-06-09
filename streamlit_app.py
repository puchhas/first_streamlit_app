import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('View Our Fruit List - Add your favorites !') 
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega3 & Bulebeery Oat Meal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
#streamlit.text(fruityvice_response.json())
# take json version and normalize it
 
#new section for fruityvice API
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

    #streamlit.write('The user entered ', fruit_choice)

# output as table display
    #streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

  #streamlit.stop

streamlit.header("Fruit Load List Contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
    
    if streamlit.button('Get Fruit Load List'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_rows = get_fruit_load_list()
        my_cnx.close()
        streamlit.dataframe(my_data_rows)

fruit_choice = streamlit.text_input('What fruit would you like to add?','')
streamlit.write('Thanks for adding ', fruit_choice)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('" + new_fruit + "')")
        return "Thanks for adding " + new_fruit
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")
