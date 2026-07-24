from datetime import datetime

class List:
    time_now = datetime.now().date()

    def __init__(self, title, descriptions, time = time_now):
        self.title = title
        self.descriptions = descriptions 
        self.time = time
        
