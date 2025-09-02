from typing import List, Dict, Any
from datetime import datetime, timedelta
import math

ClubMetrics = Dict[str, Any]

DEFAULT_WEIGHTS = {
    'avg_likes_per_post': 0.3,
    'avg_comments_per_post': 0.2,
    'followers_per_post': 0.3,
    'avg_messages_per_participant': 0.2,
    'posting_frequency': 0.1  
}

def compute_posting_frequency(post_dates: List[datetime]) -> float:
    if not post_dates or len(post_dates) == 1:
        return 0.0
    
    sorted_dates = sorted(post_dates)
    duration_days = (sorted_dates[-1] - sorted_dates[0]).days
    num_posts = len(post_dates)
    
    return 1 / (1 + duration_days / num_posts) if num_posts > 0 else 0.0

def compute_composite_score(
    club_metrics: ClubMetrics,
    weights: Dict[str, float] = None
) -> float:
    if weights is None:
        weights = DEFAULT_WEIGHTS

    insta_engagement = (
        math.log1p(club_metrics.get('likes_sum', 0) / max(club_metrics.get('num_posts', 1), 1)) * weights['avg_likes_per_post'] +
        math.log1p(club_metrics.get('comments_sum', 0) / max(club_metrics.get('num_posts', 1), 1)) * weights['avg_comments_per_post'] +
        math.log1p(club_metrics.get('followers', 0)) * weights['followers_per_post']
    )
    
    whatsapp_activity = math.log1p(club_metrics.get('total_messages', 0) / max(club_metrics.get('num_participants', 1), 1)) * weights['avg_messages_per_participant']

    frequency_score = compute_posting_frequency(club_metrics.get('post_dates', [])) * weights.get('posting_frequency', 0.1)

    score = insta_engagement + whatsapp_activity + frequency_score
    return score

def cluster_posts_into_events(post_dates: List[datetime], max_gap_days: int = 14) -> List[Dict]:
    if not post_dates:
        return []
        
    sorted_dates = sorted(post_dates)
    
    events = []
    current_event_start = sorted_dates[0]
    current_event_posts = 1

    for i in range(1, len(sorted_dates)):
        time_diff = sorted_dates[i] - sorted_dates[i-1]
        
        if time_diff.days <= max_gap_days:
            current_event_posts += 1
        else:
            events.append({
                'start_date': current_event_start,
                'end_date': sorted_dates[i-1],
                'num_posts': current_event_posts
            })
            current_event_start = sorted_dates[i]
            current_event_posts = 1
    
    events.append({
        'start_date': current_event_start,
        'end_date': sorted_dates[-1],
        'num_posts': current_event_posts
    })
    
    return events

def compute_final_score_with_events(club_metrics: ClubMetrics, events: List[Dict]) -> float:
    base_score = compute_composite_score(club_metrics)
    
    event_bonus = 0
    if events:
        num_events = len(events)
        total_posts_in_events = sum(e['num_posts'] for e in events)
        avg_posts_per_event = total_posts_in_events / num_events
        
        event_bonus = math.log1p(num_events) + math.log1p(avg_posts_per_event)
        
    return base_score + event_bonus

def normalize_scores(scores: List[float]) -> List[float]:
    if not scores:
        return []
    
    min_score = min(scores)
    max_score = max(scores)
    
    if min_score == max_score:
        return [0.0] * len(scores)
    
    normalized_scores = [
        (score - min_score) / (max_score - min_score)
        for score in scores
    ]
    
    return normalized_scores

if __name__ == '__main__':
    print("--- Example Usage of metrics.py ---") # for testing purposes

    club_a_metrics = {
        'num_posts': 25,
        'likes_sum': 25000,
        'comments_sum': 1200,
        'followers': 1500,
        'total_messages': 8500,
        'num_participants': 45,
        'post_dates': [
            datetime(2025, 8, 1),
            datetime(2025, 8, 3),
            datetime(2025, 8, 5),
            datetime(2025, 8, 20),
            datetime(2025, 8, 22),
            datetime(2025, 8, 25)
        ]
    }
    
    club_b_metrics = {
        'num_posts': 10,
        'likes_sum': 8000,
        'comments_sum': 400,
        'followers': 500,
        'total_messages': 12000,
        'num_participants': 200,
        'post_dates': [
            datetime(2025, 7, 10),
            datetime(2025, 7, 12),
            datetime(2025, 7, 14),
            datetime(2025, 7, 16),
        ]
    }
    
    score_a = compute_composite_score(club_a_metrics)
    score_b = compute_composite_score(club_b_metrics)
    
    print(f"\nComposite Score for Club A: {score_a:.2f}")
    print(f"Composite Score for Club B: {score_b:.2f}")
    
    events_a = cluster_posts_into_events(club_a_metrics['post_dates'])
    events_b = cluster_posts_into_events(club_b_metrics['post_dates'])
    
    print("\nEvents for Club A:")
    for event in events_a:
        print(f"  - Start: {event['start_date'].date()}, End: {event['end_date'].date()}, Posts: {event['num_posts']}")
    
    print("\nEvents for Club B:")
    for event in events_b:
        print(f"  - Start: {event['start_date'].date()}, End: {event['end_date'].date()}, Posts: {event['num_posts']}")
        
    final_score_a = compute_final_score_with_events(club_a_metrics, events_a)
    final_score_b = compute_final_score_with_events(club_b_metrics, events_b)
    
    print(f"\nFinal Score with Event Bonus for Club A: {final_score_a:.2f}")
    print(f"Final Score with Event Bonus for Club B: {final_score_b:.2f}")
    
    all_scores = [final_score_a, final_score_b]
    normalized_scores = normalize_scores(all_scores)
    
    print(f"\nNormalized scores for Club A and B: {normalized_scores}")
