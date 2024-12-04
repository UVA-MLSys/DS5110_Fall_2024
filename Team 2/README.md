# BigDataSystems-Fall 2024: Team 2

## Members: Isidro Pride, Abhinandan Mekap, John Le

## Introduction:
The goal of the project is redshift prediction using SDSS Data and AI-for-Astronomy Pipeline with data from Sloan Digital Sky Survey (SDSS).

## The Data: 
The data set for the project will be an astronomy related data set. The dataset will be provided by the professor. This is the basic data set chosen. The data can be located at the follow Github repository: https://github.com/mstaylor/AI-for-Astronomy.git. The dataset consists of images collected from either satellites or telescopes. Most images can be categorized as galaxies, stars, or quasars. On AWS, the link to the bucket with the data and the scripts is, https://us-east-1.console.aws.amazon.com/s3/buckets/team2cosmicai?region=us-east-1&bucketType=general&tab=objects

## Experimental Design: 
We set up Step Functions within a state machine. These input payloads and generate AWS Lambda fmi_executor payloads. Our first state machine trials were with the pre-existing MyStateMachine-e5ydt2afc state machine.
We created three State Machine trials/executions​ and updated 'world_size' parameter within the 'Lamda Init' function for our trials, specifically using 2, 8, and 32​.

This was the original trials just to get familiar with step function and state machines. We later performed this on the actual astronomy data. We cloned the cosmicai state function and executed the state machines on the astronomy data. We did three initial trials with different world sizes of 1, 10, and 100 and measured changes in duration and other metrics.


## Step by Step Procedure to reproduce results:
1. Log into AWS and search for step functions.
2. Clone cosmicai state machine.
3. Clone cosmicai2 S3 bucket as well.
4. For relatively low world sizes, you would not have to change the script. Just use the regular inference.py
5. Upload payload with bucket, scripts you want to use, and world size. To reproduce our results, execute with 1, 10, and 100.
6. Wait for execution. Duration will show up.
7. Following completion, go into you S3 bucket, results folder, and then into folder 0. Results.json will have your metrics.
8. Most likely, a world size of a 100 will not run. To fix this, you can create a copy of inference.py, and specify cuda instead of cpu.
9. Specify this script in your payload as well, and then re-run, which should execute successfully.

These are how the state machines and S3 Buckets appear:

  State Machine:

  ![image](https://github.com/user-attachments/assets/82630cc5-cdf1-400b-955d-42712fc92472)


  S3 Bucket

  ![image](https://github.com/user-attachments/assets/063c55a3-1623-4062-81fc-6f29e286ee49)

## Beyond the original specifications:
We used both the CPU and GPU for our duration measurements for CosmicAI. Created a file called inference-cuda.py that uses GPU. Those are attached to this github page.

## Results:

### Basic DS5110 State Machine
Lambda Functions    |  Duration
--------------------|------------
2                   |  4.926
8                   |  6.573
32                  |  6.615

Duration/Runtime seemed to increase as the number of lambda functions increased.

#### Testing: 

We didn't do any additional testing. Our team simply obtaining results of the duration. In addition, we did look at cloudwatch duration and max memory used. 

#### Conclusions: 

We definitely noticed a correlation between Lambda Function and Duration. However, understanding how the metrics for cloudwatch calculations would be helpful. We also obtained some costs from the billing and colst management tool on AWS. However, finding a way to measure the costs of individual executions would be helpful if possible.

### Cosmic AI Results
#### Duration
World Size       |  Duration (cpu)  |  Duration (gpu)
-----------------|------------------|-----------------
1                |  10.695          |  5.749
10               |  14.895          |  5.762
100              |  Error           |  44.717

We cloned the cosmic ai state machine and ran executions with world sizes of 1, 10, and 100, for both cpu and gpu. We had to update inference.py to use cuda instead of cpu for the device. Duration increased as we increased the world size for both cpu and gpu. CPU seemed to have issues running larger world sizes, as a world size of 100 threw an error. However, GPU ran perfectly fine. The duration difference between a world size of 10 and a world size of 100 was quite drastic.

#### Metrics for world size 1 and world size 10 with cpu
##### World Size 1
![image](https://github.com/user-attachments/assets/016dfbc4-0486-4d9c-bcc9-ae8a86fd1f1f)
##### World Size 10
![Screenshot 2024-11-24 140939](https://github.com/user-attachments/assets/c22e8bf0-31c8-4f92-89b4-dafc40f2854a)

#### Testing: 

Testing inolved simply gathering the Cosmic AI results above and comparing the durations between the cpu and gpu.

#### Conclusions:

CPU time and Execution time per batch increases with hieger world size. Total lambda cost increases with world size. Steop function cost remains constant as state transitions is constant.


