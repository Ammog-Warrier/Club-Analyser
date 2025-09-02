# 🏛️ Club Analyser

A comprehensive Python tool for analyzing and ranking student clubs based on their Instagram engagement and WhatsApp activity metrics. Features beautiful Rich-formatted output with progress tracking, detailed tables, and visual charts.

## 📋 Overview

Club Analyser evaluates student clubs using multiple data sources:
- **Instagram metrics**: Posts, likes, comments, followers
- **WhatsApp activity**: Message count, participant engagement
- **Event clustering**: Automatic detection of club events from posting patterns
- **Composite scoring**: Weighted algorithm combining all metrics

## ✨ Features

### 🎨 Rich Terminal Interface
- **Colorful output** with status indicators
- **Progress bars** with real-time updates
- **Beautiful tables** for rankings and metrics
- **Styled panels** and borders
- **Medal emojis** for top performers (🥇🥈🥉)

### 📊 Analytics & Scoring
- **Composite scoring algorithm** with configurable weights
- **Event detection** from Instagram posting patterns
- **Normalized rankings** for fair comparison
- **Category-based grouping** and analysis
- **Engagement rate calculations**

### 📈 Visualizations
- **Multiple chart types**: Bar charts, scatter plots, radar charts
- **High-resolution exports** (PNG format)
- **Interactive matplotlib displays**
- **Category distribution analysis**

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Instagram account cookies (for authentication)
- WhatsApp chat export files

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/club-analyser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Setup

1. **Configure club data** in `main.py`:
   ```python
   clubs = [
       Club(
           name="Your Club Name",
           insta_handle="instagram_handle",
           whatsapp_file="/path/to/whatsapp_export.txt",
           category="Tech"  # or "Entertainment", etc.
       ),
       # Add more clubs...
   ]
   ```

2. **Export WhatsApp chats**:
   - Open WhatsApp group
   - Go to Group Info → Export Chat → Without Media
   - Save as `.txt` file

3. **Instagram Authentication**:
   - The tool uses `instaloader` with browser cookies
   - For Linux systems, extract cookies from browser DevTools:
     - `sessionid`
     - `csrftoken` 
     - `ds_user_id`

## 🎯 Usage

### Basic Execution
```bash
python main.py
```

### Expected Output
The tool will display:
1. **Welcome panel** with project title
2. **Progress bar** showing club processing status
3. **Real-time status** for each club's data fetching
4. **Rankings table** with comprehensive metrics
5. **Category breakdown** with statistics
6. **Detailed summary** with engagement rates
7. **Visualization export** confirmation

### Sample Output Structure
```
🏛️ Club Analyser
┌─ Starting Analysis ─┐
│   Club Analyser     │
└─────────────────────┘

📋 Created 4 club objects

Processing clubs... ████████████████████ 100% 0:02:15

🏆 FINAL RANKINGS
┌──────┬─────────────┬─────────────┬───────┬───────┬───────────┬──────────┬────────┐
│ Rank │ Club Name   │ Category    │ Score │ Posts │ Followers │ Messages │ Events │
├──────┼─────────────┼─────────────┼───────┼───────┼───────────┼──────────┼────────┤
│ 🥇 1 │ Coding Club │ Tech        │ 0.892 │   25  │   1,500   │   8,500  │   3    │
│ 🥈 2 │ Music Club  │ Entertainment│ 0.745 │   18  │   1,200   │   6,200  │   2    │
└──────┴─────────────┴─────────────┴───────┴───────┴───────────┴──────────┴────────┘
```

## 📁 Project Structure

```
club-analyser/
├── main.py              # Main execution script
├── club.py              # Club data model
├── instagram.py         # Instagram data fetching
├── whatsapp.py          # WhatsApp chat parsing
├── metrics.py           # Scoring algorithms
├── visualizer.py        # Charts and Rich output
├── grouping.py          # Category management
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration

### Scoring Weights
Modify weights in `metrics.py`:
```python
DEFAULT_WEIGHTS = {
    'avg_likes_per_post': 0.3,
    'avg_comments_per_post': 0.2,
    'followers_per_post': 0.3,
    'avg_messages_per_participant': 0.2,
    'posting_frequency': 0.1
}
```

### Event Detection
Adjust clustering parameters:
```python
# In metrics.py
def cluster_posts_into_events(post_dates, max_gap_days=14):
    # max_gap_days: Maximum days between posts in same event
```

### Visual Styling
Customize Rich output in `main.py` and `visualizer.py`:
- Colors: `[red]`, `[green]`, `[blue]`, `[yellow]`, etc.
- Styles: `bold`, `dim`, `italic`
- Borders: `box.ROUNDED`, `box.DOUBLE`, `box.SIMPLE`

## 📊 Dependencies

```
certifi==2025.8.3
charset-normalizer==3.4.3
idna==3.10
instaloader==4.14.2
markdown-it-py==4.0.0
matplotlib==3.9.2
mdurl==0.1.2
numpy==2.1.1
Pygments==2.19.2
requests==2.32.5
rich==14.1.0
urllib3==2.5.0
```

## 🔍 Troubleshooting

### Instagram Authentication Issues
- **401 Errors**: Use browser cookie authentication instead of username/password
- **Rate Limiting**: Add delays between requests (currently 15 seconds)
- **Regional Blocking**: Use VPN or browser cookies from working session

### WhatsApp Parsing Issues
- **File Format**: Ensure exported as plain text (.txt)
- **Encoding**: Use UTF-8 encoding for international characters
- **File Path**: Use absolute paths for WhatsApp files

### Missing Data
- **Empty Metrics**: Check file paths and authentication
- **Zero Scores**: Verify data is being fetched correctly
- **Missing Visualizations**: Ensure matplotlib backend is properly configured

## 🎨 Rich Features

### Progress Tracking
- **Spinner animations** during processing
- **Progress bars** with percentage completion
- **Time elapsed** tracking
- **Task descriptions** with current club being processed

### Table Formatting
- **Colored columns** for different data types
- **Right-aligned numbers** for better readability
- **Medal emojis** for rankings
- **Formatted numbers** with thousand separators

### Panel Styling
- **Welcome panels** with centered text
- **Status panels** for different operations
- **Completion summaries** with statistics
- **File save confirmations**

## 🚀 Advanced Usage

### Custom Categories
Add new categories by modifying club definitions:
```python
Club(name="Art Club", category="Creative", ...)
```

### Batch Processing
Process multiple club sets by creating separate club lists:
```python
tech_clubs = [...]
entertainment_clubs = [...]
# Process separately or combine
```

### Export Options
- **PNG Charts**: High-resolution visualization exports
- **Rich Console**: Beautiful terminal output
- **Data Export**: Extend to save CSV/JSON results

## 📝 Contributing

1. Fork the repository
2. Create feature branch
3. Add Rich formatting for new features
4. Test with sample data
5. Submit pull request

## 📄 License

This project is open source. Feel free to modify and distribute.

## 🙏 Acknowledgments

- **Rich Library**: For beautiful terminal output
- **Instaloader**: For Instagram data fetching
- **Matplotlib**: For chart generation
- **NumPy**: For numerical computations

---


