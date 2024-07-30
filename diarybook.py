import datetime
import json

class Diary:
    last_id = 0

    def __init__(self, memo, tags=' ', creation_date=None):
        self.memo = memo
        self.tags = tags
        self.creation_date = creation_date or datetime.date.today()
        Diary.last_id += 1
        self.id = Diary.last_id

    def match(self, filter_text):
        return filter_text in self.memo or filter_text in self.tags

    def to_dict(self):
        return {
            'memo': self.memo,
            'tags': self.tags,
            'creation_date': self.creation_date.isoformat(),
            'id': self.id
        }

    @classmethod
    def from_dict(cls, data):
        creation_date = datetime.date.fromisoformat(data['creation_date'])
        diary = cls(data['memo'], data['tags'], creation_date)
        diary.id = data['id']
        if Diary.last_id < diary.id:
            Diary.last_id = diary.id
        return diary

class DiaryBook:
    def __init__(self):
        self.diaries = []

    def new_diary(self, memo, tags=' '):
        self.diaries.append(Diary(memo, tags))

    def search_diary(self, filter_text):
        return [diary for diary in self.diaries if diary.match(filter_text)]

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

def authenticate_user(users):
    name = input("Enter your name: ")
    password = input("Enter your password: ")

    if name in users and users[name] == password:
        print("Login successful")
        return name
    else:
        print("Invalid credentials")
        return None

def register_user(users):
    name = input("Enter a new username: ")
    if name in users:
        print("Username already exists")
        return None
    password = input("Enter a password: ")
    users[name] = password
    save_users(users)
    print("Registration successful")
    return name
