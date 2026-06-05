import json
from prettytable import PrettyTable

class ComplaintManage:
    def __init__(self, comp_file = 'Data/user_complaint.json'):
        self.comp_file = comp_file
        self.comp_data = self.loadData(self.comp_file)

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
        while(ch != '4'):
            print('''Please select option:
            1. view all complaint.
            2. Update status of complaint.
            3. Delete complaint.
            4. Exit.''')
            ch = input('Enter your choice:')
            if(ch == '1'):
                self.viewAllComplaint()
            elif(ch == '2'):
                self.updateStatus()
            elif(ch == '3'):
                self.deleteComplaint()
            elif(ch == '4'):
                print('You have manage the complaint.....')
            else:
                print('Invalid choice.....')

    def viewAllComplaint(self):
        try:
            if not self.comp_data:
                print('No complaint found.')
                return
            else:
                print('List of complaint.....')
                print('-' * 40)
                table = PrettyTable()
                table.field_names = ['Complaint id', 'Room id', 'Bed id', 'Complaint text', 'Date', 'Status']
                
                for compliant in self.comp_data:
                    table.add_row([compliant['Complaint_id'], compliant['Room_id'], compliant['Bed_id'], compliant['Complaint_text'], compliant['Date'], compliant['Status']])

                print(table)
        except Exception as e:
            print('Error:',e)
    
    def updateStatus(self):
        try:
            if not self.comp_data:
                print('No complaint found')
                return
            else:
                try:
                    complaint_id = int(input('Enter complaint id:'))
                except ValueError:
                    print("Invalid input! Complaint id must be a number.")
                    return

                complaint_found = False
                complaint_updated = []
                for complaint in self.comp_data:
                    if(complaint['Complaint_id'] == complaint_id):
                        complaint_found = True
                        print('Current complaint status.')
                        print(f"Complaint id:{complaint['Complaint_id']}")
                        print(f"Room id:{complaint['Room_id']}")
                        print(f"Bed id:{complaint['Bed_id']}")
                        print(f"Complaint:{complaint['Complaint_text']}")
                        print(f"Date:{complaint['Date']}")
                        print(f"Status:{complaint['Status']}")

                        print('-' * 40)
                        print('\nChoose new status:')
                        print('1. Pending.')
                        print('2. Resolved.')

                        while True:
                            try:    
                                ch = input('Enter your choice(1/2):')

                                if(ch == '1'):
                                    complaint['Status'] = 'Pending'
                                    break
                                elif(ch == '2'):
                                    complaint['Status']='Resolved'
                                    break
                                else:
                                    print('Invalid choice!.....')
                            except Exception as e:
                                print('Error',e)
                        complaint_updated.append(complaint)
                    else:
                        complaint_updated.append(complaint)
                    
                    self.saveData(self.comp_file, complaint_updated)
                if not complaint_found:
                    print('Complaint id not found!.....')
        except Exception as e:
            print('Error:',e)

    def deleteComplaint(self):
        try:
            if not self.comp_data:
                print('NO complaint found.....')
                return
            
            chk = input('Do you want to delete this resolved complaint? (y / n):').strip()
            if(chk.lower() in ('yes', 'y')):
                count = 0
                for complaint in self.comp_data:
                    if(complaint['Status'] == 'Resolved'):
                        count += 1
                        self.comp_data.remove(complaint)
                if count == 0:
                    print('No resolved complaint found to deleted.....')
                else:
                    print(f'{count} Resolved complaint are deleted successfully.....')    
                    
            self.saveData(self.comp_file, self.comp_data)
        except Exception as e:
            print('Error:',e)
            

if(__name__ == '__main__'):
    c1 = ComplaintManage()
    c1.menu()