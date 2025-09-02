import instaloader
from datetime import datetime
from typing import List

def fetch_instagram_metrics(club_handle: str) -> dict:
    L = instaloader.Instaloader()
    L.load_session_from_file("amg1.24567") 

    try:
        profile = instaloader.Profile.from_username(L.context, club_handle)
        likes_sum = 0
        comments_sum = 0
        post_dates: List[datetime] = []
        
        for post in profile.get_posts():
            likes_sum += post.likes
            comments_sum += post.comments
            post_dates.append(post.date_utc)
            
        followers = profile.followers
        num_posts = profile.mediacount
            
        return {
            'num_posts': num_posts,
            'likes_sum': likes_sum,
            'comments_sum': comments_sum,
            'followers': followers,
            'post_dates': post_dates
        }

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: Profile '{club_handle}' does not exist.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}