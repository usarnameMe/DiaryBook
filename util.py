import json
from diarybook import Diary

def read_from_json_into_application(path):
    with open(path) as file:
        data = json.loads(file.read())
    diaries = [Diary(entry['memo'], entry['tags']) for entry in data]
    return diaries
