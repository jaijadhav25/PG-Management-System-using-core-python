import json
import getpass
import hashlib
from admin import Admin
from person import Person

class MainLogin:
    def __init__(self, user_file = 'Data/user.json', admin_file = 'Data/login.json'):
        self.user_file = user_file
        self.admin_file = admin_file
        self.menu()

    def loadData(self, path):
        try:
            with open(path, 'r') as fp:
                return json.load(fp)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def menu(self):
        ch = '0'
        while(ch != '3'):
            print('''Please select option:
            1. Admin.
            2. User.
            3. Exit''')
            ch = input('Enter choice:')

            if ch == '1':
                self.adminLogin()
            elif ch == '2':
                self.userLogin()
            elif ch == '3':
                print('Thank you!.....')
            else:
                print('Invalid choice.....')

    def hashPassword(self, passw):
        return hashlib.md5(passw.encode()).hexdigest()
            

    def userLogin(self):
        self.user_data = self.loadData(self.user_file)
        print('-----USER LOGIN-----')
        user_id = input('Enter User ID:').strip()
        password = getpass.getpass('Enter password:').strip()
        
        hash_pass = self.hashPassword(password)

        if not self.user_data:
            print('No user data found.....')
            return
        
        for user in self.user_data:
            if(user['User_id'] == user_id and user['User_pass'] == hash_pass):
                print(f"Welcome {user['Name']}! Login Successful.")
                p1 = Person()
                return
        
        print('Invalid User ID or Password.')
        return

    def adminLogin(self):
        self.admin_data = self.loadData(self.admin_file)
        print('-----Admin login-----')
        username = input('Enter Admin Username:').strip()
        password = getpass.getpass('Enter Admin Password:').strip()

        hash_pass = self.hashPassword(password)

        if not self.admin_data:
            print('No admin data found.....')
            return
        
        for admin in self.admin_data:
            if(username in admin and admin[username] == hash_pass):
                print(f'Welcome Admin Login successfully!....')
                a1 = Admin()
                return
            
        print('Invalid Admin Username or Password.')
        return


if(__name__ == '__main__'):
    m1 = MainLogin()
