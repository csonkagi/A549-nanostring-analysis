#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Oncogene Network Schematic with Fixed Angles
- Spokes at angles: 20, 50, 120, 150, 180, 210, 240, 310, 340
- Gene boxes italicized, pastel-colored, taller, offset outward
- Spoke labels smaller, dark colors
- Hallmarks italicized outside spokes
"""

import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

# ----------------------------
# Configuration
# ----------------------------

# Light pastel colors for gene boxes
BOX_COLORS = {
    "RTKs & adaptors": "#d1b3ff",    # light purple
    "RAS–MAPK core": "#ff9999",      # light red
    "PI3K–AKT axis": "#ffcc99",      # light orange
    "Cell cycle & replication": "#ffffb3", # light yellow
    "Cell survival": "#b3ffb3",  # light green
    "Transcriptional amplifiers": "#99ccff", # light blue
    "Cytokine/inflammation": "#ffb3e6", # light magenta
    "Invasion & ECM remodeling": "#e6ccff", # light violet
    "DNA repair & stress tolerance": "#b3ffff" # light cyan
}

# Dark colors for spokes/labels
SPOKE_COLORS = {
    "RTKs & adaptors": "#6a3d9a",
    "RAS–MAPK core": "#e31a1c",
    "PI3K–AKT axis": "#ff7f00",
    "Cell cycle & replication": "#b15928",
    "Cell survival": "#33a02c",
    "Transcriptional amplifiers": "#1f78b4",
    "Cytokine/inflammation": "#b2182b",
    "Invasion & ECM remodeling": "#542788",
    "DNA repair & stress tolerance": "#01665e"
}

SPOKES = [
    "RTKs & adaptors",
    "RAS–MAPK core",
    "PI3K–AKT axis",
    "Cell cycle & replication",
    "Cell survival",
    "Transcriptional amplifiers",
    "Cytokine/inflammation",
    "Invasion & ECM remodeling",
    "DNA repair & stress tolerance",
]

# Fixed angles in degrees
ANGLES = [30, 60, 90, 120, 150, 210, 250, 290, 330]

GENES_BY_PATHWAY = {
    "RTKs & adaptors": ["EGFR", "ERBB2", "ERBB3", "FGFR1", "MET", "PDGFA"],
    "RAS–MAPK core": ["ETS1", "NRAS", "HRAS", "RAF1"],
    "PI3K–AKT axis": ["AKT2", "PIM1", "IGF1", "HSP90AB1"],
    "Cell cycle & replication": ["CCND1", "CDK4", "CCNE1", "E2F1", "PCNA", "TERT"],
    "Cell survival": ["TP53", "BIRC5", "BCL2", "BCL2L1", "BCL3", "BCL2A1"],
    "Transcriptional amplifiers": ["STAT3", "HIF1A", "JUN", "MTA1", "MYC", "MYCN"],
    "Cytokine/inflammation": ["IL6", "CXCL8", "PTGS2", "TGFB1"],
    "Invasion & ECM remodeling": ["CD44", "MMP9", "MUC1", "RET", "NPM1"],
    "DNA repair & stress tolerance": ["ERCC2", "MSH6", "FANCG", "XPC"],
}

SPOKE_EDGES = [
    ("RTKs & adaptors", "RAS–MAPK core"),
    ("RTKs & adaptors", "PI3K–AKT axis"),
    ("RAS–MAPK core", "Cell cycle & replication"),
    ("RAS–MAPK core", "Transcriptional amplifiers"),
    ("PI3K–AKT axis", "Cell survival"),
    ("PI3K–AKT axis", "Cell cycle & replication"),
    ("Cytokine/inflammation", "Transcriptional amplifiers"),
    ("Cytokine/inflammation", "Invasion & ECM remodeling"),
]

HALLMARKS = {
#    "RTKs & adaptors": "Proliferative Signaling (PS)",
    "RAS–MAPK core": "Sustaining Proliferative Signaling",
    "PI3K–AKT axis": "Resist Cell Death, Dereg. Cell Energetics",
    "Cell cycle & replication": "Proliferative Signaling, Replicative Immortality",
    "Cell survival": "Resisting Cell Death",
    "Invasion & ECM remodeling": "Activating Invasion and Metastasis",
    "DNA repair & stress tolerance": "Genome Instability",
#    "Transcriptional amplifiers": "Proliferation, Immortality, Inflammation"
    "Cytokine/inflammation": "Tumor-Promoting Inflammation, Immune Evasion"
}

# ----------------------------
# Functions
# ----------------------------

def spoke_positions(radius):
    """Return spoke endpoints at fixed angles."""
    positions = {}
    for name, deg in zip(SPOKES, ANGLES):
        theta = math.radians(deg)
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        positions[name] = (x, y)
    return positions

def place_gene_boxes(ax, origin, end, genes, box_color,
                     box_size=(1.0, 0.35), gap=0.22, start_offset=1.5):
    ox, oy = origin
    ex, ey = end
    vx, vy = (ex - ox, ey - oy)
    L = math.hypot(vx, vy)
    ux, uy = (vx / L, vy / L)

    cursor = start_offset
    last_pos = None

    for gene in genes:
        cx = ox + ux * cursor
        cy = oy + uy * cursor
        w, h = box_size

        rect = FancyBboxPatch((cx - w/2, cy - h/2),
                              w, h,
                              boxstyle="round,pad=0.02,rounding_size=0.08",
                              facecolor=box_color,
                              edgecolor="black",
                              linewidth=1.0,
                              alpha=0.9)
        ax.add_patch(rect)
        # Italicize gene code
        ax.text(cx, cy, r"$\it{" + gene + "}$",
                ha="center", va="center",
                color="black", fontsize=11, fontweight="bold")

        last_pos = (cx, cy)
        cursor += h + gap

    return last_pos

def draw_arrow(ax, src, dst, color="#555555"):
    arr = FancyArrowPatch(src, dst,
                          connectionstyle="arc3,rad=0.15",
                          arrowstyle="-|>",
                          mutation_scale=12,
                          linewidth=1.5,
                          color=color,
                          alpha=0.8)
    ax.add_patch(arr)

# ----------------------------
# Main
# ----------------------------

def main():
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect("equal")
    ax.axis("off")

    center = (0.0, 0.0)
    hub = Circle(center, 0.7, facecolor="#f7f7f7",
                 edgecolor="#222222", linewidth=1.5)
    ax.add_patch(hub)
    ax.text(0, 0, "Oncogenic\nCore Network",
            ha="center", va="center", fontsize=18, fontweight="bold")

    ring_radius = 1.3
    pos = spoke_positions(ring_radius)

    last_positions = {}

    for name in SPOKES:
        ex, ey = pos[name]
        # Draw spoke line
        ax.plot([center[0], ex], [center[1], ey],
                color=SPOKE_COLORS[name], linewidth=2, alpha=0.8)

        # Place gene boxes
        last_box = place_gene_boxes(ax, center, (ex, ey),
                                    GENES_BY_PATHWAY[name],
                                    BOX_COLORS[name])

        if last_box:
            lx, ly = last_box
            dx, dy = (ex - center[0], ey - center[1])
            norm = math.hypot(dx, dy)
            ux, uy = dx/norm, dy/norm
            label_x = lx + ux * 1.2
            label_y = ly + uy * 1.2
            # Smaller spoke labels, dark colors
            ax.text(label_x, label_y, name,
                    color=SPOKE_COLORS[name], fontsize=12, fontweight="bold",
                    ha="center", va="center")
            last_positions[name] = (lx, ly)

            # Add hallmark labels if defined
            if name in HALLMARKS:
                hx = label_x + ux * 1.3
                hy = label_y + uy * 1.3
                ax.text(hx, hy, HALLMARKS[name],
                        fontsize=12, color="#555555",
                        ha="center", va="center", fontstyle="italic")

    # Draw arrows between last box positions
    for src, dst in SPOKE_EDGES:
        if src in last_positions and dst in last_positions:
            draw_arrow(ax, last_positions[src], last_positions[dst])

    plt.tight_layout()
    plt.savefig("oncogene_network_fixed_angles.png", dpi=300)
    plt.savefig("oncogene_network_fixed_angles.svg")
    plt.show()

if __name__ == "__main__":
    main()