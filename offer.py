
import json
import random
from dotenv import load_dotenv
import os

def write_offer_to_database(new_book, new_offering, session_id):
    filename = f'session-databases/database{session_id}.json'
    offerings_section = "current book offerings"
    books_section = "books"
    
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        
        # Ensure sections exist
        if books_section not in file_data:
            file_data[books_section] = {'data': []}
        if offerings_section not in file_data:
            file_data[offerings_section] = {'data': []}
        
        # Check if book exists
        book_id = None
        for book in file_data[books_section]['data']:
            if book['info'] == new_book:
                book_id = book['book_id']
                break
        
        # If book doesn't exist, add it
        if book_id is None:
            new_book_id = 1 + get_last_book_id(file_data)
            file_data[books_section]['data'].append({
                'book_id': new_book_id,
                'info': new_book
            })
            book_id = new_book_id
        
        # Create offering with proper book_id
        new_offering['book_id'] = book_id
        file_data[offerings_section]['data'].append(new_offering)
        
        # Write back to file
        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.truncate()


def get_last_book_id(database):
    vendors = database.get("books", {}).get("data", [])
    if vendors:
        return int(vendors[-1]["book_id"])
    else:
        return 0  

def get_last_vendor_id(database):
    vendors = database.get("vendors", {}).get("data", [])
    if vendors:
        return int(vendors[-1]["vendor_id"])
    else:
        return 0  
def vendor_registration(userID, session_id):
    filename = 'session-databases/database'+session_id+'.json'
    section1 = "registered customers"
    section2 = "vendors"
    userID = int(userID)  # Convert once at the start
    
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        
        # Check if user is a registered customer
        isCustomer = False
        if section1 in file_data:
            for customer in file_data[section1]['data']:
                if customer["customer_id"] == userID:
                    isCustomer = True
                    break
        
        if not isCustomer:
            return -1
        
        # Check if user is already a vendor
        if section2 in file_data:
            for vendor in file_data[section2]['data']:
                if vendor["customer_id"] == userID:
                    return vendor["vendor_id"]
        
        # If not, add new vendor
        new_vendor_id = 1 + get_last_vendor_id(file_data)
        new_vendor = {
            "vendor_id": new_vendor_id,
            "customer_id": userID
        }
        
        # Ensure vendors section exists
        if section2 not in file_data:
            file_data[section2] = {'data': []}
        
        file_data[section2]['data'].append(new_vendor)
        
        # Reset file position and write
        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.truncate()  # Important in case new data is smaller than old
        
        return new_vendor_id


def getVendorName(vendor_id,session_id):
    filename = 'session-databases/database'+session_id+'.json'
    if vendor_id ==-1:
        return "not valid"
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        section = "vendors"
        for n in file_data:
                if n == section:
                    for i in file_data[section]['data']:
                        if i["vendor_id"] == vendor_id:
                            userID = int(i["customer_id"])
                            for j in file_data["registered customers"]["data"]:
                                if j["customer_id"] == userID:
                                    return j["name"]
    with open(filename, 'w') as f:
        json.dump(file_data,f,indent=4)

def offer(userID: str, input_self: bool = False):
    load_dotenv(dotenv_path="var.env")
    session_id = os.getenv("SESSION_ID")
    vendor_id=vendor_registration(userID,session_id)
    print(vendor_id)
    if input_self:
        title = input("Enter title: ")
        author = input("Enter author name: ")
        year = input("Enter year of publication: ")
        edition = input("Enter edition: ")
        publisher = input("Enter name of publisher company: ")
        condition = input("Enter condition (new/slightly worn/worn): ")
        description = input("Enter a description from the book: ")
        price = input("Enter price: ")
        name_vendor = input("Enter your name: ")
    else:
        sample_titles = ["The Great Gatsby", "1984", "Moby Dick", "To Kill a Mockingbird"]
        sample_authors = ["F. Scott Fitzgerald", "George Orwell", "Herman Melville", "Harper Lee"]
        sample_years = [1925, 1949, 1851, 1960]
        sample_editions = ["1st", "2nd", "Reprint", "Collector's"]
        sample_publishers = ["Penguin", "HarperCollins", "Vintage", "Random House"]
        sample_conditions = ["new", "slightly worn", "worn"]
        sample_descriptions = [
            "Classic American novel.", "Dystopian masterpiece.", 
            "A story of obsession and revenge.", "Civil rights-era courtroom drama."
        ]
        sample_prices = [10.99, 7.50, 12.00, 5.75]

        title = random.choice(sample_titles)
        author = random.choice(sample_authors)
        year = str(random.choice(sample_years))
        edition = random.choice(sample_editions)
        publisher = random.choice(sample_publishers)
        condition = random.choice(sample_conditions)
        description = random.choice(sample_descriptions)
        price = random.choice(sample_prices)
        name_vendor = getVendorName(vendor_id,session_id)

    new_book = {
        "title": title,
        "author": author,
        "year": year,
        "edition": edition,
        "publisher": publisher,
        "condition": condition,
        "description": description
    }

    new_offering = {"book_id":0,
                    "price":price,
                     "name_vendor":name_vendor,
                    "vendor_id":vendor_id
                   
                }
    
    if not name_vendor =="not valid":
        write_offer_to_database(new_book,new_offering,session_id)
    print("Offer recived.")
    
