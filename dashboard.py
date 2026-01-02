from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from flask import Flask, request, jsonify
from collections import deque
import time

# ================= Flask server =================
server = Flask(__name__)
events = deque(maxlen=5000)

@server.route("/event", methods=["POST"])
def receive_event():
    events.append(request.json)
    return jsonify({"status": "ok"})

# ================= Dash App =================
app = Dash(__name__, server=server)

app.layout = html.Div(
    style={
        "backgroundColor": "#0e1117",
        "color": "#ffffff",
        "fontFamily": "Arial",
        "padding": "20px"
    },
    children=[

        # ===== TITLE =====
        html.H1("🛡️ SDN + AI Cybersecurity Dashboard",
                style={"textAlign": "center", "marginBottom": "30px"}),

        # ===== KPI CARDS =====
        html.Div(style={"display": "flex", "justifyContent": "space-around"}, children=[
            html.Div(id="kpi-total", className="kpi"),
            html.Div(id="kpi-attacks", className="kpi"),
            html.Div(id="kpi-blocked", className="kpi"),
        ]),

        html.Hr(style={"margin": "30px 0"}),

        # ===== GRAPHS =====
        html.Div(style={"display": "flex"}, children=[
            dcc.Graph(id="rate-graph", style={"width": "65%"}),
            dcc.Graph(id="status-graph", style={"width": "35%"})
        ]),

        html.Hr(style={"margin": "30px 0"}),

        # ===== EVENT LOG =====
        html.H2("📜 Live Security Events"),
        html.Div(
            id="event-log",
            style={
                "height": "300px",
                "overflowY": "scroll",
                "backgroundColor": "#161b22",
                "padding": "10px",
                "borderRadius": "10px"
            }
        ),

        dcc.Interval(id="interval", interval=1000, n_intervals=0)
    ]
)

# ================= CALLBACK =================
@app.callback(
    Output("kpi-total", "children"),
    Output("kpi-attacks", "children"),
    Output("kpi-blocked", "children"),
    Output("rate-graph", "figure"),
    Output("status-graph", "figure"),
    Output("event-log", "children"),
    Input("interval", "n_intervals")
)
def update_dashboard(_):
    if not events:
        empty = go.Figure()
        return (
            kpi("Total Packets", 0, "#1f6feb"),
            kpi("Attacks", 0, "#da3633"),
            kpi("Blocked", 0, "#f0883e"),
            empty, empty, "Waiting for events..."
        )

    total = len(events)
    attacks = sum(1 for e in events if e["status"] == "attack")
    blocked = sum(1 for e in events if e["status"] == "blocked")

    # ===== RATE GRAPH =====
    mac_rates = {}
    for e in events:
        mac_rates.setdefault(e["mac"], []).append(e["rate"])

    rate_fig = go.Figure()
    for mac, rates in mac_rates.items():
        rate_fig.add_trace(go.Scatter(
            y=rates, mode="lines+markers", name=mac
        ))

    rate_fig.update_layout(
        title="📈 Packet Rate per MAC",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="white")
    )

    # ===== STATUS GRAPH =====
    status_fig = go.Figure([
        go.Bar(
            x=["Forwarded", "Attack", "Blocked"],
            y=[
                sum(1 for e in events if e["status"] == "forwarded"),
                attacks,
                blocked
            ],
            marker_color=["#2ea043", "#da3633", "#f0883e"]
        )
    ])

    status_fig.update_layout(
        title="🚦 Traffic Status",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="white")
    )

    # ===== EVENT LOG =====
    log = []
    for e in reversed(list(events)[-50:]):
        color = "#2ea043"
        icon = "✅"
        if e["status"] == "attack":
            color = "#da3633"
            icon = "❌"
        elif e["status"] == "blocked":
            color = "#f0883e"
            icon = "🚫"

        log.append(html.Div(
            f"{icon} [{time.strftime('%H:%M:%S', time.localtime(e['time']))}] "
            f"MAC={e['mac']} | size={e['size']} | rate={e['rate']}",
            style={"color": color, "marginBottom": "5px"}
        ))

    return (
        kpi("Total Packets", total, "#1f6feb"),
        kpi("Attacks", attacks, "#da3633"),
        kpi("Blocked", blocked, "#f0883e"),
        rate_fig,
        status_fig,
        log
    )

# ================= KPI COMPONENT =================
def kpi(title, value, color):
    return html.Div(
        style={
            "backgroundColor": "#161b22",
            "padding": "20px",
            "borderRadius": "15px",
            "width": "20%",
            "textAlign": "center",
            "border": f"2px solid {color}"
        },
        children=[
            html.H3(title),
            html.H1(str(value), style={"color": color})
        ]
    )

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
