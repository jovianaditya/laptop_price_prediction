import numpy as np
from PIL import Image
import base64
import pickle
import streamlit as stl

# Import Model
model_predict = pickle.load(open('model_tuned.pkl','rb'))

# Insert Background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    stl.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('background.jpg')  

# Set Title
stl.title('Laptop Price Prediction')

# Insert Image
image = Image.open('laptop.png')
stl.image(image, caption='Check The Price Of Your Dream Laptop')

# Brand Laptop
brand = stl.selectbox('Laptop Brand',['Acer', 'Apple', 'Asus', 'Chuwi', 'Dell', 'Fujitsu','Google', 'Huawei', 'LG','HP', 'Lenovo', 'Microsoft', 'Mediacom', 'MSI','Razer', 'Samsung','Toshiba','Vero','Xiaomi'])

# Model Name
model = stl.selectbox('Laptop Type',['Gaming', 'Netbook', 'Notebook', 'Ultrabook', 'Workstation', '2 in 1 Convertible'])

# RAM
ram = stl.selectbox('RAM',[2.0,4.0,6.0,8.0,12.0,16.0,24.0,32.0,64.0])

# Weight
weight = stl.number_input('Weight (kg)')

# Touchscreen
touchscreen = stl.selectbox('Touchscreen',['Yes','No'])

# IPS
ips = stl.selectbox('IPS',['Yes','No'])

# Screensize
screen_size = stl.number_input('Screen Size (inch)')

# Resolution
resolution = stl.selectbox('Screen Resolution',['1366x768','1440x900','1600x900','1920x1080','1920x1200','2160x1440','2256x1504','2304x1440','2400x1600','2560x1440','2560x1600','2736x1824','2880x1800','3200x1800','3840x2160'])

# CPU
cpu = stl.selectbox('CPU',['Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Other Intel Processor', 'Others'])

# GPU
gpu = stl.selectbox('GPU',['AMD', 'ARM', 'Intel', 'Nvidia'])

# HDD
hdd = stl.selectbox('HDD (GB)',[0,16,32,64,128,256,512,1024,2048])

# SSD
ssd = stl.selectbox('SSD (GB)',[0,16,32,64,128,256,512,1024,2048])

# Flash Storage
fstorage = stl.selectbox('Flash Storage (GB',[0,16,32,64,128,256,512])

# Hybrid
hybrid = stl.selectbox('Hybrid (GB)',[0,512,1024,2048])

# OS
os = stl.selectbox('Operating System',['Android', 'Chrome OS', 'Linux', 'macOS', 'Windows', 'No OS'])

if stl.button('Find Laptop Price'):
    ppi = None
    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0
    
    if ips == 'Yes':
        ips = 1
    else:
        ips = 0
    
    # Make pixel/inch feature
    X_resolution = int(resolution.split('x')[0])
    Y_resolution = int(resolution.split('x')[0])
    pixel_per_inch = ((X_resolution**2) + (Y_resolution**2))**0.5 / screen_size

    # Query command
    query = np.array([brand,model,ram,os,weight,cpu,gpu,touchscreen,ips,hdd,ssd,fstorage,hybrid,pixel_per_inch],dtype='object')

    # Predict Laptop Price
    query = query.reshape(1,14)
    stl.title(f"Predicted Price in Euros : {(int(np.exp(model_predict.predict(query)[0])))}")