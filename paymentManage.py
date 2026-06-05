import json
from prettytable import PrettyTable

class PaymentManage:
    def __init__(self, payment_file = 'Data/payment.json'):
        self.payment_file = payment_file
        self.payment_data = self.loadData(self.payment_file)

    def loadData(self, path):
        try:
            with open(path, 'r') as fp:
                return json.load(fp)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def saveData(self, path, data):
        try:
            with open(path, 'w') as fp:
                return json.dump(data, fp, indent=4)
        except Exception as e:
            print('Error:', e)

    def menu(self):
        ch = '0'
        while(ch != '2'):
            print('''Please select option:
            1.view.
            2.Exit.''')
            ch = input('Enter your choice:')
            if(ch == '1'):
                self.viewPaymentHistory()
            elif(ch == '2'):
                print('Payment manage successfully.....')
            else:
                print('Invalid choice....')


    def viewPaymentHistory(self):
        try:
            if not self.payment_data:
                print('No payment history found for this user.')
                return
            
            user_payment = [p for p in self.payment_data]

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

if(__name__ == '__main__'):
    p1 = PaymentManage()
    p1.menu()
