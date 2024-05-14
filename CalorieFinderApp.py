import streamlit as st
import os
from dotenv import load_dotenv
#loading the dot env varibale
load_dotenv() 
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def getgeminiresponse(inputprompt,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([inputprompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    


    ##initialize our streamlit app (Frontend setup)

st.set_page_config(page_title="Your Personalized Nutritional Guide")

st.header("Calorie Finder App")
# input=st.text_input("Input Prompt: ",key="input")
st.subheader("Generalised calculation of calories found in a meal. Find it out for yours..... ")
st. subheader("Upload your meal's image")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Is it healthy or not. Check it out ")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----

Also give a description of each item item in the meal.
Finally also you can mention whether the food is healthy or not annd also mention the percentage spilt of of the ratio of carbohydrates, proteins, fats, fibers, sugar and other imprtant things required in our diet.
Give alternatives of the meal if the meal is unhealthy.
"""

# If submit button is clicked  (Backend setup)

if submit:
    image_data=input_image_setup(uploaded_file)
    response=getgeminiresponse(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)
