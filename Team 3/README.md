# BigDataSystems-Fall 2024: Team 3 

## Members: 

Kanitta, Karthika, Chi, Aqsa

## Introduction: 

We have a pre-existing AWS Step function to run FMI lambda functions. With this, we will build a system that can scale within a strict budget. We hope to learn about FMI functions, AWS, and system/data parallelization. After all this has been completed, we would like to create a meaningful application with data.  

## The Data:

There will be two stages for this project. The first will be benchmarking the Step Functions without any data present. The second will use astronomy data to test the Step Function

## Experimental Design:

Within the prebuilt State Machine on AWS, we set up the Step Function that will later be used to run Lambda functions. This Step Function can have changes in payloads and the number of parallel Lambda functions they run. We ran 3 experiments to 3 payloads, invoking 2, 4, 16 parallel lambdas.  

Beyond the original specifications: 

In addition to the Step Function experiment, the team also created a GitHub project where all tasks are stored. Each task has a member assigned and is moved through the to do list.  

## Results: 

We ran 3 experiments to 3 payloads, invoking 2, 4, 16 parallel lambdas. These were then benchmarked for time and cost. These are presented in overalls below. 

Below are the time benchmarking for the lambda function with no data is below. 

| Number of Lambda invoked | Execution time(seconds) |
|--------------------------|:-----------------------:|
| 2                        |          4.720          |
| 4                        |          7.566          |
| 16                       |          5.158          |


The cost benchmarking for the lambda function with no data is noted. 

| Item                         | Cost (USD) |
|------------------------------|------------|
| Elastic Container Service    | 2.04       |
| CloudWatch                   | 0.24       |
| Key Management Service       | 0.03       |
| Simple Storage Service       | 0.03       |
| EC2 Container Registry (ECR) | 0.02       |
| Secrets Manager              | 0.01       |
| Total                        | 2.37       |


## Testing: 

The team went through the AWS set up of the Step Function. Once set up was complete, we changed the world size several times, and tracked the time. Results are presented above. Overall costs were taken. 

## Conclusions: 

Overall, the cost of running a Lambda function on AWS is very small, but it's not nothing. It will be interesting to see how costs and time change with the addition of data. 


## How to set the project environment and replicate the results

The initial Lambda function with no data was run according to the Step Function Tutorial (Semester Project) listed in the Pre-Class Assignment on Canvas. 

For the additions with data, references such as the [FMI wiki Overview](https://github.com/mstaylor/fmi/wiki/Aws) were used. The State Machine was copied and named as Group3_CosmicAI. All world size and GPU vs CPU tests were run here. When running, the "Concurrency limit" in the "Distributed Test" block was set to 20 for world sizes larger than or equal to 32.    

Data was stored in a an S3 bucket called team3cosmicai. Data files and the inference.py files were stored here. Changes to this file include using 'cuda' as the default so GPU will be used.  



