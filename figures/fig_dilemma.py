#!/usr/bin/env python3
"""
Standalone vector reproduction of Figure 3 (the deletion dilemma, fig:dilemma)
from the Lethe paper. Matches the inline pgfplots version (same data, 3x1 layout,
4.95cm x 4.6cm panels, 1.2cm inter-panel sep, log axes, colours, markers) with
ALL TEXT IN BOLD Linux Libertine O. Output: dpi=1200 PDF with embedded fonts
(pdf.fonttype=42), for \\includegraphics[width=\\columnwidth].
"""
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import FixedLocator, NullFormatter

FONT_DIR = "/home/claude/fonts"
for f in ("LinLibertineO.otf", "LinLibertineOI.otf",
          "LinLibertineO-Bold.otf", "LinLibertineO-BoldItalic.otf"):
    fm.fontManager.addfont(f"{FONT_DIR}/{f}")
LIB = "Linux Libertine O"
BW = "bold"   # everything bold
YLX = -0.126  # SAME y-label->axis distance for all three panels (small safe gap at c)

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

leakc   = (213/255, 94/255, 0/255)
crp     = (204/255, 121/255, 167/255)
crp58   = (0.58*204/255, 0.58*121/255, 0.58*167/255)
black70 = (0.30, 0.30, 0.30)
black80 = (0.20, 0.20, 0.20)
gridc   = (0.92, 0.92, 0.92)

CM = 1/2.54
PW, PH, SEP = 4.95, 4.6, 1.2
LM, RM, BM, TM = 1.45, 0.26, 1.32, 0.60
TOTW = LM + 3*PW + 2*SEP + RM
TOTH = TM + PH + BM

fig = plt.figure(figsize=(TOTW*CM, TOTH*CM))
def panel(i):
    return fig.add_axes([(LM + i*(PW+SEP))/TOTW, BM/TOTH, PW/TOTW, PH/TOTH])

def boldticks(ax):
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontweight("bold")

def style(ax, log=False):
    ax.tick_params(labelsize=11)
    ax.grid(True, which="major", color=gridc, lw=0.3, zorder=0)
    if log:
        ax.grid(True, which="minor", color=gridc, lw=0.2, zorder=0)
    ax.set_axisbelow(True)
    boldticks(ax)

# ---------------- (a) ----------------
ax = panel(0)
ax.set_title("(a)", fontsize=11, fontweight="bold", pad=2)
ax.plot([-3, 53], [0, 0], ls=(0, (3, 1.6)), color=black70, lw=1.0,
        label="Oracle rebuild", zorder=3)
xa = [0, 10, 20, 30, 40, 50]
ya = [0, 5.03, 8.71, 11.84, 14.72, 17.58]
ea = [0, 0.27, 0.33, 0.34, 0.39, 0.37]
ax.errorbar(xa, ya, yerr=ea, color=leakc, lw=1.1, marker="o", ms=3.4,
            mfc=leakc, mec=leakc, mew=0.3, capsize=1.6, elinewidth=0.7,
            ecolor=leakc, label="Tombstone", zorder=4)
ax.set_xlim(-3, 53); ax.set_ylim(-1.5, 20)
ax.set_xticks([0, 10, 20, 30, 40, 50]); ax.set_yticks([0, 5, 10, 15, 20])
ax.set_xlabel("Revoked fraction (%)", fontsize=11, fontweight="bold")
ax.set_ylabel("Top-10 drift (%)", fontsize=11, fontweight="bold")
ax.yaxis.set_label_coords(YLX, 0.5)
style(ax)
ax.legend(prop={"weight": "bold", "size": 10}, loc="upper left", frameon=False,
          handlelength=1.6, handletextpad=0.5, borderpad=0.2, labelspacing=0.3,
          bbox_to_anchor=(0.0, 1.0))

# ---------------- (b) ----------------
ax = panel(1)
ax.set_title("(b)", fontsize=11, fontweight="bold", pad=2)
ax.plot([1e6, 1.2e6, 1.8e6, 8e6], [11.8, 14.1, 21.3, 93.0],
        color=black80, lw=1.1, marker="s", ms=3.6,
        mfc=black80, mec=black80, mew=0.3, zorder=4)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(9.3e5, 8.7e6); ax.set_ylim(9.5, 180)
ax.xaxis.set_major_locator(FixedLocator([1e6, 2e6, 4e6, 8e6]))
ax.set_xticklabels(["1M", "2M", "4M", "8M"], fontsize=11, fontweight="bold")
ax.xaxis.set_minor_formatter(NullFormatter())
ax.yaxis.set_major_locator(FixedLocator([10, 20, 40, 80, 160]))
ax.set_yticklabels(["10", "20", "40", "80", "160"], fontsize=11, fontweight="bold")
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("Corpus size $N$", fontsize=11, fontweight="bold")
ax.set_ylabel("Rebuild time (s)", fontsize=11, fontweight="bold")
ax.yaxis.set_label_coords(YLX, 0.5)
style(ax, log=True)

# ---------------- (c) ----------------
ax = panel(2)
ax.set_title("(c)", fontsize=11, fontweight="bold", pad=2)
xc = [0.0167, 0.0833, 0.5, 1.0, 6.0, 24.0]
ax.plot(xc, [19.667, 3.933, 0.656, 0.328, 0.0546, 0.0137],
        color=crp, lw=1.1, marker="o", ms=3.4, mfc=crp, mec=crp, mew=0.3,
        label="$N{=}1$M", zorder=4)
ax.plot(xc, [155.0, 31.0, 5.167, 2.583, 0.431, 0.108],
        color=crp58, lw=1.1, marker="o", ms=3.4, mfc=crp58, mec=crp58, mew=0.3,
        label="$N{=}8$M", zorder=4)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(0.012, 33); ax.set_ylim(0.0065, 175)
ax.xaxis.set_major_locator(FixedLocator([0.01, 0.1, 1, 10]))
ax.set_xticklabels(["0.01", "0.1", "1", "10"], fontsize=11, fontweight="bold")
ax.xaxis.set_minor_formatter(NullFormatter())
ax.yaxis.set_major_locator(FixedLocator([0.01, 0.1, 1, 10, 100]))
ax.set_yticklabels(["0.01", "0.1", "1", "10", "100"], fontsize=11, fontweight="bold")
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("Compliance window (h)", fontsize=11, fontweight="bold")
ax.set_ylabel("% time rebuilding", fontsize=11, fontweight="bold")
ax.yaxis.set_label_coords(YLX, 0.5)
style(ax, log=True)
ax.legend(prop={"weight": "bold", "size": 10}, loc="upper right", frameon=False,
          handlelength=1.6, handletextpad=0.5, borderpad=0.2, labelspacing=0.3,
          bbox_to_anchor=(1.0, 1.0))

fig.savefig("fig_dilemma.pdf", dpi=1200)
print("wrote fig_dilemma.pdf  (%.2f x %.2f cm)  ALL BOLD" % (TOTW, TOTH))
