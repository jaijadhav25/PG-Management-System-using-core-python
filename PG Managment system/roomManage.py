import json

class RoomManage:
    def __init__(self, room_file = 'Data/room.json'):
        self.room_file = room_file
        self.rooms = self._loadData()

    def menu(self):
        ch = '0'
        while(ch != '5'):
            print('''please select option.
            1. Add Room.
            2. show Room.
            3. delete Room.
            4. update Room.
            5. Exit.''')
            ch = input('Enter your choice.')
            if(ch == '1'):
                self.addRoom()
            elif(ch == '2'):
                self.showRooms()
            elif(ch == '3'):
                self.delRoom()
            elif(ch == '4'):
                self.updateStatusRoom()
            elif(ch == '5'):
                print('you have manage the room.....')
            else:
                print('Invalid choice.....')

    def _loadData(self):
        try:
            with open(self.room_file, 'r') as fp:
                return json.load(fp)
        except(FileNotFoundError, json.JSONDecodeError):
            return []
            

    def _saveData(self):
        try:
            with open('Data/room.json','w') as fp:
                json.dump(self.rooms, fp, indent=4)
        except Exception as e:
            print('Error',e)

    def addRoom(self):
        try:
            room_id = input('Enter Room ID:')

            for r in self.rooms:
                if(r['room_id'] == room_id):
                    print('Room ID already exists! try another one.')
                    return

            while True:
                try:
                    total_beds = int(input('Enter total beds:'))
                    if(total_beds > 0):
                        break
                    else:
                        print('Total beds must be a positive number.')
                except ValueError as e:
                    print('Invalid input:',e)


            
            new_room = {
                'room_id': room_id,
                'total_beds': total_beds,
                'available_beds': total_beds,
                'beds': {f'Bed{i}':'Vacant' for i in range(1, total_beds + 1)}
            }

            self.rooms.append(new_room)
            self._saveData()
            print('Room added successfully.')
        except Exception as e:
            print('Error:',e)

    def showRooms(self):
        try:
            if not self.rooms:
                print('No rooms found')
                return
            else:
                print('\n List of Rooms:')
                print('-' * 40)
                for room in self.rooms:
                    print(f"Room ID:{room['room_id']}")
                    print(f"Total Beds:{room['total_beds']}")
                    print(f"Available beds:{room['available_beds']}")
                    print('Bed Status:')
                    for bed, status in room['beds'].items():
                        print(f' {bed}: {status}')
                    print('-' * 40)
        except Exception as e:
            print('Error:',e)
        

    def delRoom(self):
        try:
            if not self.rooms:
                print('No rooms to delete.')
                return
            else:
                room_ids = input('Enter room ID to delete:').strip()
                room_found = False

                updated_rooms = []
                for room in self.rooms:
                    if(room['room_id'] == room_ids):
                        room_found = True
                        if room['available_beds'] != room['total_beds']:
                            print('Cannot delete room! some beds are still occupied.')
                            updated_rooms.append(room)
                        else:
                            print(f'Room {room_ids} deleted successfully.')
                    else:
                        updated_rooms.append(room)
                if not room_found:
                    print('Room not found.')
                
                self.rooms = updated_rooms
                self._saveData()
        except Exception as e:
            print('Error:',e)

        

    def updateStatusRoom(self):
        try:
            if not self.rooms:
                print('No rooms to Update.')
                return
            else:
                room_ids = input('Enter room ID:').strip()
                room_found = False
                updated_room = []
                for room in self.rooms:
                    if(room['room_id'] == room_ids):
                        room_found = True
                        print('Current room status:')
                        print('-' * 40)
                        print(f"Room ID:{room['room_id']}")
                        print(f"Total Beds:{room['total_beds']}")
                        print(f"Available beds:{room['available_beds']}")
                        print('Beds status:')
                        for bed, status in room['beds'].items():
                            print(f'{bed}:{status}')
                        print('-' * 40)

                        chk = input('Do you want to change total Bed capacity (y / n):').strip()
                        if(chk.lower() in ('yes', 'y')):
                            chk1 = input('Do you want to add bed(y / n):').strip()
                            if(chk1.lower() in ('yes', 'y')):
                                while True:
                                    try:
                                        add_bed = int(input('Enter how many beds you want add:').strip())
                                        if(add_bed > 0):
                                            break
                                        else:
                                            print('No must be positive number.....')
                                    except ValueError as e:
                                        print('Value error:',e)

                                start = room['total_beds'] + 1
                                end = room['total_beds'] + add_bed + 1
                                for i in range(start, end):
                                    room['beds'][f'Bed{i}']= 'Vacant'

                                room['total_beds'] += add_bed
                                room['available_beds'] += add_bed
                                print('Bed added successfully.....')
                            chk2 = input('Do you want to remove bed(y / n):').strip()
                            if(chk2.lower() in ('yes', 'y')):
                                print(f"Current total beds:{room['total_beds']}")
                                print(f"Aviable (Vacant) beds:{room['available_beds']}")
                                remove_bed = int(input('How many beds do you want to remove:').strip())

                                vacant_bed = [bed for bed, status in room['beds'].items() if status == 'Vacant']
                                # print(vacant_bed)

                                if(remove_bed > len(vacant_bed)):
                                    print('Not enough vacant bed to remove....')
                                    return
                                
                                for i in range(len(vacant_bed) - 1, len(vacant_bed) - remove_bed - 1, -1):
                                    bed  = vacant_bed[i]
                                    del room['beds'][bed]

                                room['total_beds'] -= remove_bed
                                room['available_beds'] -= remove_bed
                                print('Bed deleted successfully.....')
                        updated_room.append(room)
                    else:
                        updated_room.append(room)

                    self.rooms = updated_room
                    self._saveData()

                if not room_found:
                    print('Room Not found.....')
                   
        except Exception as e:
            print('Error:', e)


if(__name__ == '__main__'):
    r1 = RoomManage()
    r1.menu()