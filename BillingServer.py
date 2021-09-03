from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from BuyItems import BuyItems
from Item import Item
from typing import Dict
import re
import sys
import os


app = Flask(__name__)

class Billing:
    # itemMap:Dict

    def __init__(self):
        self.itemMap={}
        Billing.boughtItemsList=[]
        self.init()

    def init(self):
        self.itemMap["Apple"] = Item(50, 10, 18, 0, False, 3, 1)
        self.itemMap["Orange"] = Item(80, 10, 18, 20, True, 0, 0)
        self.itemMap["Potato"] = Item(30, 10, 5, 0, False, 5, 2)
        self.itemMap["Tomato"] = Item(70, 10, 5, 10, True, 0, 0)
        self.itemMap["Cow Milk"] = Item(50, 15, 20, 0, False, 3, 1)
        self.itemMap["Soy Milk"] = Item(40, 15, 20, 10, True, 0, 0)
        self.itemMap["Cheddar"] = Item(50, 15, 20, 0, False, 2, 1)
        self.itemMap["Gouda"] = Item(80, 15, 20, 10, True, 0, 0)

    def get_total_real_amount(self):
        totalRealAmount = 0
        for item in Billing.boughtItemsList:
            totalRealAmount+=item.real_amount
        return totalRealAmount

    def get_total_billed_amount(self):
        total_billed_amount=0
        for item in Billing.boughtItemsList:
            total_billed_amount+=item.billed_amount
        return total_billed_amount

    def get_saved_amount(self,real_amount,billed_amount):
        return real_amount-billed_amount

    def get_customer_name(self,input_line1):
        customer_detail=input_line1.split(" ")
        customer_name=""
        for i in range(1,len(customer_detail)):
            if(customer_detail[i] == "buys"):
                break
            customer_name+=customer_detail[i]+" "

        return customer_name

    def generate_customer_invoice(self,order_list):
        orders=order_list.split(",")
        for order in orders:
            flag_unit_type_big=True
            flag_unit_type_dozen=False

            order=order.strip()
            bi=BuyItems()
            pos=order.rindex(" ")
            bi.item=order[0:pos]
            quantity=order[pos+1:]
            
            part=re.split("(?<=\\d)(?=\\D)",quantity)
            bi.quantity=int(part[0])

            if len(part) > 1:
                bi.unit = part[1]
            else:
                bi.unit = ""

            if ((bi.unit == None or len(bi.unit)== 0) == False):
				 
                if (not(bi.unit == "kg" or bi.unit=="lt")) and not(bi.unit=="dozen"):
                    flg_unit_type_big = False
				
                if (bi.unit=="dozen"):
                    bi.quantity *= 12
                    flg_unit_type_dozen = True
				
		   
            currItem = self.itemMap[bi.item]
            bi.real_amount = bi.quantity * currItem.item_price
			
            if (currItem.is_percent_discount) :
                bi.billed_amount = bi.real_amount * (100 - currItem.real_discount) / 100
            else :
                discount_item = bi.quantity // (currItem.buy_item + currItem.free_item)
                billed_quantity = bi.quantity - discount_item * currItem.free_item
                bi.billed_amount = billed_quantity* currItem.item_price
			
			
            if (flag_unit_type_big == False) :
                bi.real_amount *= pow(10, -3)
                bi.billed_amount *= pow(10, -3)
			
            if (flag_unit_type_dozen):
                bi.quantity /= 12
			
            Billing.boughtItemsList.append(bi)

def generate_billing(line1="Customer Anish Kumar buys following items",line2="Apple 6Kg, Orange 2Kg, Potato 14Kg, Tomato 3Kg, Cow Milk 8Lt, Gouda 2Kg"):
    billing=Billing()
    input_line1 = line1
    input_line2 = line2
  
    customer_name=billing.get_customer_name(input_line1)
    billing.generate_customer_invoice(input_line2)

    total_real_amount=billing.get_total_real_amount()
    total_billed_amount=billing.get_total_billed_amount()
    saved_amount=billing.get_saved_amount(total_real_amount,total_billed_amount)

    # print(f"Customer:  {customer_name}")
    # print("Item \t\t Qty \t Amount")
    customer_name = f"Customer:  {customer_name}"
    total_billed_amount="{:.2f}".format(total_billed_amount)
    total_real_amount="{:.2f}".format(total_real_amount)
    saved_amount="{:.2f}".format(saved_amount)
    for item in Billing.boughtItemsList:
        item.billed_amount = "{:.2f}".format(item.billed_amount)
    amounts = [customer_name,total_billed_amount,total_real_amount,saved_amount]
    return amounts
   
    # print(f"{item.item}  {item.quantity}  {item.unit} {item.billed_amount}")
		
    # print(f"\nTotal Amount {total_billed_amount}Rs")
    # print(f"\nYou saved       {total_real_amount} - {total_billed_amount} = {saved_amount}Rs")


@app.route('/bills')
def print_bill():
    amounts = generate_billing()
    amounts.extend(Billing.boughtItemsList)
    return render_template('bill.html',amounts=amounts)

            
if __name__ == '__main__':
    app.run(debug=True) 