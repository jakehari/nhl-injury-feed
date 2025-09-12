import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_hockey_reference_injuries():
    url = "https://www.hockey-reference.com/friv/injuries.cgi"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        injury_table = soup.find('table', {'id': 'injuries'})

        if not injury_table:
            return [{
                'player': 'No injury table found',
                'team': 'N/A',
                'injury_type': 'Website structure changed',
                'injury_date': ''
            }]

        injuries = []
        tbody = injury_table.find('tbody')

        if tbody:
            rows = tbody.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 4:
                    player = cells[0].get_text().strip()
                    team = cells[1].get_text().strip()
                    injury_type = cells[2].get_text().strip()
                    injury_date = cells[3].get_text().strip()

                    if player and team:
                        injuries.append({
                            'player': player,
                            'team': team,
                            'injury_type': injury_type,
                            'injury_date': injury_date
                        })

        if not injuries:
            return [{
                'player': 'No Current Injuries',
                'team': 'NHL',
                'injury_type': 'Clean bill of health',
                'injury_date': datetime.now().strftime('%Y-%m-%d')
            }]

        return injuries[:50]

    except Exception as e:
        return [{
            'player': 'Error',
            'team': 'SYS',
            'injury_type': f'Scraping failed: {str(e)}',
            'injury_date': ''
        }]



    