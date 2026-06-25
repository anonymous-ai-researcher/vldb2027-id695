#!/usr/bin/env python3
"""
Single-column vector reproduction of Figure 6 (fig:recall), styled to match
Figure 5 / Figure 3 (Linux Libertine O bold 11pt, pdf.fonttype=42, dpi=1200).
Two panels side by side: (a) Recall@10 vs revoked fraction; (b) revoked-user vs
unaffected-user drift scatter. Data verbatim from the inline pgfplots block.
Output for \\includegraphics[width=\\columnwidth].
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
    "xtick.color": (0.40, 0.40, 0.40), "ytick.color": (0.40, 0.40, 0.40),
    "xtick.labelcolor": "black", "ytick.labelcolor": "black",
    "xtick.major.size": 2.2, "ytick.major.size": 1.6, "ytick.major.pad": 1.6,
})

lethe = (0/255, 114/255, 178/255)
leakc = (213/255, 94/255, 0/255)
costc = (120/255, 120/255, 128/255)
good = (0/255, 158/255, 115/255)
black65 = (0.35, 0.35, 0.35)
gridc = (0.92, 0.92, 0.92)

CM = 1/2.54
PW, PH, SEP = 7.5, 5.7, 1.75
LM, RM, BM, TM = 1.7, 0.30, 1.35, 0.55
TOTW = LM + 2*PW + SEP + RM
TOTH = TM + PH + BM

fig = plt.figure(figsize=(TOTW*CM, TOTH*CM))
def panel(i):
    return fig.add_axes([(LM + i*(PW+SEP))/TOTW, BM/TOTH, PW/TOTW, PH/TOTH])

def boldticks(ax):
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontweight("bold")

def grid(ax):
    ax.grid(True, which="major", color=gridc, lw=0.3, zorder=0)
    ax.set_axisbelow(True); boldticks(ax)

xs = [10, 20, 30, 40, 50]

# ---------------- (a) Recall is preserved ----------------
ax = panel(0)
ax.set_title("(a)", fontsize=11, fontweight="bold", pad=2)
h_or, = ax.plot(xs, [0.9803, 0.9805, 0.9813, 0.9801, 0.9807],
                ls=(0, (3, 1.6)), color=black65, lw=1.0, zorder=3)
h_le = ax.errorbar(xs, [0.9763, 0.9761, 0.9761, 0.9764, 0.9762],
                   yerr=[0.0053, 0.0050, 0.0047, 0.0040, 0.0044], color=lethe,
                   lw=1.3, marker="s", ms=3.2, mfc=lethe, mec=lethe, mew=0.3,
                   capsize=1.6, elinewidth=0.7, zorder=5)
h_tb = ax.errorbar(xs, [0.9411, 0.9408, 0.9402, 0.9396, 0.9402],
                   yerr=[0.0053, 0.0052, 0.0047, 0.0052, 0.0050], color=leakc,
                   lw=1.0, marker="o", ms=3.0, mfc=leakc, mec=leakc, mew=0.3,
                   capsize=1.6, elinewidth=0.7, zorder=4)
h_pd = ax.errorbar(xs, [0.9440, 0.9442, 0.9435, 0.9449, 0.9437],
                   yerr=[0.0052, 0.0057, 0.0054, 0.0042, 0.0050], color=costc,
                   lw=1.0, marker="D", ms=3.0, mfc=costc, mec=costc, mew=0.3,
                   capsize=1.6, elinewidth=0.7, zorder=4)
ax.set_xlim(7, 53); ax.set_xticks(xs)
ax.set_ylim(0.93, 0.985); ax.set_yticks([0.94, 0.96, 0.98])
ax.set_xlabel("Revoked fraction (%)", fontsize=11, fontweight="bold")
ax.set_ylabel("Recall@10", fontsize=11, fontweight="bold")
ax.yaxis.set_label_coords(-0.155, 0.5)
grid(ax)
ax.legend([h_or, h_le, h_tb, h_pd], ["Oracle", "Lethe", "Tombstone", "Physical-delete"],
          prop={"weight": "bold", "size": 8}, loc="center", ncol=2, frameon=False,
          handlelength=1.4, handletextpad=0.4, columnspacing=1.0, labelspacing=0.3,
          bbox_to_anchor=(0.5, 0.5))

# ---------------- (b) Correct erasure, local to the view ----------------
ax = panel(1)
ax.set_title("(b)", fontsize=11, fontweight="bold", pad=2)
# ideal region
ax.fill([-1.2, 3.6, 3.6, -1.2], [-2.2, -2.2, 1.05, 1.05], color=good, alpha=0.13, zorder=0)
ax.plot([3.6, 3.6, -1.2], [-2.2, 1.05, 1.05], ls=(0, (3, 1.8)),
        color=(0.0, 0.49, 0.36), lw=0.6, zorder=1)
ax.text(0.9, -1.35, "ideal: both drifts $\\approx 0$", fontsize=7.5,
        fontstyle="italic", fontweight="bold", color=(0.0, 0.45, 0.33),
        ha="center", va="center")
def pt(x, y, ex, ey, c, mk="o", ms=4.0):
    ax.errorbar(x, y, xerr=ex, yerr=ey, color=c, marker=mk, ms=ms,
                mfc=c, mec=tuple(0.55*v for v in c), mew=0.4,
                capsize=1.6, elinewidth=0.7, ecolor=c, zorder=4)
pt(20.98, 0.24, 0.98, 0.03, leakc)           # Tombstone
pt(9.28, 2.15, 0.45, 0.15, leakc)            # Post-filter
pt(7.08, 10.42, 0.38, 0.68, costc)           # Physical-delete
pt(2.12, 0.23, 0.11, 0.03, costc, ms=3.2)    # Per-role-index
ax.errorbar(1.08, 0.25, xerr=0.05, yerr=0.03, color=lethe, capsize=1.6,
            elinewidth=0.7, ecolor=lethe, zorder=4)
ax.plot(1.08, 0.25, marker="*", ms=9, mfc=lethe, mec=(0, 0.31, 0.49),
        mew=0.5, zorder=6)
LBL = dict(fontsize=8.5, fontweight="bold")
ax.text(19.8, 0.24, "Tombstone", ha="right", va="center", **LBL)
ax.text(7.9, 10.42, "Physical-delete", ha="left", va="center", **LBL)
ax.text(9.9, 2.15, "Post-filter", ha="left", va="center", **LBL)
ax.plot([2.45, 3.95], [0.23, 0.23], color=(0.40, 0.40, 0.45), lw=0.4, zorder=2)
ax.text(4.15, 0.23, "Per-role-index", ha="left", va="center", **LBL)
ax.text(1.08, 1.35, "Lethe", color=(0, 0.31, 0.49), ha="center", va="bottom",
        fontsize=8.5, fontweight="bold")
ax.set_xlim(-1.2, 23.5); ax.set_xticks([0, 5, 10, 15, 20])
ax.set_ylim(-2.2, 11.6); ax.set_yticks([0, 2, 4, 6, 8, 10])
ax.set_xlabel("Revoked-user drift (%)", fontsize=11, fontweight="bold")
ax.set_ylabel("Unaffected-user drift (%)", fontsize=11, fontweight="bold")
ax.yaxis.set_label_coords(-0.135, 0.5)
grid(ax)

fig.savefig("fig_recall.pdf", dpi=1200)
print("wrote fig_recall.pdf  (%.2f x %.2f cm)" % (TOTW, TOTH))
