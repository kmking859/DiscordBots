import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import subprocess
import sys
import webbrowser
from pathlib import Path

class ExtraLifeBotSetup:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Extra Life Discord Bot Setup")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Configuration data
        self.config = {
            'discord_token': '',
            'channel_id': '',
            'participant_id': '',
            'hospital_name': 'A Children\'s Miracle Network hospital',
            'check_interval': 30
        }
        
        self.setup_ui()
        self.load_existing_config()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Extra Life Discord Bot Setup", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                                text="Fill out the information below to configure your Extra Life Discord bot:",
                                wraplength=550)
        instructions.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Discord Bot Token
        ttk.Label(main_frame, text="Discord Bot Token:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.token_var = tk.StringVar()
        token_entry = ttk.Entry(main_frame, textvariable=self.token_var, width=50, show="*")
        token_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Help button for Discord token
        ttk.Button(main_frame, text="How to get Discord token?", 
                  command=self.show_discord_help).grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
        
        # Channel ID
        ttk.Label(main_frame, text="Discord Channel ID:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.channel_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.channel_var, width=50).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Help button for Channel ID
        ttk.Button(main_frame, text="How to get Channel ID?", 
                  command=self.show_channel_help).grid(row=5, column=1, sticky=tk.W, padx=(10, 0))
        
        # Participant ID
        ttk.Label(main_frame, text="Extra Life Participant ID:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.participant_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.participant_var, width=50).grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Help button for Participant ID
        ttk.Button(main_frame, text="How to get Participant ID?", 
                  command=self.show_participant_help).grid(row=7, column=1, sticky=tk.W, padx=(10, 0))
        
        # Hospital Name
        ttk.Label(main_frame, text="Hospital Name:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.hospital_var = tk.StringVar(value="A Children's Miracle Network hospital")
        ttk.Entry(main_frame, textvariable=self.hospital_var, width=50).grid(row=8, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Hospital help
        hospital_help = ttk.Label(main_frame, text="(Optional: Enter your specific hospital name)", 
                                 font=('Arial', 8), foreground='gray')
        hospital_help.grid(row=9, column=1, sticky=tk.W, padx=(10, 0))
        
        # Check Interval
        ttk.Label(main_frame, text="Check Interval (seconds):").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.interval_var = tk.StringVar(value="30")
        interval_spin = ttk.Spinbox(main_frame, from_=10, to=300, textvariable=self.interval_var, width=10)
        interval_spin.grid(row=10, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Interval help
        interval_help = ttk.Label(main_frame, text="(How often to check for new donations)", 
                                 font=('Arial', 8), foreground='gray')
        interval_help.grid(row=11, column=1, sticky=tk.W, padx=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=12, column=0, columnspan=2, pady=30)
        
        # Test Connection button
        ttk.Button(button_frame, text="Test Configuration", 
                  command=self.test_config).pack(side=tk.LEFT, padx=5)
        
        # Save Config button
        ttk.Button(button_frame, text="Save Configuration", 
                  command=self.save_config).pack(side=tk.LEFT, padx=5)
        
        # Install Dependencies button
        ttk.Button(button_frame, text="Install Dependencies", 
                  command=self.install_dependencies).pack(side=tk.LEFT, padx=5)
        
        # Generate Bot File button
        ttk.Button(button_frame, text="Generate Bot File", 
                  command=self.generate_bot_file).pack(side=tk.LEFT, padx=5)
        
        # Run Bot button
        ttk.Button(button_frame, text="Run Bot", 
                  command=self.run_bot).pack(side=tk.LEFT, padx=5)
        
        # Status text area
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=13, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=20)
        
        self.status_text = tk.Text(status_frame, height=8, width=70)
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        self.log_message("Welcome to Extra Life Discord Bot Setup!")
        self.log_message("Fill in your configuration details above and click 'Install Dependencies' to start.")
    
    def log_message(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def show_discord_help(self):
        help_text = """How to get your Discord Bot Token:

1. Go to https://discord.com/developers/applications
2. Click 'New Application' and give it a name
3. Go to the 'Bot' section in the left menu
4. Click 'Reset Token' to generate a new token
5. Copy the token that appears
6. Paste it in the Discord Bot Token field above

IMPORTANT: Keep your token secret! Don't share it with anyone.

You'll also need to invite your bot to your Discord server:
1. In the Discord Developer Portal, go to OAuth2 > URL Generator
2. Select 'bot' scope
3. Select permissions: Send Messages, Embed Links, Read Message History, Manage Messages
4. Copy the generated URL and open it to invite your bot"""
        
        self.show_help_window("Discord Bot Token Help", help_text)
    
    def show_channel_help(self):
        help_text = """How to get your Discord Channel ID:

1. In Discord, go to User Settings (gear icon)
2. Go to Advanced settings
3. Enable 'Developer Mode'
4. Right-click on the channel where you want donation alerts
5. Click 'Copy ID'
6. Paste it in the Discord Channel ID field above

The Channel ID will be a long number like: 123456789012345678"""
        
        self.show_help_window("Discord Channel ID Help", help_text)
    
    def show_participant_help(self):
        help_text = """How to get your Extra Life Participant ID:

1. Go to your Extra Life fundraising page
2. Look at the URL in your browser
3. The Participant ID is the number at the end of the URL

For example, if your page URL is:
https://www.extra-life.org/participant/12345

Then your Participant ID is: 12345

Paste just the number in the Participant ID field above."""
        
        self.show_help_window("Extra Life Participant ID Help", help_text)
    
    def show_help_window(self, title, text):
        help_window = tk.Toplevel(self.root)
        help_window.title(title)
        help_window.geometry("500x400")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_existing_config(self):
        config_file = Path("extralife_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.token_var.set(saved_config.get('discord_token', ''))
                    self.channel_var.set(saved_config.get('channel_id', ''))
                    self.participant_var.set(saved_config.get('participant_id', ''))
                    self.hospital_var.set(saved_config.get('hospital_name', "A Children's Miracle Network hospital"))
                    self.interval_var.set(str(saved_config.get('check_interval', 30)))
                self.log_message("Loaded existing configuration.")
            except Exception as e:
                self.log_message(f"Error loading config: {e}")
    
    def save_config(self):
        self.config = {
            'discord_token': self.token_var.get().strip(),
            'channel_id': self.channel_var.get().strip(),
            'participant_id': self.participant_var.get().strip(),
            'hospital_name': self.hospital_var.get().strip(),
            'check_interval': int(self.interval_var.get())
        }
        
        try:
            with open("extralife_config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
            self.log_message("Configuration saved successfully!")
        except Exception as e:
            self.log_message(f"Error saving configuration: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def install_dependencies(self):
        self.log_message("Installing required Python packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py", "aiohttp", "python-dateutil"])
            self.log_message("Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            self.log_message(f"Error installing dependencies: {e}")
            messagebox.showerror("Error", "Failed to install dependencies. Make sure you have Python and pip installed.")
    
    def test_config(self):
        if not all([self.token_var.get().strip(), self.channel_var.get().strip(), self.participant_var.get().strip()]):
            messagebox.showwarning("Incomplete Configuration", "Please fill in all required fields before testing.")
            return
        
        self.log_message("Testing configuration...")
        self.log_message("Configuration looks good! (Note: Full test requires running the bot)")
    
    def generate_bot_file(self):
        if not all([self.token_var.get().strip(), self.channel_var.get().strip(), self.participant_var.get().strip()]):
            messagebox.showwarning("Incomplete Configuration", "Please fill in all required fields before generating bot file.")
            return
        
        self.save_config()
        
        bot_code = self.get_bot_code()
        
        try:
            with open("extralife_bot.py", 'w', encoding='utf-8') as f:
                f.write(bot_code)
            self.log_message("Bot file generated successfully as 'extralife_bot.py'!")
        except Exception as e:
            self.log_message(f"Error generating bot file: {e}")
            messagebox.showerror("Error", f"Failed to generate bot file: {e}")
    
    def get_bot_code(self):
        """Generate bot code with proper Unicode handling"""
        config = {
            'discord_token': self.token_var.get().strip(),
            'channel_id': self.channel_var.get().strip(),
            'participant_id': self.participant_var.get().strip(),
            'hospital_name': self.hospital_var.get().strip(),
            'check_interval': int(self.interval_var.get())
        }
        
        return '''import discord
from discord.ext import tasks
import aiohttp
import asyncio
from datetime import datetime
from dateutil import parser

# Your Configuration
DISCORD_TOKEN = "{token}"
CHANNEL_ID = {channel}
PARTICIPANT_ID = "{participant}"
HOSPITAL_NAME = "{hospital}"
CHECK_INTERVAL = {interval}

class ExtraLifeBot:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = False
        self.client = discord.Client(intents=intents)
        self.last_donation_id = None
        self.campaign_info = None
        self.setup_events()
    
    def setup_events(self):
        @self.client.event
        async def on_ready():
            print(f'Bot logged in as {{self.client.user}}')
            print(f'Monitoring channel ID: {{CHANNEL_ID}}')
            print(f'Extra Life participant: {{PARTICIPANT_ID}}')
            print(f'Hospital: {{HOSPITAL_NAME}}')
            await self.start_monitoring()
        
        @self.client.event
        async def on_error(event, *args, **kwargs):
            print(f'Discord error: {{event}}')
    
    async def start_monitoring(self):
        print('Starting donation monitoring...')
        await self.update_campaign_info()
        await self.get_latest_donation()
        self.monitor_donations.start()
    
    async def update_campaign_info(self):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://www.extra-life.org/api/participants/{{PARTICIPANT_ID}}"
                async with session.get(url) as response:
                    if response.status == 200:
                        self.campaign_info = await response.json()
                        print(f"Campaign: ${{self.campaign_info['sumDonations']}} / ${{self.campaign_info['fundraisingGoal']}}")
                    else:
                        print(f"API Error: HTTP {{response.status}}")
        except Exception as e:
            print(f'Campaign info error: {{e}}')
    
    async def get_latest_donation(self):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://www.extra-life.org/api/participants/{{PARTICIPANT_ID}}/donations"
                async with session.get(url) as response:
                    if response.status == 200:
                        donations = await response.json()
                        if donations:
                            self.last_donation_id = donations[0]['donationID']
                            print(f"Starting from donation: {{self.last_donation_id}}")
        except Exception as e:
            print(f'Donation fetch error: {{e}}')
    
    @tasks.loop(seconds=CHECK_INTERVAL)
    async def monitor_donations(self):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://www.extra-life.org/api/participants/{{PARTICIPANT_ID}}/donations"
                async with session.get(url) as response:
                    if response.status != 200:
                        return
                    donations = await response.json()
            
            await self.update_campaign_info()
            
            new_donations = []
            for donation in donations:
                if not self.last_donation_id or donation['donationID'] != self.last_donation_id:
                    new_donations.append(donation)
                else:
                    break
            
            for donation in reversed(new_donations):
                await self.post_donation_embed(donation)
                self.last_donation_id = donation['donationID']
                
        except Exception as e:
            print(f'Monitor error: {{e}}')
    
    async def post_donation_embed(self, donation):
        try:
            channel = self.client.get_channel(CHANNEL_ID)
            if not channel:
                print(f"ERROR: Channel {{CHANNEL_ID}} not found!")
                return
            
            donation_time = parser.parse(donation['createdDateUTC'])
            
            # Create embed using Unicode escapes to avoid encoding issues
            embed = discord.Embed(
                title="\\U0001f3ae New Extra Life Donation! \\U0001f3ae",
                color=0x00A651,
                timestamp=donation_time
            )
            
            embed.set_thumbnail(url="https://imagizer.imageshack.com/img922/973/l92xsR.png")
            
            donor_name = 'Anonymous'
            if donation.get('displayName') and donation['displayName'].strip():
                donor_name = donation['displayName']
            
            embed.add_field(name="\\U0001f49d Donor", value=donor_name, inline=True)
            embed.add_field(name="\\U0001f4b0 Amount", value=f"${{donation['amount']:.2f}}", inline=True)
            embed.add_field(name="\\U0001f3af Progress", value=f"${{self.campaign_info['sumDonations']}} / ${{self.campaign_info['fundraisingGoal']}}", inline=True)
            
            if donation.get('message') and donation['message'].strip():
                embed.add_field(name="\\U0001f4ac Message", value=donation['message'][:1024], inline=False)
            
            progress_percent = (self.campaign_info['sumDonations'] / self.campaign_info['fundraisingGoal']) * 100
            embed.description = f"**{{progress_percent:.1f}}% of goal reached!**\\n\\nHelping kids at {{HOSPITAL_NAME}}"
            
            embed.set_footer(
                text="Thank you for supporting Extra Life!",
                icon_url="https://assets.extra-life.org/distro/extra-life/images/extra-life-logo-square.png"
            )
            
            await channel.send(embed=embed)
            print(f"Posted: {{donor_name}} - ${{donation['amount']}}")
            
        except Exception as e:
            print(f'Embed error: {{e}}')
    
    def run(self):
        try:
            self.client.run(DISCORD_TOKEN)
        except Exception as e:
            print(f"Bot error: {{e}}")

if __name__ == "__main__":
    print("Starting Extra Life Discord Bot...")
    print("Press Ctrl+C to stop")
    bot = ExtraLifeBot()
    bot.run()
'''.format(
            token=config['discord_token'],
            channel=config['channel_id'],
            participant=config['participant_id'],
            hospital=config['hospital_name'],
            interval=config['check_interval']
        )
    
    def run_bot(self):
        if not Path("extralife_bot.py").exists():
            messagebox.showwarning("Bot Not Generated", "Please generate the bot file first.")
            return
        
        self.log_message("Starting bot... (Close this window to stop the bot)")
        try:
            subprocess.Popen([sys.executable, "extralife_bot.py"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
            self.log_message("Bot started in new window!")
        except Exception as e:
            self.log_message(f"Error starting bot: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ExtraLifeBotSetup()
    app.run()