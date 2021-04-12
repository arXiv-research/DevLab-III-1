This quickstart walks you through the process of using AutoML Tables web application to do the following steps:

Create a dataset.
Import table data from a CSV file into the dataset.
Identify schema columns in the imported data.
Train a model from the imported data.
Use the model to make predictions.
The entire process takes a couple of hours to complete. Most of that time is not active time; you can close your browser window and return to the task later.

Before you begin
Create a project and enable AutoML Tables
In the Google Cloud Console, on the project selector page, select or create a Google Cloud project.

Note: If you don't plan to keep the resources that you create in this procedure, create a project instead of selecting an existing project. After you finish these steps, you can delete the project, removing all resources associated with the project.
Go to project selector

Make sure that billing is enabled for your Cloud project. Learn how to confirm that billing is enabled for your project.

Enable the Cloud AutoML and Storage APIs.
Enable the APIs

Sample data
This quickstart uses the Bank marketing open-source dataset, which is available through a Creative Commons CCO: Public Domain license. The column names have been updated for clarity.

Create a dataset and train a model
Visit AutoML Tables in the Google Cloud Console to begin the process of creating your dataset and training your model.

Go to the AutoML Tables page

Select Datasets, and then select New dataset.

AutoML Tables datasets page

Enter Quickstart_Dataset for the dataset name and click Create dataset.

On the Import your data page, choose Select a CSV file from Cloud Storage.

Leave the Location set to Global.

Enter cloud-ml-tables-data/bank-marketing.csv for the bucket.

Click Import.

AutoML Tables create dataset page

The dataset import takes a few minutes to complete.

After the dataset import completes, select Deposit for the Target column.

The target column identifies the value the model will be trained to predict.

AutoML Tables schema page

This window provides information about your imported data. You can click individual rows to see more about distribution and correlation for a specific feature.

dataset row specifics

Click Train model. Enter Quickstart_Model for Model name, and 1 for Training budget.

AutoML Tables train page

Click Train model to start the training process.

Model training takes about two hours to complete. After the model is successfully trained, the Models tab shows high-level metrics for the model.

High-level metrics for a trained model

Select the Evaluate tab for a detailed view of the model evaluation metrics.

For this model, 1 represents a negative outcome--a deposit is not made at the bank. 2 represents a positive outcome--a deposit is made at the bank.

You can select a label to see specific evaluation metrics for that label. You can also adjust the Score threshold to see how the metrics differ for different threshold values.

AutoML Tables evaluate page

You can also scroll down to see the confusion matrix and feature importance graph.

Confusion matrix and feature importance graph

Select the Test & Use tab, and select Online prediction.

Click Deploy model to deploy your model.

You must deploy your model before you can request online predictions. Deploying a model takes a few minutes to complete.

AutoML Tables deployment button

When the model is deployed, AutoML Tables fills in sample data to help you test your model.

Select the Generate feature importance checkbox.

Click Predict to request the online prediction.

AutoML Tables predict button with feature importance checked

AutoML Tables determines the probability of each possible outcome based on the input values and displays the confidence values for the prediction in the Prediction result section.

Prediction results with feature importance

In the example above, the model is predicting the result of "1", with 99.8% certainty.

You can also submit prediction requests in batch form. Learn more.

Cleanup
If you no longer need your custom model or dataset, you can delete them.

To avoid unnecessary Google Cloud Platform charges, use the Cloud Console to delete your project if you do not need it.

Undeploy your model
Your model incurs charges while it is deployed.

Select Models and click on the model you want to undeploy.
Select the Test & Use tab and click Online prediction.
Click Remove deployment.
Undeploy model

Delete a model
To delete a model, select Models. Click the More actions menu for the model that you want to delete, and then select Delete model.

Delete model

Delete a dataset
To delete a dataset, select Datasets. Click the More actions menu for the model that you want to delete, and then select Delete dataset.
