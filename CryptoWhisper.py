import tweepy
import requests
import textblob
import time
from datetime import datetime, timedelta

# API ключи для Twitter
API_KEY = 'your_twitter_api_key'
API_SECRET_KEY = 'your_twitter_api_secret'
ACCESS_TOKEN = 'your_twitter_access_token'
ACCESS_TOKEN_SECRET = 'your_twitter_access_token_secret'

# Список криптовалютных хэштегов для поиска
CRYPTO_HASHTAGS = ['#Bitcoin', '#Ethereum', '#Crypto', '#Blockchain', '#NFTs']

# Настройка Twitter API
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Функция для получения твитов
def get_tweets(query, count=100):
    try:
        tweets = tweepy.Cursor(api.search, q=query, lang="en", result_type="recent").items(count)
        return [tweet.text for tweet in tweets]
    except tweepy.TweepError as e:
        print(f"Error fetching tweets: {e}")
        return []

# Функция для анализа тональности текста
def analyze_sentiment(text):
    blob = textblob.TextBlob(text)
    return blob.sentiment.polarity  # Значение от -1 (негатив) до 1 (позитив)

# Основная логика анализа данных
def analyze_crypto_trends():
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for hashtag in CRYPTO_HASHTAGS:
        print(f"Analyzing tweets for {hashtag}...")
        tweets = get_tweets(hashtag)
        for tweet in tweets:
            sentiment = analyze_sentiment(tweet)
            if sentiment > 0.1:
                positive_count += 1
            elif sentiment < -0.1:
                negative_count += 1
            else:
                neutral_count += 1

    print(f"\nSentiment Analysis Results:")
    print(f"Positive Sentiment: {positive_count} tweets")
    print(f"Negative Sentiment: {negative_count} tweets")
    print(f"Neutral Sentiment: {neutral_count} tweets")

    if positive_count > negative_count:
        print("\nCrypto market might be on an uptrend! 🚀")
    elif negative_count > positive_count:
        print("\nCrypto market might be heading for a downturn... ⚠️")
    else:
        print("\nMarket sentiment is neutral, no clear trend detected.")

# Прогнозирование волатильности на основе трендов
def volatility_prediction():
    current_time = datetime.now()
    previous_time = current_time - timedelta(days=1)

    print(f"\nAnalyzing volatility for the past 24 hours: {previous_time.strftime('%Y-%m-%d %H:%M:%S')} to {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Пример: Пинг API для получения данных о криптовалютах
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "1"}
    response = requests.get(url, params=params).json()

    prices = response['prices']
    max_price = max(prices, key=lambda x: x[1])
    min_price = min(prices, key=lambda x: x[1])

    volatility = (max_price[1] - min_price[1]) / min_price[1] * 100
    print(f"24h Volatility: {volatility:.2f}%")

# Запуск основного процесса
if __name__ == "__main__":
    analyze_crypto_trends()
    volatility_prediction()
