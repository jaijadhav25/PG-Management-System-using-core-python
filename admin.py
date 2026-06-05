import json
import hashlib
from roomManage import RoomManage
from userManage import UserManage
from complaintManage import ComplaintManage
from paymentManage import PaymentManage

class Admin:
        def __init__(self, admin_file = 'Data/login.json'):
            self.admin_file = admin_file
            self.admin_data = self.loadData(self.admin_file)
            self.menu()

        def loadData(self, path):
            try:
                with open(path, 'r') as fp:
                    return json.load(fp)
            except (FileNotFoundError, json.JSONDecodeError):
                return []
            
        def saveData(self, path, data):
            try:
                with open(path, 'w') as fp:
                    json.dump(data, fp, indent=4)
            except Exception as e:
                print('Error:',e)

        def menu(self):
            print('Admin login successful...')
            ch = '0'
            while(ch != '6'):
                print('''Please select option.
                1. Manage rooms.
                2. Manage user.
                3. Manage complaints.
                4. Manage payments.
                5. Add admin login.
                6. Logout.''')
                ch = input('Enter your choice:')
                if(ch == '1'):
                    r1 = RoomManage()
                    r1.menu()
                elif(ch == '2'):
                    s1 = UserManage()
                    s1.menu()
                elif(ch == '3'):
                    c1 = ComplaintManage()
                    c1.menu()
                elif(ch == '4'):
                    r1 = PaymentManage()
                    r1.menu()
                elif(ch == '5'):
                    self.addAdminLogin()
                elif(ch == '6'):
                    print('Logged out.....')
                else:
                    print('Invalid choice.....')


        def hashPassword(self, passw):
            return hashlib.md5(passw.encode()).hexdigest()
            

        def addAdminLogin(self):
            try:
                print('-----Add New Admin-----')
                
                admin_name = input('Enter new admin username:').strip()
                admin_pass = input('Enter admin password:').strip()

                if not admin_name or not admin_pass:
                    print('Username and password cannot be empty.')
                    return
                
                for admin in self.admin_data:
                    if admin_name in admin:
                        print(f'Admin {admin_name} already exists.')
                        return
                    
                hash_pass = self.hashPassword(admin_pass)

                new_admin = {admin_name: hash_pass}
                self.admin_data.append(new_admin)

                self.saveData(self.admin_file, self.admin_data)
                print(f'Admin {admin_name} added successfully.....')

            except Exception as e:
                print('Error:',e)

if(__name__ == '__main__'):
    a1 = Admin()
        