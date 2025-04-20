def db_management(i:int):
    try:
        new_db = int(i)
        print(f"You have changed {new_db} to new DB!")
    except ValueError:
        raise ValueError(f"args {i} is not an int")
            
        