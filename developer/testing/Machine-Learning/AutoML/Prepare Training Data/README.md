Introduction
The quality of your training data strongly impacts the effectiveness of the model you create, and by extension, the quality of the predictions returned from that model. You cannot modify the data after you have uploaded it. If you need to change your training data after you import it, you must update the source data and reimport.

Understanding how your data is interpreted and used by AutoML Tables enables you to upload clean, effective data.

Understanding your problem
The first step in creating effective training data is to make sure that your problem is well defined and will yield the prediction results you need. If you are new to machine learning, you should review the problem types that AutoML Tables addresses and decide what type of model you want to create. For more information about the problem types supported by AutoML Tables, see Problem types.

Determining what to include in your dataset
Next, you must determine the data to include in your training data. In some cases, you can use a table that already exists in your business data. In other cases, you must assemble data from different sources, possibly perform some data transformations, or drop some columns to create the most effective training data.

Training data requirements
Your training data must conform to the following requirements:

It must be 100 GB or smaller.

The value you want to predict (your target column) must be included.

If the data does not have this column, AutoML Tables cannot associate the training data with the desired result. The data type of this column also determines the type of your model. Learn more.

There must be at least two and no more than 1,000 columns.

One column must be the target, and there must be at least one feature available to train the model. Ideally, your training data has many more than two columns.

There must be at least 1,000 and no more than 200,000,000 rows.

Depending on how many features your dataset has, 1,000 rows might not be enough to train a high-performing model. Learn more.

Additional features based on training data
In addition, some AutoML Tables capabilities require specific data to be included in your training data:

If you want to control how your data is split into training, evaluation, and testing, see About controlling data split.

If you want to weight some rows more heavily than others, see About using weights in your training data.

For more data best practices, see Best practices for creating training data.

Preparing your import source
You can provide model training data to AutoML Tables in two ways:

Using BigQuery
Using comma-separated values (CSV) files
Which source you use depends on how your data is stored, and the size and complexity of your data. If your dataset is small, and you don't need more complex data types, CSV might be easier. For larger datasets that include arrays and structs, you must use BigQuery.

For both import sources, your data must meet the following requirements:

Has 1,000 to 200,000,000 rows.
Has between 2 and 1,000 columns.
Is 100 GB or less.
BigQuery
Your BigQuery table must use a multi-regional BigQuery dataset in the US or EU location. Depending on the location of the BigQuery table and its data source (which can be different), you need to make the permission updates listed in the table below. Note that permission changes might be needed on your home project (the project where AutoML Tables is located) or in the foreign project.

Table type	Table location	Data source location	Role addition required
Native BigQuery table	Home project	N/A	None.
Native BigQuery table	Foreign project	N/A	BigQuery Data Viewer for foreign project. Learn more.
BigQuery view	Same project	N/A	None.
BigQuery view	Different project	N/A	BigQuery Data Viewer for foreign project. Learn more.
External BigQuery data source backed by Cloud Bigtable	Home project	Home project	Bigtable Reader for home project. Learn more.
External BigQuery data source backed by Cloud Bigtable	Home project	Foreign project	Bigtable Reader for foreign project. Learn more.
External BigQuery data source backed by Cloud Bigtable	Foreign project	Foreign project	BigQuery Reader and Bigtable Reader for foreign project. Learn more.
External BigQuery data source backed by Cloud Storage	Home project	Home project	None.
External BigQuery data source backed by Cloud Storage	Home project	Foreign project	Storage Object Viewer for foreign project. Learn more.
External BigQuery data source backed by Cloud Storage	Foreign project	Foreign project	Storage Object Viewer and BigQuery Data Viewer for foreign project. Learn more.
External BigQuery data source backed by Google Sheets	Home project	N/A	Share your Sheets file with the AutoML service account. Learn more.
External BigQuery data source backed by Google Sheets	Foreign project	N/A	BigQuery Reader for foreign project and share your Sheets file with the AutoML service account.
You do not need to specify a schema for your BigQuery table. AutoML Tables automatically infers the schema for your table when you import your data.

Your BigQuery uri (specifying the location of your training data) must conform to the following format:


bq://<project_id>.<dataset_id>.<table_id>
The uri cannot contain any other special characters.

For information about BigQuery data types and how they map into AutoML Tables, see BigQuery tables. For more information about using BigQuery external data sources, see Introduction to external data sources.

CSV files
CSV file requirements
CSV files can be in Cloud Storage, or on your local computer. They must conform to the following requirements:

The first line of the first file must be a header, containing the names of the columns. If the first row of a subsequent file is the same as the header, then it is also treated as a header, otherwise it will be treated as data.
Column names can include any alphanumeric character or an underscore (_). The column name cannot begin with an underscore.
The separator character must be a comma (",").
Each file must not be larger than 10 GB.

You can include multiple files, up to a maximum amount of 100 GB.

You do not need to specify a schema for your CSV data. AutoML Tables automatically infers the schema for your table when you import your data, and uses the header row for column names.

For more information about CSV file format and data types, see CSV files.

Cloud Storage bucket requirements
If you are importing your data from Cloud Storage, it must be in a bucket that meets the following requirements:

It conforms to the Cloud Storage bucket requirements.
If the bucket is not in the same project as AutoML Tables, you must give the Storage > Storage Object Viewer role to AutoML Tables in that project. Learn more.
If you are importing your data from your local computer, you must have a Cloud Storage bucket that meets the following requirements:

It conforms to the Cloud Storage bucket requirements.
If the bucket is not in the same project as AutoML Tables, you must give the Storage > Storage Object Creator role to AutoML Tables in that project. Learn more.
AutoML Tables uses this bucket as a staging area before importing your data.

You must use the Cloud Console to import CSV files from your local computer.

How data splits are used
When you use a dataset to train a model, your data is divided into three splits: a training set, a validation set, and a test set.

The training and validation sets is used to try a vast number of preprocessing, architecture, and hyperparameter option combinations. These trials result in trained models that are then evaluated on the validation set for quality and to guide exploration of additional option combinations.

When more trials no longer lead to quality improvements, that version of the model is considered the final, best performing, trained model. Next, AutoML Tables trains two more models, using the parameters and architecture determined in the parallel tuning phase:

A model trained with your training and validation sets.

AutoML Tables generates the model evaluation metrics on this model, using your test set. This is the first time in the process that the test set is used. This approach ensures that the final evaluation metrics are an unbiased reflection of how well the final trained model will perform in production.

A model trained with your training, validation, and test sets.

This model is the one that you use to request predictions.

About controlling data split
By default, AutoML Tables randomly selects 80% of your data rows for training, 10% for validation, and 10% for testing. For datasets that do not change over time, are relatively balanced, and that reflect the distribution of the data that will be used for predictions in production, the random selection algorithm is usually sufficient. The key goal is to ensure that your test set accurately represents the data the model will see in production. This ensures that the evaluation metrics provide an accurate signal on how the model will perform on real world data.

Here are some times when you might want to actively choose what rows are used in which data split:

Your data is time-sensitive.

In this case, you should use a Time column, or a manual split that results in the most recent data being used as the test set.

Your test data includes data from populations that will not be represented in production.

For example, suppose you are training a model with purchase data from a number of stores. You know, however, that the model will be used primarily to make predictions for stores that are not in the training data. To ensure that the model can generalize to unseen stores, you should segregate your data sets by stores. In other words, your test set should include only stores different from the evaluation set, and the evaluation set should include only stores different from the training set.

Your classes are imbalanced.

If you have many more of one class than another in your training data, you might need to manually include more examples of the minority class in your test data. AutoML Tables does not perform stratified sampling, so the test set could include too few or even zero examples of the minority class.

You can control what rows are selected for which split using one of two approaches:

The data split column
The Time column
If you specify both a data split column and the Time column, only the data split column is used to split your data.

The data split column
The data split column enables you to select specific rows to be used for training, validation, and testing. When you create your training data, you add a column that can contain one of the following (case sensitive) values:

TRAIN
VALIDATE
TEST
UNASSIGNED
The values in this column must be one of the two following combinations:

All of TRAIN, VALIDATE, and TEST
Only TEST and UNASSIGNED
Every row must have a value for this column; it cannot be the empty string.

For example, with all sets specified:


"TRAIN","John","Doe","555-55-5555"
"TEST","Jane","Doe","444-44-4444"
"TRAIN","Roger","Rogers","123-45-6789"
"VALIDATE","Sarah","Smith","333-33-3333"
With only the test set specified:


"UNASSIGNED","John","Doe","555-55-5555"
"TEST","Jane","Doe","444-44-4444"
"UNASSIGNED","Roger","Rogers","123-45-6789"
"UNASSIGNED","Sarah","Smith","333-33-3333"
The data split column can have any valid column name.

If value of the data split column is UNASSIGNED, AutoML Tables automatically assigns that row to the training or validation set.

After you import your data, you select a Manual data split and specify this column as the data split column. (You can also use the mlUseColumnSpecId field.)

Note: Rows are selected for a data split randomly, but deterministically. If you are not satisfied with the makeup of your generated data splits, you must use a manual split or change the training data. Training a new model with the same training data results in the same data split.
The Time column
You use the Time column to tell AutoML Tables that time matters for your data; it is not randomly distributed over time. When you specify the Time column, AutoML Tables uses the earliest 80% of the rows for training, the next 10% of rows for validation, and the latest 10% of rows for testing.

AutoML Tables treats each row as an independent and identically distributed training example; setting the Time column does not change this. The Time column is used only to split the data set.

You must include a value for the Time column for every row in your dataset. Make sure that the Time column has enough distinct values, so that the evaluation and test sets are non-empty. Usually, having at least 20 distinct values should be sufficient.

The Time column must have a data type of Timestamp.

During schema review, you select this column as the Time column. (In the API, you use the timeColumnSpecId field.) This selection takes effect only if you have not specified the data split column.

If you have a time-related column that you do not want to use to split your data, set the data type for that column to Timestamp but do not set it as the Time column.

About using weights in your training data
By default, AutoML Tables weights each row of your training data equally-- no row is considered to be more important for training purposes than another.

Sometimes, you might want some rows to have more importance for training. For example, if you are using spending data, you might want the data associated with higher spenders to have a larger impact on the model. If missing a specific outcome is something you particularly want to avoid, then you can weight rows with that outcome more heavily.

You give rows a relative weight by adding a weight column to your dataset. The weight column must be a Numeric column. You use it to specify a value from 0 to 10000. Higher values tell AutoML Tables that the row is more important when training the model. A weight of 0 means that the row is ignored. If the value in the weight column is empty, then AutoML Tables applies a default weight of 1.

Later, when you review your schema, you specify this column as the Weight column. (You can also use the weightColumnSpecId field.)

Custom weighting schemes are used only for training the model; they do not affect model evaluation.

Requirements for the target column
The target column must conform to the following requirements:

It must be either Categorical or Numerical.
If it is Categorical, it must have at least 2 and no more than 500 distinct values.
It cannot be nullable.
