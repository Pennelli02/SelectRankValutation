import pandas as pd
import matplotlib.pyplot as plt
import os
import re


# Funzione per salvare la tabella come immagine
def generate_operation_tables_from_csv(csv_path, output_folder='output/plots/table'):
    # Crea la cartella di output
    os.makedirs(output_folder, exist_ok=True)

    # Leggi il CSV e normalizza le intestazioni
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # Rimuove eventuali spazi

    # Colonne base
    id_vars = ['Size', 'DataType']

    # Estrai le colonne di tipo Rank_* o Select_*
    value_vars = [col for col in df.columns if re.match(r'^(Rank|Select)_', col)]

    # Melt: da wide a long
    df_melted = df.melt(id_vars=id_vars, value_vars=value_vars,
                        var_name='Operation_Structure', value_name='Time')

    # Separiamo Operation e Structure
    df_melted[['Operation', 'Structure']] = df_melted['Operation_Structure'].str.split('_', expand=True)
    df_melted.drop(columns=['Operation_Structure'], inplace=True)

    # Ordina per Size
    df_melted = df_melted.sort_values(by='Size')

    # Funzione per salvare ogni tabella
    def save_table_to_png(df_table, filename):
        # Formatta i numeri a 4 cifre significative
        df_formatted = df_table.copy()
        for col in df_formatted.columns:
            if df_formatted[col].dtype.kind in 'fiu':  # float/int
                df_formatted[col] = df_formatted[col].apply(lambda x: f"{x:.4g}" if pd.notnull(x) else "")

        fig, ax = plt.subplots(figsize=(12, 4 + 0.3 * len(df_formatted)))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df_formatted.values,
                         colLabels=df_formatted.columns,
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        full_path = os.path.join(output_folder, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.close()
        return full_path

    # Genera tabelle per Operation + DataType
    saved_tables = []
    operations = df_melted['Operation'].unique()
    data_types = df_melted['DataType'].unique()

    for operation in operations:
        for dtype in data_types:
            subset = df_melted[(df_melted['Operation'] == operation) & (df_melted['DataType'] == dtype)]
            pivot_df = subset.pivot(index='Size', columns='Structure', values='Time').reset_index()
            filename = f"{operation}/{dtype}.png"
            path = save_table_to_png(pivot_df, filename)
            saved_tables.append((operation, dtype, path))
