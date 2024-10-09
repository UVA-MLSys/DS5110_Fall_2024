# BigDataSystems-Fall 2024: Team 4

The Goal of this part I of the Semester Project is to Start to build the Infrastructure needed to cheaply and efficiently run our our Semester Projects.

This implementation is done with extensive help from Mils Taylor [and his video shown in class - requires a login - should be referenced.](https://canvas.its.virginia.edu/courses/121565/pages/week-5-chapter-5?module_item_id=1220355)

>[!IMPORTANT]
> EVIDENCE FOR THE BELOW DELIVERABLES IS LINKED [here in the Experiment Presentation Deck](https://urldefense.com/v3/__https://docs.google.com/presentation/d/1zM3HT7Acrm1_QnIXYtRWA2U9EY-exZmhUDNPxALn-Yk/edit*slide=id.g30938d23901_0_836__;Iw!!OFBJNr4F2A!U9C-FlIxwd20apdomzXIdl8H4K31jl-z9rYPCLpPYNlyn5egtwWjld7yT-fU4PLjtl2ff7hg_69GTO9PYKqv$)
>
>* run the "Step Function" and measure the total execution time and cost by completing the following steps. Submit the results with snapshots of the successful execution of each of the steps as below. 
>* Create an S3 bucket that will host your python script
>* Create a folder structure within your S3 bucket
>* Upload a python script to the created folder
>* Execute the step function and validate results in the * following log group: /aws/lambda/fmi_executor
>* Remember to log something that uniquely identifies your execution in the python script. This will help you locate your execution.




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

### State Machines in Step Functions

Taken from the AWS Developer Guide - [here](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-statemachines.html)

> **Step Functions** is based on state machines and tasks.
>
> In Step Functions, **state machines** are called workflows, which are
>
> a **series of event-driven steps**.
>
> Each step in a workflow is called a state.

## `Introduction`

This initial part of the Big Data Systems Semester project, introduces Workflow Orchestration and the key part of any project which is optimizing the Budget.

The goal of the Semester Project is to develop a `Proof of Concept Model`. to do so requires being able to show and mimic the scale while being mindful of costs (large EC2 instances can be costly)

In addition to cost considerations, Lambda Functions can be scaled down to zero when there is zero work while EC2 compute instances need to be managed and shut down /manually destroyed.

While the AWS Lambda environment is highly constrained environment it [can cheaply mimic a HPC](https://arxiv.org/abs/2305.08763)

some of the infrastructure to run this experiment that is provided by the class include:

* a deployed Rendezvous sever deployed as `rendezvous.uva-ds5110.com`
* and a useable Registered Docker Image

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

## `The Data`

This is done infrastructure with the data part to come later, we are interested less so in the data and more the infrastructure here.

For a future build, an example dataset to examine
[AI for Astronomy GitHub](https://github.com/UVA-MLSys/AI-for-Astronomy/tree/main)

## `Experimental Design`

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

* an equivalent EC2 instance could be 3-5 dollars and has start up and tear down time and the potential to have unused compute running up a large bill
  
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
>* limited by the upper run time of an AWS Lambda Function (15 minutes)
>* limited to one script that has to be in an AWS S3 bucket
>* Output is sent to AWS Cloud Watch Log and should be examined using a log parser

<!-- <details><summary> META: What should be in each Section</summary>

[Canvas Source of Project Specs](https://canvas.its.virginia.edu/courses/121565/pages/review-semester-project?module_item_id=1220357)

* `Introduction`: Describe your project scenario. Starting out, what did you hope to accomplish/learn?
  
* `The Data`: Describe your data set and its significance. Where did you obtain this data set from? Why did you choose the data set that you did? Indicate if you carried out any preprocessing/data cleaning/outlier removal, and so on to sanitize your data.
  
* `Experimental Design`: Describe briefly your process, starting from where you obtained your data all the way to means of obtaining results/output.

* `Beyond the original specifications`: Highlight clearly what things you did that went beyond the original specifications. That is, discuss what you implemented that would count toward the extra-credit portion of this project (see section below).
  
* `Results`: Display and discuss the results. Describe what you have learned and mention the relevance/significance of the results you have obtained.
  
* `Testing`: Describe what testing you did. Describe the unit tests that you wrote. Show a sample run of 1 or 2 of your tests (screen captures or copy-and-paste is fine).
  
* `Conclusions`: Summarize your findings, explain how these results could be used by others (if applicable), and describe ways you could improve your program. You could describe ways you might like to expand the functionality of your program if given more time.

</details> -->
