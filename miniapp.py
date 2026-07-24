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
            targets_html += f"<p>🎯 Target {i+1}: <b>{t.strip()}</b></p>"

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{pair} Chart</title>
    <style>
        body {{
            background-color: #0b0e11;
            color: white;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        .box {{
            background-color: #1e2329;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        h2 {{ margin-top: 0; }}
        #chart {{
            height: 400px;
            width: 100%;
        }}
    </style>
</head>
<body>
    <div class="box">
        <h2>{pair} • {direction}</h2>
        <p>Entry: <b>{entry}</b></p>
        <p>Stop-Loss: <b style="color:#f6465d">{sl}</b></p>
        <p>Accuracy: <b style="color:#0ecb81">{accuracy}%</b></p>
    </div>

    <div class="box">
        <h3>Targets</h3>
        {targets_html if targets_html else "<p>No targets</p>"}
    </div>

    <div class="box">
        <h3>Live Chart</h3>
        <div id="chart"></div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        new TradingView.widget({{
            "container_id": "chart",
            "width": "100%",
            "height": 400,
            "symbol": "BINANCE:{pair}",
            "interval": "60",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#1e2329",
            "enable_publishing": false
        }});
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
