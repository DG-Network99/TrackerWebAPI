import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["products_db"]

amazon = mydb["tasks"]

def get_products():

    all_records = []
    # name, price, initprice, url, tracking_id

    for prod in amazon.find().limit(5):
        
        product = {'url' : prod['link'], 'title' : prod['title'], 
                   'price' : prod['price'], 'initPrice' : prod['initPrice'],
                   'tracking_id' : prod['users'][0]['tracking_id']
                   }
        all_records.append(product)

    return all_records   


def get_products2(tracking_id):

    all_records = []
    for prod in amazon.find():
        for user in prod['users']:
            if user["tracking_id"] == tracking_id:
                product = {'url' : prod['link'], 'title' : prod['title'], 
                   'price' : prod['price'], 'initPrice' : prod['initPrice'],
                   'tracking_id' : prod['users'][0]['tracking_id']
                   }
                return product


if __name__ == "__main__":
    data = get_products() 
    print(data)