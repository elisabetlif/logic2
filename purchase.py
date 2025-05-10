import json
from dotenv import load_dotenv
import os
from datetime import date



# Labels used:
# customer input: {customer : marketplace}
# customer ID: {customer : marketplace}
#vendor ID: {customer, marketplace : marketplace}
# book_id, price,purchase_date, sale_id, price_sold: {marketplace : marketplace}
# outputs to customer: {customer : ⊥} ← requires declassification
# Inputs are used as indices only; flows permitted without endorsement




#function to create and write the new purchase into the database
#data_input: {customer:marketplace}
#flow:  {customer:marketplace} -> {marketplace:marketplace}
#flow is allowed as the data_input is just used for indexing
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


    #The customer ID provided by the customer
    #data_input: {customer:marketplace}
    #flow:  {customer:marketplace}
    index_customer_id = data_input["customer_id"]

    #use the customer ID provided by the customer to index the database and fetch the customer ID from the database
    #data_input: {customer:marketplace}
    #flow:  {customer:marketplace}
    #customer ID is stored as {customer:marketplace} in the Marketplace database
    customer_id = fetch_customer_id(file_data, index_customer_id)
    
    #the book ID provided by the customer input
    #data_input: {customer:marketplace}
    #flow:  {customer:marketplace} -> {marketplace:marketplace}
    #flow is allowed as the data_input is just used for indexing
    index_book_id = data_input["book_id"]

    #use the book ID provided by the customer to index the database and fetch the book ID from the database
    #data_input: {customer:marketplace}
    #flow:  {customer:marketplace} -> {marketplace:marketplace}
    #flow is allowed as the data_input is just used for indexing
    book_id =fetch_book_id(file_data,index_book_id)

    #fetch vendor_id
    #data_input: {customer:marketplace}
    #flow:  {customer:marketplace} -> {customer, marketplace:marketplace}
    #flow is allowed as the data_input is just used for indexing and is not entered into the database
    vendor_id = fetch_vendor_id(file_data,book_id)
    
    
    #create the purchase date
    purchase_date = date.today()
   

    #The price provided by the customer input
    index_price_sold = data_input["price_sold"]

    #use the price provided by the customer to index the database and fetch the price from the database
    price_sold = fetch_price(file_data,index_price_sold)

    #sale_id: {marketplace:marketplace}
    #vendor_id: {vendor,marketplace:marketplace}
    #customer_id: {customer:marketplace}
    #book_id: {marketplace:marketplace}
    #purchase_date: {marketplace:marketplace}
    #price_sold: {marketplace:marketplace}
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


#Get last sales ID in order to create a new sales ID for the purchase
#{marketplace:marketplace}
def get_last_sales_id(database):
    last_sales_id = database.get("purchase_information", {}).get("data",[])
    if last_sales_id:
        return int(last_sales_id[-1]["book_id"])
    else:
        return 0


#fetch vendor ID given the book ID from the customer input
#{customer:marketplace} -> {customer, marketplace:marketplace}
#flow is allowed as the data_input is just used for indexing and is not entered into the database
#returns {customer, marketplace:marketplace}
def fetch_vendor_id(database,book_id):
    book_data = database.get("current book offerings", {}).get("data",[])
    vendor_id = next(
    (entry["vendor_id"] for entry in book_data if entry["book_id"] == book_id),
    None)
    return vendor_id

#use the customer ID from the customer input to index the corresponding customer ID in the database
# {customer:marketplace} -> {marketplace:marketplace} 
#returns {marketplace:marketplace}
def fetch_customer_id(database, index_customer_id):
    customer_data = database.get("registered customers", {}).get("data", [])
    customer_id = next(
        (entry["customer_id"] for entry in customer_data if entry["customer_id"] == index_customer_id),
        None)
    return customer_id


#use the book ID from the customer input to index the corresponding book ID in the database 
#{customer:marketplace} -> {marketplace:marketplace}
#returns {marketplace:marketplace}
def fetch_book_id(database, index_book_id):
    book_data = database.get("current book offerings", {}).get("data", [])
    book_id = next(
        (entry["book_id"] for entry in book_data if entry["book_id"] == index_book_id),
        None)
    return book_id



#use the price from the customer input to index the corresponding price in the database 
#{customer:marketplace} -> {marketplace:marketplace}
#returns {marketplace:marketplace}
def fetch_price(database, book_id):
    offerings = database.get("current book offerings", {}).get("data", [])
    price = next(
        (entry["price"] for entry in offerings if entry["book_id"] == book_id),
        None)
    return price




#check if the offer is still valid
#label: {marketplace : marketplace}
# input used to select data, not included in computation
# Safe: no endorsement or declassification needed
#check_book_offer takes in book_id from the customer input which has the label {customer:marketplace} but flow is allowed as the input is just used for indexing
def check_book_offer(book_id,session_id):
    filename = f'session-databases/database{session_id}.json'
    with open(filename, 'r+') as file:
        file_data = json.load(file)
    book_data = file_data.get("current book offerings", {}).get("data",[])
    for entry in book_data:
        if entry["book_id"] == book_id:
            return True
    return False


#check if the input price matches the bood id
#label: {marketplace : marketplace}
# input used to select data, not included in computation
# Safe: no endorsement or declassification needed
#check_price takes in price from the customer input which has the label {customer:marketplace} but flow is allowed as the input is just used for indexing
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
                return False
    return False


#get the address of the customer for the confirmation of purchase message
#{customer:marketplace} -> {marketplace:marketplace}
def get_address_of_customer(customer_id, session_id):
    filename = f'session-databases/database{session_id}.json'
    with open(filename, 'r+') as file:
        file_data = json.load(file)
    customer_data = file_data.get("registered customers", {}).get("data",[])
    for entry in customer_data:
        if entry["customer_id"] == customer_id:
            return entry["addr"]
    return None


#Book is removed from the database after being purchased
#{marketplace:marketplcace}
def remove_book_after_purchase(book_id,session_id):
    filename = f'session-databases/database{session_id}.json'
    with open(filename, 'r+') as file:
        file_data = json.load(file)
   # Remove from "current_book_offerings"
        current_offerings = file_data.get("current book offerings", {}).get("data", [])
        filtered_offerings = [entry for entry in current_offerings if entry.get("book_id") != book_id]
        file_data["current book offerings"]["data"] = filtered_offerings

     # Remove from "books"
        books_data = file_data.get("books", {}).get("data", [])
        filtered_books = [book for book in books_data if book.get("book_id") != book_id]
        file_data["books"]["data"] = filtered_books

    
        file.seek(0)
        json.dump(file_data, file, indent=2)
        file.truncate()

 
def purchase(*args):
    load_dotenv(dotenv_path="var.env")
    session_id = os.getenv("SESSION_ID")

    #customer inputs these three items and sends a purchase request to Marketplace
    #all three inputs: {customer:marketplace}
    book_id = int(input("Enter the book ID of the book you wish to purchase: "))
    price = int(input("Enter the offered price of the book: "))
    customer_id = int(input("Enter your customer ID: "))

    #get customer address using the provided customer ID
    #we're using the customer ID provided by the customer and so label is: {customer:marketplace}
    # -> Marketplace can read the customer's address but if output then needs to be declassified
    customer_address = get_address_of_customer(customer_id,session_id)

    #{customer:marketplace}
    data_input = {
      "book_id": book_id,
      "price_sold" : price,
      "customer_id" : customer_id
    }
    #label: {marketplace : marketplace}
    if check_book_offer(book_id,session_id) and check_price(price,book_id,session_id):
        write_purchase_to_database(data_input,session_id)
        remove_book_after_purchase(book_id,session_id)
       

        # Declassification required: {customer:marketplace} ⊑ {customer:⊥}
        # Marketplace outputs customer-owned data → explicit release
        print("Here is the shipping address: ", customer_address)
    else:
        return None

