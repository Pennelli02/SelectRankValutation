
from testFunctions import ARNValutation, CreateTables, BenchmarkSelectRank, PlotResults


BenchmarkSelectRank.benchmark_from_saved_structures(num_trials=50)
PlotResults.plot_benchmarks()
CreateTables.generate_operation_tables_from_csv("output/benchmark_results.csv")
# per visionare al meglio l'andamento dell'albero rosso nero con l'attributo size è stato creato un file apposito
ARNValutation.benchmark_rbt_select_rank()

