from inventory.item import Item

class Inventory:

    def __init__(self):
      self.stock_map = {}
      self.item_map = {}

    def add_item(self, code:str, item:Item, quantity:int ):
         self.item_map[code] = item
         self.stock_map[code] = self.stock_map.get(code, 0) + quantity
    
    def reduce_stock(self, code):
        if code in self.stock_map:
            self.stock_map[code] -= 1

    def get_item(self, code):
        return self.item_map[code]

    def is_available(self, code):
         return code in self.item_map and self.stock_map.get(code, 0) > 0
    
