"""
Stock Sentiment Analysis Page
美股情绪分析页面
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

from news_fetcher import NewsFetcher, get_news_with_cache
from sentiment_analyzer import (
    SentimentAnalyzer,
    SentimentLevel,
    get_sentiment_color,
    get_sentiment_emoji
)


def check_api_keys():
    """检查必要的API密钥是否配置"""
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    missing = []
    if not finnhub_key:
        missing.append("FINNHUB_API_KEY")
    if not anthropic_key:
        missing.append("ANTHROPIC_API_KEY")

    return missing


def render_sentiment_gauge(score: float, title: str = "情绪指数"):
    """渲染情绪仪表盘"""
    # 将 -1 到 1 的分数转换为 0 到 100
    gauge_value = (score + 1) * 50

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=gauge_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20, 'color': 'white'}},
        delta={'reference': 50, 'increasing': {'color': "#00C851"}, 'decreasing': {'color': "#FF4444"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#667eea"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 20], 'color': '#FF4444'},
                {'range': [20, 40], 'color': '#FF8800'},
                {'range': [40, 60], 'color': '#FFC107'},
                {'range': [60, 80], 'color': '#7CB342'},
                {'range': [80, 100], 'color': '#00C851'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': gauge_value
            }
        },
        number={'font': {'color': 'white'}}
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=300
    )

    return fig


def render_sentiment_distribution(bullish: int, bearish: int, neutral: int):
    """渲染情绪分布饼图"""
    labels = ['看涨', '中性', '看跌']
    values = [bullish, neutral, bearish]
    colors = ['#00C851', '#FFC107', '#FF4444']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors,
        textinfo='percent+label',
        textfont={'color': 'white'}
    )])

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        showlegend=True,
        legend={'font': {'color': 'white'}},
        height=300,
        title={'text': '新闻情绪分布', 'font': {'color': 'white', 'size': 16}}
    )

    return fig


def render_stock_sentiment_page():
    """渲染股票情绪分析页面"""

    st.markdown("""
        <style>
        .sentiment-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #2d2d44;
            margin: 10px 0;
        }
        .bullish-text { color: #00C851; font-weight: bold; }
        .bearish-text { color: #FF4444; font-weight: bold; }
        .neutral-text { color: #FFC107; font-weight: bold; }
        .news-item {
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
        }
        .stock-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 页面标题
    st.markdown("""
        <div class="stock-header">
            <h1 style="color: white; margin: 0;">📊 美股情绪分析</h1>
            <p style="color: rgba(255,255,255,0.8); margin-top: 10px;">
                基于AI的新闻情绪分析，帮助您了解市场情绪走向
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 检查API密钥
    missing_keys = check_api_keys()
    if missing_keys:
        st.error(f"缺少必要的API密钥: {', '.join(missing_keys)}")
        st.info("""
        请在 `.env` 文件中配置以下密钥:
        - `FINNHUB_API_KEY`: 从 https://finnhub.io/ 获取（免费）
        - `ANTHROPIC_API_KEY`: 从 https://console.anthropic.com/ 获取
        """)
        return

    # 初始化API客户端
    try:
        news_fetcher = NewsFetcher()
        sentiment_analyzer = SentimentAnalyzer()
    except Exception as e:
        st.error(f"初始化API客户端失败: {str(e)}")
        return

    # 侧边栏配置
    st.sidebar.markdown("### 🔍 分析设置")

    # 股票搜索
    symbol_input = st.sidebar.text_input(
        "输入股票代码",
        value="AAPL",
        placeholder="例如: AAPL, TSLA, NVDA"
    ).upper()

    # 搜索建议
    if symbol_input and len(symbol_input) >= 1:
        with st.sidebar.expander("搜索股票"):
            try:
                search_results = news_fetcher.search_symbol(symbol_input)
                for result in search_results[:5]:
                    st.write(f"**{result['symbol']}** - {result['description'][:30]}...")
            except Exception:
                pass

    days_back = st.sidebar.slider("新闻时间范围（天）", 1, 30, 7)

    analyze_button = st.sidebar.button("🚀 开始分析", type="primary", use_container_width=True)

    # 主内容区
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📈 股票信息")

        if analyze_button or 'last_symbol' in st.session_state:
            current_symbol = symbol_input if analyze_button else st.session_state.get('last_symbol', symbol_input)

            if analyze_button:
                st.session_state['last_symbol'] = symbol_input

            with st.spinner(f"正在获取 {current_symbol} 的数据..."):
                try:
                    # 获取股票报价
                    quote = news_fetcher.get_stock_quote(current_symbol)

                    # 显示股票信息卡片
                    price_change_color = "#00C851" if quote['change'] >= 0 else "#FF4444"
                    change_symbol = "+" if quote['change'] >= 0 else ""

                    st.markdown(f"""
                        <div class="sentiment-card">
                            <h2 style="color: white; margin: 0;">{current_symbol}</h2>
                            <h1 style="color: white; margin: 10px 0;">${quote['current_price']:.2f}</h1>
                            <p style="color: {price_change_color}; font-size: 1.2rem;">
                                {change_symbol}{quote['change']:.2f} ({change_symbol}{quote['change_percent']:.2f}%)
                            </p>
                            <p style="color: rgba(255,255,255,0.6);">
                                高: ${quote['high']:.2f} | 低: ${quote['low']:.2f} |
                                开盘: ${quote['open']:.2f}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.warning(f"获取股票报价失败: {str(e)}")

    with col2:
        if analyze_button or 'last_analysis' in st.session_state:
            if analyze_button:
                with st.spinner("AI正在分析新闻情绪..."):
                    try:
                        # 获取新闻
                        news_list = get_news_with_cache(news_fetcher, symbol_input, days_back)

                        if news_list:
                            # 批量分析
                            overall = sentiment_analyzer.analyze_batch_news(news_list, symbol_input)
                            st.session_state['last_analysis'] = overall
                            st.session_state['last_news'] = news_list
                        else:
                            st.warning("未找到相关新闻")
                            return

                    except Exception as e:
                        st.error(f"分析失败: {str(e)}")
                        return

            if 'last_analysis' in st.session_state:
                overall = st.session_state['last_analysis']

                # 显示情绪仪表盘
                gauge_fig = render_sentiment_gauge(overall.overall_score, "市场情绪")
                st.plotly_chart(gauge_fig, use_container_width=True)

    # 详细分析结果
    if 'last_analysis' in st.session_state:
        overall = st.session_state['last_analysis']
        news_list = st.session_state.get('last_news', [])

        st.markdown("---")
        st.markdown("### 📊 情绪分析报告")

        # 统计卡片
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            sentiment_emoji = get_sentiment_emoji(overall.overall_sentiment)
            st.metric(
                "整体情绪",
                f"{sentiment_emoji} {overall.overall_sentiment.value}",
                delta=f"{overall.overall_score:.2f}"
            )

        with col2:
            st.metric("分析新闻数", overall.news_count)

        with col3:
            st.metric("看涨新闻", overall.bullish_count, delta_color="normal")

        with col4:
            st.metric("看跌新闻", overall.bearish_count, delta_color="inverse")

        # 图表行
        col1, col2 = st.columns(2)

        with col1:
            # 情绪分布
            dist_fig = render_sentiment_distribution(
                overall.bullish_count,
                overall.bearish_count,
                overall.neutral_count
            )
            st.plotly_chart(dist_fig, use_container_width=True)

        with col2:
            # 关键主题
            st.markdown("#### 🏷️ 关键主题")
            for theme in overall.key_themes:
                st.markdown(f"- {theme}")

            st.markdown("#### ⚠️ 风险因素")
            for risk in overall.risk_factors:
                st.markdown(f"- {risk}")

        # AI建议
        st.markdown("---")
        st.markdown("### 💡 AI分析建议")
        st.info(overall.recommendation)
        st.caption("⚠️ 免责声明：以上分析仅供参考，不构成投资建议。投资有风险，决策需谨慎。")

        # 新闻列表
        st.markdown("---")
        st.markdown("### 📰 相关新闻")

        for news in news_list[:10]:
            news_time = news['datetime'].strftime("%Y-%m-%d %H:%M") if news['datetime'] else "未知时间"
            st.markdown(f"""
                <div class="news-item">
                    <h4 style="color: white; margin: 0 0 10px 0;">
                        <a href="{news['url']}" target="_blank" style="color: #667eea; text-decoration: none;">
                            {news['headline']}
                        </a>
                    </h4>
                    <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">
                        {news['summary'][:200]}...
                    </p>
                    <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin-top: 10px;">
                        📰 {news['source']} | 🕐 {news_time}
                    </p>
                </div>
            """, unsafe_allow_html=True)

    else:
        # 默认提示
        st.info("👆 在左侧输入股票代码并点击「开始分析」按钮")

        # 热门股票快捷按钮
        st.markdown("### 🔥 热门股票")
        hot_stocks = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META"]

        cols = st.columns(len(hot_stocks))
        for i, stock in enumerate(hot_stocks):
            with cols[i]:
                if st.button(stock, key=f"hot_{stock}"):
                    st.session_state['last_symbol'] = stock
                    st.rerun()


if __name__ == "__main__":
    render_stock_sentiment_page()
