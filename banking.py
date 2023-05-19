import mysql.connector as mysql
import random
from tabulate import tabulate
import datetime
import re
db=mysql.connect(host="localhost",user="root",password="",database="samplebanking")
command_handler=db.cursor(buffered=True)


def newuser():
    account_no=random.randint(150001,151000)
    name=input(str("NAME :"))
    i="Password Created"
    while i=="Password Created":
        password=input("PASSWORD :")
        if len(password)>=10:
            if re.search("[0-9]", password):
                if re.search("[A-Z]", password):
                    if re.search("[$@#]", password):
                        print(i)
                        break
                    else:
                        print("Password should contain atleast one special character")
                else:
                    print("Password should contain atleast one captial letter")
            else:
                print("Password should contain atleast one number")
        else:
            print("Password should be minimum 10 characters")

    balance=int(input("BALANCE : "))
    pin=int(input("PIN : "))
    

    if balance>=500:
        query_val=(account_no,name,password,balance,pin)
        command_handler.execute("INSERT INTO customers(account_no,name,password,balance,PIN,privilege) VALUES(%s,%s,%s,%s,%s,'customer')",query_val)
        db.commit()
        print(f"Rs.{balance} added Successfully")
    else:
        print("balance should not be less than 500")


def deposit():

    print("")

    account_no=int(input("ACCOUNT NO : "))

    sq="select*from customers where account_no='{}'".format(account_no)
    command_handler.execute(sq)
    sq=command_handler.fetchone()

    list2=list(sq)

    if account_no==list2[0]:
        depositAmount=int(input("DEPOSIT AMOUNT : "))
        balance=depositAmount+int(list2[3])
        print(balance)

        ns1="update customers set balance='{}' where account_no='{}'".format(balance,account_no)
        command_handler.execute(ns1)
        db.commit()

        print(f" Rs.{depositAmount} has been deposited successfully .Available account balance is Rs.{balance}")
        print("----------------------------------------------------------------------------------------------------")
        
        current_time = datetime.datetime.now()
        f=current_time.strftime("%b %d %Y %H:%M")
        g=str(f)
        
        command=f"Rs.{depositAmount} deposited by you"
        query_val=(g,account_no,command,depositAmount)
        command_handler.execute("INSERT INTO transactions(Date,Account_No,Transaction_summery,Credit,Debit) VALUES(%s,%s,%s,%s,'-')",query_val)
        db.commit()
        print("")



def withdraw():
    print("")

    account_no=int(input("ACCOUNT NO : "))
    pin=int(input("Enter your PIN : "))

    sq1="select*from customers where account_no='{}'".format(account_no)
    command_handler.execute(sq1)
    sq1=command_handler.fetchone()

    list3=list(sq1)

    if account_no==list3[0]:
        if pin==list3[4]:
            WithdrawAmount=int(input("Withdrawamount : "))

            if WithdrawAmount<=list3[3]:
                balance=int(list3[3])-WithdrawAmount
                print(balance)

                ns1="update customers set balance='{}' where account_no='{}'".format(balance,account_no)
                command_handler.execute(ns1)
                db.commit()

                print(f" Rs.{WithdrawAmount} has been debited .Available account balance is Rs.{balance}")
                current_time = datetime.datetime.now()
                f=current_time.strftime("%b %d %Y %H:%M")
                g=str(f)
        
                command=f"Rs.{WithdrawAmount} withdrawed by you"
                query_val=(g,account_no,command,WithdrawAmount)
                command_handler.execute("INSERT INTO transactions(Date,Account_No,Transaction_summery,Credit,Debit) VALUES(%s,%s,%s,'-',%s)",query_val)
                db.commit()

                print("----------------------------------------------------------------------------------------------------")
                print("")
            else:
                print("INSUFFICIENT BALANCE ")

def transfer():
    account_no=int(input("ACCOUNT NO : "))

    sq2="select*from customers where account_no='{}'".format(account_no)
    command_handler.execute(sq2)
    sq2=command_handler.fetchone()

    list4=list(sq2)


    if account_no==list4[0]:
            transferAccount=int(input("Tranferable Account no : "))
            Accounthname=input(str(" Account holder name :"))

            sq3="select*from customers where account_no='{}'".format(transferAccount)
            command_handler.execute(sq3)
            sq3=command_handler.fetchone()

            list5=list(sq3)

            if transferAccount and Accounthname in list5:
                transferAmount=int(input("Amount : "))

                if transferAmount<=list4[3]:
                    pin1=int(input("ENTER PIN : "))

                    if pin1==list4[4]:
                        balance=int(list4[3])-transferAmount
                        print(balance)

                        ns2="update customers set balance='{}' where account_no='{}'".format(balance,account_no)
                        command_handler.execute(ns2)
                        db.commit()

                        print(f" Rs.{transferAmount} has been debited .Available account balance is Rs.{balance}")
                        current_time = datetime.datetime.now()
                        f=current_time.strftime("%b %d %Y %H:%M")
                        g=str(f)
        
                        command=f"Rs.{transferAmount} has tranfered to {transferAccount} name:{list5[1]}"
                        query_val=(g,account_no,command,transferAmount)
                        command_handler.execute("INSERT INTO transactions(Date,Account_No,Transaction_summery,Credit,Debit) VALUES(%s,%s,%s,'-',%s)",query_val)
                        db.commit()

                        print("---------------------------------------------------------------------------------------------")
                        print("")

                        credit_balance=transferAmount+int(list5[3])

                        ns3="update customers set balance='{}' where account_no='{}'".format(credit_balance,transferAccount)
                        command_handler.execute(ns3)
                        db.commit()

                        current_time = datetime.datetime.now()
                        f=current_time.strftime("%b %d %Y %H:%M")
                        g=str(f)
        
                        command=f"Rs.{transferAccount} deposited. Transfered by {account_no} name :{list4[1]}"
                        query_val=(g,transferAccount,command,transferAmount)
                        command_handler.execute("INSERT INTO transactions(Date,Account_No,Transaction_summery,Credit,Debit) VALUES(%s,%s,%s,%s,'-')",query_val)
                        db.commit()
                    else:
                        print("INCORRECT PIN ")
                else:
                    print("INSUFFICIENT BALANCE ")
            else:
                print("INVALID ACCOUNT DETAILS")
    
def balance_check():
    account_no=int(input("ACCOUNT NO : "))

    sq4="select*from customers where account_no='{}'".format(account_no)
    command_handler.execute(sq4)
    sq4=command_handler.fetchone()

    list5=list(sq4)

    pin=int(input("ENTER PIN :"))
    if pin==list5[4]:
        print(f"Available Balance Rs.{list5[3]}")
        print("")
        print("--------------------------------------------------")
        print("")
def transactions():
    account_no=int(input("ACCOUNT NO :")) 
    pin=int(input("Enter your pin :"))
    print("")

    sql="select*from customers where account_no='{}'".format(account_no)
    command_handler.execute(sql)
    sql=command_handler.fetchone()

    list6=list(sql)

    if pin==list6[4]:
        sql1="select*from transactions where account_no='{}'".format(account_no)
        command_handler.execute(sql1)
        sql1=command_handler.fetchall()
        print(tabulate(sql1,headers=["Date of tranaction","Account No","Transaction Summary ","Credit ","Debit"]))
    print("")
    print("-------------------------------------------------------------------------------------------------------------")
    print("")
    

    
def login():
    user_name=input(str("USERNAME : "))
    pass_word=input(str("PASSWORD : "))

    sql="select*from customers where name='{}'".format(user_name)
    command_handler.execute(sql)
    sql=command_handler.fetchone()

    list1=list(sql)
    print(list1)

    print("-----------------------------------------------------------------------------------")
    print("")

    if user_name==list1[1]:
        if pass_word==list1[2]:
            while 1:
                
                print("1.DEPOSIT ")
                print("2.WITHDRAWEL")
                print("3.ACCOUNT TRANSFER")
                print("4.BALANCE CHECK")
                print("5.TRANSACTION HISTORY")
                print("6.Logout")
                print("------------------------------------------------------------------------")
                print("")
                user_option=int(input("OPTION : "))
                if user_option==1:
                    deposit()
                if user_option==2:
                    withdraw()
                if user_option==3:
                    transfer()
                if user_option==4:
                    balance_check()
                if user_option==5:
                    transactions()
                if user_option==6:
                    break
                    
def main():    
    while 1:
        print("")
        print("1.NEW USER ")
        print("2.LOGIN")
        print("-----------------------------------------------------------------------------------")
        print("")
        user_option=int(input("OPTION : "))
        print("")
        if user_option==1:
            newuser()
        if user_option==2:
            login()
main()
