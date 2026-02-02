# Use Case: Data Scientist

## Who Needs This

**Persona:** Jamie Torres, data scientist at e-commerce company
- Building customer recommendation system
- Analyzing product co-purchase networks (25K products, 500K edges)
- Creating dashboards for business stakeholders
- Works in Jupyter notebooks, deploys to Streamlit/Dash
- Needs to explain insights to non-technical audience

**Context:** Exploring network effects in customer behavior. Must create interactive visualizations for stakeholders to understand product relationships, identify clusters, and validate recommendations.

## Why They Need Graph Visualization

**Problem:**
- Product relationships are hidden in purchase data (which products are bought together)
- Stakeholders need to explore product clusters interactively
- Static reports don't convey network dynamics
- Business users want to filter by category, price range, season
- Insights must drive merchandising decisions (bundle recommendations, display placement)

**Success Criteria:**
- ✅ Interactive exploration (zoom, filter, hover for details)
- ✅ Web dashboard (accessible to non-technical users)
- ✅ Real-time updates (daily data refreshes)
- ✅ Professional appearance (client-facing dashboard)
- ✅ Integration with existing tools (Pandas, Jupyter)

## Requirements

### Technical
- **Scale:** 25K nodes (products), 500K edges (co-purchases)
- **Interactivity:** Hover tooltips (product name, price, category), click for details, zoom/pan
- **Output:** Web dashboard (Streamlit or Dash)
- **Data integration:** Pandas dataframes from SQL warehouse
- **Deployment:** Internal web server (accessed by stakeholders)

### Workflow
- Query product co-purchase data from data warehouse
- Build graph (NetworkX for analysis)
- Compute communities (cluster related products)
- Create interactive visualization
- Deploy to dashboard
- Stakeholders explore and generate insights

### Constraints
- Must work in browser (no desktop apps)
- Responsive to user interactions (<1 second response)
- Professional styling (company branding)
- Accessible to non-programmers

## Recommended Solution

### Primary: Plotly + Dash

**Why this choice:**
1. **Interactive by design:** Hover, zoom, pan built-in
2. **Dash integration:** Full-stack dashboards with filters, dropdowns, sliders
3. **Professional aesthetics:** Customizable themes, company branding
4. **Python-native:** Integrates with Pandas, NetworkX workflows
5. **Browser-based:** No client installation needed

**Workflow:**
```python
import networkx as nx
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Build graph from purchase data
G = nx.from_pandas_edgelist(df, 'product_a', 'product_b', edge_attr='weight')

# Community detection
communities = nx.community.louvain_communities(G)
node_colors = {node: i for i, comm in enumerate(communities) for node in comm}

# Layout
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Build Plotly figure
edge_trace = go.Scatter(
    x=[pos[e[0]][0] for e in G.edges()] + [pos[e[1]][0] for e in G.edges()],
    y=[pos[e[0]][1] for e in G.edges()] + [pos[e[1]][1] for e in G.edges()],
    mode='lines',
    line=dict(width=0.5, color='#888'),
    hoverinfo='none'
)

node_trace = go.Scatter(
    x=[pos[n][0] for n in G.nodes()],
    y=[pos[n][1] for n in G.nodes()],
    mode='markers',
    marker=dict(
        size=[G.degree(n) for n in G.nodes()],
        color=[node_colors[n] for n in G.nodes()],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Community")
    ),
    text=[f"{n}: ${price[n]}" for n in G.nodes()],  # Hover text
    hoverinfo='text'
)

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Product Co-Purchase Network',
                    hovermode='closest'
                ))

# Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Product Recommendation Explorer"),
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': cat, 'value': cat} for cat in categories],
        multi=True
    ),
    dcc.Graph(id='network-graph', figure=fig)
])

@app.callback(
    Output('network-graph', 'figure'),
    Input('category-filter', 'value')
)
def update_graph(selected_categories):
    # Filter graph by category, rebuild visualization
    # ... implementation ...
    return updated_figure

app.run_server(debug=True)
```

**Output:** Interactive dashboard with filtering, exploration, insights.

### Secondary: Plotly in Jupyter (for analysis)

**When to use:**
- Exploratory data analysis (before dashboard)
- Ad-hoc stakeholder requests (quick visualizations)
- Notebook-based reports (share via nbconvert)

**Benefit:** Same library for exploration and production dashboard (code reuse).

### Avoid: PyVis, NetworkX matplotlib, Desktop tools

**Why not PyVis:**
- Limited filtering/callback support (vis.js limitations)
- Maintenance risk (vis.js unmaintained) for production dashboard
- Harder to integrate with Dash/Streamlit workflows

**Why not NetworkX matplotlib:**
- No interactivity (static images)
- Doesn't meet "interactive exploration" requirement

**Why not Gephi/Cytoscape:**
- Desktop apps (not accessible to stakeholders)
- Manual operation (not integrated with data pipeline)

## Advanced Dashboard Features

### Interactive Filtering
```python
# Multiple filters in Dash
app.layout = html.Div([
    dcc.Dropdown(id='category', options=categories),
    dcc.RangeSlider(id='price-range', min=0, max=1000, value=[0, 1000]),
    dcc.Dropdown(id='community', options=community_ids),
    dcc.Graph(id='network')
])

# Combined callback
@app.callback(
    Output('network', 'figure'),
    [Input('category', 'value'),
     Input('price-range', 'value'),
     Input('community', 'value')]
)
def filter_graph(category, price_range, community):
    # Filter NetworkX graph
    filtered = filter_by_attributes(G, category, price_range, community)
    # Rebuild Plotly figure
    return build_figure(filtered)
```

**User experience:** Stakeholders explore product clusters by adjusting filters.

### Click-to-Detail
```python
@app.callback(
    Output('product-details', 'children'),
    Input('network', 'clickData')
)
def show_product_details(click_data):
    if click_data:
        product_id = click_data['points'][0]['text']
        # Query product details from database
        details = get_product_info(product_id)
        return html.Div([
            html.H3(details['name']),
            html.P(f"Price: ${details['price']}"),
            html.P(f"Category: {details['category']}"),
            html.P(f"Recommended with: {details['bundles']}")
        ])
    return "Click a product to see details"
```

**Use case:** Click product node → see recommendations, purchase history, pricing.

### Performance Optimization (Large Graphs)
```python
# For 25K nodes, use Scattergl for WebGL acceleration
node_trace = go.Scattergl(  # Note: Scattergl instead of Scatter
    x=[pos[n][0] for n in G.nodes()],
    y=[pos[n][1] for n in G.nodes()],
    mode='markers',
    # ... rest of config ...
)
```

**Benefit:** Smooth interactivity up to 50K nodes.

## Alternative Scenarios

### If Graph is Massive (>50K nodes)
**Switch to:** Hierarchical drill-down
- Top-level: Category clusters (Plotly, <500 nodes)
- Drill-down: Within-category graph (Plotly, <5K nodes per category)
- Avoid: Single visualization of entire graph (browser can't handle it)

### If Stakeholders Need Offline Exploration
**Add:** PyVis for standalone HTML
- Generate HTML file from current graph state
- Email to stakeholders (self-contained, no server needed)
- Warning: Not real-time, manual regeneration

### If Building Dedicated Product
**Consider:** Custom D3.js implementation
- Plotly may be limiting for highly custom interactions
- D3.js gives full control (but higher development cost)
- Use Plotly for MVP, migrate if needed

## Tools Comparison for This Use Case

| Library | Fit Score | Reasoning |
|---------|-----------|-----------|
| Plotly + Dash | ⭐⭐⭐⭐⭐ | Perfect - interactive, dashboards, professional |
| Plotly (Jupyter) | ⭐⭐⭐⭐ | Good for exploration, lacks dashboard features |
| PyVis | ⭐⭐⭐ | Quick demos, but limited production features |
| NetworkX + matplotlib | ⭐ | No interactivity (fails requirement) |
| Graphviz | ⭐ | Static only (not suitable) |
| Desktop tools | ⭐ | Not accessible to stakeholders |

## Success Indicators

**This recommendation works if:**
- ✅ Stakeholders have web browser access
- ✅ Graph fits in memory (<100K nodes)
- ✅ Team has Python expertise (Dash development)
- ✅ Interactive exploration is core requirement

**Reconsider if:**
- ❌ Graph is too large (>100K nodes) - use hierarchical approach
- ❌ Real-time streaming updates needed - add WebSocket layer
- ❌ Mobile-first requirement - Plotly mobile support is limited
- ❌ No server hosting available - use static PyVis HTML (limited features)

## Business Impact

**Insights enabled:**
1. **Product bundling:** Identify frequently co-purchased products
2. **Merchandising:** Optimize product placement on website
3. **Inventory planning:** Predict demand for related products
4. **Marketing campaigns:** Target clusters with coordinated promotions
5. **Competitive analysis:** Discover unexpected product relationships

**ROI:** Interactive exploration reduces time-to-insight from days (static reports) to minutes (dashboard exploration).
