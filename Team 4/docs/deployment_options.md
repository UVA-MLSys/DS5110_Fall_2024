## environments to test deployment

1) local
2) sagemaker (cpu / gpu)
3) Rivanna / Afton (HPU)
4) step functions (run different amounts of step functions)

## To consider


- `total cpu time (second)`: Total time spent on CPU processing during execution, in seconds.
- `total gpu time (second)`: Total time spent on GPU processing during execution, in seconds.
- `execution time per batch (second)`: Average time taken to process each batch, in seconds.
- `cpu memory (MB)`: CPU memory usage during execution, in megabytes.
- `gpu memory (MB)`: GPU memory usage during execution, in megabytes.
- `throughput (bps)`: Data processing rate in bits per second across all batches.
- `batch size`: Number of samples in each batch.
- `number of batches`: The total number of batches processed in the execution.
- `device`: The hardware device (CPU or CUDA) used for execution.
