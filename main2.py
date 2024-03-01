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
                if not self.is_valid_phone(new_phone):
                    raise ValueError("New phone number is invalid.")
                phone.value = new_phone
                found = True
                break
        if not found:
            raise ValueError(f"Phone number {old_phone} not found in contacts.")

    @staticmethod
    def is_valid_phone(phone_number):
        return len(phone_number) == 10 and phone_number.isdigit()

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

    def __str__(self):
        records_info = '\n'.join(str(record) for record in self.data.values())
        return f"Address Book:\n{records_info}"
    
    @staticmethod
    def get_upcoming_birthdays(users=None):
        tdate = dtdt.now().date()  # Змінено
        birthdays = []
        for user in users:
            bdate = user.birthday.value.date()  # Змінено
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

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)

    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts[name] = record
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, new_phone = args
    if name in contacts:
        contacts[name] = new_phone
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return f"The phone number for {name} is {contacts[name]}."
    else:
        return f"Contact {name} not found."

@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts found."
    else:
        all_contacts = "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
        return f"All contacts:\n{all_contacts}"
    
@input_error
def add_birthday(args, contacts):
    name, birthday = args
    if name in contacts:
        contacts[name].add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, contacts):
    name = args[0]
    if name in contacts and contacts[name].birthday:
        return f"The birthday for {name} is {contacts[name].birthday.value.strftime('%d.%m.%Y')}."
    else:
        return f"Birthday not found for {name}."
    
@input_error
def birthdays(contacts):
    upcoming_birthdays = AddressBook.get_upcoming_birthdays(contacts.values())
    if upcoming_birthdays:
        return "Upcoming birthdays:\n" + "\n".join(f"{contact['name']}: {contact['birthday']}" for contact in upcoming_birthdays)
    else:
        return "No upcoming birthdays."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I assist you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

# Example usage
birthday = "1990-05-20"