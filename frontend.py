import streamlit as st
from bs4 import BeautifulSoup as bs
import urllib.request
import matplotlib.pyplot as plt
import re
from sum2 import AmazonReviewExtractor
from description import AmazonDescription
from fake_useragent import UserAgent
from specs import specifications
import pandas as pd
ua=UserAgent()

st.set_page_config(page_title="Price Tracker", layout="wide")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
with st.container():
    temp_left,temp_center,temp_right=st.columns((2,1.5,2))
    with temp_center:
        def display_centered_title(text, level=1, font_size=38):
            style = f"text-align: center; font-size: {font_size}px; background-color: #FF4B4B; border-radius: 5px;"
            st.markdown(f"<h{level} style='{style}'>{text}</h{level}>", unsafe_allow_html=True)

        display_centered_title("Amazon Guider", level=2, font_size=48)
st.write("")
st.write("")
sub="Hello, Our project allows you a best purchase guide for amazon.in products!!!"
style=f"text-align: center;font-size: 18px;"
st.markdown(f"<h1 style='{style}'>{sub}<h1>", unsafe_allow_html=True)

def display_centered_des(text, level=1, font_size=38):
    style = f"text-align: center; font-size: {font_size}px;"
    st.markdown(f"<h{level} style='{style}'>{text}</h{level}>", unsafe_allow_html=True)

display_centered_des("Please enter or paste amazon.in url in below box to get started", level=2, font_size=24)


amazon_url = st.text_input("Enter or paste the URL:")
st.markdown(
    """
    <style>
    .centered {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
if st.button("SUBMIT"):
    with st.spinner("Loading..."):
        with st.container():
            image_right, price_left = st.columns((1,3))
            with price_left:
                if amazon_url:
                    headers = {"User-Agent": ua.random}
                    request = urllib.request.Request(amazon_url, headers=headers)
                    try:
                        response = urllib.request.urlopen(request)
                        soup1 = bs(response, "html.parser")
                        try:
                            name = soup1.find(id="productTitle").get_text().strip()
                            style = "font-size: 20px font-color: white"
                            prod = "Product Name:"
                            st.markdown(f"<h3 style='{style}'> {prod} </h3> {name}", unsafe_allow_html=True)                            
                        except Exception:
                            st.warning("Name Unavailable")

                        # Product Price
                        try:
                            price = soup1.find(class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay")
                            prices = price.find(class_="a-price-whole").get_text().strip()
                            style = "font-size: 20px font-color: white"
                            prod_pri = "Product Price:"
                            st.markdown(f"<h3 style='{style}'> {prod_pri} </h3> ₹{prices}", unsafe_allow_html=True)
                        except AttributeError:
                            st.warning("Price Unavailable")

                        # Product Rating
                        try:
                            rating = soup1.find(id="acrPopover")
                            rating_prod = rating.find(class_="a-size-base a-color-base").get_text()
                            style = "font-size: 20px font-color: white"
                            prod_rating = "Product Rating:"
                            st.markdown(f"<h3 style='{style}'> {prod_rating} </h3> {rating_prod}/5", unsafe_allow_html=True)
                            ratingint=int(float(rating_prod))
                            if ratingint==1:
                                st.write(":star:"*1,end='')
                            elif ratingint ==2:
                                st.write(":star:"*2,end='')
                            elif ratingint ==3:
                                st.write(":star:"*3,end='')
                            elif ratingint ==4:
                                st.write(":star:"*4,end='')
                            else:
                                st.write(":star:"*5,end='')

                        except AttributeError:
                            st.warning("Rating Unavailable")
                        try:
                            image_container = soup1.find(class_="imgTagWrapper")
                            img = image_container.find('img')['src']
                        except (AttributeError, TypeError):
                            st.warning("Image Unavailable")
                        try:
                            elements = soup1.find_all(class_="a-size-base a-link-normal")
                            rat = ' '.join([element.get_text() for element in elements])
                            rat=rat.replace(" ",'')
                            l_star_rating = []
                            c = 0
                            e = 0
                            r = ['5', '4', '3', '2', '1']
                            for i in rat:
                                if i == "%":
                                    if rat[c - 5] == r[e] or rat[c - 6] == r[e] or rat[c - 7] == r[e] or rat[c - 9] == r[e] or rat[c - 8] == r[e]:
                                        if rat[c - 3] == "r":
                                            l_star_rating.append(int(rat[c - 2:c]))
                                            e = e + 1
                                            c = c + 1
                                        elif rat[c - 2] == 'r':
                                            l_star_rating.append(int(rat[c - 1:c]))
                                            c = c + 1
                                            e = e + 1
                                        else:
                                            l_star_rating.append(int(rat[c - 3:c]))
                                            c = c + 1
                                            e = e + 1
                                    else:
                                        l_star_rating.append(0)
                                        if rat[c - 3] == "r":
                                            l_star_rating.append(int(rat[c - 2:c]))
                                            e = e + 1
                                            c = c + 1
                                        else:
                                            l_star_rating.append(int(rat[c - 1:c]))
                                            c = c + 1
                                            e = e + 1
                                else:
                                    c = c + 1

                            while len(l_star_rating) != 5:
                                l_star_rating.append(0)

                        except AttributeError:
                            st.warning("Star_Rating Unavailable")
                        try:
                            elements1 = soup1.find_all(class_="a-size-base a-color-secondary")
                            rat1 = ' '.join([element.get_text() for element in elements1])
                            l2= re.findall(r'\b\d+\b', rat1)
                            l_total_review=int(l2[-1])
                        except AttributeError:
                            st.warning("Star_Rating Unavailable")
                        try:
                            amazonrev=AmazonReviewExtractor()
                            rev_sum=amazonrev.get_reviews_summary(soup1)
                        except Exception as e:
                            st.error(f"Error: {e}")
                    except Exception as e:
                        st.error(f"Error: {e}")
                    

            with image_right:        
                st.image(img)
        with st.container():
            amazon_des=AmazonDescription()
            description=amazon_des.description_amazon(soup1)
            st.header("Specifications:")
            for paragraph in description:
                if paragraph:
                    try:
                        heading, content = re.split(r'[-:=]', paragraph, maxsplit=1)
                        st.write(f"**{heading.strip()}** - {content.strip()}")
                    except ValueError:
                        st.write(paragraph)
        with st.container():
            rev_left,rev_right=st.columns((2,3))
            with rev_right:
                fig, ax = plt.subplots(figsize=(5, 5))
                label_props = {'fontsize': 5, 'color': 'white', 'family': 'serif', 'weight': 'bold'}
                ax.pie(l_star_rating, labels=["5 stars", "4 stars", "3 stars", "2 stars", "1 star"],
                    colors=['#1f78b4', '#ff7f0e', '#33a02c', '#e31a1c', '#6a3d9a'], startangle=90,
                    shadow=True,
                    explode=(0.1, 0, 0, 0, 0), autopct="%1.2f%%", textprops=label_props, pctdistance=0.85)
                ax.legend(loc='upper right', fontsize=5)
                fig.set_facecolor("#0E1117")
                ax.set_facecolor("#0E1117")

                st.write(fig)

                style_round="font-family: cursive; border-radius: 10px;padding: 10px;border: 1px solid #ccc;"
                star_5=int((l_star_rating[0]/100)*l_total_review)
                star_4=int((l_star_rating[1]/100)*l_total_review)
                star_3=int((l_star_rating[2]/100)*l_total_review)
                star_2=int((l_star_rating[3]/100)*l_total_review)
                star_1=int((l_star_rating[4]/100)*l_total_review)
                list_stars=[star_1,star_2,star_3,star_4,star_5]
                max_rev=max(list_stars)
                min_rev=min(list_stars)
                if star_5== max(list_stars):
                    color_5="green"
                elif star_5== min(list_stars):
                    color_5="red"
                else:
                    color_5="yellow"
                if star_4== max(list_stars):
                    color_4="green"
                elif star_4== min(list_stars):
                    color_4="red"
                else:
                    color_4="yellow"
                if star_3== max(list_stars):
                    color_3="green"
                elif star_3== min(list_stars):
                    color_3="red"
                else:
                    color_3="yellow"
                if star_2== max(list_stars):
                    color_2="green"
                elif star_2== min(list_stars):
                    color_2="red"
                else:
                    color_2="yellow"
                if star_1== max(list_stars):
                    color_1="green"
                elif star_1== min(list_stars):
                    color_1="red"
                else:
                    color_1="yellow"
                rev_left1,rev_right1=st.columns((1,1))
                with rev_left1:
                    st.markdown(
                        f"""
                        <div style='{style_round}'>
                            <ul style="list-style-type: disc; color: white;">
                                <li>Number of 5-Stars Reviews: <span style="color:{color_5};">{star_5}</span></li>
                                <li>Number of 4-Stars Reviews: <span style="color:{color_4};">{star_4}</span></li>
                                <li>Number of 3-Stars Reviews: <span style="color:{color_3};">{star_3}</span></li>
                                <li>Number of 2-Stars Reviews: <span style="color:{color_2};">{star_2}</span></li>
                                <li>Number of 1-Stars Reviews: <span style="color:{color_1};">{star_1}</span></li>
                            </ul>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with rev_right1:
                    overall_rat=(((star_5*5)+(star_4*4)+(star_3*3)+(star_2*2)+(star_1*1))/l_total_review)
                    num_stars=int(overall_rat)
                    st.markdown(
                        f"""
                        <div style='{style_round}'>
                            <h4> Calculated Rating: {'⭐' * num_stars} ({overall_rat:.2f}) </h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            st.markdown("<div style='height:500px; border-left: 2px solid black'></div>", unsafe_allow_html=True)
            with rev_left:
                st.header(" Common Positive Review:")
                st.write("(NOTE: THESE ARE AI GENERATED WITH ESTIMATION)")
                style_round_1="border-radius: 10px;padding: 10px;border: 1px solid #ccc; line-height:1.5"
                st.markdown(
                        f"""
                        <div style='{style_round_1}'>
                            <p> {rev_sum[0]} </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.header("")
                st.header("Common Negative Review:")
                st.write("(NOTE: THESE ARE AI GENERATED WITH ESTIMATION)")
                style_round_1="border-radius: 10px;padding: 10px;border: 1px solid #ccc; line-height:1.5"
                st.markdown(
                        f"""
                        <div style='{style_round_1}'>
                            <p> {rev_sum[1]} </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.header("Key Specifications:")
                specs=specifications.spec(soup1)
                df = pd.DataFrame(specs.items(),columns=["Specs","Value"])
                st.write(df)
                                    




