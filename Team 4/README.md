# BigDataSystems-Fall 2024: Team 4

The Semester Project is to build and test the POC infrastructure needed to cheaply and efficiently run the AI-for-Astronomy 
Inference Model.

Most of our testing is done locally on a Mac and on our [class AWS Account Login](https://us-east-1.console.aws.amazon.com/console/home?region=us-east-1#)

>[!NOTE]
>Access to this Account might not be active after the Fall 2024 Semester is over. 





## Repo structure

```bash
├── AI-for-Astronomy
│   ├── 99_validations.ipynb
│   ├── LICENSE
│   ├── README.md
│   ├── code
│   ├── data
│   └── papers
├── README.md
├── data
│   ├── final
│   ├── interim
│   ├── predictions
│   └── raw
├── demos
├── experiments
│   ├── sql
│   └── src
├── img
│   ├── infrastructure_diagram_raw.png
│   ├── runtime_graph.png
│   ├── stepfunctions_graph.png
│   └── using_Mils_slide_to_show.png
├── keys
├── makefile
├── scratch
├── scripts
│   ├── fmi-execute-test.py
│   ├── fmi-test.py
│   └── fmi.json
├── src
│   └── __pycache__
└── tests
    └── __pycache__

```

## Table of Contents

- [BigDataSystems-Fall 2024: Team 4](#bigdatasystems-fall-2024-team-4)
  - [Repo structure](#repo-structure)
  - [Table of Contents](#table-of-contents)
  - [Group Members](#group-members)
  - [Definitions](#definitions)
  - [1: Step Functions](#1-step-functions)
  - [`Introduction`](#introduction)
  - [The Data](#the-data)
  - [Experimental Design](#experimental-design)
  - [`Beyond the original specifications`](#beyond-the-original-specifications)
  - [`Results`](#results)
    - [Time to Run for Different World Sizes](#time-to-run-for-different-world-sizes)
    - [Memory Costs](#memory-costs)
  - [`Conclusions`](#conclusions)
  - [environments to test deployment](#environments-to-test-deployment)
  - [2 rendezvous Server](#2-rendezvous-server)
  - [3: AI for Astronomy Inference](#3-ai-for-astronomy-inference)
  - [4 Cosmic AI with Lambda FMI](#4-cosmic-ai-with-lambda-fmi)

>[!IMPORTANT]
> EVIDENCE FOR THE BELOW DELIVERABLES IS LINKED [here in the Experiment Presentation Deck](https://urldefense.com/v3/__https://docs.google.com/presentation/d/1zM3HT7Acrm1_QnIXYtRWA2U9EY-exZmhUDNPxALn-Yk/edit*slide=id.g30938d23901_0_836__;Iw!!OFBJNr4F2A!U9C-FlIxwd20apdomzXIdl8H4K31jl-z9rYPCLpPYNlyn5egtwWjld7yT-fU4PLjtl2ff7hg_69GTO9PYKqv$)
>
- run the "Step Function" and measure the total execution time and cost by completing the following steps. Submit the results with snapshots of the successful execution of each of the steps as below.
- Create an S3 bucket that will host your python script
- Create a folder structure within your S3 bucket
- Upload a python script to the created folder
- Execute the step function and validate results in the * following log group: /aws/lambda/fmi_executor
- Remember to log something that uniquely identifies your execution in the python script. This will help you locate your execution.

## Group Members

| Name | Title |
|------|------|
|  Nicholas (Nick) Ray Miller    |  Data Scientist    |
|  Charles S Lotane    |  Data Scientist    |
|  Ryan Healy     |  Data Scientist    |

## Definitions

Below are some useful definitions related to the Projects Vocabulary.

To get a better sense of FMI consider reading the Wiki.
[FMI wiki Overview](https://github.com/mstaylor/fmi/wiki/Aws)

<dl>
  <dt>AWS Fargate</dt>
  <dd>a serverless compute engine that allows users to run containerized applications without having to manage the underlying infrastructure like servers or clusters</dd>

  <dt>Faas</dt>
  <dd>Functions as a Service, Serverless Computing in response to events</dd>

  <dt>FMI</dt>
  <dd>Faas Message Interface, a library for message passing and collective communication for serverless functions</dd>

  <dt>HPC</dt>
  <dd>High Performance Cluster, really meaning scaling beyond normal capabilities, think Afton or Rivanna </dd>
  
  <dt>Serverless Computing</dt>
  <dd>Cloud Computing provider (like AWS) handles the machine compute resources on demand</dd>

  <dt>World Size</dt>
  <dd>Number of Lambda Functions to invoke note: in order of 2s[2,4,6...n]</dd>

</dl>


Taken from the AWS Developer Guide - [here](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-statemachines.html)

> **Step Functions** is based on state machines and tasks.
> a **series of event-driven steps**.
>
> Each step in a workflow is called a state.

## 1: Step Functions

This implementation is done with extensive help from Mils Taylor [and his video shown in class - requires a login - should be referenced.](https://canvas.its.virginia.edu/courses/121565/pages/week-5-chapter-5?module_item_id=1220355)

## `Introduction`

This initial part of the Big Data Systems Semester project, introduces Workflow Orchestration and the key part of any project which is optimizing the Budget.

The goal of the Semester Project is to develop a `Proof of Concept Model`. to do so requires being able to show and mimic the scale while being mindful of costs (large EC2 instances can be costly)

In addition to cost considerations, Lambda Functions can be scaled down to zero when there is zero work while EC2 compute instances need to be managed and shut down /manually destroyed.

While the AWS Lambda environment is highly constrained environment it [can cheaply mimic a HPC](https://arxiv.org/abs/2305.08763)

some of the infrastructure to run this experiment that is provided by the class include:

- a deployed Rendezvous sever deployed as `rendezvous.uva-ds5110.com`
- and a useable Registered Docker Image

These can be seen on the left side of the image below.

We can build the following part of an infrastructure.

![img/Using_Mils_slide_to_show.png](img/using_Mils_slide_to_show.png)

>[!TIP]
 To run this locally you'll need the Docker Image, if building an Image from scratch or for a new application include make and Python 3.9+

 to get the Python library installed see below

```bash
# a needed dependency might be the fmi python library
# see the fmi github
git clone https://github.com/mstaylor/fmi
cd python
mkdir build
cd build
cmake ..
make
```

## The Data

This is done infrastructure with the data part to come later, we are interested less so in the data and more the infrastructure here.

For a future build, an example dataset to examine
[AI for Astronomy GitHub](https://github.com/UVA-MLSys/AI-for-Astronomy/tree/main)

## Experimental Design

The State Machine took in several parts

including

1) an event (were manually started)
2) the number of Lambda functions to test (also known as worlds)
3) a script places on S3 (locally here scripts/fmi-test.py)
4) settings in a json format (scripts/fmi.json)

The DAG for the job is the following

![test](img/stepfunctions_graph.png)

## `Beyond the original specifications`

Multiple World sizes were tested in order to give us an idea of the appropriate scale needed.

## `Results`

### Time to Run for Different World Sizes

| World Size | Run Time, sec |
|------|------|
| 2 | 4.846 |
| 4 | 4.635 |
| 20 | 5.029 |
| 50 | 6.877 |

### Memory Costs

| Memory | Duration | Cost |
|------|------|------|
| 128 MB | 11.722 s | $0.024628 |
| 512 MB | 6.678 s | $0.028035 |
| 1024 MB | 3.194 s | $0.026830 |
| 1536 MB | 1.465 s | $0.024638 |

[Google Drive - copy of referenced logs, request access if needed](https://docs.google.com/spreadsheets/d/1bSQFHwop4_Ki_NDmygVB1IjslVpnG32vNwmEyj1rDBA/edit?gid=1467612570#gid=1467612570)

- an equivalent EC2 instance could be 3-5 dollars and has start up and tear down time and the potential to have unused compute running up a large bill
  
## `Conclusions`

Using the FMI State Machines we've successfully deployed a cheap infrastructure to build our POC and simulate a real deployment.

Plus or minus some costs for startup costs and variability in cloud infrastructure start ups the provisioning of these systems is
$$T_n = \theta(log(n))$$

as can be seen in the graph below of World size (Lambda inputs) and Runtime in seconds

![Nick's Runtime Graph](img/runtime_graph.png)

Which provides us with an easy and cheap way to scale.

>[!NOTE]
> Additional Notes
>
>- limited by the upper run time of an AWS Lambda Function (15 minutes)
>- limited to one script that has to be in an AWS S3 bucket
>- Output is sent to AWS Cloud Watch Log and should be examined using a log parser



compare different data sizes, and call sizes of the step functions

## 2 rendezvous Server

Taken from [preclass assignment](https://canvas.its.virginia.edu/courses/121565/assignments/571382?module_item_id=1318706)

The Faas Message Interface(FMI) uses the TCPunch

Links to an external site. communication library and Rendezvous server to establish socket communication between ($n$) AWS Lambda functions.
To run FMI Python scripts, it is necessary to deploy a Rendezvous Server on the public internet.

The `UVA DS5110` AWS account (TODO: link here) has includes a prebuilt Docker image that can be used.

1) go to AWS ECS (Elastic Container Service)
2) select `rendezvous-tcpunch-fargate-task from the list and select rendezvous-tcpunch-fargate-task:1`
3) Select the Deploy option, Select the fargate1 cluster and select the launch type as FARGATE.
4) Scroll down to the Networking section and choose the open access security group as the only security group associated with this task.
5) Select Create at the bottom of the page
6) After the Rendezvous server starts, you will need to extract the public ip address from the task. We will use that as the IP address for the A Route 53 record.
7) Navigate to the AWS Route 53 service, select the uva-ds5110.com hosted zone, and update the rendezvous.uva-ds5110.com record with the IP Address retrieved from the previous step.
   
## 3: AI for Astronomy Inference

The code for 


    inference.png: This contains a visual representation of the inference results.
    Results.json: This JSON file contains the detailed numerical results of the inference.

Setting the Device

    To run the script on either GPU or CPU, set the --device argument accordingly:
        For GPU: use 'cuda'
        For CPU: use 'cpu'

    The default is set to run on CPU. To change the device, modify the --device argument as follows:

    parser.add_argument('--device', type=str, default='cpu', help="Device to run the model on: 'cuda' for GPU or 'cpu' for CPU")

## 4 Cosmic AI with Lambda FMI

An AWS Step function has been developed to facilate orchestration of AI For Astronomy Serverless Inference. Step functions are represented as state machines and tasks. For the DS5110 class, the cosmicai state machine has been created. This step function takes an input payload and generates appropriate AWS Lambda fmi_executor payloads

In this payload we use world_size to represent the number of lambda functions to invoke, bucket to represent the S3 bucket that contains the fmi python script, S3_object_name to represent the path on the S3 bucket where the script can be found, data_path to represent where the resized_inference.pt can be founder, and script to represent the inference script.


![FMI image](img/fmi_image.png)


```json
# payload
{
  "bucket": "cosmicai2",
  "world_size": "2",
  "object_type": "folder",
  "S3_object_name": "scripts/Anomaly Detection",
  "data_path": "/tmp/scripts/Anomaly Detection/Inference/resized_inference.pt",
  "script": "/tmp/scripts/Anomaly Detection/Inference/inference.py"
}
```




To edit the input payload:

    Navigate to the AWS Step Function service
    Select the cosmicai state machine
    Select edit to edit the state machine
    Select the Lambda init state
    On the right, scroll to the payload section


Create an S3 bucket that will host your python script
Create result and scripts folders in this S3 Bucket
Clone the following repository: https://github.com/mstaylor/AI-for-Astronomy.git
Links to an external site. (i.e., git clone https://github.com/mstaylor/AI-for-Astronomy.git
Links to an external site.)
Copy the Anomaly Detection folder located under code to the S3 bucket
Execute the step function
You can view the execution logs by navigating to the following Cloudwatch Log Group: /aws/lambda/cosmic-executor
Results of the collective reduce operation are post to the S3 Bucket's result folder under 0 (rank zero)