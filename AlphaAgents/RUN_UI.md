# AlphaAgents Streamlit UI - Quick Guide

## 🚀 Quick Start (3 Steps)

### 1. Install Requirements
```bash
cd AlphaAgents
pip install -r requirements.txt
```

### 2. Set Up API Key
Create a `.env` file with your Google API key:
```bash
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

**Get your Google API key:** https://makersuite.google.com/app/apikey

### 3. Run the App

**On a Server:**
```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

**Or use the script:**
```bash
./run_app.sh
```

**Access from your browser:**
- If on same network: `http://SERVER_IP:8501`
- Replace SERVER_IP with your server's IP address
- Example: `http://192.168.1.100:8501` or `http://your-server.com:8501`

**To find your server IP:**
```bash
hostname -I
# Or
ip addr show
```

**Alternative - SSH Port Forwarding (if connecting via SSH):**

If you're accessing the server via SSH, you can create a tunnel:
```bash
# On your local machine, run:
ssh -L 8501:localhost:8501 user@your-server-ip

# Then access: http://localhost:8501 in your local browser
```

---

## 📖 Using the UI

### Configuration (Sidebar)
- **Stock Universe**: Use 30 default stocks or enter custom tickers
- **Portfolio Size**: Number of stocks to include (3-20)
- **Risk Tolerance**: low, moderate, or high
- **Investment Horizon**: short_term, medium_term, or long_term
- **Initial Capital**: Starting investment amount ($)
- **Backtest Period**: Historical test period (1-5 years)
- **Benchmark**: Comparison ticker (default: SPY)

### Workflow
1. **Configure** parameters in sidebar
2. **Generate Portfolio** - Click "🚀 Generate AI Portfolio" (takes 2-5 minutes)
3. **Review Results** - See allocations, rationale, and sector breakdown in Portfolio tab
4. **Run Backtest** - Click "📊 Run Backtest" to test historical performance
5. **Analyze** - View charts and metrics in Backtest Results tab
6. **Download** - Export results as JSON or TXT

### What You'll See

**Portfolio Tab:**
- Executive summary and key metrics
- Holdings table with allocations
- Interactive pie chart and sector breakdown
- Detailed rationale for each stock
- Investment strategy and risk analysis
- Download options

**Backtest Results Tab:**
- Performance metrics (return, Sharpe ratio, drawdown, win rate)
- Benchmark comparison (alpha, correlation, information ratio)
- Portfolio value over time chart
- Returns distribution and drawdown charts
- Individual stock performance
- Correlation heatmap
- Download results

**About Tab:**
- System overview and features
- How the multi-agent system works
- Metrics explanation
- Disclaimer

---

## 📊 Key Features

✅ **Professional UI** - Clean design with custom theme  
✅ **AI-Powered** - Multi-agent system (Research, Analysis, Risk, Portfolio)  
✅ **Interactive Charts** - Plotly visualizations (zoom, pan, download)  
✅ **Comprehensive Backtesting** - Historical performance with detailed metrics  
✅ **Real-Time Data** - Live market data via yfinance  
✅ **Downloadable Results** - Export portfolios and backtest results  
✅ **Responsive Design** - Works on desktop and tablet  

---

## 💡 Tips

- **First run takes longer** - AI agents need time to analyze stocks
- **Choose diverse stocks** - Better for risk management
- **Match horizon to goals** - long_term for retirement, short_term for trading
- **Review rationale** - Understand why each stock was selected
- **Compare benchmarks** - See how portfolio performs vs S&P 500

---

## 🔧 Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"API key not found" error:**
- Check `.env` file exists in AlphaAgents directory
- Verify format: `GOOGLE_API_KEY=your_key` (no quotes)
- Ensure API key is valid

**"Port already in use" error:**
```bash
streamlit run app.py --server.port 8502 --server.address=0.0.0.0
```

**Can't access from browser (server setup):**

1. **Check if Streamlit is running:**
   ```bash
   ps aux | grep streamlit
   ```

2. **Check firewall - allow port 8501:**
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 8501
   sudo ufw status
   
   # CentOS/RHEL
   sudo firewall-cmd --permanent --add-port=8501/tcp
   sudo firewall-cmd --reload
   ```

3. **Verify server is listening on all interfaces:**
   ```bash
   netstat -tuln | grep 8501
   # Should show 0.0.0.0:8501, not 127.0.0.1:8501
   ```

4. **Check cloud provider security groups:**
   - AWS: Add inbound rule for port 8501
   - GCP: Add firewall rule for port 8501
   - Azure: Add inbound security rule for port 8501

**"No data available" error:**
- Verify ticker symbols are correct
- Check internet connection
- Some stocks may lack historical data

---

That's it! Simple Streamlit app, no Docker or complex setup needed. 🎉
