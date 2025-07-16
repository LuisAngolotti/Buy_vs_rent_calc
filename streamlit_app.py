import streamlit as st
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px


st.title("Buy vs rent calculator")
st.write(
    "What would your wealth be after 30 years if you bought a house or rented it instead?"
)

def rent_payment_fn(house_price, inflation_rate, spread = 0.025, housing_costs = 0.015):
    return house_price * (inflation_rate/100 + spread - housing_costs)/12

def schedule(house_price, down_payment, interest_rate, inflation_rate, ERP, years, rent_payment):
    """
    Calculate payment schedule and investment schedule
    """
    # Convert interest rate to decimal and calculate monthly rate
    
    monthly_rate = (interest_rate /100 ) / 12
    
    # Total number of payments
    n_payments = years * 12
    
    # Calculate monthly payment and yearly rent
    principal = house_price * (1 - down_payment / 100)
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    # rent_payment = monthly_payment * 12
    
    # Initialize variables for tracking
    yearly_schedule = []
    remaining_balance = house_price * (1-down_payment/100)
    investment_account = house_price * down_payment/100
    house_value = house_price
    annual_rent_payment = rent_payment * 12
    housing_expenses = 0
    cum_housing_expenses = 0
    cum_rent_payment = 0
    cum_mortgage_payment = 0
    # Calculate payments for each year
    for year in range(1, years + 1):
        yearly_interest = 0
        yearly_principal = 0
        annual_rent_payment = annual_rent_payment * (1+inflation_rate/100)
        investment_account = investment_account * (1+inflation_rate/100+ERP/100)      
        house_value = house_value * (1+inflation_rate/100)
        housing_expenses = house_value * 0.015 # Assuming 1.5% of house value as annual housing expenses (maintenance, property tax, etc.)
        # Calculate monthly payments for the current year
        for _ in range(12):
            # Calculate interest for this month
            interest_payment = remaining_balance * monthly_rate
            
            # Calculate principal for this month
            principal_payment = monthly_payment - interest_payment
            
            # Update remaining balance
            remaining_balance -= principal_payment
            
            # Add to yearly totals
            yearly_interest += interest_payment
            yearly_principal += principal_payment
 
        cum_housing_expenses += housing_expenses
        cum_rent_payment += annual_rent_payment
        cum_mortgage_payment += yearly_interest + yearly_principal
        # Add year's data to schedule
        yearly_schedule.append({
            'Year': year,
            'Interest Paid': yearly_interest,
            'Principal Paid': yearly_principal,
            'Remaining Balance': remaining_balance,
            'House Value': house_value,
            'Cummulative Mortgage Payment': cum_mortgage_payment,
            'Cummulative Housing Expenses': cum_housing_expenses,
            'Cummulative Rent': cum_rent_payment,
            'Investment Account': investment_account
        })
    
    # Create DataFrame from schedule
    schedule_df = pd.DataFrame(yearly_schedule)
    
    # Round values for better readability
    schedule_df = schedule_df.round(2)
    schedule_df['Mortgage Paid'] = schedule_df['Interest Paid'] + schedule_df['Principal Paid']
    schedule_df['Wealth if Buying'] = schedule_df['House Value'] - schedule_df['Remaining Balance'] - schedule_df['Cummulative Mortgage Payment'] - schedule_df['Cummulative Housing Expenses']
    schedule_df['Wealth if Renting'] = schedule_df['Investment Account'] - schedule_df['Cummulative Rent']
    return schedule_df

def main():
    st.set_page_config(layout='wide')
    # menu = ["Recommender", "Sentiment", "Cluster Analysis"]
    # choice = st.sidebar.radio("Menu", menu)
    # monthly_rent = st.number_input("Monthly rent you would pay for the house you want to buy", value = 1000)
    house_price = st.number_input("How much is the price of the house, including taxes", value = 400000 )
    down_payment = st.number_input("Down payment: How much of the house price (incl. taxes) you would pay upfront, in percent", value = 30 )
    inflation_rate = st.number_input("Inflation rate, in percent", value = 2.0 )
    real_return = st.number_input("Annual return above inflation you would get if you invested the down payment in an equity index ETF, in percent", value = 5.0 )
    # capital_gains_tax = st.number_input("Capital gains tax, in percent", value = 25 )
    mortgage_rate = st.number_input("Mortgage rate, in percent", value = 1.5 )
    mortgage_length = st.number_input("Mortgage length, in years", value = 30 )
    rent_pmnt = st.number_input("Typical monthly rent for a house of that price", value = rent_payment_fn(house_price, inflation_rate, spread = 0.025, housing_costs = 0.015))
    df = schedule(house_price, down_payment, mortgage_rate, inflation_rate, real_return, mortgage_length, rent_pmnt)
    # df = schedule(house_price, down_payment, interest_rate, inflation_rate, ERP, years)
    chart_data = df[['Year', 'Wealth if Buying', 'Wealth if Renting']].set_index('Year')
    st.line_chart(chart_data)
    st.dataframe(df)

if __name__ == '__main__':
    main()
