from typing import List
from datetime import datetime

class Club:
    def __init__(self, name: str, insta_handle: str, whatsapp_file: str, category: str = "uncategorized"):
        self.name = name
        self.insta_handle = insta_handle
        self.whatsapp_file = whatsapp_file
        self.category = category

        # This will be the initial placeholders for our metrics
        self.num_posts = 0
        self.likes_sum = 0
        self.comments_sum = 0
        self.followers = 0
        self.post_dates: List[datetime] = []

        self.total_messages = 0
        self.num_participants = 0
        self.first_msg_date = None
        self.last_msg_date = None
        self.events: List[dict] = [] 

        self.composite_score = 0  #The final score which   will be calculated later based on which rankings can be determined
        self.normalized_score = 0.0  # Normalized score for fair comparison across clubs

    def update_instagram_metrics(self, insta_metrics: dict):
        self.num_posts = insta_metrics.get("num_posts", 0)
        self.likes_sum = insta_metrics.get("likes_sum", 0)
        self.comments_sum = insta_metrics.get("comments_sum", 0)
        self.followers = insta_metrics.get("followers", 0)
        self.post_dates = insta_metrics.get("post_dates", [])

    def update_whatsapp_metrics(self, whatsapp_metrics: dict):
        self.total_messages = whatsapp_metrics.get("total_messages", 0)
        self.num_participants = whatsapp_metrics.get("num_participants", 0)
        self.first_msg_date = whatsapp_metrics.get("first_msg_date")
        self.last_msg_date = whatsapp_metrics.get("last_msg_date")
