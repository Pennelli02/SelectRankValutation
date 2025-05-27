import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Usa backend compatibile
import matplotlib

matplotlib.use('TkAgg')


def plot_benchmarks(csv_path="output/benchmark_results.csv"):
    df = pd.read_csv(csv_path)
    sns.set(style="whitegrid")
    os.makedirs("../output/plots", exist_ok=True)
    os.makedirs("../output/plots/confronto", exist_ok=True)

    structures = {
        "LinkedList": {
            "Select": "Select_LinkedList",
            "Rank": "Rank_LinkedList"
        },
        "BinarySearchTree": {
            "Select": "Select_BinaryTree",
            "Rank": "Rank_BinaryTree"
        },
        "RedBlackTree": {
            "Select": "Select_RedBlackTree",
            "Rank": "Rank_RedBlackTree"
        }
    }

    data_types = df["DataType"].unique()
    operations = ["Select", "Rank"]

    # 1. Confronto per tipo di dato e operazione tra tutte le strutture
    for data_type in data_types:
        subset = df[df["DataType"] == data_type]
        for op in operations:
            plt.figure(figsize=(10, 6))
            for struct_name, ops in structures.items():
                col = ops[op]
                if col in subset.columns:
                    sns.lineplot(
                        data=subset,
                        x="Size",
                        y=col,
                        label=struct_name
                    )
            plt.title(f"{op} - {data_type}")
            plt.xlabel("Dimensione struttura")
            plt.ylabel("Tempo medio (ms)")
            plt.legend(title="Struttura Dati")
            plt.tight_layout()
            filename = f"output/plots/confronto/{data_type}_{op.lower()}.png"
            plt.savefig(filename)
            plt.close()
            print(f" Salvato: {filename}")

    # 🔹 2. Dettaglio per ogni struttura per tipo di dato e operazione
    for data_type in data_types:

        subset = df[df["DataType"] == data_type]
        for struct_name, ops in structures.items():
            os.makedirs(f"output/plots/{struct_name}", exist_ok=True)
            for op, col in ops.items():
                if col in subset.columns:
                    plt.figure(figsize=(10, 6))
                    sns.lineplot(
                        data=subset,
                        x="Size",
                        y=col,
                    )
                    plt.title(f"{op} - {struct_name} - {data_type}")
                    plt.xlabel("Dimensione struttura")
                    plt.ylabel("Tempo medio (ms)")
                    plt.tight_layout()
                    os.makedirs(f"output/plots/{struct_name}/{data_type}", exist_ok=True)
                    filename = f"output/plots/{struct_name}/{data_type}/{op.lower()}.png"
                    plt.savefig(filename)
                    plt.close()
                    print(f" Salvato: {filename}")


if __name__ == "__main__":
    plot_benchmarks()
