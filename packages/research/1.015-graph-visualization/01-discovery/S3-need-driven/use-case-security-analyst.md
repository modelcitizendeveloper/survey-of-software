# Use Case: Security Analyst

## Who Needs This

**Persona:** Marcus Williams, senior security analyst at financial services company
- Investigating network intrusions and threat actor behavior
- Analyzing firewall logs, DNS queries, network traffic (100K+ events/day)
- Creating threat intelligence reports for management
- Works with SIEM tools (Splunk, ELK stack) and Python scripts
- Needs to visualize attack patterns and lateral movement

**Context:** Responding to potential APT (Advanced Persistent Threat) activity. Must map network connections, identify compromised hosts, trace attacker movement, and present findings to incident response team.

## Why They Need Graph Visualization

**Problem:**
- Network traffic logs are overwhelming (millions of connections)
- Attack patterns hidden in connection graphs (C2 servers, lateral movement)
- Must identify patient zero (initial compromise) and blast radius
- Incident reports require visual evidence (show management the attack path)
- Time-sensitive (active intrusion requires rapid analysis)

**Success Criteria:**
- ✅ Rapid analysis (identify attack patterns in minutes, not hours)
- ✅ Interactive exploration (filter by time, protocol, port)
- ✅ Clear attribution (isolate attacker IPs, compromised hosts)
- ✅ Executive-friendly visualizations (non-technical stakeholders)
- ✅ Exportable evidence (screenshots for incident reports)

## Requirements

### Technical
- **Scale:** 50K-500K nodes (IPs, domains, processes), 500K-5M edges (connections)
- **Time-series:** Filter by time windows (last hour, during incident, etc.)
- **Interactivity:** Zoom to suspicious clusters, filter noise, highlight attack chains
- **Performance:** Real-time updates (streaming logs)
- **Output:** Screenshots for reports, interactive HTML for deeper analysis

### Workflow
- Ingest logs from SIEM (Splunk query or ELK export)
- Build network graph (IP-to-IP, DNS queries, process execution)
- Detect anomalies (unusual connections, C2 patterns)
- Visualize attack path
- Export findings for incident report
- Share with SOC team for remediation

### Constraints
- Time-critical (active breach scenario)
- Must handle large datasets (millions of events)
- Browser-based (SOC analysts work in web interfaces)
- Integration with existing tools (Splunk dashboards, Kibana)

## Recommended Solution

### Primary: NetworkX + Plotly (for analysis + dashboard)

**Why this choice:**
1. **NetworkX for analysis:** Graph algorithms to detect attack patterns (shortest paths, connected components, centrality)
2. **Plotly for visualization:** Interactive exploration, filter by time/attribute
3. **Jupyter for investigation:** Ad-hoc analysis during incident response
4. **Dash for SOC dashboard:** Real-time monitoring of network connections

**Workflow:**
```python
import networkx as nx
import pandas as pd
import plotly.graph_objects as go

# Ingest firewall logs
logs = pd.read_csv('firewall_logs.csv')  # src_ip, dst_ip, port, timestamp, bytes

# Build directed graph (traffic flow)
G = nx.from_pandas_edgelist(logs, 'src_ip', 'dst_ip',
                             edge_attr=['port', 'timestamp', 'bytes'],
                             create_using=nx.DiGraph())

# Detect suspicious patterns
# 1. High betweenness centrality (potential C2 server)
betweenness = nx.betweenness_centrality(G)
suspicious_ips = [ip for ip, score in betweenness.items() if score > 0.05]

# 2. External connections from internal hosts
internal_ips = [ip for ip in G.nodes() if ip.startswith('10.')]
external_connections = [(src, dst) for src, dst in G.edges()
                        if src in internal_ips and not dst.startswith('10.')]

# 3. Lateral movement (internal-to-internal SMB/RDP connections)
lateral_movement = [(src, dst, port) for src, dst, port in
                    [(e[0], e[1], G[e[0]][e[1]]['port']) for e in G.edges()]
                    if src in internal_ips and dst in internal_ips
                    and port in [445, 3389]]  # SMB, RDP

# Visualize attack graph
pos = nx.spring_layout(G, k=0.3)

# Color nodes by type (internal, external, suspicious)
node_colors = ['red' if ip in suspicious_ips else
               'blue' if ip.startswith('10.') else 'gray'
               for ip in G.nodes()]

# Build Plotly figure
edge_trace = go.Scatter(...)  # Edges
node_trace = go.Scatter(
    x=[pos[n][0] for n in G.nodes()],
    y=[pos[n][1] for n in G.nodes()],
    mode='markers',
    marker=dict(size=10, color=node_colors),
    text=[f"{ip}<br>Connections: {G.degree(ip)}" for ip in G.nodes()],
    hoverinfo='text'
)

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(title='Network Traffic Graph'))
fig.show()
```

**Output:** Interactive graph highlighting suspicious IPs, lateral movement, external C2.

### Advanced: Dash Dashboard for SOC Monitoring
```python
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H1("SOC Network Monitoring"),
    dcc.Interval(id='interval', interval=60*1000),  # Update every minute
    dcc.Dropdown(id='time-window',
                 options=[{'label': 'Last Hour', 'value': '1h'},
                          {'label': 'Last 4 Hours', 'value': '4h'},
                          {'label': 'Last 24 Hours', 'value': '24h'}]),
    dcc.Graph(id='network-graph'),
    html.Div(id='alerts')
])

@app.callback(
    [Output('network-graph', 'figure'),
     Output('alerts', 'children')],
    [Input('interval', 'n_intervals'),
     Input('time-window', 'value')]
)
def update_dashboard(n, time_window):
    # Query recent logs from SIEM
    logs = query_splunk(time_window)
    G = build_graph(logs)

    # Detect anomalies
    anomalies = detect_anomalies(G)

    # Build visualization
    fig = build_plotly_network(G, highlight=anomalies)

    # Alert list
    alerts = html.Ul([html.Li(f"Suspicious: {ip}") for ip in anomalies])

    return fig, alerts
```

**Use case:** Real-time SOC dashboard showing live network connections with anomaly alerts.

### Alternative: PyVis (for quick incident investigation)

**When to use:**
- Ad-hoc investigation (not ongoing monitoring)
- Need standalone HTML to share with team (email attachment)
- Rapid visualization (5 lines of code)

**Example:**
```python
from pyvis.network import Network

# Quick visualization during active incident
net = Network(height='750px', width='100%', directed=True)
net.from_nx(G)

# Highlight suspicious nodes
for node in suspicious_ips:
    net.get_node(node)['color'] = 'red'

net.show('incident_graph.html')
# Email HTML to incident response team
```

### Avoid: Gephi, Cytoscape (too heavyweight)

**Why not desktop tools:**
- Slow for incident response (manual import, no scripting)
- Not integrated with SIEM workflows
- SOC analysts need browser-based tools (not desktop apps)

## Investigation Patterns

### Pattern 1: Patient Zero Identification
```python
# Find initial compromise (earliest external connection to internal host)
external_to_internal = [(src, dst, ts) for src, dst, ts in
                        [(e[0], e[1], G[e[0]][e[1]]['timestamp'])
                         for e in G.edges()]
                        if not src.startswith('10.') and dst.startswith('10.')]

earliest = min(external_to_internal, key=lambda x: x[2])
patient_zero = earliest[1]
print(f"Patient zero: {patient_zero} at {earliest[2]}")

# Visualize: Highlight patient zero + attacker IP
```

### Pattern 2: Lateral Movement Tracing
```python
# Find all paths from patient zero to other internal hosts
from itertools import islice

patient_zero = '10.0.5.42'
internal_hosts = [ip for ip in G.nodes() if ip.startswith('10.') and ip != patient_zero]

lateral_paths = {}
for target in internal_hosts:
    try:
        paths = list(islice(nx.all_simple_paths(G, patient_zero, target, cutoff=5), 10))
        if paths:
            lateral_paths[target] = paths
    except nx.NetworkXNoPath:
        continue

# Visualize: Draw paths showing how attacker moved through network
```

### Pattern 3: C2 Server Detection
```python
# High betweenness + external IP + beaconing pattern
for ip in suspicious_ips:
    if not ip.startswith('10.'):  # External IP
        # Check for regular intervals (beaconing)
        connections = [G[src][dst]['timestamp']
                       for src, dst in G.edges()
                       if dst == ip]
        intervals = [connections[i+1] - connections[i]
                     for i in range(len(connections)-1)]

        if is_regular_interval(intervals):  # Helper function
            print(f"Potential C2 server: {ip}")
            # Alert SOC team
```

## Alternative Scenarios

### If Network is Massive (>1M nodes)
**Switch to:** Graph database (Neo4j) + Plotly sampling
- Store network in Neo4j (scales to billions of nodes)
- Query suspicious subgraphs with Cypher
- Visualize sampled subgraphs in Plotly (not entire network)

### If Need Real-Time Streaming
**Add:** Apache Kafka + Dash
- Kafka for log streaming
- Dash with WebSocket for live updates
- NetworkX for incremental graph updates

### If Exporting for Executive Reports
**Add:** Graphviz for clean diagrams
- Plotly for interactive investigation
- Graphviz for static report diagrams (attack flow, timeline)
- Convert key findings to hierarchical Graphviz diagram

## Tools Comparison for This Use Case

| Library | Fit Score | Reasoning |
|---------|-----------|-----------|
| NetworkX + Plotly | ⭐⭐⭐⭐⭐ | Perfect - analysis + interactive dashboard |
| PyVis | ⭐⭐⭐⭐ | Good for quick investigation, standalone HTML |
| Graphviz | ⭐⭐⭐ | Good for report diagrams (attack timeline) |
| NetworkX + matplotlib | ⭐⭐ | Analysis OK, visualization lacks interactivity |
| Gephi/Cytoscape | ⭐ | Too slow for incident response |
| Neo4j + Bloom | ⭐⭐⭐⭐ | Best for massive graphs (>1M nodes), but heavyweight |

## Success Indicators

**This recommendation works if:**
- ✅ Need rapid analysis during active incident
- ✅ Integration with existing SIEM tools
- ✅ Browser-based workflow (SOC analyst environment)
- ✅ Network fits in memory (<1M nodes)

**Reconsider if:**
- ❌ Massive scale (>1M nodes) - use graph database (Neo4j)
- ❌ Real-time streaming required - add Kafka layer
- ❌ Forensics focus (offline analysis) - Gephi might work
- ❌ Non-Python stack - use native SIEM visualization (Splunk, Kibana)

## Integration with SIEM

### Splunk Integration
```python
import splunklib.client as client

# Query Splunk for firewall logs
service = client.connect(host='splunk.corp', port=8089,
                          username='analyst', password=os.getenv('SPLUNK_PASS'))

search_query = '''
search index=firewall earliest=-1h
| table src_ip dst_ip dst_port bytes timestamp
'''

job = service.jobs.create(search_query)
# ... wait for job completion ...

results = job.results()
logs = pd.read_csv(io.StringIO(results))

# Build graph and visualize
G = nx.from_pandas_edgelist(logs, 'src_ip', 'dst_ip')
# ... analysis ...
```

### ELK Stack Integration
```python
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://elk.corp:9200'])

query = {
    "query": {
        "range": {"@timestamp": {"gte": "now-1h"}}
    }
}

results = es.search(index='firewall-*', body=query, size=10000)
logs = pd.json_normalize(results['hits']['hits'])
# Build graph
```

**Result:** Seamless integration with existing SOC infrastructure.

## Real-World Impact

**Detection speed:** Minutes instead of hours (interactive exploration vs. log grepping)
**Attribution:** Visual evidence of attacker paths (management buy-in)
**Response:** Isolate compromised hosts faster (see blast radius)
**Reporting:** Executive-friendly visualizations (not raw logs)
**Training:** Analysts learn attack patterns through visualization
