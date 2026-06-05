import json
from datetime import date
from prettytable import PrettyTable

class Person:
    def __init__(self, complaint_file = 'Data/user_complaint.json', user_file = 'Data/user.json', payment_file = 'Data/payment.json'):
        self.comp_file = complaint_file
        self.user_file = user_file
        self.payment_file = payment_file
        self.comp_data = self.loadData(self.comp_file)
        self.user_data = self.loadData(self.user_file)
        self.payment_data = self.loadData(self.payment_file)
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
        ch = '0'
        while(ch != '6'):
            print('''Please select your choice:
            1. View your profile.
            2. Pay rent.
            3. view payment.
            4. Add complaint.
            5. view your complaint.
            6. Exit.''')
            ch = input('Enter your choice:').strip()
            if(ch == '1'):
                self.viewProfile()
            elif(ch == '2'):
                self.payRent()
            elif(ch == '3'):
                self.viewPaymentHistory()
            elif(ch == '4'):
                self.addComplaint()
            elif(ch == '5'):
                self.viewComplaint()
            elif(ch == '6'):
                print('User Logged out.....')
            else:
                print('Invalid choice.....')


    def viewProfile(self):
        try:
            if not self.user_data:
                print('NO User Data Found.....')
                return
            else:
                user_id = input('Enter user id:')

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
                    print('Profile Not Found.....')
        except Exception as e:
            print('Error:',e)

    def payRent(self):
        try:
            print('------ Pay Rent ------')
            user_id = input('Enter your user ID: ').strip()

            user = next((u for u in self.user_data if u['User_id'] == user_id), None)
            if not user:
                print('User not found!.....')
                return 
            
            while True:
                print('''Please select option to pay rent:
                1. UPI
                2. Card
                3. Bank Transfer''')
                choice = input('Enter your choice: ').strip()
                if choice == '1':
                    payment = self._process_upi()
                    break
                elif choice == '2':
                    payment = self._process_card()
                    break
                elif choice == '3':
                    payment = self._process_bank()
                    break
                else:
                    print('Invalid choice......')

            amount = '6000'

            if self.payment_data:
                last_pid = max(p['Payment_id'] for p in self.payment_data)
                payment_id = last_pid + 1
            else:
                payment_id = 1

            payment_date = date.today().strftime("%d-%m-%Y")

            pay_record = {
                'Payment_id': payment_id,
                'User_id': user['User_id'],
                'Room_id': user['Room_id'],
                'Bed_id': user['Bed_id'],
                'Amount': amount,
                'Payment_date': payment_date,
                'Method': payment['method'],
            }

            if 'masked' in payment:
                pay_record['Details'] = payment['masked']

            self.payment_data.append(pay_record)
            self.saveData(self.payment_file, self.payment_data)

            user['Payment_status'] = 'Paid'
            self.saveData(self.user_file, self.user_data)

            print(f"Payment Successful! Method: {payment['method']}")
            if 'masked' in payment:
                print(f"Details: {payment['masked']}")
            print(f'Amount Paid: ₹{amount} on {payment_date}')

        except Exception as e:
            print('Error:', e)

    def _process_upi(self):
        upi_id = input('Enter UPI ID (example: user@upi): ').strip()
        if '@' not in upi_id:
            raise ValueError('Invalid UPI ID')
        return {'method': 'UPI', 'masked': upi_id, 'paid': True}

    def _process_card(self):
        card = input('Enter Card Number (digits only, dummy): ').strip()
        cvv = input('Enter CVV (dummy): ').strip()
        if not (card.isdigit() and 13 <= len(card) <= 19):
            raise ValueError('Invalid Card Number')
        if not (cvv.isdigit() and len(cvv) in (3,4)):
            raise ValueError('Invalid CVV')
        last4 = card[-4:]
        masked = '**** **** **** ' + last4
        return {'method': 'Card', 'masked': masked, 'card_last4': last4, 'paid': True}

    def _process_bank(self):
        bank_acc = input('Enter Bank Account Number (dummy): ').strip()
        if not bank_acc.isdigit() or len(bank_acc) < 8:
            raise ValueError('Invalid Bank Account')
        return {'method': 'Bank Transfer', 'masked': '****' + bank_acc[-4:], 'paid': True}


    def viewPaymentHistory(self):
        try:
            user_id = input('Enter your user ID:')

            user_payment = [p for p in self.payment_data if p['User_id'] == user_id]

            if not user_payment:
                print('No payment history found for this user.')
                return
            
            user_payment.sort(key=lambda x: (x['Room_id'], x['Bed_id']))

            table = PrettyTable()
            table.field_names = ['Payment id', 'User id', 'Room id', 'Bed id', 'Amount', 'Payment date', 'Method']

            for p in user_payment:
                table.add_row([
                    p['Payment_id'],
                    p['User_id'],
                    p['Room_id'],
                    p['Bed_id'],
                    p['Amount'],
                    p['Payment_date'],
                    p['Method']
                ])
            
            print(table)
        except Exception as e:
            print('Error:',e)


    def addComplaint(self):
        try:
            print('Add new complaint.....')
            room_id = input('Enter your room id:')
            bed_id = input('Enter your bed id:')
            complaint_text = input('Enter your complaint:')

            if  self.comp_data:
                last_id = max(c['Complaint_id'] for c in self.comp_data)
                complaint_id = last_id + 1
            else:
                complaint_id = 1

            new_complaint = {
                'Complaint_id':complaint_id,
                'Room_id':room_id,
                'Bed_id':bed_id,
                'Complaint_text':complaint_text,
                'Date':str(date.today()),
                'Status':'Pending'
            }

            self.comp_data.append(new_complaint)
            self.saveData(self.comp_file, self.comp_data)
            print(f'Complaint : {complaint_id} \nComplaint added successfully!.....')
        except Exception as e:
            print('Error:',e)

    def viewComplaint(self):
        try:
            print('View your compliants.....')
            room_id = input('Enter room id:')
            bed_id = input('Enter bed id:')

            if not self.comp_data:
                print('No complaints found.....')
                return
            
            complaint_found = False
            for complaint in self.comp_data:
                if(complaint['Room_id'] == room_id and complaint['Bed_id'] == bed_id):
                    complaint_found = True
                    print('-' * 40)
                    print('Your complint is .....')
                    print('-' * 40)
                    print(f"Compliant ID : {complaint['Complaint_id']}")
                    print(f"Complaint : {complaint['Complaint_text']}")
                    print(f"Status : {complaint['Status']}")
                    print('-' * 40)
            if not complaint_found:
                print('No complaints found for this bed.')
        except Exception as e:
            print('Error:',e)



if(__name__ == '__main__'):
    p1 = Person()