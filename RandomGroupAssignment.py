import os
import random
import itertools
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# === メンバーリスト ===
members = {
  "B4": ["Zhang", "Arai", "Uchida", "Karasawa", "Shimabara", "Hara", "Yoshida", "Liang"],
  "M1M2": ["Ito", "Song", "Nakajima", "Kiryu", "Shigeyoshi", "Nishikata", "Watanabe"],
  "DPD": ["Fujii"]
}
PI = "Hirano"

# === 設定値 ===
START_DATE = datetime(2024, 4, 3)  # スクリプトの開始日
END_DATE = datetime(2025, 7, 19)  # スクリプトの終了日
DAYS_OF_WEEK = ["Monday", "Wednesday"]  # Lunch MTGの曜日
NUM_TEAMS = 3  # 各曜日のチーム数
SLACK_CHANNEL = "#general"  # 投稿するチャンネル


# === 事前チェック ===
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
if not SLACK_BOT_TOKEN:
  print("Error: SLACK_BOT_TOKEN is not set.")
  exit(1)
# スクリプトの実行チェック
today = datetime.today()
if today < START_DATE:
  print("Script has not started yet. Exiting.")
  exit()
if today > END_DATE:
  print("Script has expired. Exiting.")
  exit()

# === メンバーを曜日グループに分割する関数 ===
def split_into_days(members, pi, days_of_week):
  group_dict = {day: [] for day in days_of_week}
  # PIを最初に全てのグループに追加
  for day in days_of_week:
    group_dict[day].append([pi])  # PIは1つのリストとして追加
  # 各メンバーを曜日ごとに均等に割り当てるため、カテゴリごとに分けて処理
  category_members = {category: members_list for category, members_list in members.items()}
  # 各曜日グループに均等に分配する
  for category, member_list in category_members.items():
    random.shuffle(member_list)  # メンバーをシャッフルしてランダムに並べる
    # メンバーを曜日に均等に割り当てる
    for i, member in enumerate(member_list):
      day = days_of_week[i % len(days_of_week)]  # 丸めて各曜日に割り当て
      group_dict[day].append([member])  # 各メンバーをリストとして追加
  return group_dict

# === 各曜日ごとのチーム分け関数 ===
def assign_teams(group):
  combined = sum(group, [])  # groupはリストのリストなので、それらを一つのリストに統合
  random.shuffle(combined)  # シャッフルしてランダム化
  teams = [[] for _ in range(NUM_TEAMS)]  # NUM_TEAMS分の空のリストを作成
  for member, team in zip(combined, itertools.cycle(teams)):  # 均等に割り振り
    team.append(member)
  return teams

# === メッセージフォーマット関数 ===
# 翌週の日付を取得
def get_next_weekday(day_name):
  # Convert day names to weekday numbers (0 = Monday, 1 = Tuesday, etc.)
  day_to_num = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
  target_weekday = day_to_num[day_name]
  today = datetime.today()
  days_ahead = (target_weekday - today.weekday()) % 7  # 次の指定曜日までの日数
  if days_ahead == 0:  # すでにその曜日の場合、1週間後にする
    days_ahead = 7
  return today + timedelta(days=days_ahead)
# 日付フォーマット
def format_date(date):
  return date.strftime("%Y/%m/%d")
# グループ出力のフォーマット
def format_message(day, date, teams):
  message = f":calendar: *{day} ({date}) Group*\n"
  for i, team in enumerate(teams):
    label = f"• Team {i+1}"
    members_str = ', '.join(team) if team else "なし"
    message += f"{label} : {members_str}\n"
  message += "─────────────────────────\n"
  return message
# ロケーションメッセージ
if NUM_TEAMS == 1:
  LOCATION_MESSAGE = ""
elif NUM_TEAMS == 2:
  LOCATION_MESSAGE = "※ Team 1: Front (on the side of Prof. Hirano's office)  2: Back"
elif NUM_TEAMS == 3:
  LOCATION_MESSAGE = "※ Team 1: Front (on the side of Prof. Hirano's office)  2: Center  3: Back"
elif NUM_TEAMS == 4:
  LOCATION_MESSAGE = "※ Team 1: Front (on the side of Prof. Hirano's office)  2: Center (window side)  3: Center (hallway side)  4: Back"
elif NUM_TEAMS == 5:
  LOCATION_MESSAGE = "※ Team 1: Front (on the side of Prof. Hirano's office)  2: Center (window side)  3: Center (hallway side)  4: Back (window side)  5: Back (door side)"
else:
  LOCATION_MESSAGE = ""
  print(f"Warning: NUM_TEAMS = {NUM_TEAMS} exceeds predefined location mapping.")

# === Slack 投稿関数 ===
def post_to_slack(message, slack_token, channel):
  client = WebClient(token=slack_token)
  try:
    response = client.chat_postMessage(channel=channel, text=message)
    print(f"✅ Successfully posted to Slack: {response['ts']}")
  except SlackApiError as e:
    print(f"❌ Slack API Error: {e.response['error']}")

# === 実行処理 ===
print("🔄 Generating group assignments...")
group_dict = split_into_days(members, PI, DAYS_OF_WEEK)
message = "Here is the team assignment for next week.\n\n"
message += "─────────────────────────\n"
for day in DAYS_OF_WEEK:
  next_day = get_next_weekday(day)  # 日付取得
  teams = assign_teams(group_dict[day])  # 各曜日のグループをチーム分け
  formatted_message = format_message(day, format_date(next_day), teams)
  message += formatted_message
message += "\n" + LOCATION_MESSAGE
print("🚀 Posting to Slack...")
post_to_slack(message, SLACK_BOT_TOKEN, SLACK_CHANNEL)
print("✅ Done.")
