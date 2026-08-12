import os, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.makedirs("figures", exist_ok=True); os.makedirs("results", exist_ok=True)
rng = np.random.default_rng(0)
def repertoire(n_clones, alpha):
    ab = rng.pareto(alpha, n_clones) + 1; return np.sort(ab / ab.sum())[::-1]
healthy = repertoire(2000, 3.0)          # diverse, even
expanded = repertoire(2000, 0.7)         # a few dominant clones (clonal expansion)
def shannon(p): p = p[p > 0]; return -np.sum(p * np.log(p))
def clonality(p): return 1 - shannon(p) / np.log(len(p))
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].loglog(np.arange(1, len(healthy)+1), healthy, label="healthy (diverse)", color="#4C72B0")
ax[0].loglog(np.arange(1, len(expanded)+1), expanded, label="tumour (expanded)", color="#C44E52")
ax[0].set_xlabel("clone rank"); ax[0].set_ylabel("clone frequency"); ax[0].set_title("Rank-abundance of TCR clones"); ax[0].legend(fontsize=8)
metrics = {"Shannon\n(healthy)": shannon(healthy), "Shannon\n(expanded)": shannon(expanded),
           "clonality\n(healthy)": clonality(healthy), "clonality\n(expanded)": clonality(expanded)}
ax[1].bar(list(metrics), list(metrics.values()), color=["#4C72B0","#C44E52","#4C72B0","#C44E52"])
ax[1].set_title("Diversity vs clonality"); ax[1].tick_params(axis="x", labelsize=8)
fig.suptitle("TCR repertoire diversity (demo data)"); fig.tight_layout(); fig.savefig("figures/demo.png", dpi=140)
open("results/summary.csv","w").write(f"shannon_healthy,{shannon(healthy):.3f}\nshannon_expanded,{shannon(expanded):.3f}\nclonality_healthy,{clonality(healthy):.3f}\nclonality_expanded,{clonality(expanded):.3f}\n")
print(f"clonality healthy={clonality(healthy):.2f} expanded={clonality(expanded):.2f}"); print("ok")
