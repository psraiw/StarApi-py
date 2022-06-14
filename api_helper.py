from NorenRestApiPy.NorenApi import NorenApi
from threading import Timer
import pandas as pd
import time
import concurrent.futures

api = None
class order:
     def __init__(self, buy_or_sell:str, product_type:str,
                 exchange: str, tradingsymbol:str, 
                 price_type: str = 'LMT', quantity: int, price: float,trigger_price:float = None,
                 retention:str = 'DAY', remarks: str = "tag",
                 order_id:str):
        self.buy_or_sell=buy_or_sell
        self.product_type=product_type
        self.exchange=exchange
        self.tradingsymbol=tradingsymbol
        self.quantity=quantity
        self.discloseqty=discloseqty
        self.price_type=price_type
        self.price=price
        self.trigger_price=trigger_price
        self.retention=retention
        self.remarks=remarks
        self.order_id=None


    #print(ret)

    return ret

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)


class StarApiPy(NorenApi):
    
    def __init__(self, *args, **kwargs):
        super(StarApiPy, self).__init__(host='https://starapiuat.prostocks.com/NorenWClientTP', websocket='wss://starapiuat.prostocks.com/NorenWS/', eodhost='https://star.prostocks.com/chartApi/getdata')
        global api
        api = self

    def place_order(self, order: order):
        return api.place_order(buy_or_sell=order.buy_or_sell, product_type=order.product_type,
                        exchange=order.exchange, tradingsymbol=order.tradingsymbol, 
                        quantity=order.quantity, discloseqty=order.discloseqty, price_type=order.price_type, 
                        price=order.price, trigger_price=order.trigger_price,
                        retention=order.retention, remarks=order.remarks)

    def place_basket(self, orders):
        resp_err = 0
        resp_ok  = 0
        result   = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(place_order, order): order for order in  orders}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
            try:
                result.append(future.result())
            except Exception as exc:
                print(exc)
                resp_err = resp_err + 1
            else:
                resp_ok = resp_ok + 1
        return result
                
            