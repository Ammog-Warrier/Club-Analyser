import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
from club import Club
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

def create_club_visualizations(clubs: List[Club]):
    """Create comprehensive visualizations for club analysis"""
    
    #We start by setting up the matplotlib method of analysing and setting up functionsa fucntion for our matplotlib here
        plt.style.use('default')
    fig = plt.figure(figsize=(16, 12))
    
    # ExtractOver here I'm extracting data for plotting
    club_names = [club.name for club in clubs]
    scores = [club.normalized_score for club in clubs]
    followers = [club.followers for club in clubs]
    posts = [club.num_posts for club in clubs]
    likes = [club.likes_sum for club in clubs]
    comments = [club.comments_sum for club in clubs]
    messages = [club.total_messages for club in clubs]
    participants = [club.num_participants for club in clubs]
    
    # 1. Club Score Comparison (Bar Chart)
    plt.subplot(2, 3, 1)
    bars = plt.bar(range(len(club_names)), scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    plt.title('Club Normalized Scores Comparison', fontweight='bold')
    plt.xlabel('Clubs')
    plt.ylabel('Normalized Score')
    plt.xticks(range(len(club_names)), [name[:10] + '...' if len(name) > 10 else name for name in club_names], rotation=45)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{scores[i]:.3f}', ha='center', va='bottom', fontsize=9)
    
    # 2. Instagram Metrics (Scatter Plot)[ I kinda added that for variety ]
    plt.subplot(2, 3, 2)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    for i, (club, color) in enumerate(zip(clubs, colors)):
        plt.scatter(club.followers, club.likes_sum, s=club.num_posts*3, 
                   color=color, alpha=0.7, label=club.name[:10])
    plt.title('Instagram Engagement vs Followers', fontweight='bold')
    plt.xlabel('Followers')
    plt.ylabel('Total Likes')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 3. WhatsApp Activity (Horizontal Bar Chart)
    plt.subplot(2, 3, 3)
    y_pos = np.arange(len(club_names))
    plt.barh(y_pos, messages, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    plt.title('WhatsApp Messages Count', fontweight='bold')
    plt.xlabel('Total Messages')
    plt.ylabel('Clubs')
    plt.yticks(y_pos, [name[:12] for name in club_names])
    
    # Add value labels
    for i, v in enumerate(messages):
        plt.text(v + max(messages)*0.01, i, str(v), va='center', fontsize=9)
    
    # 4. Multi-metric Radar Chart
    plt.subplot(2, 3, 4)
    # Normalize metrics for radar chart
    max_followers = max(followers) if max(followers) > 0 else 1
    max_likes = max(likes) if max(likes) > 0 else 1
    max_posts = max(posts) if max(posts) > 0 else 1
    max_messages = max(messages) if max(messages) > 0 else 1
    
    angles = np.linspace(0, 2*np.pi, 4, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    for i, club in enumerate(clubs):
        values = [
            club.followers / max_followers,
            club.likes_sum / max_likes,
            club.num_posts / max_posts,
            club.total_messages / max_messages
        ]
        values += values[:1]  # Complete the circle
        
        plt.plot(angles, values, 'o-', linewidth=2, label=club.name[:10], 
                color=colors[i % len(colors)])
        plt.fill(angles, values, alpha=0.25, color=colors[i % len(colors)])
    
    plt.title('Multi-Metric Performance', fontweight='bold')
    labels = ['Followers', 'Likes', 'Posts', 'Messages']
    plt.xticks(angles[:-1], labels)
    plt.ylim(0, 1)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 5. Engagement Rate Comparison(our overall score)
    plt.subplot(2, 3, 5)
    engagement_rates = []
    for club in clubs:
        if club.followers > 0:
            engagement_rate = (club.likes_sum + club.comments_sum) / club.followers * 100
        else:
            engagement_rate = 0
        engagement_rates.append(engagement_rate)
    
    bars = plt.bar(range(len(club_names)), engagement_rates, 
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    plt.title('Instagram Engagement Rate (%)', fontweight='bold')
    plt.xlabel('Clubs')
    plt.ylabel('Engagement Rate (%)')
    plt.xticks(range(len(club_names)), [name[:10] for name in club_names], rotation=45)
    
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + max(engagement_rates)*0.01,
                f'{engagement_rates[i]:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # 6. Category Distribution (Pie Chart) so that we can see how they were grouped into various categoies via a Pie chart
    plt.subplot(2, 3, 6)
    categories = {}
    for club in clubs:
        categories[club.category] = categories.get(club.category, 0) + 1
    
    plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%',
            colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    plt.title('Clubs by Category', fontweight='bold')
    
    plt.tight_layout()
    return fig

def print_terminal_summary(clubs: List[Club], console: Optional[Console] = None):
    """Print a clean terminal summary of club rankings using Rich"""
    if console is None:
        console = Console()
    
    # Sort clubs by normalized score
    sorted_clubs = sorted(clubs, key=lambda c: c.normalized_score, reverse=True)
    
    # Create summary header
    summary_title = Text("📊 CLUB ANALYSIS SUMMARY", style="bold bright_cyan")
    summary_panel = Panel(
        Align.center(summary_title),
        title="[bold blue]Detailed Summary[/bold blue]",
        border_style="bright_cyan",
        box=box.DOUBLE
    )
    console.print(summary_panel)
    console.print()
    
    # Create detailed rankings table with our installed rich
    detailed_table = Table(
        title="🏆 DETAILED RANKINGS",
        title_style="bold gold1",
        border_style="bright_blue",
        box=box.ROUNDED,
        show_lines=True
    )
    
    detailed_table.add_column("Rank", style="bold cyan", justify="center")
    detailed_table.add_column("Club Name", style="bold white")
    detailed_table.add_column("Score", style="bold green", justify="right")
    detailed_table.add_column("Instagram", style="blue")
    detailed_table.add_column("WhatsApp", style="purple")
    detailed_table.add_column("Engagement", style="yellow", justify="right")
    
    for i, club in enumerate(sorted_clubs, 1):
        engagement_rate = ((club.likes_sum + club.comments_sum) / club.followers * 100) if club.followers > 0 else 0
        rank_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
        
        detailed_table.add_row(
            f"{rank_emoji} {i}",
            club.name,
            f"{club.normalized_score:.3f}",
            f"{club.followers:,} followers\n{club.num_posts} posts",
            f"{club.total_messages:,} messages\n{club.num_participants} participants",
            f"{engagement_rate:.1f}%"
        )
    
    console.print(detailed_table)
    console.print()
    
    # Category breakdown
    categories = {}
    for club in clubs:
        if club.category not in categories:
            categories[club.category] = []
        categories[club.category].append(club)
    
    category_summary_table = Table(
        title="📂 CATEGORY BREAKDOWN",
        title_style="bold bright_green",
        border_style="bright_green",
        box=box.ROUNDED
    )
    
    category_summary_table.add_column("Category", style="bold bright_yellow")
    category_summary_table.add_column("Club Count", style="cyan", justify="center")
    category_summary_table.add_column("Average Score", style="green", justify="right")
    category_summary_table.add_column("Top Club", style="white")
    
    for category, category_clubs in categories.items():
        avg_score = sum(c.normalized_score for c in category_clubs) / len(category_clubs)
        top_club = max(category_clubs, key=lambda c: c.normalized_score)
        
        category_summary_table.add_row(
            f"🏷️ {category.upper()}",
            str(len(category_clubs)),
            f"{avg_score:.3f}",
            f"{top_club.name} ({top_club.normalized_score:.3f})"
        )
    
    console.print(category_summary_table)
# for adding and sending thesevisualisation straight in a PNG format within our folder
def save_visualizations(clubs: List[Club], filename: str = "club_analysis.png", console: Optional[Console] = None):
    """Save visualizations to file"""
    if console is None:
        console = Console()
        
    fig = create_club_visualizations(clubs)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    # Create a panel for the save confirmation
    save_panel = Panel(
        f"[green]📊 Visualizations saved to: [bold]{filename}[/bold][/green]",
        title="[bold blue]File Saved[/bold blue]",
        border_style="green",
        box=box.SIMPLE
    )
    console.print(save_panel)
    return filename

def show_visualizations(clubs: List[Club], console: Optional[Console] = None):
    """Display visualizations and terminal summary"""
    if console is None:
        console = Console()
        
    # Create and show plots
    fig = create_club_visualizations(clubs)
    plt.show()
    
    print_terminal_summary(clubs, console)
