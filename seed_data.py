import os, django, uuid, random
os.environ['DJANGO_SETTINGS_MODULE'] = 'algoedge.settings'
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from home.models import Testimonial, FAQ
from cservice.models import Service
from learn.models import CourseCategory, Course, Lesson
from articles.models import Category, Post
from shop.models import ProductCategory, Product
from pfarm.models import PropFirm
from copytrade.models import MasterTrader
from alerts.models import Notification

print("=== Seeding AlgoEdge Test Data ===\n")

# 1. Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@algoedge.com', 'admin123')
    print("Admin created: admin / admin123")
else:
    print("Admin already exists")

# 2. Testimonials
if not Testimonial.objects.exists():
    Testimonial.objects.create(name='John Smith', title='Professional Trader', content='AlgoEdge transformed my trading completely. Their EA development service helped me automate my strategy and achieve consistent profits month after month.', rating=5, is_featured=True, order=1)
    Testimonial.objects.create(name='Sarah Johnson', title='Prop Firm Trader', content='Passed my FTMO challenge on the first attempt using their prop firm management tools. The drawdown monitoring is absolutely brilliant.', rating=5, is_featured=True, order=2)
    Testimonial.objects.create(name='Michael Chen', title='Algorithmic Developer', content='The academy courses are incredibly detailed. I went from zero coding knowledge to building my own EAs in just 3 months.', rating=5, is_featured=True, order=3)
    Testimonial.objects.create(name='Emma Williams', title='Copy Trading Investor', content='The copy trading platform is fantastic. I have been consistently earning passive income by following top traders.', rating=5, is_featured=True, order=4)
    print("Testimonials created ✓")
else:
    print("Testimonials already exist")

# 3. FAQs
if not FAQ.objects.exists():
    FAQ.objects.create(question='What is AlgoEdge?', answer='AlgoEdge is a comprehensive algorithmic trading platform offering EA development, prop firm management, copy trading, education, and premium trading tools for traders of all levels.', category='general', order=1)
    FAQ.objects.create(question='How do I get started?', answer='Simply create a free account and explore our services. You can browse courses, purchase EAs, or submit a custom development request.', category='general', order=2)
    FAQ.objects.create(question='Do I need coding experience?', answer='No! We handle all the technical development. You just need to describe your strategy and we convert it into a fully automated EA for MT4/MT5.', category='services', order=3)
    FAQ.objects.create(question='What platforms do you support?', answer='We support MT4, MT5, and cTrader platforms for our EAs and trading tools.', category='services', order=4)
    FAQ.objects.create(question='How does the Free EA program work?', answer='Register a trading account through our broker affiliate link, submit your account for verification, and unlock premium EAs for free.', category='broker', order=5)
    FAQ.objects.create(question='What is your prop firm pass rate?', answer='Our specialized EAs have a 98% pass rate across major prop firms including FTMO, MyForexFunds, and E8 Markets.', category='propfirm', order=6)
    FAQ.objects.create(question='How does copy trading work?', answer='You select a master trader, allocate funds, and our system automatically mirrors their trades to your account with full risk management.', category='copytrading', order=7)
    FAQ.objects.create(question='What payment methods do you accept?', answer='We accept Stripe (credit/debit cards), PayPal, M-Pesa, cryptocurrency, and bank transfers.', category='payment', order=8)
    print("FAQs created ✓")
else:
    print("FAQs already exist")

# 4. Services
if not Service.objects.exists():
    services = [
        ('Expert Advisor Development', 'We convert your trading strategy into a fully automated Expert Advisor for MT4/MT5 platforms with advanced risk management, money management, and optimization.', 'fas fa-code', 299, 1),
        ('Custom Indicators', 'Professional-grade custom indicators designed to your exact specifications for better market analysis and trading decisions.', 'fas fa-chart-bar', 149, 2),
        ('Trading Bots', '24/7 automated trading bots that execute your strategies without emotions, hesitation, or human error across multiple markets.', 'fas fa-robot', 499, 3),
        ('Strategy Backtesting', 'Comprehensive backtesting across multiple market conditions with detailed performance reports including Sharpe ratio, drawdown analysis, and optimization.', 'fas fa-history', 99, 4),
        ('Trading Consultation', 'One-on-one consultation with experienced algorithmic trading professionals to refine your strategies.', 'fas fa-handshake', None, 5),
        ('Algorithm Optimization', 'Fine-tune your algorithms for maximum performance and minimal drawdown using advanced optimization techniques.', 'fas fa-microchip', 199, 6),
        ('Copy Trading Setup', 'Professional copy trading infrastructure with signal management, performance tracking, and automated execution.', 'fas fa-copy', None, 7),
        ('Prop Firm Assistance', 'Expert guidance and specialized EAs designed specifically to pass prop firm challenges with a 98% success rate.', 'fas fa-trophy', 399, 8),
        ('Risk Management Tools', 'Advanced risk management systems including position sizing calculators, drawdown monitors, and portfolio risk analyzers.', 'fas fa-shield-alt', 149, 9),
        ('Signal Services', 'Real-time trading signals with verified performance track records from professional traders.', 'fas fa-signal', 49, 10),
        ('Trading Journal', 'Professional trading journal with advanced analytics, trade import, performance metrics, and psychological insights.', 'fas fa-book', 79, 11),
        ('Portfolio Analysis', 'Comprehensive portfolio analysis with risk metrics, correlation analysis, and optimization recommendations.', 'fas fa-chart-pie', 129, 12),
    ]
    for title, desc, icon, price, order in services:
        Service.objects.create(title=title, description=desc, icon=icon, price_from=price, order=order)
    print("12 Services created ✓")
else:
    print("Services already exist")

# 5. Course Categories & Courses
cat_fx, _ = CourseCategory.objects.get_or_create(name='Forex Trading', defaults={'slug': 'forex-trading', 'icon': 'fas fa-chart-line'})
cat_algo, _ = CourseCategory.objects.get_or_create(name='Algorithmic Trading', defaults={'slug': 'algorithmic-trading', 'icon': 'fas fa-robot'})
cat_prog, _ = CourseCategory.objects.get_or_create(name='Programming', defaults={'slug': 'programming', 'icon': 'fas fa-code'})

if not Course.objects.exists():
    courses_data = [
        (cat_fx, 'Forex Fundamentals', 'Learn the basics of Forex trading including currency pairs, pips, leverage, and market mechanics.', 'beginner', 0, True, 10, 4.7),
        (cat_fx, 'Advanced Price Action', 'Master price action trading with candlestick patterns, support/resistance, and market structure analysis.', 'advanced', 149, 12, 18, 4.8),
        (cat_fx, 'Risk Management Mastery', 'Essential risk management techniques every trader must know to protect capital and maximize returns.', 'intermediate', 0, True, 8, 4.9),
        (cat_fx, 'Trading Psychology', 'Develop the mindset of successful traders. Overcome fear, greed, and emotional trading.', 'beginner', 0, True, 6, 4.6),
        (cat_algo, 'Introduction to Algorithmic Trading', 'Understand the fundamentals of automated trading systems and how to design profitable algorithms.', 'beginner', 199, 15, 20, 4.7),
        (cat_algo, 'MQL5 Programming Masterclass', 'Complete course on MQL5 programming for MetaTrader 5. Build EAs, indicators, and scripts from scratch.', 'advanced', 299, 30, 40, 4.9),
        (cat_algo, 'Python for Traders', 'Learn Python programming specifically for trading applications including data analysis and backtesting.', 'intermediate', 199, 20, 24, 4.8),
        (cat_prog, 'Django for Fintech', 'Build production-ready fintech applications with Django. Covers APIs, payments, and security.', 'advanced', 249, 25, 30, 4.5),
    ]
    for cat, title, desc, level, price, hours, lessons, rating in courses_data:
        Course.objects.create(
            category=cat, title=title, short_description=desc[:200],
            description=desc, level=level, price=price,
            is_free=(price == 0), duration_hours=hours, lessons_count=lessons,
            rating=rating,             enrolled_students=random.randint(50, 500),
            is_published=True, has_certificate=True
        )
    print("8 Courses created ✓")
else:
    print("Courses already exist")

# Add lessons to courses
for course in Course.objects.all():
    if not course.lessons.exists():
        for i in range(1, min(course.lessons_count + 1, 6)):
            Lesson.objects.create(
                course=course,
                title=f'{course.title}: Lesson {i}',
                content=f'This is the content for lesson {i} of {course.title}. In this lesson you will learn key concepts and practical applications.',
                duration_minutes=random.randint(10, 45),
                order=i,
                is_free=(i == 1)
            )
        print(f"  Lessons added to: {course.title}")

# 6. Blog Categories & Posts
blog_cats = {}
for name, slug in [('Market Analysis', 'market-analysis'), ('Trading Tips', 'trading-tips'), ('Prop Firm News', 'prop-firm-news'), ('AI Trading', 'ai-trading')]:
    cat, _ = Category.objects.get_or_create(name=name, defaults={'slug': slug})
    blog_cats[name] = cat

admin_user = User.objects.get(username='admin')

if not Post.objects.exists():
    posts = [
        (blog_cats['Market Analysis'], 'EUR/USD Weekly Outlook: Bulls Eye Key Resistance', 'Market analysis for the week ahead. The EUR/USD pair is showing strong bullish momentum with key resistance levels being tested. Technical indicators suggest a potential breakout if the 1.0950 level is breached. Support levels remain solid at 1.0850.', True),
        (blog_cats['Trading Tips'], '5 Essential Risk Management Rules for Algorithmic Traders', 'Risk management is the cornerstone of successful algorithmic trading. Here are 5 essential rules: 1) Never risk more than 1-2% per trade, 2) Always use stop losses, 3) Diversify across strategies, 4) Monitor drawdown daily, 5) Keep a trading journal.', True),
        (blog_cats['Prop Firm News'], 'FTMO Announces New Challenge Rules for 2026', 'FTMO has updated their challenge rules for 2026. Key changes include reduced profit targets, extended trading periods, and new risk parameters. Our EAs have already been updated to comply with these changes.', True),
        (blog_cats['AI Trading'], 'How Machine Learning is Transforming Trading', 'Artificial intelligence and machine learning are revolutionizing algorithmic trading. From predictive models to adaptive strategies, AI-powered systems are achieving unprecedented results in market analysis and trade execution.', False),
        (blog_cats['Trading Tips'], 'Beginner Guide to Backtesting Your Strategy', 'Backtesting is crucial for validating your trading strategy. This guide covers everything from data selection to performance metrics including Sharpe ratio, maximum drawdown, and profit factor.', False),
    ]
    for cat, title, content, featured in posts:
        Post.objects.create(
            author=admin_user, category=cat, title=title,
            content=content, excerpt=content[:200],
            status='published', is_featured=featured,
            published_at=timezone.now()
        )
    print("6 Blog posts created ✓")

# 7. Product Categories & Products
prod_cats = {}
for name, slug, icon in [('Expert Advisors', 'expert-advisors', 'fas fa-robot'), ('Indicators', 'indicators', 'fas fa-chart-bar'), ('Trading Templates', 'trading-templates', 'fas fa-file-alt'), ('Scripts', 'scripts', 'fas fa-code')]:
    pc, _ = ProductCategory.objects.get_or_create(name=name, defaults={'slug': slug, 'icon': icon})
    prod_cats[name] = pc

if not Product.objects.exists():
    products = [
        (prod_cats['Expert Advisors'], 'Gold Scalper EA', 'High-frequency scalping EA optimized for XAU/USD. Advanced entry logic with tight stop losses.', 'ea', 299, 199, 4.8, 1234, True),
        (prod_cats['Expert Advisors'], 'Forex Trend Hunter', 'Multi-currency trend following EA that captures large market moves with smart trailing stops.', 'ea', 399, 299, 4.7, 856, True),
        (prod_cats['Expert Advisors'], 'Prop Firm Passer Pro', 'Specially designed EA for prop firm challenges. Conservative risk with consistent returns.', 'ea', 499, 399, 4.9, 2100, True),
        (prod_cats['Indicators'], 'Smart Support Resistance', 'Dynamic support and resistance zones with automatic zone detection and breakout alerts.', 'indicator', 79, 49, 4.6, 3421, True),
        (prod_cats['Indicators'], 'Volume Profile Pro', 'Professional volume profile indicator showing market structure, high volume nodes, and value areas.', 'indicator', 99, 69, 4.8, 2345, True),
        (prod_cats['Trading Templates'], 'Complete Trading Dashboard', 'All-in-one trading dashboard with multiple indicators, news feed, and risk calculator.', 'template', 149, 99, 4.5, 567, True),
        (prod_cats['Scripts'], 'Trade Manager Suite', 'Advanced trade management scripts for MT5 including partial closing, breakeven, and trailing stop.', 'script', 59, 39, 4.7, 1234, True),
        (prod_cats['Expert Advisors'], 'Mean Reversion Master', 'Statistical arbitrage EA that trades mean reversion across correlated currency pairs.', 'ea', 349, 249, 4.6, 654, True),
    ]
    for cat, title, desc, ptype, price, sale, rating, downloads, featured in products:
        Product.objects.create(
            category=cat, title=title, description=desc, short_description=desc[:200],
            product_type=ptype, price=price, sale_price=sale,
            version='1.0', rating=rating, download_count=downloads,
            is_featured=featured, is_published=True,
            license_type='Single License'
        )
    print("8 Products created ✓")

# 8. Prop Firms
if not PropFirm.objects.exists():
    PropFirm.objects.create(name='FTMO', description='Leading prop firm offering challenges from $10,000 to $200,000 with profit splits up to 90%.', website='https://ftmo.com', is_active=True)
    PropFirm.objects.create(name='MyForexFunds', description='Popular prop firm with flexible trading rules, no time limits on challenges, and quick payouts.', website='https://myforexfunds.com', is_active=True)
    PropFirm.objects.create(name='E8 Markets', description='Innovative prop firm with profit sharing up to 90% and unique scaling plans for consistent traders.', website='https://e8markets.com', is_active=True)
    PropFirm.objects.create(name='The Funded Trader', description='Trader-friendly prop firm known for rapid scaling, multiple platform support, and weekly payouts.', website='https://thefundedtrader.com', is_active=True)
    print("4 Prop firms created ✓")

# 9. Master Traders (Copy Trading)
if not MasterTrader.objects.exists():
    traders = [
        ('Elite Trader Pro', 'Professional trader with 15+ years experience. Specializes in EUR/USD and GBP/USD with a conservative approach.', 'IC Markets', 'Swing Trading', 'EUR/USD, GBP/USD', 68.5, 82.3, 12.4, 2.1, 1.8, 3420, 1850, 5.8, 500),
        ('Crypto King', 'Cryptocurrency specialist trading Bitcoin and Ethereum with high-probability setups.', 'Binance', 'Day Trading', 'BTC/USD, ETH/USD', 124.8, 71.5, 18.2, 1.5, 1.2, 2150, 3200, 9.2, 1000),
        ('Forex Master', 'Algorithmic trader using custom EAs for consistent returns. Low drawdown, steady growth.', 'Pepperstone', 'Automated', 'EUR/USD, USD/JPY, GBP/JPY', 42.3, 91.2, 5.8, 3.4, 2.5, 1500, 890, 3.5, 250),
    ]
    for name, bio, broker, style, instruments, roi, wr, dd, pf, sr, trades, followers, mroi, minv in traders:
        mt = MasterTrader.objects.create(
            name=name, bio=bio, broker=broker, trading_style=style,
            instruments=instruments, roi=roi, win_rate=wr, max_drawdown=dd,
            profit_factor=pf, sharpe_ratio=sr, total_trades=trades, followers=followers,
            monthly_roi=mroi, min_investment=minv, is_active=True, is_verified=True,
            risk_level='low' if dd < 10 else 'moderate'
        )
    print("3 Master Traders created ✓")

# 10. Sample notifications for admin
if not Notification.objects.filter(user=admin_user).exists():
    Notification.objects.create(user=admin_user, title='Welcome to AlgoEdge!', message='Thank you for joining. Start exploring our services and tools.', notification_type='info')
    Notification.objects.create(user=admin_user, title='Free EA Available', message='Verify your broker account to unlock premium EAs for free.', notification_type='broker')
    Notification.objects.create(user=admin_user, title='Prop Firm Challenge', message='New prop firm challenges available. Start your journey today.', notification_type='propfirm')
    print("3 Notifications created ✓")

import random
print("\n=== Seed Complete! ===")
print("Admin: http://127.0.0.1:8000/admin/ (admin / admin123)")
print(f"Site: http://127.0.0.1:8000/")
