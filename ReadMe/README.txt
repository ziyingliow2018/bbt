Instruction:
Before starting the steps, start wamp and load table.sql into phpmyadmin by importing our sql file\

We have 2 database tables. 

item- Stores all the drinks menu
order - stores all the customer order

***************************************************************************************************************************************

List of modules required
** use "pip install <module name>" to complete installation
1. flask
2. flask_sqlalchemy
3. flask_cors
4. environ
5. sys
6. os
7. requests
8. telebot
9. json
10. pika
11. mysql.connector

**************************************************************************************************************************************
Instructions on running G1T5's bubbletea solution

1. Login to docker desktop and run docker desktop

2. In command prompt, type this command: docker pull ziying123/itemdb:1.0.0 to pull the image of the docker container

3. Check that the image is being fetched locally by typing in this command 'docker images'

4. run the docker container of our itemdb by typing : 
docker run -p 5000:5000 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/bubbletea ziying123/itemdb:1.0.0

5. Check that your container is running: docker ps

6. Open another command prompt, and run our microservices: python orderdb.py ; python monitoring.py ; 
monitoring.py will receive message from orderdb via AMQP when new order is created

7. In our zip file, open login.php to access the staff UI

8. Login by clicking on sign in (we assumed that customer had already registered with us) to enter our homepage: 
index.html or sign in via facebook (the facebook API has not been made public yet)

9. At index.html, at the menu navigation bar, click on Order Form to proceed with order

10. Customer can order a drink through the place_order.html by typing their last 4 digit NRIC and choose the drinks they want. 
(we assume that users have to choose both base and topping)

11. Click on submit. Upon submit, user will be directed to payment page where they can pay via paypal 
or debitcard/credit card. (our project uses a test paypal account for demo, hence it will auto login to paypal test account)

12. Payment is completed and user will wait for their drinks!

13. Next, is the Staff UI

14. open staff_ui.html and you will see a list of un-prepared drinks (with status = Incomplete)

15. Staff can click on the update button to update the status from Incomplete to Completed 

16. Upon clicking the update button, the status will be changed to completed and will trigger the telegram API to 
send message from @SmooChaBot to the user (for this project, we put one of our member to be the default receiver) 

17. Additionally, to search for order, type the last 4 digit NRIC and the order will be retrieved if it exists in order database.

******************************************************************************************************************************************

End of tutorial :))