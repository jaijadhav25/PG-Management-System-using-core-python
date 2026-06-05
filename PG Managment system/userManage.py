import json
import hashlib
from prettytable import PrettyTable

class UserManage:
    def __init__(self, user_file='Data/user.json', room_file = 'Data/room.json'):
        self.user_file = user_file
        self.room_file = room_file
        self.user_data = self.loadData(self.user_file)
        self.room_data = self.loadData(self.room_file)

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
        ch = '0'
        while(ch != '6'):
            print('''Please select option:
            1. Add user.
            2. delete user.
            3. Update user.
            4. view specific user.
            5. show all user.
            6. Exit.''')
            ch = input('Enter your choice:')
            if(ch == '1'):
                self.addUser()
            elif(ch == '2'):
                self.deleteUser()
            elif(ch == '3'):
                self.updateUser()
            elif(ch == '4'):
                self.viewSpecificUser()
            elif(ch == '5'):
                self.showAllUser()
            elif(ch == '6'):
                print('you have manage the User.....')
            else:
                print('Invalid choice.....')

    def hash_password(self, passw):
        return hashlib.md5(passw.encode()).hexdigest()

    def addUser(self):
        try:
            print('Add new user.....')
            user_id = input('Enter user id:').strip()
            if not user_id:
                print('User id is necessary.....')
                return
                
            for user in self.user_data:
                if(user['User_id'] == user_id):
                    print('User id is already exist....')
                    return
                
                
            while True:
                name = input('Enter name of user:').strip()
                if not name:
                    print('Name cannot be empty!.....')
                    continue
                
                if all(part.isalpha() for part in name.split()) and name == name.title(): 
                    break
                else:
                    print('Invalid name should contain alphabet and have format like Ranjit Kamble.....')
            
            
            while True:
                user_pass = input('Enter user passward:').strip()
                if(len(user_pass)<5):
                    print('Password to short, password length must be greater than 5.....')
                else:
                    break
            
            while True:
                contact = input('Enter contact number:').strip()
                if(contact.isdigit() and len(contact) == 10):
                    break
                else:
                    print('Invalid contact number.....')
            
            while True:
                aadhar = input('Enter aadhar number:')
                if(aadhar.isdigit() and len(aadhar) == 12):
                    break
                else:
                    print('Invalid aadhar number.....')


            hash_pass = self.hash_password(user_pass)        
            room_id = input('Enter room id:')
            for room in self.room_data:
                if(room['room_id'] == room_id):

                    for bed_nm , status in room['beds'].items():
                        if(status == 'Vacant'):
                            room['beds'][bed_nm] = 'Occupied'
                            room['available_beds'] -=1


                            user = {
                                'User_id':user_id,
                                'Name':name,
                                'User_pass':hash_pass,
                                'Contact_no':contact,
                                'Aadhar_no':aadhar,
                                'Room_id':room_id,
                                'Bed_id':bed_nm,
                            }
                            self.user_data.append(user)

                            self.saveData(self.user_file, self.user_data)
                            self.saveData(self.room_file, self.room_data)

                            print(f"User '{name}' added successfully!.....")
                            print(f"Room: {room_id}, Bed: {bed_nm}")
                            return
                    print("No vacant bed available in this room!.....")
                    return
            
            print('Room id not found!.....')
        except Exception as e:
            print('Error:',e)

    def deleteUser(self):
        try:
            print('Remove User')
            user_id = input('Enter user id to remove:')
            
            user_to_remove = None
            for user in self.user_data:
                if(user['User_id'] == user_id):
                    user_to_remove = user
                    break

            if not user_to_remove:
                print('User not found!.....')
                return
            
            for room in self.room_data:
                if(room['room_id'] == user_to_remove['Room_id']):
                    bed_id = user_to_remove['Bed_id']
                    if bed_id in room['beds']:
                        room['beds'][bed_id] = 'Vacant'
                        room['available_beds'] += 1
                    break

            self.user_data.remove(user_to_remove)

            self.saveData(self.user_file, self.user_data)
            self.saveData(self.room_file, self.room_data)

            print(f"User {user_to_remove['Name']} removed successfully!.....")
            print(f"Room {user_to_remove['Room_id']}, Bed {user_to_remove['Bed_id']} is now Vacant.")
        except Exception as e :
            print('Error:',e)

        

    def updateUser(self):
        try:
            print('Update User Data.....')
            user_id = input('Enter user id to update user data:')

            user_found = False
            user_to_update = []
            for user in self.user_data:
                if(user['User_id'] == user_id):
                    user_found = True
                    chk = input('Do you want to change the user information(y / n):').strip()
                    if(chk.lower() in ('yes', 'y')):
                        chk1 = input('Do you want to change user name(y / n):').strip()
                        if(chk1.lower() in ('yes', 'y')):
                            while True:
                                name = input('Enter name of user:').strip()
                                if all(part.isalpha() for part in name.split()) and name == name.title():
                                    user['Name'] = name
                                    print('Name updated successfully!.....')
                                    break
                                else:
                                    print('Invalid name should contain alphabet and have format like Ranjit Kamble.....')
                            
                        chk2 = input('Do you want to update user contact number(y / n):').strip()
                        if(chk2.lower() in ('yes', 'y')):
                            while True:
                                contact = input('Enter new contact number:').strip()
                                if(contact.isdigit() and len(contact) == 10):
                                    break
                                else:
                                    print('Invalid contact number.....')
                            user['Contact_no'] = contact
                            print('contact number updated successfully!.....')
                    user_to_update.append(user)
                else:
                    user_to_update.append(user)
                        
                self.user_data = user_to_update
                self.saveData(self.user_file, self.user_data)
            if not user_found:
                print('User Not found!.....')
        except Exception as e:
            print('Error:',e)

    def viewSpecificUser(self):
        try:
            if not self.user_data:
                print('No User Data Found.')
                return
            else:
                user_id = input('Enter user id to view profile:')
                user_found = False
                for user in self.user_data:
                    if(user['User_id'] == user_id):
                        user_found = True
                        print('User profile is:')
                        print('-' * 40)
                        print(f"User ID:{user['User_id']}")
                        print(f"Name:{user['Name']}")
                        print(f"User Password:{user['User_pass']}")
                        print(f"Contact number:{user['Contact_no']}")
                        print(f"Aadhar number:{user['Aadhar_no']}")
                        print(f"Room ID:{user['Room_id']}")
                        print(f"Bed id:{user['Bed_id']}")
                        print('-' * 40)
                if not user_found:
                    print('User not found.....')

        except Exception as e:
            print('Error')

    def showAllUser(self):
        try:
            if not self.user_data:
                print('No user found')
                return
            else:
                print('List of user.....')
                print('-' * 40)
                tabel = PrettyTable()
                tabel.field_names = ['User_ID', 'Name', 'User_Password', 'Contact_number', 'Aadhar_number', 'Room_ID', 'Bed_ID']

                sorted_user = sorted(self.user_data, key = lambda s:(s['Room_id'], s['Bed_id']))
                
                for user in sorted_user:
                    tabel.add_row([user['User_id'],user['Name'],user['User_pass'],user['Contact_no'],user['Aadhar_no'],user['Room_id'],user['Bed_id']])
                
                print(tabel)
                    
        except Exception as e:
            print('Error:',e)


if(__name__ == '__main__'):
    s1 = UserManage()
    s1.menu()



        