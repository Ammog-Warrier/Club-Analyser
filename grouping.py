from typing import List, Dict
from club import Club

def group_clubs_by_category(clubs: List[Club]) -> Dict[str, List[Club]]:
    groups: Dict[str, List[Club]] = {}
    for club in clubs:
        cat = club.category or "uncategorized" # based on the initial category
        if cat not in groups:
            groups[cat] = []
        groups[cat].append(club)
    return groups