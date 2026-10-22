import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from routing import create_network, find_route

st.set_page_config(
    page_title="Intelligent Routing Simulator",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Intelligent Routing Simulator")
st.write("Explore shortest-path routing and network link failures.")

G = create_network()

positions = {
    "A": (0, 2),
    "B": (2, 3),
    "C": (2, 1),
    "D": (4, 2),
    "E": (4, 0),
    "F": (6, 1)
}

edges = list(G.edges())
edge_names = ["No failure"] + [
    f"{u} - {v}" for u, v in edges
]

st.sidebar.header("Routing Controls")

source = st.sidebar.selectbox(
    "Source Router", list(G.nodes()), index=0
)
destination = st.sidebar.selectbox(
    "Destination Router", list(G.nodes()), index=5
)
failed_link = st.sidebar.selectbox(
    "Simulate Link Failure", edge_names
)

# Copy the network so the original stays unchanged
H = G.copy()

if failed_link != "No failure":
    u, v = failed_link.split(" - ")
    H.remove_edge(u, v)

path, cost = find_route(H, source, destination)

st.subheader("Network Topology")

fig = go.Figure()

# Draw all available links
for u, v, data in H.edges(data=True):
    x1, y1 = positions[u]
    x2, y2 = positions[v]

    fig.add_trace(go.Scatter(
        x=[x1, x2], y=[y1, y2],
        mode="lines",
        line=dict(color="gray", width=2),
        hoverinfo="text",
        text=f"{u} - {v}, Cost: {data['weight']}",
        showlegend=False
    ))

    fig.add_annotation(
        x=(x1 + x2) / 2,
        y=(y1 + y2) / 2,
        text=str(data["weight"]),
        showarrow=False,
        bgcolor="white"
    )

# Highlight the selected shortest route
if path:
    for u, v in zip(path[:-1], path[1:]):
        x1, y1 = positions[u]
        x2, y2 = positions[v]

        fig.add_trace(go.Scatter(
            x=[x1, x2], y=[y1, y2],
            mode="lines",
            line=dict(color="green", width=5),
            hoverinfo="skip",
            showlegend=False
        ))

# Draw routers
fig.add_trace(go.Scatter(
    x=[positions[n][0] for n in H.nodes()],
    y=[positions[n][1] for n in H.nodes()],
    mode="markers+text",
    text=list(H.nodes()),
    textposition="top center",
    marker=dict(size=35, color="lightblue",
                line=dict(width=2, color="navy")),
    showlegend=False
))

fig.update_layout(
    height=480,
    showlegend=False,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Routing Result")

if source == destination:
    st.info("Source and destination are the same router.")
elif path:
    col1, col2 = st.columns(2)

    col1.metric("Total Routing Cost", cost)
    col2.metric("Number of Links", len(path) - 1)

    st.success("Best Route: " + " → ".join(path))
else:
    st.error("No route available between these routers.")

if failed_link != "No failure":
    st.warning(f"Link failure simulated: {failed_link}")

st.caption(
    "Educational simulation using Dijkstra's shortest-path algorithm."
)