import psutil
import pyautogui
import discord_webhook
import time
import configparser
import os
import requests

CONFIG_DEFAULTS = {
    'webhook_url': 'YOUR_WEBHOOK_URL_HERE',
    'update_interval': '60',
    'note': 'ur gay',
    'update_check_enabled': 'true',
}

config = configparser.ConfigParser()

if not os.path.isfile('config.ini'):
    config['cac'] = CONFIG_DEFAULTS
    with open('config.ini', 'w') as f:
        config.write(f)

config.read('config.ini')
webhook_url = config.get('cac', 'webhook_url', fallback=CONFIG_DEFAULTS['webhook_url'])
update_interval = int(config['cac']['update_interval'])
note = config['cac']['note']
update_check_enabled = config['cac']['update_check_enabled']

print(""" 
 ▄  █ ████▄ ████▄ ▄█▄      ▄▄▄▄▄   
█   █ █   █ █   █ █▀ ▀▄   █     ▀▄ 
██▀▀█ █   █ █   █ █   ▀ ▄  ▀▀▀▀▄   
█   █ ▀████ ▀████ █▄  ▄▀ ▀▄▄▄▄▀    
   █              ▀███▀            
  ▀                                
""")
frame_char = "="
frame_width = 50
top_line = frame_char * frame_width
print(f"\n{top_line}")
print("\nConfig Settings:")
print(f"Webhook URL: {webhook_url}")
print(f"Update Interval: {update_interval} seconds")
print(f"Note: {note}")
print(f"Roblox Update Detected: {update_check_enabled}\n")

roblox_version = None

while True:

    if config.getboolean('cac', 'update_check_enabled'):
        try:
            response = requests.get('https://setup.rbxcdn.com/version')
            response.raise_for_status()
            latest_version = response.json()['Version']
            
            if roblox_version != latest_version:
                roblox_version = latest_version
                print(f'[ + ] New Roblox update detected --> Closing Roblox account manager!')
                for process in psutil.process_iter(['name', 'cmdline']):
                    if 'RobloxAccountManager.exe' in process.info['name'] and 'NoUpdatePrompt' in process.info['cmdline']:
                        if psutil.pid_exists(process.pid):
                            process.terminate()
                print(f'[ + ] Current Roblox version: {latest_version}')

        except Exception as e:
            pass

    num_roblox_tabs = len([p for p in psutil.process_iter() if p.name() == "RobloxPlayerBeta.exe" and p.memory_info().rss >= 100*1024*1024])

    screenshot_path = "screenshot.png"
    pyautogui.screenshot(screenshot_path)

    webhook = discord_webhook.DiscordWebhook(url=webhook_url)

    embed = discord_webhook.DiscordEmbed(title="VPS STAT CHECK", description=note, color=0x7289da)
    embed.set_image(url="attachment://screenshot.png")
    embed.set_footer(text=f"Dữ liệu sẽ được tải lên sau mỗi {update_interval} giây")
    embed.add_embed_field(name="<:hoocstok:1045320042230841356> Roblox Tabs", value=f"`{num_roblox_tabs}`")

    webhook.add_file(file=open(screenshot_path, "rb"), filename="screenshot.png")

    webhook.add_embed(embed)
    response = webhook.execute()

    time.sleep(update_interval)
