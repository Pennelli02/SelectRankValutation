import gc
import os
import random
import sys
import joblib
from StruttureDati import ListaOrdinata, ABR, ARN  # Adatta i nomi ai tuoi moduli

sys.setrecursionlimit(100000000)
output_dir = "../input"


def creation_data_structure():
    os.makedirs(output_dir, exist_ok=True)
    data_configs = {
        'random': lambda n: random.sample(range(1, n + 1), n),
        'sorted': lambda n: sorted(random.sample(range(1, n + 1), n)),
        'reverse': lambda n: sorted(random.sample(range(1, n + 1), n), reverse=True),
        'randomDuplicate': lambda n: [random.randint(1, n) for _ in range(n)]
    }

    sizes = [10, 20, 30, 40, 50, 60, 70, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 250, 300, 400, 500,
             600, 700, 900, 1000, 1200, 1400]

    for data_type, generator in data_configs.items():
        for size in sizes:
            print(f"\n Generando {data_type} con N={size}")

            data = generator(size)

            # Strutture dati
            ll = ListaOrdinata.OrderedLinkedList()
            bst = ABR.BinarySearchTree()
            rbt = ARN.TreeRedBlack()
            for val in data:
                ll.insert(val)
                bst.insert(val)
                rbt.insert(val)

            i_select = size // 2
            try:
                val_ll = ll.select(i_select)
                val_bst = bst.os_select(i_select + 1)  # 1-based
                val_rbt = rbt.Os_Select(rbt.root, i_select + 1)  # 1-based
            except Exception as e:
                print(f" Errore nel calcolo del valore centrale: {e}")
                continue

            if not (val_ll == val_bst == val_rbt):
                print(f" Valori select non coerenti:\n  LL={val_ll}\n  BST={val_bst}\n  RBT={val_rbt}")

            print(f" Valore centrale selezionato: {val_ll}")
            rank_value = val_ll

            base_filename = f"{output_dir}/{data_type}_{size}"
            joblib.dump(rank_value, f"{base_filename}_rank_value.joblib", compress=3)
            joblib.dump(ll, f"{base_filename}_linkedlist.joblib", compress=3)
            joblib.dump(bst, f"{base_filename}_bst.joblib", compress=3)
            joblib.dump(rbt, f"{base_filename}_rbt.joblib", compress=3)

            # Libera memoria
            del ll, bst, rbt, data
            gc.collect()


if __name__ == "__main__":
    creation_data_structure()
