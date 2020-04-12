E_INT, E_FLOAT, E_STR = "INT", "FLOAT", "STR"

class EventGet:

    def __init__(self, val):
        self.val = None
        self.type = {int:E_INT, float:E_FLOAT, str:E_STR}[val]

class EventSet:

    def __init__(self, val):
        self.val = val
        self.type = {int:E_INT, float:E_FLOAT, str:E_STR}[type(val)]

class NullHandler:

    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, obj, event):
        if self.successor is not None:
           return self.successor.handle(obj, event)

class StrHandler(NullHandler):
    
    def handle(self, obj, event):
        if event.type == E_STR:
            if event.val is None:
                return obj.string_field
            else:
                obj.string_field = event.val
        else:
            return super().handle(obj, event)

class FloatHandler(NullHandler):

    def handle(self, obj, event):
        if event.type == E_FLOAT:
            if event.val is None:
                return obj.float_field
            else:
                obj.float_field = event.val
        else:
            return super().handle(obj, event)

class IntHandler(NullHandler):
    
    def handle(self, obj, event):
        if event.type == E_INT:
            if event.val is None:
                return obj.integer_field
            else:
                obj.integer_field = event.val
        else:
            return super().handle(obj, event)
