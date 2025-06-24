!pip install discord.py nest_asyncio pandas matplotlib prophet requests geopy --quiet
DISCORD_TOKEN = ""
import discord
from discord.ext import commands
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import requests
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import asyncio
import nest_asyncio
import matplotlib.dates as mdates

nest_asyncio.apply()


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# 📍 Geocode U.S. city name to lat/lon
def get_us_city_coordinates(city):
    geolocator = Nominatim(user_agent="discord-rain-bot")
    location = geolocator.geocode(city + ", USA")
    if not location:
        raise ValueError("City not found")
    return location.latitude, location.longitude

# ☔ Fetch 1 year of historical daily rainfall data
def get_rainfall_data(lat, lon):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=365)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}"
        f"&daily=precipitation_sum&timezone=auto"
    )
    response = requests.get(url).json()
    if "daily" not in response:
        raise ValueError("Rainfall data not available")

    df = pd.DataFrame({
        "ds": pd.to_datetime(response["daily"]["time"]),
        "y": response["daily"]["precipitation_sum"]
    })
    return df

# 📈 Forecast + Simple Chart + Summary
def forecast_rainfall(df, city):
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=10)
    forecast = model.predict(future)

    # Forecasted data only (next 10 days)
    forecast_range = forecast.tail(10)

    # Combine with last 30 days of real data
    recent_data = df.tail(30)
    combined = pd.concat([
        pd.DataFrame({'ds': pd.to_datetime(recent_data['ds']), 'rainfall': recent_data['y'], 'type': 'Actual'}),
        pd.DataFrame({'ds': pd.to_datetime(forecast_range['ds']), 'rainfall': forecast_range['yhat'], 'type': 'Forecast'})
    ])

    # 📊 Plot as simple bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = {'Actual': '#4a90e2', 'Forecast': '#f39c12'}
    for label, group in combined.groupby('type'):
        ax.bar(group['ds'], group['rainfall'], label=label, color=colors[label], width=0.8)

    # Highlight "Today"
    today = pd.to_datetime(df['ds'].iloc[-1])
    ax.axvline(today, color='red', linestyle='--', label='Today')

    ax.set_title(f"☔ Rainfall: Last 30 Days + 10-Day Forecast\n📍 {city.title()}", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Rainfall (mm)")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    chart_path = f"{city.lower().replace(' ', '_')}_forecast.png"
    plt.savefig(chart_path)
    plt.close(fig)

    # 📝 Text summary
    avg_rain = forecast_range['yhat'].mean()
    max_day = forecast_range.loc[forecast_range['yhat'].idxmax()]
    min_day = forecast_range.loc[forecast_range['yhat'].idxmin()]

    summary = (
        f"📍 **{city.title()} Rainfall Forecast (Next 10 Days)**\n\n"
        f"📊 Average rain: **{avg_rain:.1f} mm/day**\n"
        f"🌧️ Most rain: **{max_day['ds'].date()} — {max_day['yhat']:.1f} mm**\n"
        f"🌤️ Least rain: **{min_day['ds'].date()} — {min_day['yhat']:.1f} mm**"
    )

    return chart_path, summary

# 🎯 Discord Command
@bot.command()
async def rain(ctx, *, city="New York"):
    await ctx.send(f"🌍 Getting rainfall forecast for **{city.title()}**...")

    try:
        lat, lon = get_us_city_coordinates(city)
        df = get_rainfall_data(lat, lon)
        chart_path, summary = forecast_rainfall(df, city)
        await ctx.send(summary)
        await ctx.send(file=discord.File(chart_path))
    except Exception as e:
        print("Error:", e)
        await ctx.send("❌ Could not retrieve or forecast rainfall. Try another U.S. city.")

# ▶️ Start Bot
async def start_bot():
    await bot.start(DISCORD_TOKEN)

await start_bot()

