# SuperMarketBilling
A supermarket bill will be generated using python, flask, SQLite DB -> which takes input from user, uses existing discounts and costs of items stored in sqlite db, calculate the bills and display it to the user on localhost using flask in bill format.


We take inputs from a user like what all items, quantity of each item bought in a file. We have the cost of each item, discount on each item already ready(eg:flat 10% dicount type or 2+1 type of offers) stored in sqlite db, we will first parse the file which has details of items bought by user, calculate the cost of each item, total cost, Discount on each item, total discount and then store them in sqlite db again, then displaying the output on localhost as a bill format using flask. 
