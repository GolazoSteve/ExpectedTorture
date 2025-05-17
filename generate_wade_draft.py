# generate_wade_draft.py (modular, no Google Drive)

import os
import re
import requests
import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI

# === CONFIG ===
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TEAM_ID = 137  # Giants
TIMEZONE = ZoneInfo("America/Los_Angeles")

# === HELPERS ===
def get_most_recent_game_id(team_id, max_days_back=3):
    today = datetime.datetime.now(TIMEZONE).date()
    for i in range(max_days_back):
        check_date = today - datetime.timedelta(days=i)
        date_str = check_date.strftime("%Y-%m-%d")
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}&teamId={team_id}"
        r = requests.get(url).json()
        dates = r.get("dates", [])
        if dates:
            games = dates[0].get("games", [])
            if games:
                return games[0]["gamePk"], date_str
    return None, None

def get_boxscore(game_id):
    return requests.get(f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore").json()

def get_linescore(game_id):
    return requests.get(f"https://statsapi.mlb.com/api/v1/game/{game_id}/linescore").json()

def get_condensed_game_link(game_id):
    url = f"https://www.mlb.com/gameday/{game_id}/final/video"
    page = requests.get(url)
    for line in page.text.split("\n"):
        if "condensed" in line.lower() and "mp4" in line:
            match = re.search(r"https.*?\.mp4", line)
            if match:
                return match.group(0)
    return "Highlight video not available."

def gpt_generate(prompt, temperature=0.8):
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are WADE, a tortured, stat-obsessed, emotionally damaged San Francisco Giants fan AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

# === MAIN PIPELINE ===
def run_gpt_fill_pipeline_minimal():
    game_id, date_str = get_most_recent_game_id(TEAM_ID)
    if not game_id:
        return {
            "title": f"WADE: No Giants Game in last {max_days_back} days",
            "sections": {
                "Greeting": "The machine awoke. But there was no baseball.",
                "Recap": "No data. No chaos. No hope."
            }
        }

    box = get_boxscore(game_id)
    linescore = get_linescore(game_id)
    condensed_link = get_condensed_game_link(game_id)

    home = box["teams"]["home"]["team"]["name"]
    away = box["teams"]["away"]["team"]["name"]
    home_score = linescore["teams"]["home"]["runs"]
    away_score = linescore["teams"]["away"]["runs"]

    giants_is_home = home == "San Francisco Giants"
    giants_score = home_score if giants_is_home else away_score
    opp_score = away_score if giants_is_home else home_score
    opponent = away if giants_is_home else home

    result = "won" if giants_score > opp_score else "lost"
    scoreline = f"{giants_score}–{opp_score}"

    # Prompt generation
    recap_prompt = f"Write a one-paragraph WADE-style live reaction recap of a game the Giants {result} {scoreline} vs the {opponent}. Include emotional glitching and dry sarcasm."
    recap = gpt_generate(recap_prompt)

    return {
        "title": f"WADE: {result.upper()} {scoreline} vs {opponent}",
        "sections": {
            "Greeting": "Good morning. Here’s what happened to the Giants last night.",
            "Box Score": f"**Final Score:** Giants {giants_score} – {opponent} {opp_score}",
            "Highlights": f"[Watch the condensed game here]({condensed_link})",
            "Recap": recap
        }
    }
