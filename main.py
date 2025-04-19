from enum import Enum
import importlib

class Choice(Enum):
    search = "search"
    purchase = "purchase"
    offer = "offer"
    db_management = "db_management"


def main():
    while(True):
        func_name,args=user_input()
        print(args)
        if func_name =='end':
            break
        mod = importlib.import_module(func_name)
        func = getattr(mod, func_name, None)

        if callable(func):
            func()
        else:
            print(f"{func_name} not found in {func_name}")
#offer
#search
#purchase
#change db
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
            print("Input must be an integer choice between 1-3!")

  
    

if __name__ == "__main__":
    main()