#!/usr/bin/env python3
"""
Extra Life Discord Bot - All-in-One Installer
Just double-click this file to set up everything!
"""

import sys
import subprocess
import webbrowser
import os
from pathlib import Path

def print_header():
    print("=" * 40)
    print("  EXTRA LIFE DISCORD BOT SETUP")
    print("=" * 40)
    print()

def check_python():
    """Check if Python is adequate"""
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7+ required")
        print(f"   You have: {sys.version}")
        print("   Please download Python from: https://python.org")
        return False
    
    print(f"SUCCESS: Python {sys.version.split()[0]} - Good!")
    return True

def install_packages():
    """Install required packages"""
    packages = ["discord.py", "aiohttp", "python-dateutil"]
    print("\nInstalling required packages...")
    
    for pkg in packages:
        print(f"   Installing {pkg}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", pkg
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   SUCCESS: {pkg}")
        except subprocess.CalledProcessError:
            print(f"   ERROR: Failed to install {pkg}")
            return False
    
    print("SUCCESS: All packages installed!")
    return True

def get_user_input():
    """Simple command-line setup"""
    print("\n" + "="*50)
    print("CONFIGURATION SETUP")
    print("="*50)
    
    config = {}
    
    # Discord Token
    print("\n1. DISCORD BOT TOKEN")
    print("   Go to: https://discord.com/developers/applications")
    print("   Create app -> Bot -> Copy Token")
    webbrowser.open("https://discord.com/developers/applications")
    config['discord_token'] = input("\n   Paste your bot token here: ").strip()
    
    # Channel ID  
    print("\n2. DISCORD CHANNEL ID")
    print("   Enable Developer Mode in Discord settings")
    print("   Right-click your channel -> Copy ID")
    config['channel_id'] = input("\n   Paste channel ID here: ").strip()
    
    # Participant ID
    print("\n3. EXTRA LIFE PARTICIPANT ID")
    print("   Check your fundraising page URL")
    print("   extra-life.org/participant/YOUR_ID")
    config['participant_id'] = input("\n   Enter just the ID number: ").strip()
    
    # Hospital Name
    print("\n4. HOSPITAL NAME")
    print("   Enter your specific hospital name")
    print("   Or press Enter for default")
    hospital = input("\n   Hospital name [default: A Children's Miracle Network hospital]: ").strip()
    config['hospital_name'] = hospital or "A Children's Miracle Network hospital"
    
    return config

def create_bot_file(config):
    """Create the bot file with user's config"""
    
    bot_code = '''import discord
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
CHECK_INTERVAL = 30

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
            
            # Create embed with gaming emojis
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
        hospital=config['hospital_name']
    )
    
    with open("extralife_bot.py", "w", encoding='utf-8') as f:
        f.write(bot_code)
    
    print("SUCCESS: Bot file created: extralife_bot.py")

def main():
    try:
        print_header()
        
        if not check_python():
            input("Press Enter to exit...")
            return
        
        if not install_packages():
            print("ERROR: Package installation failed!")
            input("Press Enter to exit...")
            return
        
        config = get_user_input()
        
        if not all([config['discord_token'], config['channel_id'], config['participant_id']]):
            print("ERROR: Missing required information!")
            input("Press Enter to exit...")
            return
        
        create_bot_file(config)
        
        print("\n" + "=" * 30)
        print("  SETUP COMPLETE!")
        print("=" * 30)
        print("\nSUCCESS: Your bot is ready!")
        print("To start: python extralife_bot.py")
        print("To stop: Press Ctrl+C")
        print()
        
        start_now = input("Start the bot now? (y/n): ").lower().strip()
        if start_now in ['y', 'yes']:
            print("\nStarting bot...")
            try:
                subprocess.run([sys.executable, "extralife_bot.py"])
            except KeyboardInterrupt:
                print("\nBot stopped!")
    
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()