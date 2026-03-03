import pandas as pd
import plotly.graph_objects as go

# ------------------------
# Load stability file
# ------------------------
df = pd.read_excel("91GMM_Stability_4and6.xlsx")

# ------------------------
# Define cluster columns
# ------------------------
gmm4_col = "GMM4"
gmm6_col = "GMM6"

# ------------------------
# Build transition matrix (GMM4 → GMM6)
# ------------------------
transition_matrix = pd.crosstab(df[gmm4_col], df[gmm6_col])

# Count genes per cluster
gmm4_counts = df[gmm4_col].value_counts().sort_index()
gmm6_counts = df[gmm6_col].value_counts().sort_index()

# ------------------------
# Sankey diagram
# ------------------------
sources, targets, values = [], [], []

# Build labels with counts
labels = [f"4-{c} ({gmm4_counts[c]} genes)" for c in gmm4_counts.index] + \
         [f"6-{c} ({gmm6_counts[c]} genes)" for c in gmm6_counts.index]

label_to_index = {label: i for i, label in enumerate(labels)}

# Map transitions
for c4 in transition_matrix.index:
    for c6 in transition_matrix.columns:
        val = transition_matrix.loc[c4, c6]
        if val > 0:
            src_label = f"4-{c4} ({gmm4_counts[c4]} genes)"
            tgt_label = f"6-{c6} ({gmm6_counts[c6]} genes)"
            sources.append(label_to_index[src_label])
            targets.append(label_to_index[tgt_label])
            values.append(val)

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color="blue"
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    )
)])

fig.update_layout(
    title_text="<b>Cluster transitions: GMM-4 → GMM-6</b>",
    font_size=14,
    title_x=0.5   # centers the title horizontally
)
# Export as SVG
fig.write_image("Cluster_Transitions_Sankey.svg")

print("Exported Sankey diagram with cluster gene counts as SVG.")