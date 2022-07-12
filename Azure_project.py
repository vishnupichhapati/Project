#Code written for website in streamlit
#All the code written using Azure API 
# and published in github
#using streamlit we created a webpage


import streamlit as st
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
import json

st.set_page_config(layout="wide")
st.sidebar.image('images/Azure_Image.png', width=300)
st.sidebar.header('A website using Azure Api')
st.sidebar.markdown('Face Api,Translator Api')


app_mode = st.sidebar.radio(
    "",
    ("About Me","Face Recognization","Object Detection","Translator"),
)


st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.sidebar.markdown('---')
st.sidebar.write('N.V.Suresh Krishna | sureshkrishnanv24@gmail.com https://github.com/sureshkrishna123')

if app_mode =='About Me':
    st.image('images/wp4498220.jpg', use_column_width=True)
    st.markdown('''
              # About Me \n 
                Hey this is ** N.V.Suresh Krishna **. \n
                
                
                Also check me out on Social Media
                - [git-Hub](https://github.com/sureshkrishna123)
                - [LinkedIn](https://www.linkedin.com/in/suresh-krishna-nv/)
                - [Instagram](https://www.instagram.com/worldofsuresh._/)
                - [Portfolio](https://sureshkrishna123.github.io/sureshportfolio/)\n
                If you are interested in building more about Microsoft Azure then   [click here](https://azure.microsoft.com/en-in/)\n
                ''')
               

if app_mode=='Face Recognization':
  st.image(os.path.join('./images','facial-recognition-software-image.jpg'),use_column_width=True )
  st.title("Face Recognition(Powered by Azure)")
  st.header('Face Recognition:')
  st.markdown("Using Azure I build to detect, identify and analyse faces in images.")
  st.text("Detect the objects in images")
  
  image_file =  st.file_uploader("Upload Images (less than 1mb)", type=["png","jpg","jpeg"])
  if image_file is not None:
    img = Image.open(image_file)
    st.image(image_file,width=250,caption='Uploaded image')
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')#PNG
    image = byte_io.getvalue()


  button_translate=st.button('Click me',help='To give the image')

  if button_translate and image_file :

    def draw_face(img):

        subscription_key = 'ea8c44f876804e43ab35a26a09d59da5'  
        BASE_URL = "https://recognition-ai.cognitiveservices.azure.com/" + '/face/v1.0/detect'  
        headers = {
        # Request headers
        'Content-Type': 'application/octet-stream', 
        'recognitionModel': 'recognition_01' ,
        'Ocp-Apim-Subscription-Key': subscription_key,
        'detectionModel': 'detection_01',
        }
        response = requests.post(BASE_URL, headers=headers, data=image)
        faces = response.json()
        print(faces)
        def getRectangle(faceDictionary):
            rect = faceDictionary['faceRectangle']
            left = rect['left']
            top = rect['top']
            bottom = left + rect['height']
            right = top + rect['width']
            return ((left, top), (bottom, right))


        output_image = Image.open(BytesIO(image))
        
    #   For each face returned use the face rectangle and draw a red box.
        draw = ImageDraw.Draw(output_image)
        for face in faces:
            draw.rectangle(getRectangle(face), outline='red',width=2)
        return output_image
   #image_data = open(image_file, "rb").read()

    image = draw_face(img)

    st.image(image, caption='Output image')
    
    
    
if app_mode =='Object Detection':
    
    st.image(os.path.join('./images','object.jpg'),use_column_width=True )
    st.markdown("<h1 style='text-align: center; color: skyblue; '> Object Recognition </h1>", unsafe_allow_html=True)

    st.title("Object Recognition(Powered by Azure)")

    st.markdown("Using Azure I build to **_Object_ detection** , it identify and analyse the image.")
    st.text("Detect the objects in images")

    url_file =  title = st.text_input('Paste image address URL')
    st.text("Example :- https://www.intelligentliving.co/wp-content/uploads/2019/12/sculptures-reclaimed-materials-brianmock8_201911323127.jpg")
    button_translate=st.button('Click me',help='To give the image')

    if button_translate and url_file :
   
        subscription_key = 'afac470736ce49ca8352ec7c83736fc7'
        endpoint = 'https://objectdetection21.cognitiveservices.azure.com/'
        
            # Add your Computer Vision subscription key and endpoint to your environment variables.
        analyze_url = endpoint + "vision/v3.1/analyze"
        
        # Set image_url to the URL of an image that you want to analyze.
        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        params = {'visualFeatures': 'Categories,Description,Color'}
        data = {'url': url_file}
        response = requests.post(analyze_url, headers=headers,params=params, json=data)
        response.raise_for_status()

        # The 'analysis' object contains various fields that describe the image. The most
        # relevant caption for the image is obtained from the 'description' property.
        analysis = response.json()
        print(json.dumps(response.json()))
        image_caption = analysis["description"]["captions"][0]["text"].capitalize()
        response_image = requests.get(url_file)
        
        # Display the image and overlay it with the caption.
        aux_im = Image.open(BytesIO(response_image.content))
        captio=st.subheader(image_caption)
        st.image(aux_im, caption=image_caption)

 
if app_mode =='Translator':
   
    st.image(os.path.join('./images','unnamed.png'),use_column_width=True )
    st.markdown("<h1 style='text-align: center; color: skyblue; '> language Translator: </h1>", unsafe_allow_html=True)

    
    
    st.markdown("For more documentation on language support in Azure:[click here](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/language-support)")
    st.markdown('---')

    detect=st.text_input('Enter the text to detect (No language Restriction):')

    detect_select=st.selectbox("select language to translate" ,['arabic','bangla','chinese','dutch','english','french','german','greek','hindi','hungarian','indonesian','irish','italian','japanese','kannada','korean','malayalam','nepali','portuguese','punjabi','russian','spanish','tamil','telugu','turkish','urdu'],key=1)

    if detect_select == 'arabic':
        detect_lang= 'ar'
    elif detect_select == 'bangla':
        detect_lang= 'bn'
    elif detect_select == 'chinese':
        detect_lang= 'lzh'
    elif detect_select == 'dutch':
        detect_lang= 'nl'
    elif detect_select == 'english':
        detect_lang= 'en'
    elif detect_select == 'french':
        detect_lang= 'fr'
    elif detect_select == 'german':
        detect_lang= 'de'
    elif detect_select == 'greek':
        detect_lang= 'el'
    elif detect_select == 'hindi':
        detect_lang= 'hi'
    elif detect_select == 'hungarian':
        detect_lang= 'hu'
    elif detect_select == 'indonesian':
        detect_lang= 'id'
    elif detect_select == 'irish':
        detect_lang= 'ga'
    elif detect_select == 'italian':
        detect_lang= 'it'
    elif detect_select == 'japanese':
        detect_lang= 'ja'
    elif detect_select == 'kannada':
        detect_lang= 'kn'
    elif detect_select == 'korean':
        detect_lang= 'ko'
    elif detect_select == 'malayalam':
        detect_lang= 'ml'
    elif detect_select == 'nepali':
        detect_lang= 'ne'
    elif detect_select == 'portuguesei':
        detect_lang= 'pt'
    elif detect_select == 'punjabi':
        detect_lang= 'pa'
    elif detect_select == 'russian':
        detect_lang= 'ru'
    elif detect_select == 'spanish':
        detect_lang= 'es'
    elif detect_select == 'tamil':
        detect_lang= 'ta'
    elif detect_select == 'telugu':
        detect_lang= 'te'  
    elif detect_select == 'turkish':
        detect_lang= 'tr'
    elif detect_select == 'urdu':
        detect_lang= 'ur'          


    button_detect=st.button('Click me',help='To detect language')

    if button_detect and detect:
        import requests, uuid, json

        # Add your subscription key and endpoint
        subscription_key ="6f7488eb5fe442a8adc4cdcd4cd50474"
        endpoint = "https://api.cognitive.microsofttranslator.com/"

        # Add your location, also known as region. The default is global.
        # This is required if using a Cognitive Services resource.
        location = "eastus"

        path = '/translate'
        constructed_url = endpoint + path

        params = {
            'api-version': '3.0',
            'to': [detect_lang]
        }
        constructed_url = endpoint + path

        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text': detect
        }]

        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response123 = request.json()
        dump=json.dumps(response123, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
        response=json.loads(dump)
        conv_str=str(response)
        st.success(conv_str[55:])
        st.spinner(text="Done")

    elif button_detect:
        st.error("!! Please enter input in any language")

    st.markdown('---')
    
