<p align="center">
  <strong>BigDataSystems-Fall 2024: Team 1</strong>
</p>
<p align="center">
## Members
</p>
<p align="center">
  <strong>George Shoriz</strong><br>
  <strong>Harold Haugen</strong><br>
  <strong>Dan Anthony</strong><br>
  <strong>Zack Lisman</strong>
</p>

## Introduction

This project focuses on creating scalable and efficient data processing pipelines using the *AWS Step Function with Lambda*. Our objective is to investigate and implement critical data processing techniques such as cleaning, outlier removal, pre-processing, and model training while ensuring the system is optimized for both performance and cost-efficiency. By leveraging parallel Lambda executions and varying workload parameters (like `world_size`), the project sought to improve scalability and resource utilization. 

We aim to get a better grasp of AWS capabilities and how to use them to optimize operations while keeping costs low and efficiency high. Our goal is to create a functional pipeline that will increase our ability to manage massive datasets, automate operations, and deploy machine learning models effectively.

## The Data

As of *10/6/24*, the dataset has not been provided yet. It is expected that each project group is provided the same dataset to work with. This section will be updated with indications of any preprocessing, data cleaning, or outlier removal applied to the dataset.

## Experimental Design

The design process begins with a dataset like AI-for-Astronomy. The dataset will be cleaned, with missing values handled and outliers detected to assure quality. The cleaned data is then saved as a CSV file and transferred to an S3 bucket for further processing.

We next create a *Step Function* that calls an *AWS Lambda* function to execute data processing operations like data loading and machine learning model training. Once the model has completed its run, the results are recorded and shown in tables and visualizations for easy interpretation. Throughout the process, testing and validation are carried out to assure the outputs' dependability and correctness.

## Beyond the Original Specifications

We went beyond the project's initial scope by experimenting with different `world_size` parameters in *AWS Step Function with Lambda*. This allowed us to observe how changing the number of parallel processes affected both performance and cost efficiency. 

Testing alternative `world_size` parameters helps determine the best configuration for our dataset, resulting in improved scalability and resource utilization. Additionally, we leveraged a *team group chat* for regular communication to coordinate our tasks, share insights, and manage project tasks.

## Results

| World Size | Lambda Init Duration (sec) | MapState Duration (sec) | Step Function Duration (sec) |
|------------|----------------------------|-------------------------|------------------------------|
| 2          | 0.373                      | 2.609                   | 3.161                        |
| 10         | 0.199                      | 3.203                   | 3.554                        |
| 24         | 0.476                      | 5.040                   | 5.682                        |

Experimenting with different `world_size` values in *AWS Step Functions with Lambda* revealed that increasing parallelism helps scalability but provides diminishing returns in performance beyond a certain point. Execution times varied, with lower `world_size` combinations being more cost-effective and time-efficient. Memory utilization was constant across workloads, allowing for better resource allocation.

## Testing

After configuring the *AWS Step Function*, we concentrated on testing its performance by modifying the `world_size` parameter to see how it affected execution time and resource use. Different configurations were examined to see how well the system performed in parallel tasks. We monitored the duration and billed time of each run to ensure that performance increases did not come at the expense of efficiency.

## Conclusion

Our findings showed that altering the `world_size` parameter has a considerable influence on both execution time and costs. For example, when we set the `world_size` to 2, the Step Function time was 3.1 seconds, but raising the `world_size` to 24 resulted in a duration of more than 5.6 seconds, even though more parallel processing was occurring. This shows that, after a certain point, increased parallelism creates overhead, resulting in inefficiencies rather than speed advantages.

These insights may be useful to anyone looking to optimize *AWS Step Functions with Lambda* for similar operations, as knowing this balance is critical for improving both performance and cost-efficiency.

To improve the program, we would investigate methods to decrease the cost of larger `world_size` setups, such as improving Lambda function coordination or dynamically allocating resources.
