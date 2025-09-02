from datetime import datetime
from typing import List, Dict
import re

def parse_whatsapp_chat(file_path: str) -> Dict:
    messages = []
    participants = set()
    dates = []

    pattern = re.compile(r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2} (?:AM|PM)) - (.*?): (.*)')

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                date_str, time_str, sender, message = match.groups()
                dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %I:%M %p")
                dates.append(dt)
                participants.add(sender)
                messages.append({'sender': sender, 'datetime': dt, 'message': message})

    total_messages = len(messages)
    num_participants = len(participants)
    first_msg = min(dates) if dates else None
    last_msg = max(dates) if dates else None

    return {
        'total_messages': total_messages,
        'num_participants': num_participants,
        'first_msg_date': first_msg,
        'last_msg_date': last_msg,
        'messages': messages
    }
