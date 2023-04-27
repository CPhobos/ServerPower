import subprocess
import time
import requests
import re 

_webhook = "<webhook_here>"
_username = "Web Server Notifications"
_delay_in_mins = 5

def send_to_webhook(
    message: str, 
    embed_description,
    embed_title,
    embed_footer_text
    ):
    data = {
        "content":  message,
        "username": _username,
        "embeds": [
            {
                "description" : embed_description,
                "title" : embed_title,
                "footer": {
                    "text": embed_footer_text
                }
            }
        ]
    }
    requests.post(_webhook, json=data)


def get_uptime():
  
    temp = str(subprocess.Popen(
        ["uptime", "-p"], 
        stdout = subprocess.PIPE
    ).communicate()[0])

    return re.search(r"(\d+[\w\s,]+)(?:\\n')", temp).group(1)
    
def get_battery_perc():
    temp = str(subprocess.Popen(
        ["acpi"], 
        stdout = subprocess.PIPE
    ).communicate())
    return re.search(r'\b\d+\b%', temp).group()

while True:
    current_battery_level = int(get_battery_perc().replace("%", ""))
    
    if(current_battery_level <= 20):
        send_to_webhook(
            "",
            f"Battery Percentage: {get_battery_perc()}",
            "Battery Warning",
            f"Uptime: {get_uptime()}"
        )
    time.sleep(_delay_in_mins * 60)