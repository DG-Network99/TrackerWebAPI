import pymongo
import re

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tasks"]

prodcol = mydb["tasks"]

async def get_products(user_id):

    all_records = []
    
    count = 0
    for prod in prodcol.find():

        count+=1 
        try:             
            # user = i['users'][1]['userId']
            # Dina user_id : 1378380156
            for user in prod['users']:
                if user['userId'] == int(user_id):
                    print("Found")
                    try:
                        # print(i)
                        print(prod['title'])
                        print(prod['merchant'])
                        print(prod['link'])
                        # l= str(i['initPrice']).encode("utf-8")
                        # print(l)
                        if "₹" in prod['price']:
                            price = prod['price'].replace("₹", "")
                            print(price)
                        if type(prod['initPrice'])=="str" and "₹" in prod['initPrice']:
                            init_price = prod['initPrice'].replace("₹", "")
                            print(init_price)
                        else:
                            init_price = prod['initPrice']
                            print(init_price)
                        product = {'url' : prod['link'], 'title' : prod['title'], 
                                    'price' : prod['price'], 'initPrice' : prod['initPrice'],
                                    'tracking_id' : user['tracking_id']
                                    }
                        all_records.append(product)    
                            
                            
                    except Exception as e:
                        print(e)    

                
        except Exception as e:
                # print(e)
                pass
    # for prod in prodcol.find().limit(5):
        
    #     product = {'url' : prod['link'], 'title' : prod['title'], 
    #                'price' : prod['price'], 'initPrice' : prod['initPrice'],
    #                'tracking_id' : prod['users'][0]['tracking_id']
    #                }
    #     all_records.append(product)

    return all_records   


def get_products2(tracking_id):

    all_records = []
    for prod in prodcol.find():
        for user in prod['users']:
            if user["tracking_id"] == tracking_id:

                #change 'date' to 'x' and 'price' to 'y' for chart plotting
                price_history = []
                for x in prod['priceHistory']:
                    y={}
                    price = re.sub("[^\d\.]", "", x['price'])
                    y['x'] = x['date'] 
                    y['y'] = price
                    del x['date']
                    del x['price']
                    price_history.append(y)


                product = {'url' : prod['link'], 'title' : prod['title'], 
                   'price' : prod['price'], 'initPrice' : prod['initPrice'],
                   'tracking_id' : prod['users'][0]['tracking_id'],
                   'price_history' : price_history
                   }
                return product


if __name__ == "__main__":
    data = get_products() 
    print(data)