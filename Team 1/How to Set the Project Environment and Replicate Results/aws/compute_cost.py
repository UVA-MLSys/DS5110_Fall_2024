import boto3
from datetime import datetime, timedelta
import time

# for 50 MB 
# Duration: 14186.75 ms	Billed Duration: 14848 ms	Memory Size: 10240 MB	Max Memory Used: 4131 MB	Init Duration: 660.76 ms	

num_requests = 100
duration = 30 # seconds
memory_allocated = 5 # GB 
storage = 2 # GB

compute_per_GB_s = 0.0000166667 # USD per GB/s
GB_s = num_requests * duration * memory_allocated # compute power used in GB/s
compute_charges = GB_s * compute_per_GB_s

charges_per_request = 2e-7
request_charges = num_requests * charges_per_request

storage_per_GB_s = 3.09e-8 # USD per GB/s
storage_charges = (storage - 0.5)* (num_requests * duration) *storage_per_GB_s if storage > 0.5 else 0

total_charges = compute_charges + request_charges +  storage_charges

print(f'Compute charges: ${compute_charges:.3g}, Request charges: ${request_charges:.3g}, Storage charges: ${storage_charges:.3g}')
print(f'Total charges: ${total_charges:.3g}.')