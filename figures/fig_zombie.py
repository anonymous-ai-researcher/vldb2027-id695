#!/usr/bin/env python3
"""
Single-column vector reproduction of Figure 5 (a revoked vector still routes,
fig:zombie), styled to MATCH Figure 3 (fig_dilemma.py): same Linux Libertine O
bold 11pt text, same 3x1 layout, 4.95cm x 4.6cm panels, 1.2cm inter-panel sep,
same colours/markers/axis styling. Output: dpi=1200 PDF with embedded fonts
(pdf.fonttype=42), for \\includegraphics[width=\\columnwidth].
Data taken verbatim from the inline pgfplots fig:zombie block.
"""
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import os
import matplotlib.font_manager as fm

# Load the Linux Libertine O fonts bundled alongside this script so figures
# match the paper's body text. If they are missing, fall back gracefully to
# matplotlib's default font (the figure still renders, just in a different face).
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
LIB = "Linux Libertine O"
_have_libertine = True
try:
    for _f in ("LinLibertineO.otf", "LinLibertineOI.otf",
               "LinLibertineO-Bold.otf", "LinLibertineO-BoldItalic.otf"):
        _p = os.path.join(FONT_DIR, _f)
        if os.path.exists(_p):
            fm.fontManager.addfont(_p)
        else:
            _have_libertine = False
    if not _have_libertine:
        LIB = "DejaVu Sans"  # matplotlib default fallback
except Exception:
    LIB = "DejaVu Sans"
    _have_libertine = False
YLX = -0.150   # y-label -> axis distance (consistent across panels)

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.family": LIB, "font.size": 11, "font.weight": "bold",
    "mathtext.fontset": "custom",
    "mathtext.rm": f"{LIB}:bold", "mathtext.bf": f"{LIB}:bold",
    "mathtext.it": f"{LIB}:italic:bold",
    "mathtext.cal": f"{LIB}:bold", "mathtext.sf": f"{LIB}:bold",
    "mathtext.tt": f"{LIB}:bold",
    "axes.linewidth": 0.4, "axes.edgecolor": (0.725, 0.725, 0.725),
    "axes.labelweight": "bold", "axes.titleweight": "bold",
    "xtick.major.width": 0.4, "ytick.major.width": 0.4,
    "xtick.minor.width": 0.3, "ytick.minor.width": 0.3,
    "xtick.color": (0.40, 0.40, 0.40), "ytick.color": (0.40, 0.40, 0.40),
    "xtick.labelcolor": "black", "ytick.labelcolor": "black",
    "xtick.major.size": 2.2, "ytick.major.size": 1.6, "ytick.major.pad": 1.6,
    "xtick.minor.size": 1.2, "ytick.minor.size": 1.2,
})

leakc = (213/255, 94/255, 0/255)     # Tombstone
pfilt = (230/255, 159/255, 0/255)    # Post-filter
lethe = (0/255, 114/255, 178/255)    # Lethe
black65 = (0.35, 0.35, 0.35)         # Oracle dashed
black55 = (0.45, 0.45, 0.45)         # random line
gridc = (0.92, 0.92, 0.92)

CM = 1/2.54
PW, PH, SEP = 4.95, 4.6, 1.2
LM, RM, BM, TM = 1.55, 0.26, 1.32, 0.55
TOTW = LM + 3*PW + 2*SEP + RM
TOTH = TM + PH + BM

fig = plt.figure(figsize=(TOTW*CM, TOTH*CM))
def panel(i):
    return fig.add_axes([(LM + i*(PW+SEP))/TOTW, BM/TOTH, PW/TOTW, PH/TOTH])

def boldticks(ax):
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontweight("bold")

def style(ax):
    ax.tick_params(labelsize=11)
    ax.grid(True, which="major", color=gridc, lw=0.3, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(-3, 53); ax.set_xticks([0, 10, 20, 30, 40, 50])
    ax.set_xlabel("Revoked fraction (%)", fontsize=11, fontweight="bold")
    boldticks(ax)

xs = [0, 10, 20, 30, 40, 50]
def eb(ax, x, y, e, c, mk, ms, lw=1.1):
    return ax.errorbar(x, y, yerr=e, color=c, lw=lw, marker=mk, ms=ms,
                       mfc=c, mec=c, mew=0.3, capsize=1.6, elinewidth=0.7,
                       ecolor=c, zorder=4)

# ---------------- (a) Traversal / operational leakage ----------------
ax = panel(0)
ax.set_title("(a)", fontsize=11, fontweight="bold", pad=2)
h_or, = ax.plot([-3, 53], [0, 0], ls=(0, (3, 1.6)), color=black65, lw=1.0, zorder=3)
h_tb = eb(ax, xs, [0, 13.243, 16.494, 19.795, 22.750, 25.912],
          [0, 0.785, 0.679, 0.549, 0.602, 0.556], leakc, "o", 3.4)
h_pf = eb(ax, xs, [0, 14.747, 18.377, 22.047, 25.583, 29.193],
          [0, 0.697, 0.540, 0.539, 0.679, 0.534], pfilt, "^", 3.6)
h_le, = ax.plot(xs, [0, 0, 0, 0, 0, 0], color=lethe, lw=1.4, marker="s",
                ms=3.2, mfc=lethe, mec=lethe, mew=0.3, zorder=5)
ax.set_ylim(-2, 33); ax.set_yticks([0, 10, 20, 30])
ax.set_ylabel("Operational leakage (%)", fontsize=11, fontweight="bold")
ax.yaxis.set_label_coords(YLX, 0.5)
style(ax)
ax.legend([h_tb, h_pf, h_le, h_or], ["Tombstone", "Post-filter", "Lethe", "Oracle"],
          prop={"weight": "bold", "size": 9}, loc="upper left", frameon=False,
          handlelength=1.5, handletextpad=0.4, borderpad=0.15, labelspacing=0.25,
          bbox_to_anchor=(-0.02, 1.02))

# ---------------- (b) Drift ----------------
ax = panel(1)
ax.set_title("(b)", fontsize=11, fontweight="bold", pad=2)
ax.plot([-3, 53], [0, 0], ls=(0, (3, 1.6)), color=black65, lw=1.0, zorder=3)
eb(ax, xs, [0, 5.028, 8.707, 11.842, 14.722, 17.578],
   [0, 0.266, 0.329, 0.339, 0.388, 0.367], leakc, "o", 3.4)
eb(ax, xs, [0, 5.421, 9.320, 12.765, 15.924, 18.924],
   [0, 0.332, 0.281, 0.340, 0.350, 0.468], pfilt, "^", 3.6)
eb(ax, xs, [0, 0.316, 0.494, 0.713, 0.932, 0.936],
   [0, 0.245, 0.274, 0.317, 0.328, 0.408], lethe, "s", 3.2)
ax.set_ylim(-1.5, 21); ax.set_yticks([0, 5, 10, 15, 20])
ax.set_ylabel("Top-10 drift (%)", fontsize=11, fontweight="bold")
ax.yaxis.set_label_coords(YLX, 0.5)
style(ax)

# ---------------- (c) Distinguishing AUC ----------------
ax = panel(2)
ax.set_title("(c)", fontsize=11, fontweight="bold", pad=2)
ax.plot([-3, 53], [0.5, 0.5], ls=(0, (3, 1.6)), color=black55, lw=0.9, zorder=3)
ax.text(27, 0.492, "random (indistinguishable)", fontsize=8, fontweight="bold",
        color=(0.30, 0.30, 0.30), ha="center", va="top")
xc = [10, 20, 30, 40, 50]
eb(ax, xc, [0.781, 0.821, 0.861, 0.879, 0.880],
   [0.015, 0.016, 0.013, 0.004, 0.001], leakc, "o", 3.4)
eb(ax, xc, [0.796, 0.839, 0.864, 0.865, 0.865],
   [0.011, 0.016, 0.005, 0.001, 0.001], pfilt, "^", 3.6)
eb(ax, xc, [0.508, 0.509, 0.509, 0.506, 0.508],
   [0.011, 0.012, 0.011, 0.012, 0.011], lethe, "s", 3.2)
ax.set_ylim(0.46, 0.92); ax.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9])
ax.set_ylabel("Distinguishing AUC", fontsize=11, fontweight="bold")
ax.yaxis.set_label_coords(YLX, 0.5)
style(ax)

fig.savefig("fig_zombie.pdf", dpi=1200)
print("wrote fig_zombie.pdf  (%.2f x %.2f cm)  ALL BOLD" % (TOTW, TOTH))
