from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/miniapp", response_class=HTMLResponse)
async def miniapp(request: Request):
    pair = request.query_params.get("pair", "BTCUSDT")
    direction = request.query_params.get("direction", "Long")
    entry = request.query_params.get("entry", "-")
    targets = request.query_params.get("targets", "")
    sl = request.query_params.get("sl", "-")
    accuracy = request.query_params.get("accuracy", "-")

    targets_html = ""
    if targets:
        for i, t in enumerate(targets.split(",")):
            targets_html += f"<div style='margin:6px 0'>🎯 Target {i+1}: <b>{t.strip()}</b></div>"

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GG-Shot • {pair}</title>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <style>
        body {{
            background: #0b0e11;
            color: #eaecef;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 16px;
        }}
        .card {{
            background: #1e2329;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 16px;
        }}
        h2 {{ margin: 0 0 12px 0; font-size: 22px; }}
        .row {{ display: flex; justify-content: space-between; margin: 8px 0; font-size: 15px; }}
        .label {{ color: #848e9c; }}
        .green {{ color: #0ecb81; }}
        .red {{ color: #f6465d; }}
        #tvchart {{ height: 480px; border-radius: 12px; overflow: hidden; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>📈 {pair} • {direction}</h2>
        <div class="row"><span class="label">Entry Zone</span> <b>{entry}</b></div>
        <div class="row"><span class="label">Stop-Loss</span> <b class="red">{sl}</b></div>
        <div class="row"><span class="label">Accuracy</span> <b class="green">{accuracy}%</b></div>
    </div>

    <div class="card">
        <h3 style="margin-top:0">🎯 Targets</h3>
        {targets_html if targets_html else "<div>No targets</div>"}
    </div>

    <div class="card">
        <h3 style="margin-top:0">Live Chart</h3>
        <div id="tvchart"></div>
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
            height: 480,
            width: "100%"
        }});
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html)

if __name__ == "__main__":
    print("🚀 Improved Mini App running...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
