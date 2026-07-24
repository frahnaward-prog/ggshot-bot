from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/miniapp", response_class=HTMLResponse)
async def miniapp(request: Request):
    # Get data from URL parameters (sent by the bot)
    pair = request.query_params.get("pair", "BTCUSDT")
    direction = request.query_params.get("direction", "Long")
    entry = request.query_params.get("entry", "-")
    targets = request.query_params.get("targets", "")
    sl = request.query_params.get("sl", "-")
    accuracy = request.query_params.get("accuracy", "-")

    # Format targets nicely
    targets_html = ""
    if targets:
        for i, t in enumerate(targets.split(",")):
            targets_html += f"""
            <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #2a2f36;">
                <span style="color:#848e9c;">Target {i+1}</span>
                <span style="color:#0ecb81; font-weight:600;">{t.strip()}</span>
            </div>
            """

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GG-Shot • {pair}</title>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Roboto+Mono:wght@400;500&amp;display=swap');
        
        body {{
            background: #0b0e11;
            color: #eaecef;
            font-family: 'Inter', system_ui, sans-serif;
            margin: 0;
            padding: 16px;
            line-height: 1.5;
        }}
        
        .container {{
            max-width: 420px;
            margin: 0 auto;
        }}
        
        .card {{
            background: #1e2329;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }}
        
        .header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }}
        
        .pair {{
            font-size: 24px;
            font-weight: 700;
            color: #fff;
        }}
        
        .direction {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }}
        
        .long {{ background: #0ecb81; color: #fff; }}
        .short {{ background: #f6465d; color: #fff; }}
        
        .section-title {{
            font-size: 15px;
            color: #848e9c;
            margin-bottom: 12px;
            font-weight: 500;
        }}
        
        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #2a2f36;
        }}
        
        .info-row:last-child {{
            border-bottom: none;
        }}
        
        .label {{
            color: #848e9c;
            font-size: 14px;
        }}
        
        .value {{
            font-weight: 600;
            font-size: 15px;
        }}
        
        .accuracy {{
            color: #0ecb81;
            font-weight: 700;
        }}
        
        #tvchart {{
            height: 420px;
            border-radius: 12px;
            overflow: hidden;
            margin-top: 8px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #5e6673;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="card">
            <div class="header">
                <div>
                    <div class="pair">{pair}</div>
                    <div style="font-size:13px; color:#848e9c;">1h • Mid-Term</div>
                </div>
                <div style="margin-left:auto;">
                    <span class="direction {'long' if direction.lower() == 'long' else 'short'}">
                        {direction.upper()}
                    </span>
                </div>
            </div>
        </div>

        <!-- Key Info -->
        <div class="card">
            <div class="section-title">KEY LEVELS</div>
            
            <div class="info-row">
                <span class="label">Entry Zone</span>
                <span class="value">{entry}</span>
            </div>
            <div class="info-row">
                <span class="label">Stop-Loss</span>
                <span class="value" style="color:#f6465d;">{sl}</span>
            </div>
            <div class="info-row">
                <span class="label">Accuracy</span>
                <span class="value accuracy">{accuracy}%</span>
            </div>
        </div>

        <!-- Targets -->
        <div class="card">
            <div class="section-title">TARGETS</div>
            {targets_html if targets_html else '<div style="color:#848e9c;">No targets set</div>'}
        </div>

        <!-- Live Chart -->
        <div class="card">
            <div class="section-title">LIVE CHART</div>
            <div id="tvchart"></div>
        </div>

        <div class="footer">
            GG-Shot • Real-time signals
        </div>
    </div>

    <script>
        new TradingView.widget({{
            container_id: "tvchart",
            symbol: "BINANCE:{pair}",
            interval: "60",
            theme: "dark",
            style: "1",
            locale: "en",
            toolbar_bg: "#1e2329",
            enable_publishing: false,
            hide_top_toolbar: false,
            hide_legend: false,
            height: 420,
            width: "100%"
        }});
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    print("🚀 Premium Mini App running...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
