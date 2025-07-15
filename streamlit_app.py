import streamlit as st
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


st.title("Buy vs rent calculator")
st.write(
    "What would be your wealth after 30 years if you 1) bought the house or 2) rented it instead?"
)

def house_wealth(monthly_rent, inlfation_rate, house_price, down_payment, capital_gains_tax, mortgage_rate, mortgage_length):
    list_of_years = list(range(0, mortgage_length + 1))
    wealth = []
    for i 


    


def main():
    st.set_page_config(layout='wide')
    # menu = ["Recommender", "Sentiment", "Cluster Analysis"]
    # choice = st.sidebar.radio("Menu", menu)
    monthly_rent = st.text_input("Monthly rent you would pay for the house you want to buy", value = 1000)
    inlfation_rate = st.text_input("Inflation rate, in percent", value = 2 )
    real_return = st.text_input("Annual return above inflation you would get if you invested in an equity index ETF, in percent", value = 5 )
    house_price = st.text_input("How much is the asking price of the house", value = 400000 )
    down_payment = st.text_input("How much of the house you would pay upfront, in percent", value = 30 )
    capital_gains_tax = st.text_input("Capital gains tax, in percent", value = 25 )
    mortgage_rate = st.text_input("Mortgage rate, in percent", value = 1.5 )
    mortgage_length = st.text_input("Mortgage length, in years", value = 30 )


    st.write(
    "Some assumptions:" \
    "Long-term, house prices grow in tandem with inflation "
    "(I know it sounds unrealistic today, but on average across 30 years, it holds pretty well)"
)



if __name__ == '__main__':
    main()