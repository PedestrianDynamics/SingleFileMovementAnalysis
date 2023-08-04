from pylab import *


def style_plot():
    params = {
        'font.style': 'normal',
        'font.family': 'serif',
        'font.variant': 'normal',
        'font.weight': 'normal',
        'font.stretch': 'normal',
        'font.size': 12,
        'axes.facecolor': 'white',
        'axes.edgecolor': 'black',
        'axes.linewidth': 1.0,
        'axes.titlesize': 100,
        'axes.labelpad': 25,
        'axes.titlepad': 20,
        'axes.labelsize': 75,
        'axes.labelweight': 'normal',
        'xtick.major.size': 4,  # major tick size in points
        'xtick.minor.size': 2,  # minor tick size in points
        'xtick.major.width': 0.5,  # major tick width in points
        'xtick.minor.width': 20,  # minor tick width in points
        'xtick.major.pad': 10,  # distance to major tick label in points
        'xtick.minor.pad': 4,  # distance to the minor tick label in points
        'xtick.color': 'k',  # color of the tick labels
        'xtick.labelsize': 100,  # fontsize of the tick labels
        'ytick.labelsize': 100,  # fontsize of the tick labels
        'xtick.direction': 'in',  # direction: in, out, or inout
        'ytick.major.size': 4,  # major tick size in points
        'ytick.minor.size': 2,  # minor tick size in points
        'ytick.major.width': 0.5,  # major tick width in points
        'ytick.minor.width': 0.5,  # minor tick width in points
        'ytick.major.pad': 10,  # distance to major tick label in points
        'ytick.minor.pad': 4,  # distance to the minor tick label in points
        'ytick.color': 'k',  # color of the tick labels
        'ytick.direction': 'in',  # direction: in, out, or inout
        'legend.numpoints': 1,
        'legend.fontsize': 55,
        'legend.borderpad': 0.5,  # border whitespace in fontsize units
        'legend.borderaxespad': 0.5,  # the border between the axes and legend edge in fraction of font
        'legend.loc': 'upper right',
        'legend.markerscale': 1.5,  # the relative size of legend markers vs. original
        # 'legend.edgecolor': 'none',
        'legend.handletextpad': 0.5,  # Distance between legend marker and text
        'lines.markersize': 20,
        'lines.linewidth': 1.0,
        'lines.markeredgewidth': 3,  # the line width around the marker symbol
        'figure.figsize': [36, 36],
        # 'figure.constrained_layout.use': True,
        # 'figure.figsize': [20, 20],
        'savefig.format': 'pdf',
        'grid.linestyle': '--',
        'legend.loc' : 'upper left',
        'mathtext.fontset':  'dejavuserif'  # change the font of mathtext (r"$$")
    }

    rcParams.update(params)
    return True
