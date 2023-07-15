import pymongo

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# myclient = pymongo.MongoClient("mongodb://MainTracker:%24tr0ngPa%24%24w0rD1@89.116.230.121:27017/")
# myclient = pymongo.MongoClient("mongodb://testtracker:Dina1234##@89.116.230.121:27017/test")
# myclient = pymongo.MongoClient("mongodb://TestTracker:$tr0ngPa$$w0rD1@89.116.230.121:27017/test")
# myclient = pymongo.MongoClient("mongodb://testtracker:Dina1234##@89.116.230.121:27017/TestTracker")
# myclient = pymongo.MongoClient("mongodb://TestTracker:$tr0ngPa$$w0rD1@89.116.230.121:27017/test")
# myclient = pymongo.MongoClient("mongodb://dina:$tr0ngPa$$w0rD1@89.116.230.121:27017/BackupMain")
myclient = pymongo.MongoClient("mongodb://BackupMain:%24tr0ngPa%24%24w0rD1@89.116.230.121:27017/MainTracker")
print(True)
print(myclient.list_database_names())
mydb = myclient["MainTracker"]

mycol = mydb["tasks"]
print(mycol)

query = {"merchant": "flipkart"}
products = mycol.find(query)
print(products)
for prod in products:
     
     print(prod.users)


# mydict = { "name": "John", "address": "Highway 37" }
# mycol.insert_one(mydict)

# count = 0
# for i in mycol.find():

#     count+=1
    
#     try: 
#         # print(i['users'][0])
        
#         user = i['users'][0]['userId']
#         if user == 1970524063:
#             print("Found")
#             try:
#                 # print(i)
#                 print(i['title'])
#                 print(i['merchant'])
#                 print(i['link'])
#                 # l= str(i['initPrice']).encode("utf-8")
#                 # print(l)
#                 if "₹" in i['price']:
#                     price = i['price'].replace("₹", "")
#                     print(price)
#                 if type(i['initPrice'])=="str" and "₹" in i['initPrice']:
#                     init_price = i['initPrice'].replace("₹", "")
#                     print(init_price)
#                 else:
#                     init_price = i['initPrice']
#                     print(init_price)
                     
                     
#             except Exception as e:
#                  print(e)    

            
#     except Exception as e:
#             # print(e)
#             pass
            

# print(count)    

