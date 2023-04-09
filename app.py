import pandas as pd
import streamlit as st
from glob import glob
from PIL import Image
import requests

# Define a function to filter attractions by city
def filter_attractions(city):
    return [attraction for attraction in attractions if attraction["city"] == city]

# Define the Streamlit app
def main():
    st.title("Attraction Sites")
    
    # Create a tab layout with two tabs
    city = st.selectbox("Select a city", cities)

    # Filter the attractions by the selected city and display them as tiles
    city_attractions = filter_attractions(city)
    for i in range(0, len(city_attractions), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            if i < len(city_attractions):
                img = Image.open(requests.get(city_attractions[i]["image"], stream=True).raw)
                st.image(img.resize((800, 800)), use_column_width=True, caption=city_attractions[i]["name"])
                st.write("Rank: ", city_attractions[i]['final_rank'])
                st.write("Rating: ", city_attractions[i]['ratings'])
                st.write("Reviews: ", city_attractions[i]['reviews'])
                st.write(city_attractions[i]['notes'])
        with col2:
            if i+1 < len(city_attractions):
                img = Image.open(requests.get(city_attractions[i+1]["image"], stream=True).raw)
                st.image(img.resize((800, 800)), use_column_width=True, caption=city_attractions[i+1]["name"])
                st.write("Rank: ", city_attractions[i+1]['final_rank'])
                st.write("Rating: ", city_attractions[i+1]['ratings'])
                st.write("Reviews: ", city_attractions[i+1]['reviews'])
                st.write(city_attractions[i+1]['notes'])        
        with col3:
            if i+2 < len(city_attractions):
                img = Image.open(requests.get(city_attractions[i+2]["image"], stream=True).raw)
                st.image(img.resize((800, 800)), use_column_width=True, caption=city_attractions[i+2]["name"])
                st.write("Rank: ", city_attractions[i+2]['final_rank'])
                st.write("Rating: ", city_attractions[i+2]['ratings'])
                st.write("Reviews: ", city_attractions[i+2]['reviews'])
                st.write(city_attractions[i+2]['notes'])                        

# Run the Streamlit app
if __name__ == "__main__":
    df = []
    files = glob('./output/*.csv')

    for file in files:
        df.append(pd.read_csv(file))

    df = pd.concat(df, axis=0)
    df = df.rename(columns={'attractions':'name'})



    attractions = df.to_dict(orient='records')
    cities = df.city.unique()
    print(cities)
    main()
