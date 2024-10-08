# BigDataSystems-Fall 2024: Team 4

Step Function Place holder Text

Mils Taylor [video shown in class - requires a login](https://canvas.its.virginia.edu/courses/121565/pages/week-5-chapter-5?module_item_id=1220355)

>![NOTE]

* limited by the upper run time of an AWS Lambda Function (15 minutes)
* limited to one script that has to be in an AWS S3 bucket
* Output is sent to AWS Cloud Watch Log.

## Definitions

Below are some useful definitions related to the Projects Vocabulary.

To get a better sense of FMI consider reading the Wiki.
[FMI wiki Overview](https://github.com/mstaylor/fmi/wiki/Aws)


<dl>
  <dt>Faas</dt>
  <dd>Functions as a Service, Serverless Computing in response to events</dd>
    
  <dt>FMI</dt>
  <dd>Faas Message Interface, a library for message passing and collective communication for serverless functions</dd>
  
  <dt>Serverless Computing</dt>
  <dd>Cloud Computing provider (like AWS) handles the machine compute resources on demand</dd>

  <dt>World Size</dt>
  <dd>Number of Lambda Functions to invoke</dd>

</dl>


### State Machines in Step Functions

Taken from the AWS Developer Guide - [here](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-statemachines.html)

> **Step Functions** is based on state machines and tasks.
>
> In Step Functions, **state machines** are called workflows, which are
> 
>  a **series of event-driven steps**.
> 
>  Each step in a workflow is called a state.

## Group Members

| Name | Title |
|------|------|
|  Nicholas (Nick) Ray Miller    |  Data Scientist    |
|  Charles S Lotane    |  Data Scientist    |
|  Ryan Healy     |  Data Scientist    |

## `Introduction`

We hope to learn
  
## `The Data`

[source - AI for Astronomy GitHub](https://github.com/UVA-MLSys/AI-for-Astronomy/tree/main)

 Describe your data set and its significance. Where did you obtain this data set from? Why did you choose the data set that you did? Indicate if you carried out any preprocessing/data cleaning/outlier removal, and so on to sanitize your data.
  
## `Experimental Design`

 Describe briefly your process, starting from where you obtained your data all the way to means of obtaining results/output.

## `Beyond the original specifications`

 Highlight clearly what things you did that went beyond the original specifications. That is, discuss what you implemented that would count toward the extra##credit portion of this project (see section below).
  
## `Results`

 Display and discuss the results. Describe what you have learned and mention the relevance/significance of the results you have obtained.
  
## `Testing`

| World Size | Run Time, sec |
|------|------|
| 2 | 4.846 |
| 4 | 4.635 |
| 20 | 5.029 |
| 50 | 6.877 |

| Memory | Duration | Cost |
|------|------|------|
| 128 MB | 11.722 s | $0.024628 |
| 512 MB | 6.678 s | $0.028035 |
| 1024 MB | 3.194 s | $0.026830 |
| 1536 MB | 1.465 s | $0.024638 |

[Google Drive - logs, request access if needed](https://docs.google.com/spreadsheets/d/1bSQFHwop4_Ki_NDmygVB1IjslVpnG32vNwmEyj1rDBA/edit?gid=1467612570#gid=1467612570)
  
## `Conclusions`

 Summarize your findings, explain how these results could be used by others (if applicable), and describe ways you could improve your program. You could describe ways you might like to expand the functionality of your program if given more time.

<details><summary> META: What should be in each Section</summary>

[Canvas Source of Project Specs](https://canvas.its.virginia.edu/courses/121565/pages/review-semester-project?module_item_id=1220357)

* `Introduction`: Describe your project scenario. Starting out, what did you hope to accomplish/learn?
  
* `The Data`: Describe your data set and its significance. Where did you obtain this data set from? Why did you choose the data set that you did? Indicate if you carried out any preprocessing/data cleaning/outlier removal, and so on to sanitize your data.
  
* `Experimental Design`: Describe briefly your process, starting from where you obtained your data all the way to means of obtaining results/output.

* `Beyond the original specifications`: Highlight clearly what things you did that went beyond the original specifications. That is, discuss what you implemented that would count toward the extra-credit portion of this project (see section below).
  
* `Results`: Display and discuss the results. Describe what you have learned and mention the relevance/significance of the results you have obtained.
  
* `Testing`: Describe what testing you did. Describe the unit tests that you wrote. Show a sample run of 1 or 2 of your tests (screen captures or copy-and-paste is fine).
  
* `Conclusions`: Summarize your findings, explain how these results could be used by others (if applicable), and describe ways you could improve your program. You could describe ways you might like to expand the functionality of your program if given more time.

</details>
