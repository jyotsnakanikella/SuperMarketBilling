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
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///itemDB.db'
app.config['connect_args'] ={'timeout': 10}
db=SQLAlchemy(app)

global items_from_db
class ItemDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    item_price = db.Column(db.Integer,nullable=False)
    category_discount = db.Column(db.Integer,nullable=False)
    sub_category_discount = db.Column(db.Integer,nullable=False)
    item_discount = db.Column(db.Integer,nullable=False)
    is_percent_discount = db.Column(db.Boolean, default=False, nullable=False)
    buy_item = db.Column(db.Integer,nullable=False)
    free_item = db.Column(db.Integer,nullable=False)
    real_discount = db.Column(db.Integer,default=0)

    def __repr__(self):
        return 'Itemdetails ' + str(self.id)
    
class Billing:
    # itemMap:Dict

    def __init__(self):
        self.itemMap={}
        Billing.boughtItemsList=[]
    #     self.init()

    # def init(self):
    #     self.itemMap["Apple"] = Item(50, 10, 18, 0, False, 3, 1)
    #     self.itemMap["Orange"] = Item(80, 10, 18, 20, True, 0, 0)
    #     self.itemMap["Potato"] = Item(30, 10, 5, 0, False, 5, 2)
    #     self.itemMap["Tomato"] = Item(70, 10, 5, 10, True, 0, 0)
    #     self.itemMap["Cow Milk"] = Item(50, 15, 20, 0, False, 3, 1)
    #     self.itemMap["Soy Milk"] = Item(40, 15, 20, 10, True, 0, 0)
    #     self.itemMap["Cheddar"] = Item(50, 15, 20, 0, False, 2, 1)
    #     self.itemMap["Gouda"] = Item(80, 15, 20, 10, True, 0, 0)

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
        global items_from_db
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
				
		    
            currItem = items_from_db[bi.item]
            bi.real_amount = bi.quantity * currItem[0]
			
            if (currItem[4]) :
                bi.billed_amount = bi.real_amount * (100 - currItem[7]) / 100
            else :
                discount_item = bi.quantity // (currItem[5] + currItem[6])
                billed_quantity = bi.quantity - discount_item * currItem[6]
                bi.billed_amount = billed_quantity* currItem[0]
			
			
            if (flag_unit_type_big == False) :
                bi.real_amount *= pow(10, -3)
                bi.billed_amount *= pow(10, -3)
			
            if (flag_unit_type_dozen):
                bi.quantity /= 12
			
            Billing.boughtItemsList.append(bi)

def generate_billing(line1="Customer Anish Kumar buys following items",line2="Apple 6Kg, Orange 2Kg, Potato 14Kg, Tomato 3Kg, Cow Milk 8Lt, Gouda 2Kg"):
    item_details_dict = get_Item_Details()

    billing=Billing()
    input_line1 = line1
    input_line2 = line2
  
    customer_name=billing.get_customer_name(input_line1)
    billing.generate_customer_invoice(input_line2)

    total_real_amount=billing.get_total_real_amount()
    total_billed_amount=billing.get_total_billed_amount()
    saved_amount=billing.get_saved_amount(total_real_amount,total_billed_amount)

    customer_name = f"Customer:  {customer_name}"
    total_billed_amount="{:.2f}".format(total_billed_amount)
    total_real_amount="{:.2f}".format(total_real_amount)
    saved_amount="{:.2f}".format(saved_amount)
    for item in Billing.boughtItemsList:
        item.billed_amount = "{:.2f}".format(item.billed_amount)
    amounts = [customer_name,total_billed_amount,total_real_amount,saved_amount]
    return amounts

def get_Item_Details():
    all_items = ItemDetails.query.all()
    get_Item_Details_dict(all_items)
    print(items_from_db)

def get_Item_Details_dict(all_items):
    dict = {}
    for item in all_items:
        dict[item.name] = [item.item_price,item.category_discount,item.sub_category_discount,item.item_discount,item.is_percent_discount,item.buy_item,item.free_item,item.real_discount]
    global items_from_db
    items_from_db = dict

@app.route('/billsfromdb')
def print_bill_from_db():
    add_items_to_db()
    amounts = generate_billing()
    amounts.extend(Billing.boughtItemsList)
    return render_template('billDB.html',amounts=amounts)  

def calculateRealDiscount():

    final_dict = {}
    dictionary = {'apple':[10, 18, 0,False],'orange':[10, 18, 20, True],'potato':[10, 5, 0, False],'tomato':[10, 5, 10, True],'cowMilk':[15, 20, 0, False],'soyMilk':[15, 20, 10, True],'cheddar':[15, 20, 0, False],'gouda':[15, 20, 10, True]}
    for key in dictionary:
        if(dictionary[key][3]==True):
            if(dictionary[key][2]>dictionary[key][0] and dictionary[key][2]>dictionary[key][1]):
                final_dict[key]= dictionary[key][2] 
            elif(dictionary[key][1]>dictionary[key][0]):
                final_dict[key]= dictionary[key][1]    
            else:
                final_dict[key]= dictionary[key][0]       
        else:
            final_dict[key]= dictionary[key][2] 
    return final_dict

def add_items_to_db():
    # itemlist=[]
    dict=calculateRealDiscount()
    
    apple = ItemDetails(name="Apple",item_price=50, category_discount=10, sub_category_discount=18, item_discount=0, is_percent_discount=False, buy_item=3, free_item=1,real_discount=dict['apple'])
    orange = ItemDetails(name="Orange",item_price=80, category_discount=10, sub_category_discount=18, item_discount=20, is_percent_discount=True, buy_item=0, free_item=0,real_discount=dict['orange'])
    potato = ItemDetails(name="Potato",item_price=30, category_discount=10, sub_category_discount=5, item_discount=0, is_percent_discount=False, buy_item=5, free_item=2,real_discount=dict['potato'])
    tomato = ItemDetails(name="Tomato",item_price=70, category_discount=10, sub_category_discount=5, item_discount=10, is_percent_discount=True, buy_item=0, free_item=0,real_discount=dict['tomato'])
    cowMilk = ItemDetails(name="Cow Milk",item_price=50, category_discount=15, sub_category_discount=20, item_discount=0, is_percent_discount=False, buy_item=3, free_item=1,real_discount=dict['cowMilk'])
    soyMilk = ItemDetails(name="Soy Milk",item_price=40, category_discount=15, sub_category_discount=20, item_discount=10, is_percent_discount=True, buy_item=0, free_item=0,real_discount=dict['soyMilk'])
    cheddar = ItemDetails(name="Cheddar",item_price=50, category_discount=15, sub_category_discount=20, item_discount=0, is_percent_discount=False, buy_item=2, free_item=1,real_discount=dict['cheddar'])
    gouda = ItemDetails(name="Gouda",item_price=80, category_discount=15, sub_category_discount=20, item_discount=10, is_percent_discount=True, buy_item=0, free_item=0,real_discount=dict['gouda'])

    itemlist=[apple,orange,potato,tomato,cowMilk,soyMilk,cheddar,gouda]
    db.session.add_all(itemlist)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True) 