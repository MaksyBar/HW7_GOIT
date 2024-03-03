import datetime as dt                                                                        
from datetime import datetime as dtdt
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number")
        super().__init__(value)

class Birthday:
    def __init__(self, value):
        try:
            self.value = dt.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    @staticmethod
    def validate_birthday(birthday):
        try:
            dt.datetime.strptime(birthday, '%d.%m.%Y')
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                if not len(phone) == 10 and phone.isdigit():
                    raise ValueError("New phone number is invalid.")
                phone.value = new_phone
                found = True
                break
        if not found:
            raise ValueError(f"Phone number {old_phone} not found in contacts.")

    # @staticmethod
    # def is_valid_phone(phone_number):
    #     return len(phone_number) == 10 and phone_number.isdigit()

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def __str__(self):
        phone_numbers = "; ".join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {phone_numbers}"

class AddressBook(UserDict):
    
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        tdate = dtdt.now().date()  
        birthdays = []
        for user in self.data.values():  
            bdate = user.birthday.value.date()  
            bdate = bdate.replace(year=tdate.year)
            days_between = (bdate - tdate).days
            if 0 <= days_between < 7:
                if bdate.weekday() < 5:
                    birthdays.append({'name': user.name.value, 'birthday': bdate.strftime("%d.%m.%Y")})
                else:
                    if (bdate + dt.timedelta(days=1)).weekday() == 0:
                        birthdays.append({'name': user.name.value, 'birthday': (bdate + dt.timedelta(days=1)).strftime("%d.%m.%Y")})
                    elif (bdate + dt.timedelta(days=2)).weekday() == 0:
                        birthdays.append({'name': user.name.value, 'birthday': (bdate + dt.timedelta(days=2)).strftime("%d.%m.%Y")})
        return birthdays