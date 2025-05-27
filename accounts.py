from fastapi import FastAPI
import json
import sqlite3

def connect_db():
    conn=sqlite3.connect("bank.db")
    return conn
 
app = FastAPI()

account={}
 
def load_users():
    with open("db.json", 'r') as f:
        data = json.load(f)
        return data 
def save_user(users):
    with open("db.json", 'w') as f:
        json.dump(users, f, indent=4)


@app.post("/users/create/")
def create_account( first_name:str, last_name:str, acc_no:int, ifsc:str, branch_name:str, balance:float):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute ('''INSERT INTO accounts (first_name, last_name, acc_no, ifsc, branch_name, balance) VALUES (?, ?, ?, ?, ?, ?) ''', 
                    (first_name, last_name, acc_no, ifsc, branch_name, balance))

    conn.commit()
    conn.close()
 
    return {"output" : "Account created successfully"}

    

@app.post("/users/credit")
def credit_money(acc_no:int,credit_amount:float):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE acc_no = ?",(acc_no,))
    data = cursor.fetchone()
    if  data:
        new_balance = data[0] + credit_amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE acc_no = ?", (new_balance, acc_no))
        conn.commit()
        return {"message": "Money credited", "new_balance": new_balance}
    else :
        return {"error" : "Account not found" }
        

@app.post("/users/debit")
def debit_money(acc_no:int,debit_amount:float):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE acc_no = ?", (acc_no,))
    data = cursor.fetchone()
    if not data:
        return{"error" : "Account not found" }
    new_balance = data[0] - debit_amount
    cursor.execute("UPDATE accounts SET balance = ? WHERE acc_no = ?", (new_balance, acc_no))
    conn.commit()
    return {"message": "Money debited", "new_balance": new_balance}


@app.post("/users/transfer")
def transfer_money (from_accno:int,to_accno:int,transfer_amount:float):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE acc_no = ?", (from_accno,))
    from_data = cursor.fetchone()
    if not from_data:
        return {"error":"Sender account not found"}
    
    cursor.execute("SELECT balance FROM accounts WHERE acc_no = ?", (to_accno,))
    to_data = cursor.fetchone()
    if not to_data:
        return {"error":"Receiver account not found"}
    if from_data[0]<transfer_amount:
        return {"error":"Insufficient balance"}
    
    cursor.execute("UPDATE accounts SET balance = ? WHERE acc_no = ?", (from_data[0] - transfer_amount, from_accno))
    cursor.execute("UPDATE accounts SET balance = ? WHERE acc_no = ?", (to_data[0] + transfer_amount,to_accno))
    conn.commit()
    return {"message": "Transfer successful"}


@app.get("/users/detail")
def get_account_details(acc_no:int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE acc_no = ? ", (acc_no,))
    data = cursor.fetchone()
    
    if data:
        accounts = {
            "id": data[0],
            "acc_no": data[1],
            "ifsc": data[2],
            "branch_name": data[3],
            "first_name": data[4],
            "last_name": data[5],
            "balance": data[6]
        }
        return {"accounts": accounts}
    else:
        return {"error":"Account not found"}