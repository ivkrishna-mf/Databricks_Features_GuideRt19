# Distributed PyTorch with TorchDistributor
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.ml.torch.distributor import TorchDistributor

def train_fn(epochs: int):
    import torch, torch.distributed as dist
    dist.init_process_group("nccl")
    model = torch.nn.parallel.DistributedDataParallel(build_model().cuda())
    for _ in range(epochs):
        train_one_epoch(model)          # your loop; each rank reads its shard
    dist.destroy_process_group()

TorchDistributor(num_processes=8, local_mode=False, use_gpu=True).run(train_fn, 5)
