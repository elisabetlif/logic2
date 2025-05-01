import os

def db_management():

    for filename in os.listdir('session-databases'):
        file_path = os.path.join('session-databases', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
        