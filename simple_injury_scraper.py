  #!/usr/bin/env python3
  """
  Simple NHL Injury Scraper
  Gets current injury data from Hockey Reference
  """

  import requests
  from bs4 import BeautifulSoup
  from datetime import datetime
  import json

  def scrape_hockey_reference_injuries():
      """Scrape current injuries from Hockey Reference"""
      url = "https://www.hockey-reference.com/friv/injuries.cgi"

      try:
          headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)
  AppleWebKit/537.36'
          }
          response = requests.get(url, headers=headers, timeout=10)
          response.raise_for_status()

          soup = BeautifulSoup(response.content, 'html.parser')

          # Find the injury table
          injury_table = soup.find('table', {'id': 'injuries'})

          if not injury_table:
              print("Could not find injury table")
              return []

          injuries = []
          rows = injury_table.find('tbody').find_all('tr')

          for row in rows:
              cells = row.find_all(['th', 'td'])
              if len(cells) >= 4:
                  player_cell = cells[0]
                  team_cell = cells[1] if len(cells) > 1 else None
                  injury_cell = cells[2] if len(cells) > 2 else None
                  date_cell = cells[3] if len(cells) > 3 else None

                  player_name = player_cell.get_text().strip() if player_cell else ""
                  team = team_cell.get_text().strip() if team_cell else ""
                  injury_type = injury_cell.get_text().strip() if injury_cell else ""
                  injury_date = date_cell.get_text().strip() if date_cell else ""

                  if player_name and team:
                      injuries.append({
                          'player': player_name,
                          'team': team,
                          'injury_type': injury_type,
                          'injury_date': injury_date,
                          'source': 'Hockey Reference',
                          'scraped_at': datetime.now().isoformat()
                      })

          return injuries

      except Exception as e:
          print(f"Error scraping Hockey Reference: {e}")
          return []

  def format_injury_report(injuries):
      """Format injuries into readable report"""
      if not injuries:
          return "No current injuries found"

      report = []
      report.append("🏒 CURRENT NHL INJURIES")
      report.append("=" * 40)
      report.append(f"📅 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
      report.append(f"📊 Total Injured Players: {len(injuries)}")
      report.append("")

      # Group by team
      by_team = {}
      for injury in injuries:
          team = injury['team']
          if team not in by_team:
              by_team[team] = []
          by_team[team].append(injury)

      for team, team_injuries in sorted(by_team.items()):
          report.append(f"🔸 {team}:")
          for injury in team_injuries:
              report.append(f"  • {injury['player']}: {injury['injury_type']}")
              if injury['injury_date']:
                  report.append(f"    📅 {injury['injury_date']}")
          report.append("")

      report.append("📊 Source: Hockey-Reference.com")
      return "\n".join(report)

  def main():
      print("🚀 Scraping current NHL injuries...")
      injuries = scrape_hockey_reference_injuries()

      if injuries:
          # Create readable report
          report = format_injury_report(injuries)
          print("\n" + report)

          # Save to file
          timestamp = datetime.now().strftime('%Y%m%d_%H%M')

          # Save readable report
          report_file = f"nhl_injuries_report_{timestamp}.txt"
          with open(report_file, 'w') as f:
              f.write(report)
          print(f"\n💾 Report saved to: {report_file}")

          # Save raw data
          data_file = f"nhl_injuries_raw_{timestamp}.json"
          with open(data_file, 'w') as f:
              json.dump(injuries, f, indent=2)
          print(f"📄 Raw data saved to: {data_file}")

      else:
          print("❌ No injuries found or error occurred")

  if __name__ == "__main__":
      main()