import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.text import Text
from rich.align import Align
from rich import box

from club import Club
from instagram import fetch_instagram_metrics
from whatsapp import parse_whatsapp_chat
from grouping import group_clubs_by_category
from metrics import (
    compute_composite_score, 
    cluster_posts_into_events, 
    compute_final_score_with_events,
    normalize_scores
)
from typing import List, Dict
from visualizer import show_visualizations, save_visualizations, print_terminal_summary

def main():
    console = Console()
    
    # Create welcome panel
    welcome_text = Text("🏛️  Club Analyser", style="bold magenta")
    welcome_panel = Panel(
        Align.center(welcome_text),
        title="[bold blue]Starting Analysis[/bold blue]",
        border_style="bright_blue",
        box=box.ROUNDED
    )
    console.print(welcome_panel)
    console.print()
    
    clubs = [
        Club(
            name="Coding Club ", 
            insta_handle="snuc_cc",  
            whatsapp_file="/home/ammog/Desktop/testData/WhatsApp Chat with SNUCCC Discussions.txt", 
            category="Tech"  
        ),
        Club(
            name="Music Club",
            insta_handle="snuc_isai",
            whatsapp_file="/home/ammog/Desktop/testData/WhatsApp Chat with 🎶ISAI'24🎶.txt",
            category="Entertainment"
        ),
        Club(
            name="QUiz Club",
            insta_handle="snuc_cognitionquiz",
            whatsapp_file="/home/ammog/Desktop/testData/WhatsApp Chat with Cognition - The SNUC Quiz Club.txt",
            category="Entertainment"
        ),
        Club(
            name="Dance Club",
            insta_handle="snuc_rhythm",
            whatsapp_file="/home/ammog/Desktop/testData/WhatsApp Chat with Rhythm - SNU.txt",
            category="Entertainment"
        )
        
    ]
    
    console.print(f"[green]📋 Created {len(clubs)} club objects[/green]")
    console.print()
    
    # Start of the club computations is over here 
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Processing clubs...", total=len(clubs))
        
        for i, club in enumerate(clubs, 1):
            progress.update(task, description=f"[cyan]Processing {club.name}...")
            
            club_panel = Panel(
                f"[bold yellow]Club {i}: {club.name}[/bold yellow]\n[dim]Category: {club.category}[/dim]",
                border_style="yellow",
                box=box.SIMPLE
            )
            console.print(club_panel)
        
            console.print(f"[blue]📱 Fetching Instagram metrics for @{club.insta_handle}[/blue]")
            try:
                insta_metrics = fetch_instagram_metrics(club.insta_handle)
                if insta_metrics:
                    club.update_instagram_metrics(insta_metrics)
                    console.print(f"   [green]✅ Instagram: {club.num_posts} posts, {club.followers:,} followers[/green]")
                    
                else:
                    console.print(f"   [red]❌ Failed to fetch Instagram metrics for @{club.insta_handle}[/red]")
            except Exception as e:
                console.print(f"   [red]❌ Instagram error: {e}[/red]")
            time.sleep(15)
            
            console.print(f"[purple]💬 Parsing WhatsApp chat[/purple]")
            try:
                whatsapp_metrics = parse_whatsapp_chat(club.whatsapp_file)
                if whatsapp_metrics:
                    club.update_whatsapp_metrics(whatsapp_metrics)
                    console.print(f"   [green]✅ WhatsApp: {club.total_messages:,} messages, {club.num_participants} participants[/green]")
                else:
                    console.print(f"   [red]❌ Failed to parse WhatsApp chat[/red]")
            except Exception as e:
                console.print(f"   [red]❌ WhatsApp error: {e}[/red]")
        
            console.print(f"[orange3]📊 Computing metrics and scores...[/orange3]")
            try:
                club_metrics = {
                    'num_posts': club.num_posts,
                    'likes_sum': club.likes_sum,
                    'comments_sum': club.comments_sum,
                    'followers': club.followers,
                    'total_messages': club.total_messages,
                    'num_participants': club.num_participants,
                    'post_dates': club.post_dates
                }
                
                events = cluster_posts_into_events(club.post_dates)
                club.events = events
                
                club.composite_score = compute_final_score_with_events(club_metrics, events)
                
                console.print(f"   [green]✅ Score: {club.composite_score:.2f}, Events: {len(events)}[/green]")
                
            except Exception as e:
                console.print(f"   [red]❌ Metrics computation error: {e}[/red]")
            
            progress.advance(task)
            console.print()
    
    console.print(f"[cyan]🎯 Normalizing scores across all clubs...[/cyan]")
    all_scores = [club.composite_score for club in clubs]
    normalized_scores = normalize_scores(all_scores)
    
    for club, norm_score in zip(clubs, normalized_scores):
        club.normalized_score = norm_score
    
    clubs_sorted = sorted(clubs, key=lambda c: c.normalized_score, reverse=True)
    
    console.print(f"[cyan]📂 Grouping clubs by category...[/cyan]")
    grouped_clubs = group_clubs_by_category(clubs)
    console.print()
    
    # Our Ranking Table
    rankings_table = Table(
        title="🏆 FINAL RANKINGS",
        title_style="bold gold1",
        border_style="bright_blue",
        box=box.ROUNDED
    )
    
    rankings_table.add_column("Rank", style="bold cyan", justify="center")
    rankings_table.add_column("Club Name", style="bold white")
    rankings_table.add_column("Category", style="dim")
    rankings_table.add_column("Score", style="bold green", justify="right")
    rankings_table.add_column("Posts", style="blue", justify="right")
    rankings_table.add_column("Followers", style="magenta", justify="right")
    rankings_table.add_column("Messages", style="yellow", justify="right")
    rankings_table.add_column("Events", style="red", justify="right")
    
    for rank, club in enumerate(clubs_sorted, 1):
        rank_emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🏅"
        rankings_table.add_row(
            f"{rank_emoji} {rank}",
            club.name,
            club.category,
            f"{club.normalized_score:.3f}",
            str(club.num_posts),
            f"{club.followers:,}",
            f"{club.total_messages:,}",
            str(len(club.events))
        )
    
    console.print(rankings_table)
    console.print()
    
    # Create our category table
    category_table = Table(
        title="📂 CLUBS BY CATEGORY",
        title_style="bold bright_cyan",
        border_style="bright_green",
        box=box.ROUNDED
    )
    # Most of the styles are from rich documentation
    category_table.add_column("Category", style="bold bright_yellow")
    category_table.add_column("Club Count", style="cyan", justify="center")
    category_table.add_column("Clubs", style="white")
    category_table.add_column("Avg Score", style="green", justify="right")
    
    for category, category_clubs in grouped_clubs.items():
        club_list = ", ".join([f"{club.name} ({club.normalized_score:.3f})" for club in category_clubs])
        avg_score = sum(c.normalized_score for c in category_clubs) / len(category_clubs)
        
        category_table.add_row(
            f"🏷️ {category.upper()}",
            str(len(category_clubs)),
            club_list,
            f"{avg_score:.3f}"
        )
    
    console.print(category_table)
    console.print()
    
    # Create completion panel
    completion_text = Text("✨ Analysis Complete!", style="bold bright_green")
    stats_text = f"📈 Processed {len(clubs)} clubs across {len(grouped_clubs)} categories"
    
    completion_panel = Panel(
        Align.center(f"{completion_text}\n\n{stats_text}"),
        title="[bold green]Summary[/bold green]",
        border_style="bright_green",
        box=box.DOUBLE
    )
    console.print(completion_panel)
    
    console.print(f"[cyan]📊 Generating visualizations...[/cyan]")
    print_terminal_summary(clubs_sorted, console)
    
    save_visualizations(clubs_sorted, "club_analysis_charts.png", console)
    
    
    return clubs_sorted, grouped_clubs

if __name__ == "__main__":
    ranked_clubs, categorized_clubs = main()
