This page describes how to use AutoML Tables to train a custom model based on your dataset. You must already have created a dataset and imported data into it.

Introduction
You create a custom model by training it using a prepared dataset. AutoML Tables uses the items from the dataset to train the model, test it, and evaluate its performance. You can review the results, adjust the training dataset as needed and train a new model using the improved dataset.

As part of preparing to train a model, you update the schema information of the dataset. These schema updates affect any future model that uses that dataset. Models that have already begun training are unaffected.

Training a model can take several hours to complete. You can check training progress in the Cloud Console, or by using the Cloud AutoML API.

Since AutoML Tables creates a new model each time you start training, your project may include numerous models. You can get a list of the models in your project and can delete models that you no longer need.

Models must be retrained periodically so that they can continue to serve predictions. For predictions without feature importance, a model must be retrained very two years. For predictions with feature importance, a model must be retrained every six months.

Training a model
Console
REST & CMD LINE
More
If needed, open the Datasets page and click on the dataset you want to use.

This opens the dataset in the Train tab.

AutoML Tables schema page

Select the target column for your model.

This is the value that the model is trained to predict. Its data type determines whether the resulting model is a regression (Numeric) or a classification (Categorical) model. Learn more.

If your target column has a data type of Categorical, it must have at least two and no more than 500 distinct values.

Review Data type, Nullability, and the data statistics for each column in your dataset.

You can click on individual columns to get more details about that column. Learn more about schema review.

AutoML Tables schema page

If you want to control your data split, click Edit additional parameters and specify a data split column or a Time column. Learn more.

AutoML Tables schema page

If you want to weight your training examples by the value of a column, click Edit additional parameters and specify the appropriate column. Learn more.

Review the summary statistics and details to ensure that your data quality is what you expect, and that you have identified any columns that need to be excluded when you create your model.

For more information, see Analyzing your training data.

When you are satisfied with your dataset schema, click Train model at the top of the screen.

When you make changes to your schema, AutoML Tables updates the summary statistics, which can take a few moments to complete. You do not need to wait for this process to complete before initiating model training.

AutoML Tables schema page

For Training budget, enter the maximum number of training hours for this model.

Training budget is between 1 and 72 hours. This is the maximum amount of training time you will be charged for.

Suggested training time is related to the size of your training data. The table below shows suggested training time ranges by row count; a large number of columns will also increase training time.

Rows	Suggested training time
Less than 100,000	1-3 hours
100,000 - 1,000,000	1-6 hours
1,000,000 - 10,000,000	1-12 hours
More than 10,000,000	3 - 24 hours
Model creation includes other tasks besides training, so the total time it takes to create your model is longer than the training time. For example, if you specify 2 training hours, it could still take 3 or more hours before the model is ready to deploy. You are charged only for actual training time.

Learn more about training prices.

If AutoML Tables detects that the model is no longer improving before the training budget is exhausted, it stops training. If you want to use the entire budgeted training time, open Advanced options and disable Early stopping.

In the Input feature selection section, exclude any columns that you targeted for exclusion in the schema analysis step.

If you do not want to use the default optimization objective, open Advanced options and select the metric you want AutoML Tables to optimize for when training your model. Learn more.

Depending on the data type of your target column, there might be only one choice for Optimization objective.

Click Train model to begin model training.

Training a model can take several hours to complete depending on the size of the dataset and the training budget. You can close your browser window without affecting the training process.

After the model is successfully trained, the Models tab shows high-level metrics for the model, such as precision and recall.

High-level metrics for a trained model

For help with evaluating the quality of your model, see Evaluating models.

Schema review
AutoML Tables infers the data type and whether a column is nullable for each column based on the original data type (if it was imported from BigQuery) and the values in the column. You should check each column and make sure it looks correct.

Use the following list to review your schema:

Fields that contain free-form text should be Text.

Text fields are separated into tokens by UnicodeScriptTokenizer, with individual tokens being used for model training. The UnicodeScriptTokenizer tokenizes text by whitespace, while also separating punctuation from text and different languages from each other.

If the value of a column is one of a finite set of values, it should probably be Categorical, regardless of the type of data used in the field.

For example, you might have codes for colors: 1 = red, 2 = yellow, etc. You should make sure that such a field was designated as Categorical.

An exception to this guidance is if the column contains multi-word strings. In this case, you should set it as a Text column, even if it has a low cardinality. AutoML Tables tokenizes Text columns, and might be able to derive prediction signal from the individual tokens or their order.

If a field is marked non-nullable, it means that it had no null values for the training dataset. Make sure this will be true for your prediction data as well; if a column is marked non-nullable, and a value is not supplied for it at prediction time, a prediction error is returned for that row.

Analyzing your training data
If a column has a high percentage of missing values, make sure this is expected, and not due to a data collection issue.

Make sure the number of invalid values is relatively low or zero.

Any row that contains one or more invalid value is automatically excluded from being used for model training.

If Distinct values for a Categorical column approaches the number of rows (for example, more than 90%), that column will not provide much training signal. It should be excluded from training. ID columns should always be excluded.

If a column's Correlation with Target value is high, make sure that is expected, and not an indication of target leakage.

If the column will be available when you request predictions, then it is probably a feature with strong explanatory power and can be included. However, sometimes features with high correlation are in fact derived from the target or collected after the fact. These features must be excluded from training, because they are not available at prediction time, so the model is unusable in production.

Correlation is calculated for categorical, numeric, and timestamp columns, using Cramér's V. For numeric columns, it is calculated using bucket counts generated from quantiles.

About model optimization objectives
The optimization objective impacts how your model is trained, and therefore how it performs in production. The table below provides some details about what kinds of problems each objective is best for:

Optimization objective	Problem type	API value	Use this objective if you want to...
AUC ROC	Classification	MAXIMIZE_AU_ROC	Distinguish between classes. Default value for binary classification.
Log loss	Classification	MINIMIZE_LOG_LOSS	Keep prediction probabilities as accurate as possible. Default value for multi-class classification.
AUC PR	Classification	MAXIMIZE_AU_PRC	Optimize results for predictions for the less common class.
Precision at Recall	Classification	MAXIMIZE_PRECISION_AT_RECALL	Optimize precision at a specific recall value.
Recall at Precision	Classification	MAXIMIZE_RECALL_AT_PRECISION	Optimize recall at a specific precision value.
RMSE	Regression	MINIMIZE_RMSE	Capture more extreme values accurately.
MAE	Regression	MINIMIZE_MAE	View extreme values as outliers with less impact on model.
RMSLE	Regression	MINIMIZE_RMSLE	Penalize error on relative size rather than absolute value. Especially helpful when both predicted and actual values can be quite large.
