# LunchMTG Group Assignment Bot

## Description
This script automates the assignment of team members for weekly lunch meetings and posts the assignments to a designated Slack channel.

## Features
- **Automatic** Team Assignment: Randomly distributes members into teams for designated meeting days.
- **Configurable Team Count**: Allows setting a predefined number of teams per day.
- **Slack Integration**: Posts the assigned teams to a specified Slack channel.
- **Github Actions Automation**: Runs the script automatically on a defined schedule using GitHub Actions.

## Usage
1. Modify Configuration:
  Update the script parameters in `RandomGroupAssignment.py` as needed:
  - **Active period**: `START_DATE` and `END_DATE` to define when the script should operate.
  - **Member list**: `members` dictionary to reflect the current group members.
  - **Meeting days**: `DAYS_OF_WEEK = ["Monday", "Wednesday"]` to specify the days.
  - **Number of teams**: `NUM_TEAMS = 3` to configure the number of teams per day.
  - **Slack channel**: `SLACK_CHANNEL = "#general"` to specify the channel for posting assignments.
2. Automate Execution with GitHub Actions:
  The script is configured to run automatically using GitHub Actions. Ensure that the workflow (`schedule.yml`) is correctly set up in `.github/workflows/`. 
  **Workflow Schedule**
  The current schedule runs every Friday at 3:00 AM UTC (12:00 PM JST):
  ```yml:schedule
  on:
    schedule:
      - cron: '0 3 * * 5' # Runs every Friday at 3:00 AM UTC (JST 12:00 PM)
  ```

## Implementation Details
### GitHub Actions Automation
The script is set to run automatically via cron using GitHub Actions. The workflow file is located in `.github/workflows/schedule.yml`. The script will check if the current date falls within the specified range (`START_DATE` and `END_DATE`) before executing the assignment. 
### Slack Integration
The script uses the `slack_sdk` library to send messages to Slack. To enable this, set up a Slack bot token:
1. Create a Slack app and add **chat:write** permissions.
2. Install the app to your workspace and obtain the **OAuth token**.
3. Store the token in your GitHub repository as a secret:
  - Go to **Settings > Secrets and variables > Actions > New repository secret**.
  - Name the secret `SLACK_BOT_TOKEN` and paste the token value.
### References
- [GitHub Actions ワークフローで処理を定期実行する方法](https://gotohayato.com/content/514/)
- [Slack ボットの作成手順](https://qiita.com/odm_knpr0122/items/04c342ec8d9fe85e0fe9)
- [slackでbotのメッセージを削除する](https://yiskw713.hatenablog.com/entry/delete-slack-bot-message)
