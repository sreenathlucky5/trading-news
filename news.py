# =====================================================
# ELITE GLOBAL + INDIAN MARKET & CRYPTO ALERT TELEGRAM BOT
# SAFE VERSION WITH ERROR HANDLING
# =====================================================

import feedparser
import requests
from datetime import datetime
import pytz  # timezone support

# ---------------- TELEGRAM CONFIG ----------------
BOT_TOKEN = "8505207910:AAEoQz_86_4bu412JQK0rJ4gKihgNbuz2vU"
CHAT_ID = "1301385888"
TG_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# ---------------- RSS FEEDS ----------------
RSS_FEEDS = [
    # Global macro & finance
    "https://www.reuters.com/rssFeed/businessNews",
    "https://www.reuters.com/rssFeed/worldNews",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "https://www.investing.com/rss/news.rss",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.marketwatch.com/rss/topstories",
    # Indian business & finance
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "http://www.moneycontrol.com/rss/latestnews.xml",
    "https://www.livemint.com/rss/markets",
    "https://www.livemint.com/rss/money",
    "https://www.goodreturns.in/rss/feeds/news-fb.xml",
    "https://www.goodreturns.in/rss/feeds/money-news-fb.xml",
    "https://www.businessleague.in/category/stock-markets/feed",
    "https://www.businessleague.in/category/economy/feed",
    # Geo-political
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.bbc.com/news/world/rss.xml",
    # Crypto
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss"
]

# ---------------- FETCH NEWS WITH ERROR HANDLING ----------------
def fetch_news():
    headlines = []
    for feed in RSS_FEEDS:
        try:
            data = feedparser.parse(feed)
            for entry in data.entries[:2]:  # take top 2 news per feed
                headlines.append(entry.title)
        except Exception as e:
            print(f"[Warning] Failed to fetch feed: {feed} | Error: {e}")
    return list(set(headlines))  # remove duplicates

# ---------------- ANALYZE NEWS IMPACT ----------------
def analyze_impact(news_list):
    report = ""
    score = 0

    for h in news_list:
        hl = h.lower()

        # CENTRAL BANK
        if any(k in hl for k in ["fed", "rate cut", "dovish", "pause"]):
            report += f"• {h}\nImpact: Liquidity ↑ → Crypto, Stocks ↑\n\n"
            score += 5
        elif any(k in hl for k in ["rate hike", "hawkish", "inflation surge"]):
            report += f"• {h}\nImpact: Liquidity ↓ → Risk-OFF\n\n"
            score -= 5

        # INFLATION / ECON DATA
        elif any(k in hl for k in ["cpi", "inflation", "jobs data", "gdp"]):
            report += f"• {h}\nImpact: Rate / growth expectations shift\n\n"
            score += 3

        # WAR / SANCTIONS
        elif any(k in hl for k in ["war", "conflict", "sanction", "attack"]):
            report += f"• {h}\nImpact: Oil & Gold ↑ → Crypto volatile\n\n"
            score -= 4

        # POLITICIANS
        elif any(k in hl for k in ["president", "prime minister", "treasury", "minister"]):
            report += f"• {h}\nImpact: FX & global sentiment shift\n\n"
            score -= 2

        # CRYPTO REGULATION / ETF
        elif any(k in hl for k in ["bitcoin etf", "crypto regulation", "ban", "sec"]):
            report += f"• {h}\nImpact: Direct Crypto Exchange Reaction\n\n"
            score += 4

    return report, score

# ---------------- DETERMINE MARKET BIAS ----------------
def determine_bias(score):
    if score >= 8:
        return "🟢 STRONG RISK-ON (Buy dips, momentum favored)"
    elif score <= -8:
        return "🔴 STRONG RISK-OFF (Capital protection mode)"
    else:
        return "🟡 MIXED / WAIT & WATCH"

# ---------------- SEND TELEGRAM ALERT ----------------
def send_alert():
    try:
        news = fetch_news()
        analysis, score = analyze_impact(news)
        bias = determine_bias(score)

        ist = pytz.timezone("Asia/Kolkata")
        message = f"""
🚨 *GLOBAL + INDIAN MARKET & CRYPTO ALERT*
🕒 {datetime.now(ist).strftime('%d %b %Y | %H:%M IST')}

🔥 *TOP MARKET-MOVING NEWS*
{analysis if analysis else "• No major expectation-changing news"}

📊 *TRADING SENTIMENT*
{bias}

⚠️ Focus on liquidity, not noise.
"""

        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(TG_URL, data=payload)
        if response.status_code == 200:
            print("[Success] Alert sent to Telegram ✅")
        else:
            print(f"[Error] Failed to send Telegram alert | Status Code: {response.status_code}")
    except Exception as e:
        print(f"[Error] Failed to send alert: {e}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    send_alert()
