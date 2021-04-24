This section presents the dataset used for the study and the methodology proposed to enhance object detection in
the context of autonomous vehicles. Firstly, the anchor optimization procedure and the modifications applied to the
Faster R-CNN architecture are described. Secondly, the different learning strategies studied to address class imbalance
are explained. Thirdly, the proposed ensemble model is presented. In the final section, the remaining implementation
details are provided to allow reproducibility. The complete source code can be found at [52].

3.1. Waymo Open Dataset
The Waymo Open Dataset [14] consists of 1150 driving video scenes across different urban areas (Phoenix, San
Francisco, and Mountain View) and at different times of the day (day, night, and dawn). Each scene captures syn-
chronized LiDAR and camera data for 20 seconds, resulting in around 200 frames per scene. The problem addressed
in this study is 2D object detection. This task is to assign 2D bounding boxes to objects that are present in a single
RGB camera image. Waymo’s vehicle is equipped with five high-resolution cameras (Front, Front Left, Front Right,
Side Left, and Side Right). Frontal cameras obtain images with a resolution of 1920x1280, while lateral cameras have
an image size of 1920x886. All cameras have a ±25.2 o horizontal field of view (HFOV). An example of the images
captured by all cameras in a single frame is presented in Figure 1. As it is done in Waymo’s online challenge, the
images obtained from all cameras are considered a single dataset for evaluation purposes.

The dataset contains around 10 million manually annotated labels across all cameras. Three different classes
are considered for this problem: vehicles (which includes any wheeled motor object such as cars or motorbikes),
pedestrians and cyclists. Figure 2a shows an example of the labeled data provided, which are tightly fitting bounding
boxes around the objects. Furthermore, Waymo provides two different difficulty levels for the labels (Level 1 and 2),
which are illustrated in Figure 2b. Level 2 instances are objects considered as hard and the criteria depends on both
the human labelers and the object statistics. For the evaluation, the level 2 metrics are cumulative and also include all
objects belonging to level 1. The count of objects of the different classes is presented in Table 1. As can be seen, there
is a significant class imbalance between vehicles and pedestrians, and the number of cyclist labels is minimal.

Table 1: Count of labeled objects in the Waymo dataset
Vehicle Pedestrian Cyclist
Count 7.7M 2.1M 63K
Percentage 78.07% 21.29% 0.64%

The dataset is divided into 1000 scenes for training and validation (around 1 million images), and 150 for testing
(around 150k images). Waymo provides an online submission tool to evaluate the models over the testing set, since
those labels are not publicly available. The scenes composing the test set are from a different geographical area, which
ensures that the capacity of generalization of trained models is properly evaluated.

3.2. Faster R-CNN architecture
Faster R-CNN has been extensively used in the recent literature as a general-purpose object detection framework
[17]. This detector follows a multi-task learning procedure, combining classification and bounding box regression to
solve the detection problem. It uses a convolutional backbone (e.g. VGG, ResNet) to extract hierarchical features
from the images, and consists of two stages: a region proposal network (RPN) and a Fast R-CNN header network.
Figure 3 shows the Faster R-CNN architecture, illustrating the complete two-stage process.
In the first stage, the RPN uses features from an intermediate level of the feature extractor to predict class-agnostic
box proposals (object or background). This is achieved by predicting multiple candidate boxes at each location
using multi-scale reference anchors. Afterwards, a limited number of these proposals (typically 300) are selected
as regions of interest (ROIs) and pass to the second stage. The selected ROIs are used to crop features from the
same intermediate feature map using a ROI pooling operation. Those cropped features are then fed to the remaining
layers of the backbone network to predict a class and perform a box refinement for each proposal. In Faster R-CNN,
convolutional features are shared between both stages, which improves accuracy and speed. However, its bottleneck
is the number of ROIs proposed by the RPN, since the computation of the second stage is run once per each proposal.

In this study, the ResNet-101 backbone network is used, since it provides a good speed/accuracy trade-off [53]. It is
also the network provided for the baseline results published with the Waymo dataset, which allows a fair comparison.
As in the original implementation [32], features used in the RPN are extracted from block 3 of the ResNet. In the
second stage, ROIs are cropped and resized to 14x14, and then max-pooled to 7x7 before being fed to block 4.
However, our proposal does not rely on this specific backbone and can be used with other existing anchor-based
two-stage detectors.

Despite its advantages, there are several aspects of Faster R-CNN that can be improved to better adapt it to the
characteristics of the problem addressed in this study, which is object detection in the autonomous driving scenario.
The improvements proposed to the original architecture are highlighted in red in Figure 3: the per-region anchor
generation optimization in the RPN; and the ROIs spatial features concatenation in the header classification network.
The details of these modifications are provided in the following sections.

3.3. Anchor generation optimization
The first stage of the Faster R-CNN is the region proposal network (RPN) that selects the ROIs to be forwarded
to the detection stage. The ROIs are generated using a convolutional sliding window over some intermediate feature
map of the backbone network. These proposals are parametrized relative to reference boxes known as anchors. In
order to detect different sized objects, the RPN predicts multiple region proposals at each location by using multi-scale
anchors. There are k anchor boxes with different scales and aspect ratios centered at each pixel of the feature map.
The scale ratio is defined with respect to a base of 256, and the aspect ratio is the width over the height of the box.

The size and shape of these anchors have to be manually defined and is critical for the success of the detector [54].
In this self-driving scenario, the shape of objects captured by the cameras can be significantly different depending
on their class and position in the image. The shape of pedestrians tends to be tall and narrow, while vehicles are often
wider and more squared. Furthermore, the perspective projection of the cameras equipped in autonomous vehicles
is an important factor that must be considered for object detection [46]. The original RPN implementation in Faster
R-CNN using ResNet proposes multiple anchors with different scales ratios (0.25, 0.5, 1, 2) and aspect ratios (0.5, 1, 2)
at each location [32]. This uniform configuration was found to work well for general-purpose object detection, but
it is far from optimal in this particular application. Those pre-defined scales and aspect ratios do not coincide with
the size of the objects seen from on-board cameras, hence resulting in many invalid anchors and useless computation.
Therefore, in this study, the aim is to find a better configuration for those values of scale and aspect ratio.
Due to the perspective of the cameras in the vehicle, the size of the captured objects highly depends on their
position in the image. Therefore, one of the first steps of this study is to analyze the relationship between bounding
box dimensions and their location in the image. Figure 4 displays the distribution of all objects in the dataset with
respect to two variables: the vertical position of the center of the object (y-axis center), and the object’s height. Due to
the different dimensions and nature of frontal and lateral cameras, the analysis is separated for both of them to check
for any significant particularities. As can be seen in the figure, there is a strong correlation between both variables. For
frontal cameras, there is a 0.67 Pearson correlation coefficient, while for lateral cameras the correlation is 0.69. This
positive correlation implies that objects of larger size tend to appear at the bottom part of the image, while smaller
objects are more often at the top part of the image, as they are further away.

These findings confirm the fact that a uniform anchor generation across the image is not optimal for this context.
This anchor dimension mismatch can significantly decrease the performance of the detector. The next steps of the
paper focus on how the anchor generation process has been modified to adapt it for this specific problem and improve
the detection accuracy. Our perspective-aware proposal is divided into two steps: the division of the images in key
regions using a clustering analysis, and the per-region anchor optimization using an evolutionary algorithm.
Figure 4: Correlation between the object size and its location in the image. The (0,0) point refers to the top left corner of the image. The regression
line illustrates the strong positive correlation.

3.3.1. Region division using clustering
Given the different characteristics of objects depending on their location in the image, the objective is to find a
better anchor generation methodology that accounts for the perspective projection. In contrast to the default uniform
generation method, the proposal is to divide the image into several key regions and obtain the best configuration for
each of them independently. In order to find the optimal division in regions, a clustering analysis is performed with
respect to the aspect and scale ratio of all 10 million objects in the dataset. When the K-Means algorithm is applied,
the best division is obtained with two clusters after analyzing internal validity indices such as the Silhouette index.
Figure 5 shows the distribution of elements in the cluster according to the values of both features. As can be seen,
while the aspect ratio is similar for the elements in both clusters, there is a significant difference in the scale ratio.
The distribution plot shows that the K-Means clustering algorithm assigns to cluster 1 the majority of the larger scale
elements (those that have a scale ratio greater than 1), and to cluster 0 the smaller scale objects (those that have a scale
ratio below 1).

With the clustering results, the region division can be obtained by analyzing the position in the image of the
objects belonging to each cluster, which is illustrated in Figure 6a. This figure plots the center of objects in both x and
y-axis (horizontal and vertical position). Frontal and lateral cameras are combined for this clustering study, hence a
normalized value is used for the vertical position of the objects. As can be seen in the figure, the majority of elements
of cluster 1 (larger objects) are in the bottom part of the image. In contrast, elements in cluster 0 are spread across
the middle and upper part of the image. The spatial bounds that delimit the clusters can be found with the help of
the density distribution of the position of elements. For each cluster, we define the interval delimited by two values
α and β that contains 99% of the elements, in order to allow for the presence of outliers. Those two values define the
interval in which the majority of elements of each cluster are positioned in the image. Figure 6a displays the α and β
values with dotted red lines. For cluster 0, the bounds are at positions 0.188 and 0.691. For cluster 1, only the first
bound (0.392) is displayed since the elements spread until the bottom of the image. If those bounds are combined, we
can establish four key regions in the image that will have objects with significantly different characteristics. The final
result of the region division study is depicted in Figure 6b, in which some example images are shown with the bounds
for the four regions (R1, R2, R3, and R4). These images clearly illustrate the difference in scale between objects of
different regions.

3.3.2. Evolutionary algorithm to optimize anchors per region
Once the region division has been defined, an evolutionary algorithm (EA) is designed to find the optimal values
for scale and aspect ratios for each of them. An evolutionary algorithm minimizes a fitness function by exploring a
population of possible solutions over a specific number of generations. The population is formed by individuals that
are represented as a chromosome, which are a combination of genes. For this problem, the chromosome is encoded as
a set of 7 floating-point numbers representing the parameters that define an anchor. The first three numbers correspond
to the aspect ratios and the remaining four correspond to the scale ratios. The objective is to search for the best value
of each gene within defined boundaries and with a specified decimal precision. The EA creates a random initial
population of a specific size. From the initial population, the algorithm combines the best individuals using single-
point crossover and creates a new generation. The crossover is applied separately to the aspect ratio and scale ratio
genes, so that there is no interference between the two parameters. Additionally, a low mutation probability is added
to maintain genetic diversity over generations. The complete parameter configuration of the proposed EA is presented
in Table 2. The gene boundaries are defined considering the size of images and the limitations of using ResNet-101 as
a backbone network. Given the base anchor scale of 256, the specified boundaries imply that the maximum possible
scale is 1024 pixels and the minimum is 16 pixels (which is the receptive field unit of the network).

Table 2: Parameter configuration of the evolutionary algorithm
Parameter Value
Gene boundaries [0.06, 4]
Gene precision 10−3
Crossover probability 0.8
Mutation probability 0.2
Population size 100
Num. Generations 50
An individual can be represented as X = (A, S ), where A = (a1, a2, a3) defines the three possible aspect ratios
and S = (s1, s2, s3, s4) defines the four possible scale ratios. The decoded individual defines a set of 12 anchor
configurations Bai j , which are conformed by the cartesian product between aspect and scale ratio (Bai j = A ⊗ S ).
Therefore, the whole decoding process of an individual X can be expressed as follows:
X = {Bai j}, where Bai j = (ai
, sj) for i ∈ {1, .., 3}, j ∈ {1, .., 4} (1)
The goal of the proposed EA is to maximize the intersection between the anchors generated from the decoded
individual and the ground truth boxes in the images. This is measured using the Intersection over Union (IoU) metric,
which is presented in Equation 2. The IoU is defined as the ratio of area-of-overlap to area-of-union of a ground truth
bounding box Bgt and a proposed base anchor Ba:
IoU(Bgt, Ba) =
area(Bgt ∩ Ba)
area(Bgt ∪ Ba)
=
area(Bgt ∩ Ba)
area(Bgt) + area(Ba) − area(Bgt ∩ Ba)
(2)
The IoU metric is used for defining the EA fitness function (Eq. 3), which evaluates the quality of the solutions
provided by individuals in the population. For an individual X, the decoded chromosome generates the 12 possible
anchors (4 scales and 3 aspect ratios). For each ground truth bounding box, the fitness function finds the maximum
overlap obtained with the proposed anchor boxes and averages the result among all objects. A logarithmic factor is
applied in order to ensure that there are less ground truth boxes with a maximum IoU lower than 0.5 [55]. In the
equation, K refers to the number of ground truth objects.
Fitness(X) =
1
K
X
K
k=1

−

1 − maxIoU(Bgtk
, X)
2
∗ log 
maxIoU(Bgtk
, X)


maxIoU(Bgtk
, X) = max
i=1..3
j=1..4

IoU(Bgtk
, Bai j)

(3)
Table 3 presents the optimized parameters that are obtained for each region. As can be seen, the optimal values
found by the evolutionary algorithm are significantly different from the original configuration. Regions at the top of
the image with smaller objects have lower scale ratios. The scale in R1 and R2 ranges from values close to zero and
up to a maximum of 0.5, which means that default anchors of scale 1 and 2 are not suitable. In contrast, R4 accounts
for the presence of larger objects with values ranging from 0.6 until 2.9. Figure 7 presents an example that shows the
difference between the uniform anchor generation (red boxes) and our optimized proposal (blue boxes). The dotted
red boxes illustrate useless default anchors that have a great size mismatch with objects in different regions. In regions
with small objects, the original strategy generates useless large-scale anchors. Analogously, in the bottom part of the
image where there are objects closer to the camera, it generates very small inefficient anchors. Our proposal generates
anchors with a higher matching precision, which results in a more effective detector. In the experimental study, the
parameter optimization process is also analyzed separating frontal and lateral cameras, in order to check if there is a
further improvement.

Table 3: Optimized anchor configuration found with the evolutionary algorithm. The values for scale and aspect ratios for each region are provided.
Parameter Region Values
Scale Ratio
Original 0.25, 0.5, 1, 2
R1 0.074, 0.158, 0.250, 0.414
R2 0.082, 0.155, 0.254, 0.500
R3 0.095, 0.189, 0.518, 1.557
R4 0.598, 1.101, 1.800, 2.852
Aspect ratio
Original 0.5, 1, 2
R1 0.344, 0.672, 1.801
R2 0.461, 0.853, 2.246
R3 0.473, 0.905, 2.497
R4 0.314, 0.805, 2.136

3.4. ROIs spatial features concatenation
As it was seen in the previous Section 3.3, the spatial location of objects in this context plays an important role
in the detection problem. Considering this fact, we propose a slight yet effective modification to the second stage of
the Faster R-CNN framework. The information used by the second stage only comes from the convolutional features
cropped from an intermediate feature map of the backbone network, which are then max-pooled to a 7 × 7 × 1024
map. This implies that the spatial characteristics of each box proposal are lost in the ROI pooling process. The size
(width and height) and position of the proposed bounding box with respect to the complete image are not taken into
account by the Fast-RCNN header network. In this multi-class object detection problem with images from on-board
cameras of a vehicle, the position of the box has a significant correlation with its dimensions. Therefore, including this
information in the class-specific prediction and box refinement done in the second stage can enhance the localization
accuracy.

For these reasons, our proposal is to construct those spatial features and concatenate them to the convolutional
features of each ROI obtained from the cropped map. This process is illustrated in the flowchart displayed in Figure 8,
and in Figure 3 with more detail. For each of the N selected ROIs, cropped features are fed to the fourth block of the
ResNet backbone. Then, the network is divided into two branches for different tasks: classification and bounding-box
regression. In each branch, the convolutional features are flattened using a spatial average pooling, which converts the
N × 7 × 7 × 2048 maps into N × 2048 neurons. At this point, four features are concatenated for each ROI proposal in
both branches: the width of the box, the height of the box, the horizontal position of the center of the box (X center),
and the vertical position of the center of the box (Y center). This results in a layer of N × 2052 neurons. Those
combined features are then used to predict the class and refine the boxes by means of a fully connected (FC) layer.


3.5. Learning strategies to address class imbalance
Class imbalance is an important issue that may severely degrade the performance of detectors if it is not properly
addressed [56]. In object detection, there are two different class imbalance problems: background-foreground and
foreground-foreground. The background-foreground imbalance is associated with the small number of positive ex-
amples (bounding boxes matching an object) compared to the number of negatives boxes (background of the image).

The foreground-foreground problem refers to the imbalance between object classes of a dataset, which often leads to
overfitting on the over-represented class. Since the foreground-background imbalance is unavoidable and does not de-
pend on the specific dataset, it has attracted more interest in the recent literature. However, in the self-driving dataset
used in this study, there is a significant imbalance between vehicles (80%) and the other type of objects (pedestrians
20% and cyclists less than 1%).

In order to alleviate the foreground-background imbalance, Faster R-CNN uses hard sampling techniques based
on heuristic methods. In the first stage, random sampling is used for training the RPN. To avoid a bias in the learning
towards negative samples, 128 positive and 128 negative examples are randomly selected to contribute to the loss
function. In the second stage, the employed strategy is to limit the search space. For the Fast R-CNN detection
network, only the best N ROIs are selected according to their objectness scores, while maintaining a 1:3 positive-
negative ratio. However, this methodology presents the problem that all examples are equally weighted once they are
sampled. The original Faster R-CNN implementation does not take into account the presence of under-represented
objects, which limits performance under high imbalance. Therefore, we aim to design a better training procedure that
addresses the foreground-foreground imbalance in this scenario.

Our proposal is to study how the loss function of two-stage detectors can be modified using cost-sensitive re-
weighting techniques, which has been one of the main approaches in the literature for class imbalance problems [57].

These techniques are based on assigning relatively higher costs to minority instances, hence building a better class-
balanced loss. In this work, we explore two re-weighting alternatives that can improve overall detection accuracy:
balance the loss function with weights that are proportional to the class distribution; and the use of focal loss, which
has been traditionally used for one-stage detectors.

3.5.1. Weight assignment based on class distribution
The first approach is to assign different weights to instances of each class depending on the class frequency
distribution. This simple yet effective method has been widely used in many computer vision tasks [58]. As stated
before, in Faster R-CNN, the training is framed as a multi-task learning problem that combines classification and
bounding box regression. We propose to modify the loss function by adding a weight wi parameter to the classification
and regression terms. The complete loss function with weights assignment is expressed in Equation 4:

where pi
is the predicted probability of proposal i being an object, and pi∗ is the groundtruth label (0 or 1). ti
are the four predicted box coordinates, and ti∗ are the ground truth coordinates. wi
is the weight assigned depending on the ground truth class. Ncls and Nreg are normalization terms which are set to the RPN mini-batch size, which is
typically 256. Lcls is the binary cross-entropy function and Lreg is the smooth L1 loss function.

Note that we have described only the RPN loss function for simplicity, but the modification is done in both
stages. The loss function in the second stage is the same, except that in the RPN the classification problem is binary
(background vs object) while in the Fast R-CNN header network the classification is multi-class. This implies that
the multi-class cross-entropy function is used. In this case, the normalization parameters are set to the number of ROI
proposals that pass to the second stage.

In order to obtain the best possible performance, a grid search is performed to find the optimal weight value
for each class. The search involves experimenting with different sets of weights, considering four possible values
(0.3, 0.5, 0.7, 0.9) that can be assigned to vehicles and pedestrians. The maximum weight (1.0) is kept for cyclists
since they are extremely underrepresented.

3.5.2. Reduced Focal Loss
The second re-weighting alternative that is explored is focal loss, which was introduced in [26] as an improvement
to the RetinaNet one-stage detector. The focal loss function belongs to another line of work that assigns weights
according to sample difficulty. These methods assume that training a detector with hard examples improves perfor-
mance. A method of this family that has been used in two-stage detectors is Online Hard Example Mining (OHEM)
[59]. However, OHEM requires more memory consumption and increases training time. Although focal loss was
found to be more effective than OHEM for imbalance problems, it has not been used extensively in two-stage detec-
tors. In this work, we study the application of the focal loss function to the Faster R-CNN framework and propose a
modification to better adjust it to its characteristics.
Focal loss (FL) assigns higher weights to hard examples, with the aim of alleviating the high background-
foreground imbalance. As it shown in Equation 5, focal loss modifies the standard cross-entropy equation by adding
a factor (1 − pi)
γ
. When γ > 0, the relative loss for easy and well-classified samples is reduced, putting the effort on
the classification of hard examples.

Although this function was introduced to reduce the influence of easy background examples, it also has an effect on
the foreground-foreground imbalance. Instances from minority classes often have higher losses since they are rare and
their features are usually poorer. However, the direct application of focal loss in two-stage detectors presents several
problems. Firstly, focal loss can have as a side-effect that the learning is biased towards noisy or mislabeled data,
which is also hard to classify [57]. Furthermore, focal loss contradicts slightly the behaviour of two-stage detectors:

RPN aims to maximize recall (allowing false positives), while the job of Fast R-CNN header network is to classify
proposals correctly. An extreme focus on hard samples can reduce the recall of RPN, which implies that lower-quality
proposals pass to the second stage. Therefore, inspired by the work in [60], we propose a modified version called
reduced focal loss (RFL).

Reduced focal loss aims to perform hard example mining but softening the effect of difficult samples. This is
achieved by applying the factor only to instances with losses that are above a certain threshold. The loss of samples
that are below the threshold remains unaltered, which means that is the same as the original cross-entropy loss. This
approach is formulated in Equation 6. RFL is applied in the classification term of the loss function in both stages of
the Faster R-CNN detector.

Following [60], the thresholds are fixed to 0.5 and 0.25 for the RPN and Fast R-CNN respectively. RFL is more
suitable than the original focal loss for two-stage detectors, and can significantly improve the performance over rare
and difficult instances. Another important advantage that is obtained when using focal loss here is that all anchors can
be considered in the RPN loss function. The sampling process in the original RPN discards many anchor boxes that
can be useful for the training process, especially those hard negatives that are close to an object.

3.6. Ensemble model
Ensemble models can be key to further improve the robustness of detection systems. However, ensembling object
detectors is not straightforward due to the specific particularities of this problem: multiple classes with different
shapes, overlapping bounding boxes, etc. [61]. In this work, we propose to build an ensemble that combines the
output of models from the different learning strategies presented in the previous Section 3.5. The ensemble model
is based on Non-Maximum Suppression (NMS) [62], and uses the affirmative ensembling strategy proposed in [63].

With this strategy, when one of the methods proposes the presence of an object in a region, such a detection is
considered as valid. Later, the NMS algorithm is applied to merge detections by removing redundant overlapping
boxes. NMS selects proposals in descending order of confidence scores, and discards boxes that have an IoU overlap
with already selected boxes greater than a pre-defined threshold. Our proposal is to merge the output of three models
with different training schemes: original Faster R-CNN training, re-weighting proportional to class distribution, and
reduced focal loss re-weighting. With this approach, the aim is to enhance detection accuracy without a significant
increase in computation. If the predictions from the single models are obtained in parallel with different devices,
the overhead introduced by the NMS algorithm is minimal. The only parameter that has to be tuned for the NMS
ensemble is the IoU threshold. We explored values ranging from 0.5 and 0.9, and found consistent and similar results
on values between 0.6 and 0.8. Therefore, the IoU threshold was fixed to the intermediate value 0.7, which is also the
same value used internally in the ROI selection process of Faster R-CNN.

Furthermore, Test-Time Augmentation (TTA) is also explored in the experiments as another ensemble technique.
TTA is to create random modifications of the test images, obtaining predictions with a model for each of them, and then
ensemble the results. The only augmentation that is exploited is scale augmentation, with the objective of improving
the detection of small objects. The test images are resized using the factors 0.8, 1, and 1.2 with respect to the original
image scale. This is done for each of the three considered models, and detections are merged as explained above.

3.7. Other implementation details
For the implementation, the popular TensorFlow Object Detection API as been used [64]. Except for the proposed
modifications, the original Faster-RCNN implementation is followed in terms of parameter choice. The architecture
is trained end-to-end, which means that RPN and header networks are jointly trained. The original resolution of the
images is maintained for frontal (1920×1280) and lateral (1920×886) cameras. The COCO pre-trained Faster R-CNN
model available in the TensorFlow repository is used for initializing the network weights. Transfer learning is used
since it is a common practice in the object detection field to avoid excessive training times [1]. For each experiment,
the models are fine-tuned for 500k iterations, using the SGD optimizer with learning momentum 0.9. The initial
learning rate is set to 0.001, and decrease by 10x after 200k and 400k steps. For training the models, a batch size of 1
is used, which was the maximum allowed by the GPU memory given that the images have very high resolution. The
ROI proposals mini-batch size is increased to 256 during training in order to accelerate convergence [21]. At test time,
the original value of 300 proposals is kept. The only data augmentation technique used in single models is random
horizontal flip.
