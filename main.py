import os
import requests
import json

# GitHub Secrets에서 보안 정보를 가져옵니다
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_latest_trend():
    """글로벌 IT 트렌드 1순위를 가져옵니다."""
    try:
        top_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
        news = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{top_ids[0]}.json").json()
        title = news.get('title')
        url = news.get('url', f"https://news.ycombinator.com/item?id={top_ids[0]}")
        return f"제목: {title}\n링크: {url}"
    except:
        return "데이터 수집 지연"

def run_intelligence():
    news_data = get_latest_trend()
    
    # 2026년 표준 Gemini 2.5 API 직접 호출
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": f"당신은 글로벌 전략 비서 Alpha-Nexus입니다. 다음 뉴스의 비즈니스 기회를 날카롭게 1문장 요약하세요: {news_data}"}]}]
    }

    try:
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        strategy = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        # 텔레그램 전송
        report = f"🏆 [Alpha-Nexus HQ 무인 보고]\n\n{strategy}\n\n🔗 {news_data}"
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={report}")
        print("✅ 보고 완료!")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    run_intelligence()
