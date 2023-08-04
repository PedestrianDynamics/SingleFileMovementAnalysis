from pylab import *


def style_plot():
    params = {
        'font.style': 'normal',
        'font.family': 'serif',
        "mathtext.fontset": "cm",  # change the font of mathtext (r"$$")
        # 'font.variant': 'normal',
        # 'font.weight': 'normal',
        # 'font.stretch': 'normal',
        'font.size': 30,
        # 'axes.facecolor': 'white',
        # 'axes.edgecolor': 'black',
        # 'axes.linewidth': 1.0,  # the width of the plot frame
        'axes.titlesize': 30,
        'axes.labelpad': 15,  # spacing or distance between the tick labels and the axis labels
        'axes.titlepad': 15,
        'axes.labelsize': 30,
        # 'axes.labelweight': 'normal',
        # 'xtick.major.size': 4,  # major tick size in points
        # 'ytick.major.size': 4,  # major tick size in points
        # 'xtick.minor.size': 2,  # minor tick size in points
        # 'ytick.minor.size': 2,  # minor tick size in points
        # 'xtick.major.width': 0.5,  # major tick width in points
        # 'ytick.major.width': 0.5,  # major tick width in points
        # 'xtick.minor.width': 20,  # minor tick width in points
        # 'ytick.minor.width': 0.5,  # minor tick width in points
        # 'xtick.major.pad': 10,  # distance to major tick label in points
        # 'ytick.major.pad': 10,  # distance to major tick label in points
        # 'xtick.minor.pad': 4,  # distance to the minor tick label in points
        # 'ytick.minor.pad': 4,  # distance to the minor tick label in points
        # 'xtick.color': 'k',  # color of the tick labels
        # 'ytick.color': 'k',  # color of the tick labels
        'xtick.labelsize': 20,  # font size of the tick labels
        'ytick.labelsize': 20,  # font size of the tick labels
        # 'xtick.direction': 'in',  # direction: in, out, or inout
        # 'ytick.direction': 'in',  # direction: in, out, or inout
        # 'legend.numpoints': 1,
        'legend.fontsize': 30,
        # 'legend.borderpad': 0.5,  # border whitespace in fontsize units
        # 'legend.borderaxespad': 0.5,  # the border between the axes and legend edge in fraction of font
        # 'legend.loc': 'upper right',
        # 'legend.markerscale': 1.5,  # the relative size of legend markers vs. original
        # 'legend.edgecolor': 'none',
        # 'legend.handletextpad': 0.5,  # Distance between legend marker and text
        # 'lines.markersize': 20,
        # 'lines.linewidth': 1.0,
        # 'lines.markeredgewidth': 3,  # the line width around the marker symbol
        # 'figure.constrained_layout.use': True,
        'figure.figsize': [12, 8],
        'savefig.format': 'pdf',
        'savefig.bbox': 'tight', # Tweak spacing to prevent clipping of ylabel
        'savefig.dpi': 100,
        # 'grid.linestyle': '--',
    }

    rcParams.update(params)
    return True
