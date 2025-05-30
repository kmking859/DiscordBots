Extra Life Discord Bot
Automatically post beautiful Discord embeds when someone donates to your Extra Life campaign!
Limited support available - https://discord.gg/PQHq3m8Suq
Feel Generous, want to show appreciation? 💰 https://www.extra-life.org/participant/551698

🎮 Features

Real-time donation alerts - Posts beautiful embeds for every donation
Anonymous donation support - Handles both named and anonymous donors
Custom hospital names - Set your specific hospital or use the default
Progress tracking - Shows current total, goal, and percentage
Donation messages - Includes any messages donors leave
Custom branding - Uses Extra Life themed graphics

🚀 Quick Setup (Choose Your Method)
Option 1: GUI Setup (Easiest)

Install Python from https://python.org (check "Add Python to PATH")
Download setup_gui.py
Double-click setup_gui.py to run
Follow the visual setup wizard

Option 2: Command Line Setup

Install Python from https://python.org (check "Add Python to PATH")
Download simple_installer.py
Run python simple_installer.py
Follow the prompts

Option 3: Windows One-Click

Install Python from https://python.org (check "Add Python to PATH")
Download start_installer.bat
Double-click start_installer.bat
Follow the prompts

📋 Discord Bot Setup (Detailed Instructions)
Step 1: Create Discord Application

Go to https://discord.com/developers/applications
Click "New Application"
Give it a name (e.g., "Extra Life Bot")
Click "Create"

Step 2: Create Bot and Get Token

In your application, click "Bot" in the left sidebar
Click "Add Bot" (if not already a bot)
Under the Token section, click "Reset Token"
Copy the token that appears
⚠️ Keep this token secret! Don't share it with anyone

Step 3: Set Bot Permissions
In the Bot section, under Bot Permissions, enable:

✅ Send Messages
✅ Embed Links
✅ Read Message History
✅ Manage Messages

Step 4: Generate Invite Link

Click "OAuth2" → "URL Generator" in the left sidebar
Under Scopes, select: ✅ bot
Under Bot Permissions, select the same permissions as Step 3:

✅ Send Messages
✅ Embed Links
✅ Read Message History
✅ Manage Messages


Copy the generated URL at the bottom
Open the URL in a new tab to invite your bot to your server

Step 5: Get Channel ID

In Discord, go to User Settings (gear icon) → Advanced
Enable "Developer Mode"
Right-click the channel where you want donation alerts
Click "Copy ID"

Step 6: Get Extra Life Participant ID

Go to your Extra Life fundraising page
Look at the URL: https://www.extra-life.org/participant/12345
Your Participant ID is the number at the end (12345 in this example)

🎯 What You'll Get
When someone donates, your bot posts:
🎮 New Extra Life Donation! 🎮

💝 Donor: John Smith
💰 Amount: $25.00
🎯 Progress: $175 / $500

💬 Message: "Great cause! Keep it up!"

35.0% of goal reached!
Helping kids at [Your Hospital Name]

Thank you for supporting Extra Life! • Today at 3:45 PM
🔧 Configuration Options

Hospital Name: Enter your specific hospital or use default
Check Interval: How often to check for donations (default: 30 seconds)
Custom Settings: All stored in extralife_config.json

🐛 Troubleshooting
"Python is not recognized"

Solution: Reinstall Python from python.org
Important: Check "Add Python to PATH" during installation
Restart your computer after installing

"Bot not responding"

Check your Discord bot token is correct (no extra spaces)
Make sure you reset the token in Discord Developer Portal and copied the new one
Verify the bot was invited to your server with proper permissions
Check the channel ID is correct (long number like 123456789012345678)

"Channel not found"

Double-check your channel ID (should be 18-19 digits)
Make sure the bot has access to that channel
Verify the bot has Send Messages and Embed Links permissions

"Participant not found"

Verify your Extra Life participant ID (just the number, no letters)
Make sure your fundraising page is public and active
Check you're fundraising for the current year (2025)

"Permission denied" or "Missing permissions"

In Discord Developer Portal, make sure your bot has:

Send Messages ✅
Embed Links ✅
Read Message History ✅
Manage Messages ✅


Re-invite your bot using the OAuth2 URL with correct permissions

Dependencies installation fails

Make sure Python and pip are properly installed
Try running as administrator (Windows) or with sudo (Mac/Linux)
Manual install: pip install discord.py aiohttp python-dateutil

💡 Pro Tips

Test it: Make a small $5 donation to yourself to test the bot
Keep it running: The bot needs to stay running to catch donations
Save your files: Keep extralife_bot.py and extralife_config.json
Multiple servers: You can invite the same bot to multiple Discord servers
Restart if needed: If donations stop appearing, restart the bot

📁 Files Created
After setup, you'll have:

extralife_bot.py - Your configured bot (this runs your bot)
extralife_config.json - Your saved settings
Console output showing bot status and donation activity

❓ FAQ
Q: Do I need to keep my computer running?
A: Yes, the bot runs on your computer. If you turn it off, the bot stops.
Q: Can I use this for team fundraising?
A: Yes! Just use your team's participant ID instead of your individual one.
Q: Will it catch donations I already received?
A: No, it only monitors for NEW donations from when you start the bot.
Q: Can I customize the embed colors/text?
A: Yes! Edit the extralife_bot.py file after generation to customize appearance.
Q: Is my Discord token safe?
A: Your token stays on your computer only. Never share it with anyone!
🆘 Still Need Help?

Read this README carefully - most issues are covered above
Check the console output when running the bot for error messages
Verify all your IDs and tokens are correct (most common issue)
Try the test methods in the examples folder
Ask in Extra Life Discord communities for fundraising questions

🎉 Contributing
Found a bug? Have a feature request? Feel free to open an issue or submit a pull request!
📜 License
MIT License - Feel free to modify and share!

Happy fundraising! 🎮❤️
Built with ❤️ for the Extra Life community
