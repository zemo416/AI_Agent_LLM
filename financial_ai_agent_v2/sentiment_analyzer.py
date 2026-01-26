"""
Sentiment Analyzer Module
使用Claude API进行股市新闻情绪分析
"""

import os
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import anthropic


class SentimentLevel(Enum):
    """情绪等级"""
    VERY_BULLISH = "非常看涨"
    BULLISH = "看涨"
    NEUTRAL = "中性"
    BEARISH = "看跌"
    VERY_BEARISH = "非常看跌"


@dataclass
class SentimentResult:
    """情绪分析结果"""
    headline: str
    sentiment: SentimentLevel
    score: float  # -1 到 1
    confidence: float  # 0 到 1
    key_factors: List[str]
    impact_duration: str  # 短期/中期/长期
    summary: str


@dataclass
class OverallSentiment:
    """整体情绪汇总"""
    symbol: str
    overall_sentiment: SentimentLevel
    overall_score: float
    news_count: int
    bullish_count: int
    bearish_count: int
    neutral_count: int
    key_themes: List[str]
    recommendation: str
    risk_factors: List[str]


class SentimentAnalyzer:
    """Claude情绪分析引擎"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"

    def analyze_single_news(self, news: Dict) -> SentimentResult:
        """
        分析单条新闻的情绪

        Args:
            news: 新闻数据字典

        Returns:
            SentimentResult对象
        """
        prompt = f"""分析以下股市新闻的情绪和市场影响。

标题: {news.get('headline', '')}
摘要: {news.get('summary', '')}
来源: {news.get('source', '')}
股票代码: {news.get('symbol', '')}

请以JSON格式返回分析结果:
{{
    "sentiment": "VERY_BULLISH/BULLISH/NEUTRAL/BEARISH/VERY_BEARISH",
    "score": 0.0,  // -1到1之间的数值，-1最看跌，1最看涨
    "confidence": 0.0,  // 0到1之间，表示分析的置信度
    "key_factors": ["因素1", "因素2"],  // 影响判断的关键因素
    "impact_duration": "短期/中期/长期",  // 预计影响持续时间
    "summary": "简短的分析总结"
}}

只返回JSON，不要其他内容。"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text.strip()
            # 清理可能的markdown代码块标记
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            result_text = result_text.strip()

            result = json.loads(result_text)

            sentiment_map = {
                "VERY_BULLISH": SentimentLevel.VERY_BULLISH,
                "BULLISH": SentimentLevel.BULLISH,
                "NEUTRAL": SentimentLevel.NEUTRAL,
                "BEARISH": SentimentLevel.BEARISH,
                "VERY_BEARISH": SentimentLevel.VERY_BEARISH
            }

            return SentimentResult(
                headline=news.get('headline', ''),
                sentiment=sentiment_map.get(result["sentiment"], SentimentLevel.NEUTRAL),
                score=float(result["score"]),
                confidence=float(result["confidence"]),
                key_factors=result["key_factors"],
                impact_duration=result["impact_duration"],
                summary=result["summary"]
            )

        except Exception as e:
            # 返回默认中性结果
            return SentimentResult(
                headline=news.get('headline', ''),
                sentiment=SentimentLevel.NEUTRAL,
                score=0.0,
                confidence=0.0,
                key_factors=[f"分析失败: {str(e)}"],
                impact_duration="未知",
                summary="无法完成分析"
            )

    def analyze_batch_news(
        self,
        news_list: List[Dict],
        symbol: str
    ) -> OverallSentiment:
        """
        批量分析新闻并生成整体情绪报告

        Args:
            news_list: 新闻列表
            symbol: 股票代码

        Returns:
            OverallSentiment对象
        """
        if not news_list:
            return OverallSentiment(
                symbol=symbol,
                overall_sentiment=SentimentLevel.NEUTRAL,
                overall_score=0.0,
                news_count=0,
                bullish_count=0,
                bearish_count=0,
                neutral_count=0,
                key_themes=[],
                recommendation="无足够数据进行分析",
                risk_factors=[]
            )

        # 准备新闻摘要
        news_summaries = []
        for i, news in enumerate(news_list[:15]):  # 限制15条避免token过长
            news_summaries.append(
                f"{i+1}. [{news.get('source', 'Unknown')}] {news.get('headline', '')}"
            )

        news_text = "\n".join(news_summaries)

        prompt = f"""作为金融分析师，分析以下关于{symbol}的新闻汇总，给出整体市场情绪判断。

近期新闻列表:
{news_text}

请以JSON格式返回综合分析:
{{
    "overall_sentiment": "VERY_BULLISH/BULLISH/NEUTRAL/BEARISH/VERY_BEARISH",
    "overall_score": 0.0,  // -1到1
    "bullish_count": 0,  // 利好新闻数量
    "bearish_count": 0,  // 利空新闻数量
    "neutral_count": 0,  // 中性新闻数量
    "key_themes": ["主题1", "主题2", "主题3"],  // 主要新闻主题
    "recommendation": "基于当前新闻情绪的投资建议（仅供参考，不构成投资建议）",
    "risk_factors": ["风险1", "风险2"]  // 需要关注的风险因素
}}

只返回JSON，不要其他内容。"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text.strip()
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            result_text = result_text.strip()

            result = json.loads(result_text)

            sentiment_map = {
                "VERY_BULLISH": SentimentLevel.VERY_BULLISH,
                "BULLISH": SentimentLevel.BULLISH,
                "NEUTRAL": SentimentLevel.NEUTRAL,
                "BEARISH": SentimentLevel.BEARISH,
                "VERY_BEARISH": SentimentLevel.VERY_BEARISH
            }

            return OverallSentiment(
                symbol=symbol,
                overall_sentiment=sentiment_map.get(
                    result["overall_sentiment"],
                    SentimentLevel.NEUTRAL
                ),
                overall_score=float(result["overall_score"]),
                news_count=len(news_list),
                bullish_count=int(result["bullish_count"]),
                bearish_count=int(result["bearish_count"]),
                neutral_count=int(result["neutral_count"]),
                key_themes=result["key_themes"],
                recommendation=result["recommendation"],
                risk_factors=result["risk_factors"]
            )

        except Exception as e:
            return OverallSentiment(
                symbol=symbol,
                overall_sentiment=SentimentLevel.NEUTRAL,
                overall_score=0.0,
                news_count=len(news_list),
                bullish_count=0,
                bearish_count=0,
                neutral_count=0,
                key_themes=[],
                recommendation=f"分析失败: {str(e)}",
                risk_factors=[]
            )


def get_sentiment_color(sentiment: SentimentLevel) -> str:
    """获取情绪对应的颜色代码"""
    colors = {
        SentimentLevel.VERY_BULLISH: "#00C851",
        SentimentLevel.BULLISH: "#7CB342",
        SentimentLevel.NEUTRAL: "#FFC107",
        SentimentLevel.BEARISH: "#FF8800",
        SentimentLevel.VERY_BEARISH: "#FF4444"
    }
    return colors.get(sentiment, "#FFC107")


def get_sentiment_emoji(sentiment: SentimentLevel) -> str:
    """获取情绪对应的emoji"""
    emojis = {
        SentimentLevel.VERY_BULLISH: "🚀",
        SentimentLevel.BULLISH: "📈",
        SentimentLevel.NEUTRAL: "➡️",
        SentimentLevel.BEARISH: "📉",
        SentimentLevel.VERY_BEARISH: "💥"
    }
    return emojis.get(sentiment, "➡️")
