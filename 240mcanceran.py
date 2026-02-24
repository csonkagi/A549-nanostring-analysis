import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D

# Load dataset
df = pd.read_excel("240lung cancer genes data.xlsx")

# Compute mean and SD (half difference) for each dose
for dose in ['40', '80', '150', '300']:
    df[f'mean_{dose}'] = (df[f'{dose}/1'] + df[f'{dose}/2']) / 2
    df[f'sd_{dose}'] = np.abs(df[f'{dose}/1'] - df[f'{dose}/2']) / 2

# Compute relative expression and propagated error
for dose in ['40', '80', '300']:
    df[f'rel_{dose}'] = df[f'mean_{dose}'] / df['mean_150']
    df[f'rel_err_{dose}'] = df[f'rel_{dose}'] * np.sqrt(
        (df[f'sd_{dose}'] / df[f'mean_{dose}'])**2 +
        (df['sd_150'] / df['mean_150'])**2
    )
    df[f'rel_err_ratio_{dose}'] = df[f'rel_err_{dose}'] / df[f'rel_{dose}']

# Compute total error
df['total_error'] = df['rel_err_ratio_40'] + df['rel_err_ratio_80'] + df['rel_err_ratio_300']

# Reliability classification
def classify_reliability(total_error):
    if total_error <= 0.30:
        return 'green'
    elif total_error <= 0.45:
        return 'light green'
    elif total_error <= 0.55:
        return 'yellow'
    elif total_error <= 0.65:
        return 'light red'
    else:
        return 'red'

df['Reliability_Category'] = df['total_error'].apply(classify_reliability)

# Export columns
columns = ['Gene Code']
columns += [f'{dose}/{rep}' for dose in ['40', '80', '150', '300'] for rep in ['1', '2']]
columns += ['mean_150', 'sd_150']
for dose in ['40', '80', '300']:
    columns += [f'rel_{dose}', f'rel_err_{dose}', f'rel_err_ratio_{dose}']
columns += ['total_error', 'Reliability_Category']

# Export full dataset
df[columns].to_excel("240 genes error propagation.xlsx", index=False)

# Filtered dataset
df_filtered = df[(df['mean_150'] > 20) & (df['total_error'] < 0.55)].copy()
df_filtered[columns].to_excel("110 genes error filtered.xlsx", index=False)

# Print filtered count
print(f"Filtered dataset contains {len(df_filtered)} genes.")

# Color map
color_map = {
    'green': 'green',
    'light green': '#66bb66',
    'yellow': 'gold',
    'light red': '#ff6666',
    'red': 'red'
}

# Legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='≤ 0.30 (green)', markerfacecolor='green', markersize=9),
    Line2D([0], [0], marker='o', color='w', label='≤ 0.45 (light green)', markerfacecolor='#66bb66', markersize=9),
    Line2D([0], [0], marker='o', color='w', label='≤ 0.55 (yellow)', markerfacecolor='gold', markersize=9),
    Line2D([0], [0], marker='o', color='w', label='≤ 0.65 (light red)', markerfacecolor='#ff6666', markersize=9),
    Line2D([0], [0], marker='o', color='w', label='> 0.65 (red)', markerfacecolor='red', markersize=9)
]

# Plot function
def plot_3d(dataframe, title):
    fig = plt.figure(figsize=(14, 9))
    ax = fig.add_subplot(111, projection='3d')

    for _, row in dataframe.iterrows():
        x, y, z = row['rel_40'], row['rel_80'], row['rel_300']
        color = color_map[row['Reliability_Category']]
        ax.scatter(x, y, z, c=color, marker='o', s=50, edgecolors='k', alpha=0.8)

    ax.set_xlabel('Expression Ratio @ 40 ppm')
    ax.set_ylabel('Expression Ratio @ 80 ppm')
    ax.set_zlabel('Expression Ratio @ 300 ppm')
    ax.set_title(title)

    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.05, 0.5),
              fontsize=9, title='Reliability Categories', title_fontsize=10)

    plt.tight_layout()
    plt.show()

# Plot full dataset
plot_3d(df, 'Relative Gene Expression Reliability Classification (All Genes)')

# Plot filtered dataset
plot_3d(df_filtered, 'Relative Gene Expression Reliability Classification (Filtered Genes)')