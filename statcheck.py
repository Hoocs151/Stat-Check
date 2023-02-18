import psutil
import pyautogui
import discord_webhook
import time
import configparser
import os

CONFIG_DEFAULTS = {
    'webhook_url': 'YOUR_WEBHOOK_URL_HERE',
    'update_interval': '60',
    'note': 'nah',
}

config = configparser.ConfigParser()

if not os.path.isfile('config.ini'):
    config['cac'] = CONFIG_DEFAULTS
    with open('config.ini', 'w') as f:
        config.write(f)

config.read('config.ini')
webhook_url = config['cac']['webhook_url']
update_interval = int(config['cac']['update_interval'])
note = config['cac']['note']

print(f""" 
 ▄  █ ████▄ ████▄ ▄█▄      ▄▄▄▄▄   
█   █ █   █ █   █ █▀ ▀▄   █     ▀▄ 
██▀▀█ █   █ █   █ █   ▀ ▄  ▀▀▀▀▄   
█   █ ▀████ ▀████ █▄  ▄▀ ▀▄▄▄▄▀    
   █              ▀███▀            
  ▀                                
                                    """)
print(f"Webhook URL: {webhook_url}")
print(f"Update interval: {update_interval} seconds")
print(f"Note: {note}")

while True:
    cpu_percentages = psutil.cpu_percent(interval=None, percpu=True)
    cpu_usage = sum(cpu_percentages) / len(cpu_percentages)
    ram_usage = (psutil.virtual_memory().used / psutil.virtual_memory().total) * 100

    num_roblox_tabs = len([p for p in psutil.process_iter() if p.name() == "RobloxPlayerBeta.exe" and p.memory_info().rss >= 100*1024*1024])

    screenshot_path = "screenshot.png"
    pyautogui.screenshot(screenshot_path)

    webhook = discord_webhook.DiscordWebhook(url=webhook_url)

    embed = discord_webhook.DiscordEmbed(title="VPS STAT CHECK", description=note, color=0x7289da)
    embed.set_image(url="attachment://screenshot.png")
    embed.set_footer(text=f"Dữ liệu sẽ được tải lên sau mỗi {update_interval} giây")
    embed.add_embed_field(name="<:hoccongviec:1028367476037259424> CPU Usage", value=f"`{cpu_usage}%`")
    embed.add_embed_field(name="<:hoccongviec:1028367476037259424> RAM Usage", value=f"`{ram_usage}%`")
    embed.add_embed_field(name="<:hoocstok:1045320042230841356> Roblox Tabs", value=f"`{num_roblox_tabs}`")

    webhook.add_file(file=open(screenshot_path, "rb"), filename="screenshot.png")

    webhook.add_embed(embed)
    response = webhook.execute()

    time.sleep(update_interval)
