"""Rebuild E6 architecture and results figures: pip install matplotlib."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets/e6_custom_v1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "svg.fonttype": "none"})
NAVY, TEAL, GRAY = "#183549", "#087f8c", "#5f7080"

def build():
    e6 = json.loads((DATA / "e6_update100_summary.json").read_text())
    paired_path = DATA / "matched_comparison.json"
    paired = json.loads(paired_path.read_text()) if paired_path.exists() else None
    if paired and (paired["rows"] != 300 or not paired["audit_passed"]):
        raise ValueError("Incomplete comparison cannot be rendered")
    original = paired["original_summary"] if paired else None
    fig, ax = plt.subplots(figsize=(14, 8), facecolor="white")
    ax.set(xlim=(0,14), ylim=(0,8)); ax.axis("off")
    ax.text(.5,7.55,"E6: learning computable representations",fontsize=23,weight="bold",color=NAVY)
    ax.text(.5,7.07,"Synthetic task families / model-only generation / post-generation scoring",color=GRAY)
    def box(x,y,w,h,title,body,color="#edf5f7"):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.03,rounding_size=0.10",facecolor=color,edgecolor="#bacbd3"))
        ax.text(x+.18,y+h-.32,title,weight="bold",color=NAVY,fontsize=13)
        ax.text(x+.18,y+h-.66,body,va="top",color=NAVY,fontsize=11,linespacing=1.4)
    def arrow(x1,y1,x2,y2):
        ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops={"arrowstyle":"->","color":GRAY,"lw":1.8})
    box(.5,4.7,3.65,1.65,"1,500 training tasks","500 per domain\nMath / programming / logic\nChecked maps + answers")
    box(5.0,4.7,3.8,1.65,"E6 adaptation","Original Qwen3-8B + fresh LoRA\n100 updates / fixed final checkpoint")
    box(9.7,4.7,3.8,1.65,"Original Qwen3-8B","Same base revision\nNo adapter or additional training")
    arrow(4.15,5.55,5.0,5.55)
    box(.5,2.05,3.65,1.95,"300 development tasks","100 per domain / familiar families\nPreviously inspected development\nSame IDs, prompts and decoding")
    box(5.0,2.05,8.5,1.95,"Matched model-only evaluation","Each model generates its own answer/map; no solver repairs the answer.\nScore final-answer accuracy and reference-contract validity separately.\n"+("Both 300-task results verified." if paired else "E6: 268/300 (89.33%) / Original: completion pending."))
    arrow(4.15,3.05,5.0,3.05);arrow(6.9,4.7,6.9,4.0);arrow(11.6,4.7,11.6,4.0)
    ax.text(.5,1.35,"Representation",weight="bold",color=NAVY)
    ax.text(2.6,1.35,"Signed cardinalities (math) / indexed relations (programming) / finite-set logic",color=GRAY,fontsize=11)
    ax.text(.5,.67,"Boundary: this comparison does not establish transfer to unseen source material or isolate a causal set-map benefit.",color=GRAY,fontsize=11)
    for ext in ("svg","png"): fig.savefig(ROOT/("architecture."+ext),dpi=150,bbox_inches="tight",facecolor="white")
    plt.close(fig)
    labels=["Math", "Programming", "Logic", "Overall"]
    keys=["math","programming","logic","all"]
    fig,ax=plt.subplots(figsize=(11,6),facecolor="white")
    e=[100*e6["groups"][k]["answer_correct"]/e6["groups"][k]["rows"] for k in keys]
    if original:
        o=[100*original["groups"][k]["answer_correct"]/original["groups"][k]["rows"] for k in keys]
        bars1=ax.bar([x-.2 for x in range(4)],o,width=.36,label="Original Qwen3-8B",color="#98a9b6")
        bars2=ax.bar([x+.2 for x in range(4)],e,width=.36,label="E6 update100",color=TEAL)
        ax.bar_label(bars1,labels=[f"{v:.1f}%" for v in o],padding=4)
    else:
        bars2=ax.bar(range(4),e,width=.5,label="E6 update100",color=TEAL)
    ax.bar_label(bars2,labels=[f"{v:.2f}%" for v in e],padding=4)
    ax.set(xticks=range(4),xticklabels=labels,ylim=(0,110),ylabel="Final-answer accuracy (%)")
    ax.set_title("E6 custom development results",loc="left",fontsize=20,weight="bold",pad=22,color=NAVY)
    ax.spines[["top","right"]].set_visible(False);ax.grid(axis="y",alpha=.18);ax.set_axisbelow(True)
    ax.legend(loc="upper right",frameon=False)
    fig.text(.125,.015,"300 previously inspected development tasks / 100 per domain / single seed\n"+("Matched Original/E6 comparison; not unseen-source transfer." if paired else "Original matched result pending; missing results are not plotted as zero."),fontsize=10,color=GRAY)
    fig.subplots_adjust(bottom=.18,top=.85)
    for ext in ("svg","png"):fig.savefig(ROOT/"figures"/("e6_results."+ext),dpi=150,bbox_inches="tight",facecolor="white")
    plt.close(fig)
    for svg in (ROOT/"architecture.svg", ROOT/"figures/e6_results.svg"):
        svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())+"\n",encoding="utf-8",newline="\n")
    (ROOT/"architecture.mmd").write_text('flowchart TB\n  T["1500 synthetic training tasks + checked maps"] --> E["Qwen3-8B + fresh LoRA: E6 fixed update100"]\n  O["Original Qwen3-8B: no adaptation"] --> V["Same 300 development tasks; matched prompts and greedy decoding"]\n  E --> V\n  V --> S["Model-only generation; post-generation answer and map scoring"]\n  S --> B["Previously inspected familiar families; unseen-source transfer unproven"]\n',encoding="utf-8",newline="\n")

if __name__ == "__main__":build()
