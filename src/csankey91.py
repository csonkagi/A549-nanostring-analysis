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

# Build labels with bold integer cluster numbers
labels = [f"4-{int(c)} ({gmm4_counts[c]} genes)" for c in gmm4_counts.index] + \
         [f"6-{int(c)} ({gmm6_counts[c]} genes)" for c in gmm6_counts.index]

label_to_index = {label: i for i, label in enumerate(labels)}

for c4 in transition_matrix.index:
    for c6 in transition_matrix.columns:
        val = transition_matrix.loc[c4, c6]
        if val > 0:
            src_label = f"4-{int(c4)} ({gmm4_counts[c4]} genes)"
            tgt_label = f"6-{int(c6)} ({gmm6_counts[c6]} genes)"
            sources.append(label_to_index[src_label])
            targets.append(label_to_index[tgt_label])
            values.append(val)

# ------------------------
# Define colors
# ------------------------
gmm4_colors = {1: "orange", 2: "yellow", 3: "green", 4: "blue"}
node_colors = [gmm4_colors[int(c)] for c in gmm4_counts.index]

# Assign GMM6 colors based on dominant incoming GMM4 cluster
for c6 in gmm6_counts.index:
    dominant_c4 = transition_matrix[c6].idxmax()
    node_colors.append(gmm4_colors[int(dominant_c4)])

# ------------------------
# Fixed node positions (adjust manually as needed)
# ------------------------
x_left = 0.0
y_positions_left = [0.1, 0.3, 0.5, 0.7]   # adjust manually

x_right = 1.0
y_positions_right = [0.1, 0.3, 0.48, 0.65, 0.8, 0.95]  # adjust manually

x_positions = [x_left]*len(gmm4_counts) + [x_right]*len(gmm6_counts)
y_positions = y_positions_left + y_positions_right

# ------------------------
# Build Sankey
# ------------------------
fig = go.Figure(data=[go.Sankey(
    arrangement="fixed",
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=node_colors,
        x=x_positions,
        y=y_positions
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    )
)])

fig.update_layout(
    title=dict(
        text="<b>Cluster transitions: GMM-4 → GMM-6</b>",
        x=0.5,
        xanchor="center"
    ),
    font=dict(size=18)  # <-- increase this value for larger node labels
)

fig.write_image("Cluster_Trans_Sankey.svg")

print("Exported Sankey diagram with bold integer cluster labels and fixed positions.")