from bs4 import BeautifulSoup
import requests
import streamlit as st

target_url = 'https://www.technolife.com/product/list/69_800_801/%D8%AA%D9%85%D8%A7%D9%85%DB%8C-%DA%AF%D9%88%D8%B4%DB%8C%E2%80%8C%D9%87%D8%A7'
response = requests.get(target_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')


if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

st.title('MOBILE STORE', text_alignment='center')

if st.session_state['page'] == 'main':
    col1, col2, col3 = st.columns(3)
    if col1.button("BROWSE PHONES", width=200):
        st.session_state['page'] = 'phone'
        st.rerun()

if st.session_state['page'] == 'phone':
    st.title('PHONES LIST', text_alignment='center')
    
    if st.sidebar.button('Back to Home'):
        st.session_state['page'] = 'main'
        st.rerun()
        
    base_url = 'https://www.technolife.com/'
    
    descriptions = soup.select('section.relative.w-full h2')
    prices = soup.select('section.relative.w-full div.flex.justify-between p.text-primary-shade-1')
    raw_prices = soup.select('section.relative.w-full div.flex.justify-end ')
    images = soup.select('div.relative.mx-auto a img')

    for item in raw_prices:
        try:
            float(item.get_text())
        except ValueError:
            if item.get_text() != '':
                prices.insert(raw_prices.index(item), item)
    
    while len(prices) != 0:
        cols = st.columns(4)
        for i in range(4):
            if len(prices) == 0:
                break
            
            with cols[i]:
                image_url = base_url + images[0].get('src')
                image_response = requests.get(image_url)
                st.image(image_response.content, width='content')

                st.text(descriptions[0].get_text())
                st.text(prices[0].get_text())
                
                descriptions.remove(descriptions[0])
                prices.remove(prices[0])
                images.remove(images[0])
