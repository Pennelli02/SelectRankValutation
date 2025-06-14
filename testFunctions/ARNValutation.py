import timeit
import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from StruttureDati import ARN  # Assicurati che questo punti alla tua classe TreeRedBlack
import numpy as np
from scipy.interpolate import make_interp_spline




def benchmark_rbt_select_rank(trials=1000, output_dir="output/plots/RBTLarge"):
    os.makedirs(output_dir, exist_ok=True)
    sizes = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 70000, 100000, 200000, 500000, 700000,
             1000000]

    results = {
        "Size": [],
        "Select_Time_ms": [],
        "Rank_Time_ms": [],
    }

    for size in sizes:
        print(f" Benchmarking ARN con N = {size}")
        data = random.sample(range(1, size + 1), size)

        tree = ARN.TreeRedBlack()
        for val in data:
            tree.insert(val)

        i_select = size // 2
        target_value = sorted(data)[i_select]
        target_node = tree.search(target_value)

        def avg_time(func):
            return sum(timeit.timeit(func, number=1) * 1000 for _ in range(trials)) / trials

        t_select = avg_time(lambda: tree.Os_Select(tree.root, i_select + 1))
        t_rank = avg_time(lambda: tree.Os_Rank(target_node)) if target_node else float("nan")

        results["Size"].append(size)
        results["Select_Time_ms"].append(t_select)
        results["Rank_Time_ms"].append(t_rank)

    # Salva i risultati
    df = pd.DataFrame(results)
    df.to_csv("output/benchmark_rbt_large.csv", index=False)

    # Grafico SELECT
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Size", y="Select_Time_ms", marker="o", color="blue")
    plt.title("Tempo SELECT su Red-Black Tree")
    plt.xlabel("Dimensione dell'albero")
    plt.ylabel("Tempo medio (ms)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/plots/RBTLarge/select.png")
    # plt.show()

    # Grafico RANK
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Size", y="Rank_Time_ms", color="green")
    plt.title(" Tempo RANK su Red-Black Tree")
    plt.xlabel("Dimensione dell'albero")
    plt.ylabel("Tempo medio (ms)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/plots/RBTLarge/rank.png")
    # plt.show()


if __name__ == "__main__":
    benchmark_rbt_select_rank()
