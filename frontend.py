import streamlit as st
import sqlite3


def create_account( first_name:str, last_name:str, acc_no:int, ifsc:str, branch_name:str, balance:float):
    
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts ( first_name, last_name, acc_no, ifsc, branch_name, balance) VALUES (?, ?, ?, ?, ?, ?)", 
                       ( first_name, last_name, acc_no, ifsc, branch_name, balance))
        conn.commit()
        st.success(" Account created successfully!")
        conn.close()


st.title("MET BANK")

tab1, tab2, tab3, tab4 = st.tabs(["Create Account", "Deposit Money", "Withdraw Money", "Transfer Money"])


with tab1:
    st.header("Create a New Account")
    with st.form("create_account"):
        first_name = st.text_input("Enter first_name")
        last_name = st.text_input("Enter last_name")
        acc_no = st.text_input("Enter Your acc_no")
        ifsc = st.text_input("Enter Your ifsc_no")
        branch_name = st.text_input("Enter branch_name")
        balance = st.number_input("balance")
        if st.form_submit_button("Create"):
            create_account( first_name, last_name,acc_no, ifsc, branch_name, balance)


with tab2:
    st.header("Deposit Money")
    with st.form("deposit_form"):
        account_id = st.text_input("Account ID")
        amount = st.number_input("Amount to Deposit")
        submit = st.form_submit_button("Deposit")
        if submit:
            st.success(f"${amount:.2f} deposited into account {account_id}")

with tab3:
    st.header("Withdraw Money")
    with st.form("withdraw_form"):
        account_id = st.text_input("Account ID")
        amount = st.number_input("Amount to Withdraw")
        submit = st.form_submit_button("Withdraw")
        if submit:
            st.success(f"${amount:.2f} withdrawn from account {account_id}")


with tab4:
    st.header("Transfer Money")
    with st.form("transfer_form"):
        from_account = st.text_input("From Account ID")
        to_account = st.text_input("To Account ID")
        amount = st.number_input("Amount to Transfer")
        submit = st.form_submit_button("Transfer")
        if submit:
            st.success(f"${amount:.2f} transferred from {from_account} to {to_account}")