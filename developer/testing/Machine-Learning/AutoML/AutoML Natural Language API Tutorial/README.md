This tutorial demonstrates how to create a custom model for classifying content using AutoML Natural Language. The application trains a custom model using a corpus of crowd-sourced "happy moments" from the Kaggle open-source dataset HappyDB. The resulting model classifies happy moments into categories reflecting the causes of happiness.

The data is made available through a Creative Commons CCO: Public Domain license.

The tutorial covers training the custom model, evaluating its performance, and classifying new content.

Viewing Code Samples: Most of the code samples in this tutorial are taken from larger code files located in GitHub. You can view and download the complete file from which a code sample is taken by clicking the "View on GitHub" button provided above a sample.
Prerequisites
Configure your project environment
In the Google Cloud Console, on the project selector page, select or create a Google Cloud project.

Note: If you don't plan to keep the resources that you create in this procedure, create a project instead of selecting an existing project. After you finish these steps, you can delete the project, removing all resources associated with the project.
Go to project selector

Make sure that billing is enabled for your Cloud project. Learn how to confirm that billing is enabled for your project.

Enable the AutoML Natural Language APIs.
Enable the APIs

Install the gcloud command line tool.
Follow the instructions to create a service account and download a key file.
Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path to the service account key file that you downloaded when you created the service account. For example:

     export GOOGLE_APPLICATION_CREDENTIALS=key-file
Add your new service account to the AutoML Editor IAM role with the following commands. Replace project-id with the name of your GCP project and replace service-account-name with the name of your new service account, for example service-account1@myproject.iam.gserviceaccount.com.

     gcloud auth login
     gcloud config set project project-id
     gcloud projects add-iam-policy-binding project-id 

       --member=serviceAccount:service-account-name 

       --role='roles/automl.editor'
Allow the AutoML Natural Language service accounts to access your Google Cloud project resources:

gcloud projects add-iam-policy-binding project-id 

  --member="serviceAccount:custom-vision@appspot.gserviceaccount.com" 

  --role="roles/storage.admin"
Install the client library.
Set the PROJECT_ID and REGION_NAME environment variables.

Replace project-id with the Project ID of your Google Cloud Platform project. AutoML Natural Language currently requires the location us-central1.

     export PROJECT_ID="project-id"
     export REGION_NAME="us-central1"
     
Create a Google Cloud Storage bucket to store the documents that you will use to train your custom model.

The bucket name must be in the format: $PROJECT_ID-lcm. The following command creates a storage bucket in the us-central1 region named $PROJECT_ID-lcm.

gsutil mb -p $PROJECT_ID -c regional -l $REGION_NAME gs://$PROJECT_ID-lcm/
Copy the happiness.csv file from the public bucket to your Google Cloud Storage bucket.

The happiness.csv file is in the NL-classification folder in the public bucket cloud-ml-data.
Source code file locations
If you want the source code, it can be found here. Please feel free to copy the source code files into your Google Cloud Platform project folder. Otherwise, we recommend directly copying the code from this page as you reach each step.

Python
Java
Node.js
The tutorial consists of these Python programs:

language_text_classification_create_dataset.py – Includes functionality to create a dataset
import_dataset.py – Includes functionality to import a dataset
language_text_classification_create_model.py – Includes functionality to create a model
list_model_evaluations.py – Includes functionality to list model evaluations
language_text_classification_predict.py – Includes functionality related to prediction
delete_model.py - Include functionality to delete a model
Running the application
Step 1: Create a dataset
The first step in creating a custom model is to create an empty dataset that will eventually hold the training data for the model. When you create a dataset, you specify the type of classification you want your custom model to perform:

MULTICLASS assigns a single label to each classified document
MULTILABEL allows a document to be assigned multiple labels
This tutorial creates a dataset named ‘happydb’ and uses MULTICLASS.

Copy the Code
Python
Java
Node.js
Open in Cloud Shell Open in Cloud Shell View on GitHub

from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
# project_id = "YOUR_PROJECT_ID"
# display_name = "YOUR_DATASET_NAME"

client = automl.AutoMlClient()

# A resource that represents Google Cloud Platform location.
project_location = f"projects/{project_id}/locations/us-central1"
# Specify the classification type
# Types:
# MultiLabel: Multiple labels are allowed for one example.
# MultiClass: At most one label is allowed per example.
metadata = automl.TextClassificationDatasetMetadata(
    classification_type=automl.ClassificationType.MULTICLASS
)
dataset = automl.Dataset(
    display_name=display_name,
    text_classification_dataset_metadata=metadata,
)

# Create a dataset with the dataset metadata in the region.
response = client.create_dataset(parent=project_location, dataset=dataset)

created_dataset = response.result()

# Display the dataset information
print("Dataset name: {}".format(created_dataset.name))
print("Dataset id: {}".format(created_dataset.name.split("/")[-1]))
Request
Run the create_dataset function to create an empty dataset. You'll need to modify the following lines of code:

Set the project_id to your PROJECT_ID
Set the display_name for the dataset (happydb)

Python
Java
Node.js

python language_text_classification_create_dataset.py
Response
The response includes the details of the newly created dataset, including the Dataset ID that you'll use to reference the dataset in future requests. We recommend that you set an environment variable DATASET_ID to the returned Dataset ID value.


Dataset name: projects/216065747626/locations/us-central1/datasets/TCN7372141011130533778
Dataset id: TCN7372141011130533778
Dataset display name: happydb
Text classification dataset specification:
       classification_type: MULTICLASS
Dataset example count: 0
Dataset create time:
       seconds: 1530251987
       nanos: 216586000
Step 2: Import training items into the dataset
The next step is to populate the dataset with a list of training content items labeled using the target categories.

The import_dataset function interface takes as input a .csv file that lists the locations of all training documents and the proper label for each training document. (See Preparing your training data for details about the required format.) For this tutorial, we will be using happiness.csv, which you uploaded to Google Cloud Storage above.

Copy the Code
Python
Java
Node.js
Open in Cloud Shell Open in Cloud Shell View on GitHub

from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
# project_id = "YOUR_PROJECT_ID"
# dataset_id = "YOUR_DATASET_ID"
# path = "gs://YOUR_BUCKET_ID/path/to/data.csv"

client = automl.AutoMlClient()
# Get the full path of the dataset.
dataset_full_id = client.dataset_path(project_id, "us-central1", dataset_id)
# Get the multiple Google Cloud Storage URIs
input_uris = path.split(",")
gcs_source = automl.GcsSource(input_uris=input_uris)
input_config = automl.InputConfig(gcs_source=gcs_source)
# Import data from the input URI
response = client.import_data(name=dataset_full_id, input_config=input_config)

print("Processing import...")
print("Data imported. {}".format(response.result()))
Request
Run the import_data function to import the training content. The first piece of code to change is the Dataset ID from the previous step and the second is the URI of happiness.csv. You'll need to modify the following lines of code:

Set the project_id to your PROJECT_ID
Set the dataset_id for the dataset (from the output of the previous step)
Set the path which is the URI of the (gs://YOUR_PROJECT_ID-lcm/csv/happiness.csv)

Python
Java
Node.js

python import_dataset.py
Response

Processing import...
Dataset imported.
Step 3: Create (train) the model
Now that you have a dataset of labeled training documents, you can train a new model.

Copy the Code
Python
Java
Node.js
Open in Cloud Shell Open in Cloud Shell View on GitHub

from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
# project_id = "YOUR_PROJECT_ID"
# dataset_id = "YOUR_DATASET_ID"
# display_name = "YOUR_MODEL_NAME"

client = automl.AutoMlClient()

# A resource that represents Google Cloud Platform location.
project_location = f"projects/{project_id}/locations/us-central1"
# Leave model unset to use the default base model provided by Google
metadata = automl.TextClassificationModelMetadata()
model = automl.Model(
    display_name=display_name,
    dataset_id=dataset_id,
    text_classification_model_metadata=metadata,
)

# Create a model with the model metadata in the region.
response = client.create_model(parent=project_location, model=model)

print("Training operation name: {}".format(response.operation.name))
print("Training started...")
Request
Call the create_model function to create a model. The Dataset ID is from the previous steps. You'll need to modify the following lines of code:

Set the project_id to your PROJECT_ID
Set the dataset_id for the dataset (from the output of the previous step)
Set the display_name for your model (happydb_model)

Python
Java
Node.js

python language_text_classification_create_model.py
Response
The create_model function kicks off a training operation and prints the operation name. Training happens asynchronously and can take a while to complete, so you can use the operation ID to check training status. When training is complete, create_model returns the Model ID. As with the Dataset ID, you might want to set an environment variable MODEL_ID to the returned Model ID value.


Training operation name: projects/216065747626/locations/us-central1/operations/TCN3007727620979824033
Training started...
Model name: projects/216065747626/locations/us-central1/models/TCN7683346839371803263
Model id: TCN7683346839371803263
Model display name: happydb_model
Model create time:
        seconds: 1529649600
        nanos: 966000000
Model deployment state: deployed
Step 4: Evaluate the model
After training, you can evaluate your model's readiness by reviewing its precision, recall, and F1 score.

The display_evaluation function takes the Model ID as a parameter.

Copy the Code
Python
Java
Node.js
Open in Cloud Shell Open in Cloud Shell View on GitHub

from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
# project_id = "YOUR_PROJECT_ID"
# model_id = "YOUR_MODEL_ID"

client = automl.AutoMlClient()
# Get the full path of the model.
model_full_id = client.model_path(project_id, "us-central1", model_id)

print("List of model evaluations:")
for evaluation in client.list_model_evaluations(parent=model_full_id, filter=""):
    print("Model evaluation name: {}".format(evaluation.name))
    print("Model annotation spec id: {}".format(evaluation.annotation_spec_id))
    print("Create Time: {}".format(evaluation.create_time))
    print("Evaluation example count: {}".format(evaluation.evaluated_example_count))
    print(
        "Classification model evaluation metrics: {}".format(
            evaluation.classification_evaluation_metrics
        )
    )
Request
Make a request to display the overall evaluation performance of the model by executing the following request. You'll need to modify the following lines of code:

Set the project_id to your PROJECT_ID
Set the model_id to your model's id

Python
Java
Node.js

python list_model_evaluations.py
Response
If the precision and recall scores are too low, you can strengthen the training dataset and re-train your model. For more information, see Evaluating models.


Precision and recall are based on a score threshold of 0.5
Model Precision: 96.3%
Model Recall: 95.7%
Model F1 score: 96.0%
Model Precision@1: 96.33%
Model Recall@1: 95.74%
Model F1 score@1: 96.04%
Step 5: Deploy the model
When your custom model meets your quality standards, you can deploy it and then make predictions request.

Copy the Code
Python
Java
Node.js
Open in Cloud Shell Open in Cloud Shell View on GitHub

from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
# project_id = "YOUR_PROJECT_ID"
# model_id = "YOUR_MODEL_ID"

client = automl.AutoMlClient()
# Get the full path of the model.
model_full_id = client.model_path(project_id, "us-central1", model_id)
response = client.deploy_model(name=model_full_id)

print(f"Model deployment finished. {response.result()}")
Request
For the deploy_model function you'll need to modify the following lines of code:

Set the project_id to your PROJECT_ID
Set the model_id to your model's id

Python
Java
Node.js

python deploy_model.py
Response

Model deployment finished.
Step 6: Use the model to make a prediction
After you deploy your model, you can use it to classify novel content.

Copy the Code
Python
Java
Node.js
Open in Cloud Shell Open in Cloud Shell View on GitHub

from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
# project_id = "YOUR_PROJECT_ID"
# model_id = "YOUR_MODEL_ID"
# content = "text to predict"

prediction_client = automl.PredictionServiceClient()

# Get the full path of the model.
model_full_id = automl.AutoMlClient.model_path(project_id, "us-central1", model_id)

# Supported mime_types: 'text/plain', 'text/html'
# https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#textsnippet
text_snippet = automl.TextSnippet(content=content, mime_type="text/plain")
payload = automl.ExamplePayload(text_snippet=text_snippet)

response = prediction_client.predict(name=model_full_id, payload=payload)

for annotation_payload in response.payload:
    print(u"Predicted class name: {}".format(annotation_payload.display_name))
    print(
        u"Predicted class score: {}".format(annotation_payload.classification.score)
    )
Request
For the predict function you'll need to modify the following lines of code:

Set the project_id to your PROJECT_ID
Set the model_id to your model's id
Set the content you want to predict

Python
Java
Node.js

python language_text_classification_predict.py
Response
The function returns the classification score for how well the content matches each category.


Prediction results:
Predicted class name: affection
Predicted class score: 0.9702693223953247
Step 7: Delete a Model
When you are done using this sample model, you can delete it permanently. You will no longer be able to use the model for prediction.

Copy the Code
Python
Java
Node.js
Open in Cloud Shell Open in Cloud Shell View on GitHub

from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
# project_id = "YOUR_PROJECT_ID"
# model_id = "YOUR_MODEL_ID"

client = automl.AutoMlClient()
# Get the full path of the model.
model_full_id = client.model_path(project_id, "us-central1", model_id)
response = client.delete_model(name=model_full_id)

print("Model deleted. {}".format(response.result()))
Request
Make a request with operation type delete_model to delete a model you created you'll need to modify the following lines of code:

Set the project_id to your PROJECT_ID
Set the model_id to your model's id

Python
Java
Node.js

python delete_model.py
Response

Model deleted.
