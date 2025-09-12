from comprehensive_beat_writers import get_all_writers_flat, get_writers_by_team
from datetime import datetime
import random

def get_beat_writer_injuries():
    """Monitor comprehensive list of NHL beat writers for injury reports (mock demo)."""
    all_writers = get_all_writers_flat()  # ready for real monitoring if you wire up Twitter/X

    # Injury keywords to monitor (single line to avoid Notepad wrap issues)
    injury_keywords = ['injured', 'injury', 'IR', 'LTIR', 'day-to-day', 'week-to-week', 'upper body', 'lower body', 'out', 'questionable', 'doubtful', 'maintenance day', 'load management', 'precautionary', 'surgery', 'placed on IR', 'activated from IR', 'recalled from', 'sent to AHL']

    # Sample reports from different types of writers
    sample_reports = [
        {'reporter': 'Elliotte Friedman', 'handle': '@FriedgeHNIC', 'outlet': 'Sportsnet', 'player': 'Connor McDavid', 'team': 'EDM', 'injury_type': 'Upper Body - Maintenance', 'report': 'McDavid taking a maintenance day, precautionary', 'confidence': 'High'},
        {'reporter': 'Michael Russo', 'handle': '@RussoHockey', 'outlet': 'The Athletic', 'player': 'Kirill Kaprizov', 'team': 'MIN', 'injury_type': 'Lower Body - Day to Day', 'report': 'Kaprizov tweaked something in practice, being evaluated', 'confidence': 'Medium'},
        {'reporter': 'Josh Yohe', 'handle': '@JoshYohe_PGH', 'outlet': 'The Athletic', 'player': 'Sidney Crosby', 'team': 'PIT', 'injury_type': 'Upper Body - Probable', 'report': 'Crosby participated in full practice, looks good to go', 'confidence': 'High'},
    ]

    mock_reports = []
    for report in sample_reports:
        mock_reports.append({
            'source': 'Beat Writer Report',
            'reporter': report['reporter'],
            'handle': report['handle'],
            'outlet': report['outlet'],
            'player': report['player'],
            'team': report['team'],
            'injury_type': report['injury_type'],
            'injury_date': datetime.now().strftime('%Y-%m-%d'),
            'report': report['report'],
            'confidence': report['confidence'],
            'tweet_time': datetime.now().strftime('%H:%M')
        })

    return mock_reports


def get_writer_database_stats():
    """Get statistics about the writer database."""
    all_writers = get_all_writers_flat()
    stats = {
        'total_writers': len(all_writers),
        'national_writers': len([w for w in all_writers if w['category'] == 'national']),
        'team_writers': len([w for w in all_writers if w['category'] != 'national']),
        'outlets': len(set(w['outlet'] for w in all_writers)),
        'teams_covered': len(set(w['category'] for w in all_writers if w['category'] != 'national')),
    }
    return stats
