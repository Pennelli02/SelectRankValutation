import timeit
import os
import joblib
import numpy as np
import pandas as pd

from collections import defaultdict


def benchmark_from_saved_structures(folder="input", output_csv="output/benchmark_results.csv", num_trials=5):
    results = {
        "DataType": [], "Size": [],
        "Select_LinkedList": [], "Rank_LinkedList": [],
        "Select_BinaryTree": [], "Rank_BinaryTree": [],
        "Select_RedBlackTree": [], "Rank_RedBlackTree": []
    }

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Raggruppa per tipo di dato
    grouped_files = defaultdict(list)
    for filename in os.listdir(folder):
        if filename.endswith("_linkedlist.joblib"):
            base = filename.replace("_linkedlist.joblib", "")
            try:
                data_type, size = base.split("_")
                size = int(size)
                grouped_files[data_type].append((size, base))
            except ValueError:
                print(f" Errore parsing nome file: {filename}")
                continue

    # Ordina i gruppi per data_type e size
    for data_type in sorted(grouped_files.keys()):
        for size, base in sorted(grouped_files[data_type], key=lambda x: x[0]):
            try:
                # Caricamento strutture
                ll = joblib.load(os.path.join(folder, f"{base}_linkedlist.joblib"))
                bst = joblib.load(os.path.join(folder, f"{base}_bst.joblib"))
                rbt = joblib.load(os.path.join(folder, f"{base}_rbt.joblib"))
                x_rank = joblib.load(os.path.join(folder, f"{base}_rank_value.joblib"))
            except Exception as e:
                print(f" Errore nel caricamento di {base}: {e}")
                continue

            print(f" Benchmarking {base}")
            i_select = size // 2

            def avg_measure(func):
                try:
                    times = [timeit.timeit(func, number=1000) * 1000 for _ in range(num_trials)]
                    return np.mean(times)
                except Exception as e:
                    print(f" Errore durante il timing: {e}")
                    return float('nan')

            results["DataType"].append(data_type)
            results["Size"].append(size)

            # Linked List
            try:
                results["Select_LinkedList"].append(avg_measure(lambda: ll.select(i_select)))
                results["Rank_LinkedList"].append(avg_measure(lambda: ll.rank(x_rank)))
            except Exception as e:
                print(f" Errore in LinkedList: {e}")
                results["Select_LinkedList"].append(float('nan'))
                results["Rank_LinkedList"].append(float('nan'))

            # Binary Tree
            try:
                results["Select_BinaryTree"].append(avg_measure(lambda: bst.os_select(i_select + 1)))
                results["Rank_BinaryTree"].append(avg_measure(lambda: bst.os_rank(x_rank)))
            except Exception as e:
                print(f" Errore in BinaryTree: {e}")
                results["Select_BinaryTree"].append(float('nan'))
                results["Rank_BinaryTree"].append(float('nan'))

            # Red-Black Tree
            try:
                nodo = rbt.search(x_rank)
                if nodo:
                    results["Select_RedBlackTree"].append(avg_measure(lambda: rbt.Os_Select(rbt.root, i_select)))
                    results["Rank_RedBlackTree"].append(avg_measure(lambda: rbt.Os_Rank(nodo)))
                else:
                    print(f" Nodo non trovato in RBT per {x_rank}")
                    results["Select_RedBlackTree"].append(float('nan'))
                    results["Rank_RedBlackTree"].append(float('nan'))
            except Exception as e:
                print(f" Errore in RedBlackTree: {e}")
                results["Select_RedBlackTree"].append(float('nan'))
                results["Rank_RedBlackTree"].append(float('nan'))

            print(f" Benchmark {data_type}-{size} completato.")

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f" Benchmark salvato in {output_csv}")
    return df


if __name__ == "__main__":
    benchmark_from_saved_structures(
        folder="input",
        output_csv="output/benchmark_results.csv",
        num_trials=100
    )
