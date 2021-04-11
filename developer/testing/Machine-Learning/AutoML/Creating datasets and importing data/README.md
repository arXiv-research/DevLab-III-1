A dataset is a Google Cloud object that contains your source table data, along with schema information that determines model training parameters. The dataset serves as the input for training a model.

A project can have multiple datasets. You can get a list of the available datasets and can delete datasets you no longer need.

When you update a dataset or its schema information, you affect any future model that uses that dataset. Models that have already begun training are unaffected.

Before you can use AutoML Tables, you must have set up your project as described in Before you begin. Before you can create a dataset, you must have created your training data as described in Preparing your training data.

Creating a dataset
Console
REST & CMD LINE
More
Visit the AutoML Tables page in the Google Cloud Console to begin the process of creating your dataset.

Go to the AutoML Tables page

Select Datasets, and then select New dataset.

Enter the name of your dataset and specify the Region where the dataset will be created.

For more information, see Locations.

Click Create dataset.

The Import tab is displayed. You can now import your data.

Importing data into a dataset
You cannot import data into a dataset that already contains data. You must first create a new dataset.

Console
REST & CMD LINE
More
If needed, select your dataset from list on the Datasets page to open its Import tab.

Choose the import source for your data: BigQuery, Cloud Storage, or your local computer. Provide the information required.

If you load your CSV files from your local computer, you must provide a Cloud Storage bucket. Your files are loaded to that bucket before they are imported into AutoML Tables. The files remain there after the data import unless you remove them.

The bucket must be in the same location as your dataset. Learn more.

Click Import to start the import process.

When the import process finishes, the Train tab is displayed, and you are ready to train your model.
