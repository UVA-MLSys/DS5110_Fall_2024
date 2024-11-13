BigDataSystems-Fall 2024: Team 2

Members: Isidro Pride, Abhinandan Mekap, John Le

Introduction:

The Data: 
The data set for the project will be an astronomy related data set. The dataset will be provided by the professor. This is the basic data set chosen. The data can be located at the follow Github repository: https://github.com/mstaylor/AI-for-Astronomy.git. The dataset consists of images collected from either satellites or telescopes. Most images can be categorized as galaxies, stars, or quasars.  

Experimental Design: 
We set up a Step Function within a state machine. This will take input payloads and generate AWS Lambda fmi_executor payloads. 
We created three State Machine trials/executions​. We used the pre-existing MyStateMachine-e5ydt2afc state machine. We updated 'world_size' parameter within the 'Lamda Init' function for our trials, specifically using 2, 8, and 32​

Beyond the original specifications:
We used results from the step function execution, but also cloudwatch results.

Results: 
# Lambda Functions  |  Duration
-------------------------------
2                   |  4.926
8                   |  6.573
32                  |  6.615

Duration/Runtime seemed to increase as the number of lambda functions increased.

Testing: 

We didn't do any additional testing. Our team simply obtaining results of the duration. In addition, we did look at cloudwatch duration and max memory used. 

Conclusions: 

We definitely noticed a correlation between Lambda Function and Duration. However, understanding how the metrics for cloudwatch calculations would be helpful. We also obtained some costs from the billing and colst management tool on AWS. However, finding a way to measure the costs of individual executions would be helpful if possible.
