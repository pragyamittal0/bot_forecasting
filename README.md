

# 🌧️ Rainfall Forecast Discord Bot

A smart Discord bot that provides **10-day rainfall forecasts** for **U.S. cities** using real weather data and time-series prediction via Facebook's `Prophet`. Built for farmers, planners, logistics, and weather enthusiasts.

---

## 📦 Features

- 🔍 Forecast rainfall for any U.S. city using `!rain <city>`
- 📈 Uses real historical data from [Open-Meteo API](https://open-meteo.com/)
- 🤖 Forecasts the next 10 days using `Prophet`
- 🖼️ Sends a clear bar chart + readable summary to Discord
- 🧠 Designed for simplicity, accuracy, and real-world use

---

## 🚀 Example

> Command:
```

!rain seattle

```

> Bot response:
```

📍 Seattle Rainfall Forecast (Next 10 Days)

📊 Average rain: 4.2 mm/day
🌧️ Most rain: 2025-07-01 — 6.1 mm
🌤️ Least rain: 2025-06-27 — 2.0 mm

````

📊 Plus a clean chart of the forecasted and recent rainfall!

<img width="706" alt="Screenshot 2025-06-24 at 2 35 43 PM" src="https://github.com/user-attachments/assets/9b66771f-12a6-4f5c-927c-a5f29ebd9406" />
---

## ⚙️ How It Works

1. Uses [Open-Meteo](https://open-meteo.com/) to pull 1 year of historical rainfall
2. Trains a `Prophet` model for each query
3. Predicts rainfall for the next 10 days
4. Sends both a chart and natural-language summary back via Discord

---

## 🧰 Tech Stack

- `Python 3.8+`
- [`discord.py`](https://github.com/Rapptz/discord.py)
- [`Prophet`](https://facebook.github.io/prophet/)
- [`Open-Meteo`](https://open-meteo.com/) API
- `Matplotlib`, `Pandas`, `Geopy`

---

## 🛠️ Setup

### 1. Clone this repo
```bash
git clone https://github.com/yourusername/rainfall-forecast-bot.git
cd rainfall-forecast-bot
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

<sub>(Or manually install `discord.py`, `prophet`, `geopy`, `matplotlib`, `pandas`, `requests`, `nest_asyncio`)</sub>

### 3. Create your Discord bot

* Go to [Discord Developer Portal](https://discord.com/developers/applications)
* Create a bot and copy the **bot token**
* Enable **"MESSAGE CONTENT INTENT"** under "Bot" settings

### 4. Run the bot

Edit the Python file and insert your token:

```python
DISCORD_TOKEN = "your-bot-token-here"
```

Then start:

```bash
python bot.py
```

---

## 💬 Commands

| Command        | Description                    |
| -------------- | ------------------------------ |
| `!rain <city>` | Forecast next 10 days rainfall |

*U.S. cities only (Open-Meteo supports U.S. lat/lon queries)*

---

## 📌 Example Use Cases

* 🌱 Agricultural planning and irrigation scheduling
* 🚛 Logistics & delivery weather prep
* 🏗️ Construction site safety
* 🎉 Outdoor event planning
* 📚 Weather education tools

---

## 📃 License

MIT License © 2025 \[Your Name]

---

## 🤝 Contribute

Pull requests are welcome! If you’d like to:

* Add support for worldwide locations
* Expand to temperature/alerts
* Build a web or mobile interface

Let’s collaborate! 🌍

---

## 🙋‍♂️ Questions?

Open an issue or reach out via Discord.

```

---

Would you like:
- A `requirements.txt` file to go with this?
- A deploy-to-Replit or Railway button?
- Auto-update feature for daily forecasts?

Let me know and I’ll package that for you!
```
