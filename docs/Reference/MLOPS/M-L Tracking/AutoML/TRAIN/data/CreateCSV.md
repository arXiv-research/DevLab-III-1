Create CSV files with video URIs and labels
Once your files have been uploaded to Cloud Storage, you can create CSV files that list all of your training data and the category labels for that data. The CSV files can have any filenames, must be UTF-8 encoded, and must end with the .csv extension.

There are three files that you can use for training and verifying your model:

File	Description
Model training file list	
Contains paths to the training and test CSV files.

This file is used to identify the locations of separate CSV files that describe your training and testing data.

Here are some examples of the contents of the file list CSV file:

Example 1:


TRAIN,gs://automl-video-demo-data/traffic_videos/traffic_videos_train.csv
TEST,gs://automl-video-demo-data/traffic_videos/traffic_videos_test.csv
Example 2:


UNASSIGNED,gs://automl-video-demo-data/traffic_videos/traffic_videos_labels.csv
Training data	
Used to train the model. Contains URIs to video files, the label identifying the object category, the instance id that identifies the object instance across video frames in a video (optional), the time offset of the labeled video frame, and the object bounding box coordinates.

If you specify a training data CSV file, you must also specify a test or an unassigned data CSV file.

Test data	
Used for testing the model during the training phase. Contains the same fields as in the training data.

If you specify a test data CSV file, you must also specify a training or an unassigned data CSV file.

Unassigned data	
Used for both training and testing the model. Contains the same fields as in the training data. Rows in the unassigned file are automatically divided into training and testing data, typically 80% for training and 20% for testing.

You can specify only an unassigned data CSV file without training and testing data CSV files. You can also specify only the training and testing data CSV files without an unassigned data CSV file.

The training, test, and unassigned files must have one row of an object bounding box in the set you are uploading, with these columns in each row:

The content to be categorized or annotated. This field contains a Cloud Storage URI for the video. Cloud Storage URIs are case-sensitive.

A label that identifies how the object is categorized. Labels must start with a letter and only contain letters, numbers, and underscores. AutoML Video Object Tracking also allows you to use labels with white spaces.

An instance ID that identifies the object instance across video frames in a video (Optional). If it is provided, AutoML Video Object Tracking uses them for object tracking tuning, training and evaluation. The bounding boxes of the same object instance present in different video frames are labeled as the same instance ID. The instance id is only unique in each video but not in the dataset. For example, if two objects from two different videos have the same instance ID, it does not mean they are the same object instance.

The time offset of the video frame that indicates the duration offset from the beginning of the video. The time offset is a floating number and the units are in second.

The timeoffset of the annotations you provide does not need to align with the frame rate of AutoML Video Object Tracking's system. The annotations are rounded to the timestamp of the nearest frame, which is at most 0.05s away in 10fps videos.
A bounding box for an object in the video frame The bounding box for an object can be specified in two ways:

Using 2 vertices consisting of a set of x,y coordinates if they are diagonally opposite points of the rectangle, as shown in this example:

Bounding_box


x_relative_min, y_relative_min,,,x_relative_max,y_relative_max,,
Using all 4 vertices:

x_relative_min,y_relative_min,x_relative_max,y_relative_min,x_relative_max,y_relative_max,x_relative_min,y_relative_max
Each vertex is specified by x, y coordinate values. These coordinates must be a float in the 0 to 1 range, where 0 represents the minimum x or y value, and 1 represents the greatest x or y value.

For example, (0,0) represents the top left corner, and (1,1) represents the bottom right corner; a bounding box for the entire image is expressed as (0,0,,,1,1,,), or (0,0,1,0,1,1,0,1).

AutoML Video Object Tracking API does not require a specific vertex ordering. Additionally, if four specified vertices don't form a rectangle parallel to image edges, AutoML Video Object Tracking API specifies vertices that do form such a rectangle.

Note: You can use Cloud Video Intelligence API's Object Tracking feature to help build your dataset by getting more generalized labels and bounding boxes for object tracks in a video.
Examples of CSV dataset files
The following rows demonstrate how to specify data in a dataset. The example includes a path to a video on Cloud Storage, a label for the object, a times offset to begin tracking, and two diagonal vertices.


video_uri,label,instance_id,time_offset,x_relative_min,y_relative_min,
x_relative_max,y_relative_min,x_relative_max,y_relative_max,x_relative_min,y_relative_max

gs://folder/video1.avi,car,,12.90,0.8,0.2,,,0.9,0.3,,
gs://folder/video1.avi,bike,,12.50,0.45,0.45,,,0.55,0.55,,
where in the first row,

VIDEO_URI is gs://folder/video1.avi,
LABEL is car,
INSTANCE_ID not specified,
TIME_OFFSET is 12.90,
X_RELATIVE_MIN,Y_RELATIVE_MIN are 0.8,0.2,
X_RELATIVE_MAX,Y_RELATIVE_MIN not specified,
X_RELATIVE_MAX,Y_RELATIVE_MAX are 0.9,0.3,
X_RELATIVE_MIN,Y_RELATIVE_MAX are not specified
As stated previously, you can also specify your bounding boxes by providing all four vertices, as shown in the following examples.


gs://folder/video1.avi,car,,12.10,0.8,0.8,0.9,0.8,0.9,0.9,0.8,0.9
gs://folder/video1.avi,car,,12.90,0.4,0.8,0.5,0.8,0.5,0.9,0.4,0.9
gs://folder/video1.avi,car,,12.10,0.4,0.2,0.5,0.2,0.5,0.3,0.4,0.3
You do not need to specify validation data to verify the results of your trained model. AutoML Video Object Tracking automatically divides the rows identified for training into training and validation data, where 80% is used for training and 20% for validation.

Troubleshooting CSV dataset issues
If you have issues specifying your dataset using a CSV file, check the CSV file for the following list of common errors:

Using unicode characters in labels. For example, Japanese characters are not supported.
Using spaces and non-alphanumeric characters in labels
Empty lines
Empty columns (lines with two successive commas)
Incorrect capitalization of Cloud Storage video paths
Incorrect access control configured for your video files. Your service account should have read or greater access, or files must be publicly-readable.
References to non-video files (such as PDF or PSD files). Likewise, files that are not video files but that have been renamed with a video extension will cause an error.
URI of video points to a different bucket than the current project. Only videos in the project bucket can be accessed.
Non-CSV-formatted files.
