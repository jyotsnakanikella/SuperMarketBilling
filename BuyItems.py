class BuyItems:
    # item:str #name of buied item
    # quantity:int #quantity of buied item
    # unit:str #unit of buied item (kg, lt, dozen etc.)
    # real_amount:float #real cost of item without discount
    # billed_amount:float #cost of item after discount

    
    @property
    def item(self):
        return self._item
       
    @item.setter
    def item(self, a):
        self._item = a

    @property
    def quantity(self):
        return self._quantity
       
    @quantity.setter
    def quantity(self, a):
        self._quantity = a

    @property
    def unit(self):
        return self._unit
       
    @unit.setter
    def unit(self, a):
        self._unit = a

    
    @property
    def real_amount(self):
        return self._real_amount

    @real_amount.setter
    def real_amount(self, a):
        self._real_amount = a

    @property
    def billed_amount(self):
        return self._billed_amount    
       
    @billed_amount.setter
    def billed_amount(self, a):
        self._billed_amount = a

    
                  