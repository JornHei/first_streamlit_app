import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healty Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = streamlit.multiselect("Pick some furits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


def get_frutyvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  return pandas.json_normalize(fruityvice_response.json())

#New Section to display fruityvice api
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('what fruit would you like information about?', 'Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_normalized = get_frutyvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

def get_fruit_load_list():
  with my_cxn.cursor() as my_cur:
    my_cur = my_cnx.cursor()
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

def insert_in_fruit_load_list(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute('insert into fruit_load_list values ("{new_fruit"})')
    return "Thanks for adding '{new_fruit}'"

if streamlit.button('Get Fruit Load List):                    
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
                    
fruit_to_add = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  thank_you_note = insert_row_snowflake(fruit_to_add)
  streamlit.write('Thanks for adding', fruit_to_add)
