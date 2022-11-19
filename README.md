# WhatsApp-Chat-Analyzer

A web app designed in python with the help of streamlit to analyze and visualyse WhatsApp chats.

## Features:
  - Total shared content
  - Different timelines
  - Chattiest users
  - Emojis Used
  - Wordcloud
  - Heatmap
  
## Future Features:
  - Adding more plots and visualizations
  
## Requirements:
  - emoji - `pip install emoji`
  - pandas - `pip install pandas`
  - seaborn - `pip install seaborn`
  - streamlit - `pip install streamlit`
  - wordcloud - `pip install wordcloud`
  - matplotlib - `pip install matplotlib`
  - urlextract - `pip install urlextract`
  
**_Note:_** All of these packages can be installed by `pip install emoji pandas seaborn streamlit wordcloud matplotlib urlextract`

## How to run?
  - Go to https://hs-wca.herokuapp.com/
  - Upload the text file of your WhatsApp chat in the sidebar on the left and click Analyze button.
  
### How to get the text file of WhatsApp chats?
  - Open WhatsApp in mobile device and go to the WhatsApp chat you want to analyze
  - Click three dots on the top right
  - Click **More**
  - Click **Export chat**
  - Click **Without media**
  - It will take a few moments to extract the chat, then it will ask to share the chat. You need to share this chat to anyone to get access to it.
  - Download this `.txt` file and upload it in the website [here](https://hs-wca.herokuapp.com/)
