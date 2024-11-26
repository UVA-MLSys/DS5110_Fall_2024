# Notes on our Model

This file contains important notes for anyone that wants to better understand the `AI for Astronomy` Github and Modeling.

**ALL Questions about the model or its development should first refer to the project GitHub and its maintainers.**

>[!NOTE]
>the git for `Ai for Astronomy is separate from the git of this project, think of it almost as a submodule. make sure its up to date.

```bash
cd ../AI-for-Astronomy
git pull # should be current.
```


## Description of Each Folder and File

Anomaly_Detection
├── Fine_Tune_Model
├── Inference
├── Plots
├── blocks
├── Astronomy_Overview.pptx
├── NormalCell.py
├── Plot_Redshift.py
├── README.pdf
```

[Taken heavily from the inference readme](https://github.com/UVA-MLSys/AI-for-Astronomy/tree/main/code/Anomaly%20Detection)

| Folder/File              | Description                                                                                      |
|--------------------------|--------------------------------------------------------------------------------------------------|
| **Fine_Tune_Model**      | Contains model weights.                                                                         |
| **Inference**            | Code and data required for running inference.                                                   |
| **Plots**                | Generated visualizations, such as plots of model evaluation metrics and analysis results.        |
| **blocks**               | Source code for fine-tuning.                                                                     |
| **Astronomy_Overview.pptx**  | PowerPoint presentation summarizing the astronomy aspects of the project.                      |
| **NormalCell.py**        | Python implementation of standard and customized multi-head self-attention mechanisms.           |
| **Plot_Redshift.py**     | Script for generating visualizations and evaluations related to redshift analysis.               |
| **README.pdf**           | Detailed guide providing step-by-step instructions for running inference.                        |

## Model Metrics to Consider

>[!WARNING]
>When considering deployment options, we want to be able balance the integrity of the model along with the various costs and performance of deployment, that means understanding and monitoring these metrics

- **Mean Absolute Error (MAE)**: Measures the average magnitude of the errors between predicted and true values, providing insight into prediction accuracy.
- **Mean Square Error (MSE)**: Quantifies the average of squared errors, emphasizing larger deviations to highlight significant prediction errors.
- **Bias**: Measures the average residuals between predicted and true values, indicating any systematic over- or underestimation in predictions.
- **Precision**: Represents the expected scatter of errors, reflecting the consistency of the model's predictions.
- **R² Score**: Evaluates how well the model predicts compared to the mean of true values; a value closer to 1 indicates better predictive performance.

## Terms

>[!IMPORTANT]
>Redshift Prediction in this context, is more about Astronomy than AWS Redshift.

This definition is (Taken from the ASTROMAE paper)[https://arxiv.org/abs/2409.01825]

>Redshift prediction is a fundamental task in astronomy, essential for understanding the expansion of the universe and determining the distances of astronomical objects. Accurate redshift prediction plays a crucial role in advancing our knowledge of the cosmos

This paper can also be found in the docs/ folder with all credit due to its authors Amirreza Dolatpour Fathkouhi and Geoffrey Charles Fox.