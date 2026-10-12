import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"

n = np.linspace(1, 80, 2000)

fig, ax = plt.subplots(figsize=(6, 3.8))
ax.plot(n, np.log2(n), color="#dc2626", label=r"$\log_2 n$")
ax.plot(n, np.sqrt(n), color="#2563eb", label=r"$\sqrt{n}$")

ax.axvline(5, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
ax.axvline(15, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)

ax.plot([4, 16], [2, 4], "o", color="black", markersize=4)

ax.set_xticks([0, 5, 15, 40, 60, 80])
ax.set_xlim(0, 80)
ax.set_ylim(0, 9.5)
ax.set_xlabel("$n$")
ax.grid(alpha=0.3)
ax.legend(loc="upper left")
fig.savefig("informe/figuras/act2_log_vs_raiz.pdf", bbox_inches="tight")
