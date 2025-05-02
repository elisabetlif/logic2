from enum import Enum
from dotenv import load_dotenv
import os
import importlib
import shutil
from pathlib import Path

class Choice(Enum):
    search = "search"
    purchase = "purchase"
    offer = "offer"
    db_management = "db_management"

def copyDB(session_id):
    src_path = Path('database.json')
    dest_folder = Path('session-databases')
    new_name = 'database'+str(session_id)+'.json'
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_file = dest_folder / (new_name)
    shutil.copy2(src_path, dest_file)

def update_session():
    load_dotenv(dotenv_path="var.env")
    new_session = 1+int(os.getenv("SESSION_ID"))
    os.environ['SESSION_ID']=str(new_session)
    with open("var.env", "w") as f:
        f.write(f"SESSION_ID={new_session}\n")
    copyDB(new_session)


def main():
    while(True):
        func_name,args=user_input()
        if func_name =='end':
            break
        mod = importlib.import_module(func_name)
        func = getattr(mod, func_name, None)

        if callable(func):
            try:
                func(*args)
            except Exception as e:
                print("Something went wrong:", e)
        else:
            print(f"{func_name} not found in {func_name}")

def user_input():
    print("\nWelcome\n")
    print("Actions:")
    print(" 1. Search \n 2. Purchase\n 3. Offer\n 4. Change DB")

    while True:
        val = input(">").split(" ")
        if val[0]=='':
            return ('end', 0)
        try:
            choice = int(val[0])

            if choice not in range(1,5):
                raise ValueError
            return (list(Choice)[choice-1].value, val[1:])
        except ValueError:
            print("Input must be an integer choice between 1-4!")

  
    

if __name__ == "__main__":
    update_session()
    main()