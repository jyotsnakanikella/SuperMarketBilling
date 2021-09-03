
class Item:
    # item_price:int #price of item
    # category_discount:int #Category level discount
    # sub_category_discount:int #Sub category level discount
    # item_discount:int #real discount on item, 0 when giving free items on purchase
    # is_percent_discount:bool #to check if discount is of percentage type or free item on purchase
    # buy_item:int #Number of items to be buied to get free item 
    # free_item:int #Number of free items the customer can get
    # real_discount:int

    def __init__(self,item_price,category_discount,sub_category_discount,item_discount,is_percent_discount,buy_item,free_item):
        self.item_price=item_price
        self.category_discount=category_discount
        self.sub_category_discount=sub_category_discount
        self.item_discount=item_discount
        self.is_percent_discount=is_percent_discount
        self.buy_item=buy_item
        self.free_item=free_item
        if(self.is_percent_discount):
            self.setRealDiscount()

    def setRealDiscount(self):
        if(self.item_discount>self.category_discount and self.item_discount>self.sub_category_discount):
            self.real_discount=self.item_discount
        elif(self.sub_category_discount>self.category_discount):
            self.real_discount=self.sub_category_discount
        else:
            self.real_discount=self.category_discount

