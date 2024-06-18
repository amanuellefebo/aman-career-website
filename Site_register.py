import streamlit as st 
import pandas as pd
import streamlit as st
import smtplib
import os
import ssl 
import smtplib
from email.message import EmailMessage
sender='amanuelmarkos.1@gmail.com'
password="rznmjwfkqnxpbssj"
import mysql.connector
mydb=mysql.connector.connect(host='localhost',
                             user='root',
                             password='Rahel2023.',
                             database='user_db'
                             )
mycursor=mydb.cursor()
def main():
    st.subheader('welcome to our website')
    st.subheader("where do you want to go?")
    option=st.selectbox("select an options", ("subscribe to our channel","update my credential","cancel subscription"))
    if option == "subscribe to our channel":
        
            option=st.selectbox("select an options",("yes","no"))
            if option == 'yes':
                st.subheader("Do you want to subscribe?")
                first_name=st.text_input("Enter your first name")
                last_name=st.text_input("Enter your last name")
                email=st.text_input("Enter your email")
                sql="insert into persons(first_name,last_name,email) values(%s,%s,%s)"
                val=(first_name,last_name,email)
                if st.button('enter'):
                    reciever=email
                    mycursor.execute(sql,val)
                    mydb.commit()
                    st.success("Thanks for registeration, we will send you an email confirmation")
                    subject="Congrat for Registration" 
                    body= """
                    Dear Subcriber,
                    congra you succesfully subscribed to our movie channel for free.
                    As a reminder, we highly encourage you to vist the timely content
                    that we post every time.
                    With regards,
                    WSB Data Science Team
                    """
                    em=EmailMessage() 
                    em['From']=sender 
                    em['to']= reciever 
                    em['sub']=subject 
                    em.set_content(body) 
                    context=ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp: 
                        smtp.login(sender,password) 
                        smtp.sendmail(sender,reciever,em.as_string())
                        quit()
            elif option=='no': 
                st.write('try again other time')
            

                
               
            
        
    elif option == "update my credential":
        option=st.selectbox("you can update",('yes','no'))
        if option == 'yes':
            st.subheader("Do you want to update your credential")
            email=st.text_input('enter your email')
            new_f_name=st.text_input('enter your new_f_name')
            new_l_name=st.text_input('enter your new_l_name')
            if st.button('enter'): 
                sql="update persons set first_name=%s,last_name=%s where email=%s" 
                val=(new_f_name,new_l_name,email) 
                mycursor.execute(sql,val) 
                mydb.commit()
                st.write("Your data is updated successfully")
            
                
        elif option =='no':
           st.write("you can return back to the main menu")
        
            
            
        
    elif option=='cancel subscription':
        option=st.selectbox(('are you sure you want to delete?'),('yes','no'))
        if option=='yes': 
            id=st.number_input("enter your id")
            if st.button('enter'):
                st.subheader("cancel subcription")
                
                sql="Delete from persons where id=%s" 
                val=(id,) 
                mycursor.execute(sql,val) 
                mydb.commit() 
                st.success('Your subscription is delete from our system')
                    
        elif option =='no':
            if st.button('enter'):
                st.write("Your subscription is active")
        
            
            
       
       
       
           
           
       
if __name__ =="__main__":
    main()


    



 