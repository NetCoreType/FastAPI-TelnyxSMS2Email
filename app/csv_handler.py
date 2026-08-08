import csv
from pathlib import Path
from datetime import datetime

PATH = "../data/message_log/"
EMAIL_LIST_PATH = "../data/email_list"


class CSVHandler:
    def __init__(self) -> None:
        self.check_path()
        self.check_for_email_list_file()
        self.email_dict = self.load_csv_to_dict()

    def check_path(self):
            path = Path(PATH)
            if not path.is_dir():
                path.mkdir(parents=True)
    
    def check_for_email_list_file(self):
        path = Path(EMAIL_LIST_PATH)
        if not path.is_file():
            with open(EMAIL_LIST_PATH, "w") as file:
                file.write("phone_number,email_address")
    
    def load_csv_to_dict(self):
        dict = {}
        with open(EMAIL_LIST_PATH, "r") as email_file:
            data = csv.DictReader(email_file)
            for row in data:
                key = row.pop("phone_number")
                dict[key] = row
        return dict

    def match_phone_number(self, to_phone_number: str):
        if to_phone_number in self.email_dict:
            email_address = self.email_dict[to_phone_number]["email_address"]
            if "@" in email_address:
                return email_address
            else: 
                return 0
        else:
            return 0

    def record_message_to_file(self, from_address, to_address, message_text, message_occured_time):
        message_time = datetime.fromisoformat(message_occured_time)
        with open(f"{PATH}{message_time.strftime("%Y-%m-%d_%H-%M-%S")}", "w") as file:
            file.write(f"FROM: {from_address}\nTO: {to_address}\n{message_text}")

    