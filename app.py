import pandas as pd
import streamlit as st
from glob import glob
from PIL import Image
import requests

# Define a function to filter attractions by city
def filter_attractions(city):
    return [attraction for attraction in attractions if attraction["city"] == city]

# Define the Streamlit app
def main(df, cities):
    st.title("Attraction Sites")
    
    # Add a dropdown menu to select the sorting key
    sort_keys = ["final_rank","name","ratings","reviews", "cs_multiply","cs_weighted_sum",
                 "cs_rank","cs_gm", "cs_add_scaled","cs_borda_count", "cs_pca"]
    
    # Options to select from
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox("Select a city", cities)

    with col2:
        sort_by = st.selectbox("Sort by", sort_keys)


    # Filter the attractions by the selected city and display them as tiles
    city_attractions = filter_attractions(city)



    # Sort the attractions list based on the selected key
    if sort_by == "name":
        city_attractions = sorted(city_attractions, key=lambda x: x["name"])
    elif sort_by == "final_rank":
        city_attractions = sorted(city_attractions, key=lambda x: x["final_rank"])
    elif sort_by == "ratings":
        city_attractions = sorted(city_attractions, key=lambda x: x["ratings"], reverse=True)
    elif sort_by == "reviews":
        city_attractions = sorted(city_attractions, key=lambda x: x["reviews"], reverse=True)
    elif sort_by == "cs_multiply":
        city_attractions = sorted(city_attractions, key=lambda x: x["cs_multiply"], reverse=True)
    elif sort_by == "cs_weighted_sum":
        city_attractions = sorted(city_attractions, key=lambda x: x["cs_weighted_sum"], reverse=True)
    elif sort_by == "cs_rank":
        city_attractions = sorted(city_attractions, key=lambda x: x["cs_rank"])
    elif sort_by == "cs_gm":
        city_attractions = sorted(city_attractions, key=lambda x: x["cs_gm"], reverse=True)
    elif sort_by == "cs_add_scaled":
        city_attractions = sorted(city_attractions, key=lambda x: x["cs_add_scaled"], reverse=True)
    elif sort_by == "cs_borda_count":
        city_attractions = sorted(city_attractions, key=lambda x: x["cs_borda_count"], reverse=True)
    elif sort_by == "cs_pca":
        city_attractions = sorted(city_attractions, key=lambda x: x["cs_pca"], reverse=True)



    for i in range(0, len(city_attractions), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            if i < len(city_attractions):
                img = Image.open(requests.get(city_attractions[i]["image"], stream=True).raw)
                st.image(img.resize((800, 800)), use_column_width=True, caption=city_attractions[i]["name"])
                st.write("Rank: ", city_attractions[i]['final_rank'])
                st.write("Rating: ", city_attractions[i]['ratings'])
                st.write("Reviews: ", city_attractions[i]['reviews'])
                try:
                    st.write("Category: ", city_attractions[i]['category'].repalce("-", " "))
                except:
                    st.write("Category: ", "-")
                st.write(city_attractions[i]['notes'])
        with col2:
            if i+1 < len(city_attractions):
                img = Image.open(requests.get(city_attractions[i+1]["image"], stream=True).raw)
                st.image(img.resize((800, 800)), use_column_width=True, caption=city_attractions[i+1]["name"])
                st.write("Rank: ", city_attractions[i+1]['final_rank'])
                st.write("Rating: ", city_attractions[i+1]['ratings'])
                st.write("Reviews: ", city_attractions[i+1]['reviews'])
                try:
                    st.write("Category: ", city_attractions[i+1]['category'].repalce("-", " "))
                except:
                    st.write("Category: ", "-")
                st.write(city_attractions[i+1]['notes'])        
        with col3:
            if i+2 < len(city_attractions):
                img = Image.open(requests.get(city_attractions[i+2]["image"], stream=True).raw)
                st.image(img.resize((800, 800)), use_column_width=True, caption=city_attractions[i+2]["name"])
                st.write("Rank: ", city_attractions[i+2]['final_rank'])
                st.write("Rating: ", city_attractions[i+2]['ratings'])
                st.write("Reviews: ", city_attractions[i+2]['reviews'])
                try:
                    st.write("Category: ", city_attractions[i+2]['category'].repalce("-", " "))
                except:
                    st.write("Category: ", "-")
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
    main(df, cities)
