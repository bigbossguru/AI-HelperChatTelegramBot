# AI-HelperChatTelegramBot

A simple AI Helper Chat Telegram Bot with integration OpenAI's models like GPT-Chat and DALL-E

### Create the Linux service

```
sudo nano /etc/systemd/system/telegabot.service
```

Paste this into this telegabot.service file

```
[Unit]
Description=AI Telegram Chat Bot
After=multi-user.target

[Service]
User=root
Type=simple
WorkingDirectory=/root/AI-HelperChatTelegramBot
ExecStart=/root/AI-HelperChatTelegramBot/.venv/bin/python3 bot.py
Restart=on-failure

[Install]
WantedBy=multi-user.target

```

```
sudo systemctl daemon-reload
sudo systemctl enable telegabot.service
sudo systemctl start telegabot.service
sudo systemctl status telegabot.service

```
