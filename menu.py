import sys
import json
from diarybook import DiaryBook, Diary, load_users, save_users, authenticate_user, register_user

class Menu:
    def __init__(self):
        self.users = load_users()
        self.user = None
        self.diarybook = DiaryBook()
        self.choices = {
            "1": self.show_diaries,
            "2": self.add_diary,
            "3": self.search_diaries,
            '4': self.quit
        }

    def display_menu(self):
        print(""" 
                     Notebook Menu  
                    1. Show diaries
                    2. Add diary
                    3. Search diaries
                    4. Quit program
                    """)

    def run(self):
        self.user_authentication()
        self.load_user_diaries()
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def user_authentication(self):
        choice = input("Do you want to (1) Login or (2) Register? ")
        if choice == '1':
            self.user = authenticate_user(self.users)
            if not self.user:
                self.user_authentication()
        elif choice == '2':
            self.user = register_user(self.users)
            if not self.user:
                self.user_authentication()

    def show_diaries(self, diaries=None):
        if not diaries:
            diaries = self.diarybook.diaries
        for diary in diaries:
            print(f"{diary.id}-{diary.memo}")

    def add_diary(self):
        memo = input("Enter a memo:         ")
        tags = input("add tags:             ")
        self.diarybook.new_diary(memo, tags)
        self.save_user_diaries()
        print("Your note has been added")

    def search_diaries(self):
        filter_text = input("Search for:  ")
        diaries = self.diarybook.search_diary(filter_text)
        for diary in diaries:
            print(f"{diary.id}-{diary.memo}")

    def quit(self):
        print("Thank you for using diarybook today")
        sys.exit(0)

    def save_user_diaries(self):
        if self.user:
            with open(f'{self.user}_diaries.json', 'w') as f:
                json.dump([diary.to_dict() for diary in self.diarybook.diaries], f)

    def load_user_diaries(self):
        try:
            with open(f'{self.user}_diaries.json', 'r') as f:
                file_content = f.read()
                if not file_content.strip():
                    return
                diaries_data = json.loads(file_content)
                self.diarybook.diaries = [Diary.from_dict(data) for data in diaries_data]
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

if __name__ == "__main__":
    Menu().run()
