# Big Data Systems Semester Project

<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

 Using this project we build a Proof of Concept to relate two sources of Daily collective Sentiment:

 1) The Top 25 voted on World News stories on Reddit
 2) Movements in the Financial Markets.

 While there are many ways this can be scaled and iterated on, we are interested in using the tools on AWS to show different ways this could be done in production.

 Wether its general curiosity in Social Listening, or looking to build out more sophisticated indicators based on "which way the tide is turning", there are many different ways.

 The API connections of Reddit and Yahoo Finance tend to be a bit permissive but make sure to check the Terms on Service.

 [Class AWS Account](https://us-east-1.console.aws.amazon.com/console/home?region=us-east-1# )

## Data

* Reddit News and Stock data collected from specifically from, 2008-06-08 to 2016-07-01 (2008 - 2016) [Source on Kaggle](https://www.kaggle.com/datasets/aaron7sun/stocknews)

There are three CSV datasets given in the download Reddit, the Dow Jones Average, and both datasets connected by date.

### About the Data

* `RedditNews.csv`:
    >All news are ranked from top to bottom based on how hot they are. There are 25 lines for each date.

* `DJIA_table.csv`:
    > The Down Jones Industrial Average (DIJA) with the Open, High, Low, Close, (or OHLC), Volume, and Adjusted Close per day.
    > Downloaded directly from Yahoo Finance: [Yahoo Finance Python API docs](https://polygon.io/stocks?utm_term=yahoo%20finance%20api&utm_campaign=Stocks+-+USA&utm_source=adwords&utm_medium=ppc&hsa_acc=4299129556&hsa_cam=1330311037&hsa_grp=133850757326&hsa_ad=591580364583&hsa_src=g&hsa_tgt=kwd-2472582053&hsa_kw=yahoo%20finance%20api&hsa_mt=b&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=EAIaIQobChMI54izy8TyiAMVzXBHAR1_JBvoEAAYASAAEgJSuvD_BwE)

* `Combined_News_DJIA.csv`:
    >"Date", "Label", and Reddit World News headlines ranging from "Top1" to "Top25".

  >[!NOTE]
  `Label` or Target is **"1" when DJIA Adj Close value rose or stayed as the same** and **"0" when DJIA Adj Close value decreased**

## Data Diagram
![drawio archeiturue diagram](/Team%204/docs/imgs/project_start_modeling.drawio.png)

## Contributors

| Name | Title |
|------|------|
|  Nicholas (Nick) Ray Miller    |  Data Scientist    |
|  Charles S Lotane    |  Data Scientist    |
|  Ryan Healy     |  Data Scientist    |

### Advisors

| Name | Title |
|------|------|
| Dr. Judy Fox     | Professor, Lead Technical Advisor      |
|  Miles Zhou     | Ph.D.  Candidate in Data Science    |
|   Md Khairul Islam   |    Ph.D.  Candidate in Data Science  ||

## Repo Structure

```bash

├── README.md
├── data # .gitignore
│   ├── interim
│   ├── processed
│   └── raw
│       └── stock_reddit_data
│           ├── Combined_News_DJIA.csv
│           ├── RedditNews.csv
│           └── upload_DJIA_table.csv
├── demos
├── docs
│   └── imgs
│       └── grading_rubric.png
├── experiments
│   ├── notebooks
│   ├── sql
│   └── src
├── keys # pem files to connect to AWS
├── makefile
├── pylintrc # Google Style Guide
├── requirements.txt
├── scripts # automation
├── src # reuseable functions
└── tests # built using pytest
```

## Write Up Details

[Canvas Source of Project Specs](https://canvas.its.virginia.edu/courses/121565/pages/review-semester-project?module_item_id=1220357)

* `Introduction`: Describe your project scenario. Starting out, what did you hope to accomplish/learn?
  
* `The Data`: Describe your data set and its significance. Where did you obtain this data set from? Why did you choose the data set that you did? Indicate if you carried out any preprocessing/data cleaning/outlier removal, and so on to sanitize your data.
  
* `Experimental Design`: Describe briefly your process, starting from where you obtained your data all the way to means of obtaining results/output.

* `Beyond the original specifications`: Highlight clearly what things you did that went beyond the original specifications. That is, discuss what you implemented that would count toward the extra-credit portion of this project (see section below).
  
* `Results`: Display and discuss the results. Describe what you have learned and mention the relevance/significance of the results you have obtained.
  
* `Testing`: Describe what testing you did. Describe the unit tests that you wrote. Show a sample run of 1 or 2 of your tests (screen captures or copy-and-paste is fine).
  
* `Conclusions`: Summarize your findings, explain how these results could be used by others (if applicable), and describe ways you could improve your program. You could describe ways you might like to expand the functionality of your program if given more time.
