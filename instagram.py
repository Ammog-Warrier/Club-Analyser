import instaloader
import time
from datetime import datetime
from typing import List
import requests
from getpass import getpass

def fetch_instagram_metrics(club_handle: str, max_posts: int = 50) -> dict:
    L = instaloader.Instaloader()
    # A few of these rate limiters were added by LLM because I was troubleshooting this wierd error :(
    # Configure instaloader for better rate limiting and timeout handling
    L.context.request_timeout = 60  # Increased timeout to 60 seconds
    L.context.sleep = True  # Enable automatic sleep between requests
    
    try:
        print(f"   📱 Session loaded successfully for @{club_handle}")
    except Exception as e:
        print(f"   ⚠️  Session loading issue: {e}")
        print("   🔑 Creating new session...")
        try:
            username = input("Enter Instagram username: ")
            password = getpass("Enter Instagram password: ")# THis was initially working with L.load_session_from_file("YOUR USER_NAME")
            L.login(username, password)
            print("   ✅ New session created and saved")
        except Exception as login_error:
            print(f"   ❌ Login failed: {login_error}")
            print("   ⚠️  Continuing with anonymous access (limited functionality)")
            # Continue without login - some public profiles may still work

    # Retry mechanism for profile fetching
    max_retries = 3
    retry_delay = 10
    
    for attempt in range(max_retries):
        try:
            print(f"   🔄 Attempt {attempt + 1}/{max_retries} to fetch profile @{club_handle}")
            profile = instaloader.Profile.from_username(L.context, club_handle) # THis is actually where the 401 break happens
            break
        except (requests.exceptions.ReadTimeout, requests.exceptions.Timeout) as e:
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"   ⏳ Timeout error, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            else:
                print(f"   ❌ Failed after {max_retries} attempts: {e}")
                return {}
        except Exception as e:
            print(f"   ❌ Profile fetch error: {e}")
            return {}
    
    try:
        likes_sum = 0
        comments_sum = 0
        post_dates: List[datetime] = []
        post_count = 0
        
        print(f"   📊 Fetching up to {max_posts} recent posts...")
        
        for post in profile.get_posts():
            if post_count >= max_posts:
                break
                
            likes_sum += post.likes
            comments_sum += post.comments
            post_dates.append(post.date_utc)
            post_count += 1
            
            # Rate limiting: sleep between each post fetch. This worked the very first time but then proceeded to not work 
            if post_count % 5 == 0:  # Every 5 posts
                print(f"   ⏳ Processed {post_count} posts, rate limiting...")
                time.sleep(12)  # Increased delay to 12 seconds every 5 posts
            else:
                time.sleep(3)  # Increased delay to 3 seconds between individual posts
            
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
        print(f"   ❌ Error: Profile '{club_handle}' does not exist.")
        return {}
    except instaloader.exceptions.LoginRequiredException:
        print(f"   ❌ Login required for '{club_handle}'. Session may be expired.")
        return {}
    except instaloader.exceptions.TooManyRequestsException:
        print(f"   ❌ Rate limited for '{club_handle}'. Try again later.")
        return {}
    except instaloader.exceptions.ConnectionException as e:
        print(f"   ❌ Connection error for '{club_handle}': {e}")
        return {}
    except Exception as e:
        print(f"   ❌ Unexpected error for '{club_handle}': {e}")
        return {}
