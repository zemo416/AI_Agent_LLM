"""
Finnhub News Fetcher Module
获取美股相关新闻数据
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time


class NewsFetcher:
    """Finnhub新闻数据获取器"""

    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")
        if not self.api_key:
            raise ValueError("FINNHUB_API_KEY is required")

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """发送API请求"""
        params["token"] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def get_company_news(
        self,
        symbol: str,
        days_back: int = 7
    ) -> List[Dict]:
        """
        获取特定股票的新闻

        Args:
            symbol: 股票代码 (如 AAPL, TSLA)
            days_back: 获取多少天内的新闻

        Returns:
            新闻列表
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        params = {
            "symbol": symbol.upper(),
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d")
        }

        news = self._make_request("company-news", params)

        # 格式化返回数据
        formatted_news = []
        for item in news:
            formatted_news.append({
                "id": item.get("id"),
                "headline": item.get("headline", ""),
                "summary": item.get("summary", ""),
                "source": item.get("source", ""),
                "url": item.get("url", ""),
                "datetime": datetime.fromtimestamp(item.get("datetime", 0)),
                "symbol": symbol.upper(),
                "category": item.get("category", ""),
                "related": item.get("related", "")
            })

        return formatted_news

    def get_market_news(self, category: str = "general") -> List[Dict]:
        """
        获取市场整体新闻

        Args:
            category: 新闻类别 (general, forex, crypto, merger)

        Returns:
            新闻列表
        """
        params = {"category": category}
        news = self._make_request("news", params)

        formatted_news = []
        for item in news:
            formatted_news.append({
                "id": item.get("id"),
                "headline": item.get("headline", ""),
                "summary": item.get("summary", ""),
                "source": item.get("source", ""),
                "url": item.get("url", ""),
                "datetime": datetime.fromtimestamp(item.get("datetime", 0)),
                "category": item.get("category", ""),
                "image": item.get("image", "")
            })

        return formatted_news

    def get_stock_quote(self, symbol: str) -> Dict:
        """
        获取股票实时报价

        Args:
            symbol: 股票代码

        Returns:
            报价信息
        """
        params = {"symbol": symbol.upper()}
        quote = self._make_request("quote", params)

        return {
            "symbol": symbol.upper(),
            "current_price": quote.get("c", 0),
            "change": quote.get("d", 0),
            "change_percent": quote.get("dp", 0),
            "high": quote.get("h", 0),
            "low": quote.get("l", 0),
            "open": quote.get("o", 0),
            "previous_close": quote.get("pc", 0),
            "timestamp": datetime.fromtimestamp(quote.get("t", 0))
        }

    def search_symbol(self, query: str) -> List[Dict]:
        """
        搜索股票代码

        Args:
            query: 搜索关键词

        Returns:
            匹配的股票列表
        """
        params = {"q": query}
        result = self._make_request("search", params)

        symbols = []
        for item in result.get("result", []):
            symbols.append({
                "symbol": item.get("symbol", ""),
                "description": item.get("description", ""),
                "type": item.get("type", "")
            })

        return symbols[:10]  # 返回前10个结果


class NewsCache:
    """简单的新闻缓存，避免频繁API调用"""

    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, key: str) -> Optional[List[Dict]]:
        """获取缓存"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: List[Dict]):
        """设置缓存"""
        self.cache[key] = (value, time.time())

    def clear(self):
        """清空缓存"""
        self.cache = {}


# 全局缓存实例
news_cache = NewsCache()


def get_news_with_cache(
    fetcher: NewsFetcher,
    symbol: str,
    days_back: int = 7
) -> List[Dict]:
    """带缓存的新闻获取"""
    cache_key = f"{symbol}_{days_back}"

    cached = news_cache.get(cache_key)
    if cached:
        return cached

    news = fetcher.get_company_news(symbol, days_back)
    news_cache.set(cache_key, news)

    return news
