
import json
import random

def write_offer_to_database(data_input, filename='database.json'):
    section = "current book offerings"
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        for n in file_data:
            if n == section:
                file_data[section]['data'].append(data_input)
        
    with open(filename, 'w') as f:
        json.dump(file_data,f,indent=4)


def vendor_registration(name_vendor, filename='database.json'):
    new_vendor ={
        "vendor_id" : random.randint(1,100000),
        "name"  : name_vendor                          
    }
    section = "vendors"
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        for n in file_data:
            if n == section:
                for i in file_data[section]['data']:
                    if i["name"] == name_vendor:
                        return None
        else:
            file_data[section]['data'].append(new_vendor)

    with open(filename, 'w') as f:
        json.dump(file_data,f,indent=4)

def offer():
    title = input("Enter title: ")
    author = input("Enter author name: ")
    year = input("Enter year of publication: ")
    edition = input("Enter edition: ")
    publisher = input("Enter name pf publisher company: ")
    condition = input("Enter condition: new/slightly worn/worn: ")
    description = input("Enter a description from the book: ")
    price = input("Enter price: ")
    name_vendor = input("Enter your name: ")

    new_data={
        "title":title,
        "author":author,
        "year":year,
        "edition" : edition,
        "publisher" : publisher,
        "condition" : condition,
        "description" : description,
        "price" : price,
        "name_vendor" : name_vendor
    }
    write_offer_to_database(new_data)

    vendor_registration(name_vendor)
