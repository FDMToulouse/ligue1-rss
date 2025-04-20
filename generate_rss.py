import requests
from feedgen.feed import FeedGenerator
from datetime import datetime

# === CONFIGURATION ===
API_KEY = '3931784d446b590bb378e0299187060c'
API_URL = 'https://v3.football.api-sports.io/fixtures'
LEAGUE_ID = 61  # Ligue 1
SEASON = 2024

headers = {
    'x-apisports-key': API_KEY
}

params = {
    'league': LEAGUE_ID,
    'season': SEASON,
    'live': 'all'
}

# === APPEL API ===
response = requests.get(API_URL, headers=headers, params=params)
data = response.json()

# === GÉNÉRATION RSS ===
fg = FeedGenerator()
fg.title('Scores en direct - Ligue 1')
fg.link(href='https://www.ligue1.fr', rel='alternate')
fg.description('Flux RSS des scores en direct de la Ligue 1')

for match in data['response']:
    teams = match['teams']
    goals = match['goals']
    fixture = match['fixture']
    status = match['fixture']['status']['long']

    title = f"{teams['home']['name']} {goals['home']} - {goals['away']} {teams['away']['name']} ({status})"
    link = f"https://www.ligue1.fr"  # Tu peux mettre un lien vers les détails si tu veux
    pub_date = datetime.fromisoformat(fixture['date'].replace('Z', '+00:00'))

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)
    fe.pubDate(pub_date)
    fe.description(f"Début : {pub_date.strftime('%H:%M')} UTC")

# === SAUVEGARDE RSS ===
fg.rss_file('ligue1_scores.xml')
print("✅ Flux RSS généré → ligue1_scores.xml")
