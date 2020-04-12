import os
import csv

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)
    def get_photo_file_ext(self):
            file = os.path.split(self.photo_file_name)
            ext_do = file[1].split('.')
            ext = ext_do[1]
            return '.' + ext


class Car(CarBase):
    car_type = 'car'
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        try:
            self.body_length, self.body_width, self.body_height = (float(c) for c in body_whl.split('x', 2))
        except ValueError:
            self.body_length, self.body_width, self.body_height = float(0), float(0), float(0)
    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = 'spec_machine'
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter = ';')
        next(reader)
        for row in reader:
            try:
                if row[0] == 'car':
                    if row[1] and '.' in row[3] and row[5] and row[2]:
                        car_list.append(Car(row[1], row[3], row[5], row[2]))
                elif row[0] == 'truck':
                    if row[1] and '.' in row[3] and row[5]:
                        car_list.append(Truck(row[1], row[3], row[5], row[4]))
                elif row[0] == 'spec_machine':
                    if  row[1] and '.' in row[3] and row[5] and row[6]:
                        car_list.append(SpecMachine(row[1], row[3], row[5], row[6]))
            except ValueError:
                continue
            except IndexError:
                break
    return car_list

#cars = get_car_list('csv_example.csv')
#print(cars)