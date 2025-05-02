import json
from dotenv import load_dotenv
import os
from datetime import date

#def write_purchase_to_database(data_input,session_id):
def write_purchase_to_database(data_input,session_id):
    filename = f'session-databases/database{session_id}.json'
    
    purchase_section = "purchase_information"

    with open(filename, 'r+') as file:
        file_data = json.load(file)

     # Ensure sections exist
        if purchase_section not in file_data:
            return 0
    
    
    #create sales_id
    new_sales_id = 1+ get_last_sales_id(file_data)


    #extract the customer_id from the customer input
    customer_id = data_input["customer_id"]
    
    #extract the book_id from the customer input
    book_id = data_input["book_id"]

    #fetch vendor_id
    vendor_id = fetch_vendor_id(file_data,book_id)
    
    
    #create the purchase date
    purchase_date = date.today()
   

    #extract price from customer input
    price_sold = data_input["price_sold"]

    #let's construct the purchase data that will go into the database
    new_purchase = {
        "sale_id": new_sales_id,
        "vendor_id" : vendor_id,
        "customer_id": customer_id,
        "book_id" : book_id,
        "purchase_date" : purchase_date.isoformat(),
        "price_sold" : price_sold
    }
    
    
    # Write back to file
    with open(filename, 'w') as file:
        file_data[purchase_section]['data'].append(new_purchase)
        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.truncate()


def get_last_sales_id(database):
    last_sales_id = database.get("purchase_information", {}).get("data",[])
    if last_sales_id:
        return int(last_sales_id[-1]["book_id"])
    else:
        return 0


def fetch_vendor_id(database,book_id):
    book_data = database.get("current book offerings", {}).get("data",[])
    vendor_id = next(
    (entry["vendor_id"] for entry in book_data if entry["book_id"] == book_id),
    None)
    return vendor_id


#check if the offer is still valid
def check_book_offer(book_id,session_id):
    filename = f'session-databases/database{session_id}.json'
    with open(filename, 'r+') as file:
        file_data = json.load(file)
    book_data = file_data.get("current book offerings", {}).get("data",[])
    for entry in book_data:
        if entry["book_id"] == book_id:
            return True
    print("We're not currently offering this book")
    return False


#check if the input price matches the bood id       
def check_price(price,book_id,session_id):
    filename = f'session-databases/database{session_id}.json'
    with open(filename, 'r+') as file:
        file_data = json.load(file)
    book_data = file_data.get("current book offerings", {}).get("data",[])
    for entry in book_data:
        if entry["book_id"] == book_id:
            if  entry["price"] == price:
                return True
            else:
                print("You have input the wrong price, redo the process")
                return False
    return False



def get_address_of_customer(customer_id, session_id):
    filename = f'session-databases/database{session_id}.json'
    with open(filename, 'r+') as file:
        file_data = json.load(file)
    customer_data = file_data.get("registered customers", {}).get("data",[])
    for entry in customer_data:
        if entry["customer_id"] == customer_id:
            return entry["addr"]
    return None

 
def purchase(*args):
    load_dotenv(dotenv_path="var.env")
    session_id = os.getenv("SESSION_ID")

    #customer inputs these three items and  sends a purchase request to Marketplace
    book_id = int(input("Enter the book ID of the book you wish to purchase: "))
    price = int(input("Enter the offered price of the book: "))
    customer_id = int(input("Enter your customer ID: "))

    customer_address = get_address_of_customer(customer_id,session_id)

    data_input = {
      "book_id": book_id,
      "price_sold" : price,
      "customer_id" : customer_id
    }

    if check_book_offer(book_id,session_id) and check_price(price,book_id,session_id):
        write_purchase_to_database(data_input,session_id)
        print("congrats on your purchase!")
        print("Here is the shipping address: ", customer_address)
    else:
        print("redo the process")

