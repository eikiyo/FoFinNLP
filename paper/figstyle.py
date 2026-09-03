"""
Location: paper-a/paper/figstyle.py
Purpose: The ONE definition of every visual constant the figures use. Split out so make_figures and
         figpanels reference the same colour and the same font size rather than each holding a
         copy: two copies of "the rule colour" is how two panels of one figure come to disagree.
         A hardcoded hex or point size anywhere else in paper/ is a bug.
Functions: apply()
Calls: matplotlib.pyplot.rcParams
Imports: matplotlib
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402

# CONCEPT COLOURS -- one concept, one colour, in every exhibit it appears in. Defined here and
# nowhere else: a second copy is how "the flagged colour" comes to mean two things across two
# figures. Colour is the THIRD encoding, never the first: every panel that contrasts two concepts
# also separates them by position and by hatch or marker, so the figures survive a greyscale print.
#
# THREE accents and two neutrals, and both numbers are arithmetic rather than taste. The engine's
# G4 holds an accent to WCAG AA (4.5:1) against the page and its G3 caps a figure at three accents;
# this set is the largest one that clears both, so G4 is now RUN on every figure instead of being
# declared inapplicable, which is what it was until 2026-07-29. Measured against white: clean 4.70,
# flagged 5.19, observed 10.98. Under simulated deuteranopia the three separate by dE 94, 153 and
# 159, all far past the 30 the gate requires -- warm against cool is the strongest two-way pair
# available, which is why the old magenta (#AA3377, only dE 85 from clean) is gone.
#
# `null` and `threshold` are NEUTRALS by the engine's own list, which is why a background
# distribution and a reference rule do not spend one of the three accents. #999999 replaces the
# old #BBBBBB: same role, one step darker, and it is the lightest grey the engine treats as a
# neutral rather than as an accent that fails AA.
CONCEPT = {"clean": "#4477AA", "flagged": "#CC3311", "observed": "#2c3e50",
           "null": "#999999", "threshold": "#333333"}
# The stroke every INTERVAL is drawn in. Black, and that is arithmetic too: an interval is only
# ever read where it crosses a bar, so the pair that matters is stroke-against-FILL, not
# stroke-against-page. #666666 scored 1.06:1 on the flagged fill and 1.22:1 on the clean one --
# the least visible mark in a figure whose intervals are its evidence. #333333 reaches only
# 2.08 and 2.69. Black clears the 3:1 non-text threshold on every fill in this paper (4.47:1 on
# clean, 4.05:1 on flagged) and nothing lighter does.
INTERVAL = "#000000"
# CHROME is the frame, not the data: drawn behind every mark, never passed to a colour gate, and
# deliberately outside CONCEPT so a grid line cannot be mistaken for a fourth accent.
CHROME = {"band": "#DDDDDD", "grid": "#BBBBBB"}
HATCH = {"flagged": "///", "after": "\\\\\\"}
COL = {"single": CONCEPT["observed"], "rule": CONCEPT["threshold"], **CHROME, **CONCEPT}
# Colours that carry TEXT rather than fill, held by figgate to WCAG 4.5:1 against white AND 2.0
# pairwise. EXACTLY TWO, and that is arithmetic rather than taste: a third colour would have to
# sit 2.0 from both of these while staying under the luminance that 4.5:1 on white allows, and no
# such colour exists. The grey formerly used for small annotations (#666666) sat at 1.9 from the
# primary and 1.2 from the accent, so it was replaced rather than exempted -- 7pt annotations
# print better in the darker colour anyway. COL["rule"] keeps #666666 for RULES and error bars,
# which are lines, not text.
TEXT_COL = ("#2c3e50", "#4477AA")
FS = {"axis": 8, "tick": 7, "annot": 7, "panel": 8}
# "interval" is separate from "series" so an error bar's weight cannot drift when a line's does.
# 0.8pt with caps, per the rebuild brief; "null" is the no-change rule in the repair panel, which
# has to be the most prominent mark on that panel because the null IS the finding there.
LW = {"spine": 0.6, "series": 1.1, "rule": 0.8, "grid": 0.5, "interval": 0.8, "null": 1.6}
# Every reference-line label carries this box. layout-math's answer to a label that must sit on
# the rule it names: an opaque patch in the page colour, so the rule stops short of the glyphs
# instead of running through them. Opaque, not alpha-blended -- a see-through box still lets the
# rule cross the text, and figclearance refuses to count one as a mask.
LABEL_BOX = {"facecolor": "white", "edgecolor": "none", "pad": 0.8}

# ACL single column. MEASURED from the compiled document (\the\columnwidth = 219.086pt at
# 72.27pt/in = 3.0315in), not taken from the style guide's rounded 3.05. The difference matters:
# \includegraphics[width=\columnwidth] scales the figure by columnwidth/(saved width), so a figure
# that saves WIDER than the column is shrunk, and its 7pt annotations print below 7pt.
COLPT = 219.086
WIDTH_FLOOR = 0.94                      # scaling a figure UP more than this looks inconsistent
# The authored canvas is NOT the saved width: savefig(bbox_inches="tight") crops to the real ink,
# which grows when a tick label or annotation reaches past the canvas. fig2's model names did
# exactly that, saving at 222.3pt against a 219.1pt column and printing its 7pt labels at 6.90pt.
# Each figure's width is asserted against the column AFTER it is written; these are whatever makes
# that assertion pass.
COLWIDTH = {"fig1_lineup.pdf": 3.647, "fig2_contamination.pdf": 3.185,
            "fig3_transfer.pdf": 3.12, "fig4_observability.pdf": 3.14,
            "figA1_reliability.pdf": 3.255}


def apply() -> None:
    """Applied once, before any axes exist. Font family matched to the paper body: a sans-serif
    figure in a Times paper is the most common tell of a rushed submission."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "font.size": FS["tick"], "axes.labelsize": FS["axis"],
        # 7pt of clearance between an axis label and its tick labels, set ONCE rather than at each
        # set_xlabel call. The engine's overlap gate pads text boxes by 6px before testing, so the
        # matplotlib default of 4 puts a label inside its own ticks on every panel here.
        "axes.labelpad": 7,
        "xtick.labelsize": FS["tick"], "ytick.labelsize": FS["tick"],
        "axes.linewidth": LW["spine"], "axes.spines.top": False, "axes.spines.right": False,
        "xtick.major.width": LW["spine"], "ytick.major.width": LW["spine"],
        "xtick.major.size": 2.5, "ytick.major.size": 2.5,
        "figure.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    })
