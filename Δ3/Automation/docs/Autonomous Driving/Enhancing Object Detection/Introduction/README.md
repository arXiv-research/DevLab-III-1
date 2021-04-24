Developing robust machine learning models that can accurately detect and classify multiple objects in an image
remains a core challenge in computer vision. Object detection has attracted the interest of many researchers due
to its application to multiple real-world problems such as autonomous driving [1, 2], robotic vision [3], security
surveillance [4], or land monitoring [5]. In recent years, the latest advancements in this field have been achieved
thanks to the development of deep convolutional networks. Deep learning has proven to be a very powerful tool for
learning abstract hierarchical representations of raw input data [6]. With the increase of availability and quality of
remote sensing data collected by different sensors (higher resolution RGB cameras, LiDAR and radar data, etc.), deep
learning models have pushed the state-of-the-art in many visual recognition tasks [7].
In particular, object detection is one of the main perception problems that the advanced driver assistance system
(ADAS) of autonomous vehicles faces. The multi-modal sensors equipped in these vehicles provide valuable data
to be used with popular deep learning-based object detectors. Nevertheless, the perception systems of self-driving
vehicles need to be accurate and robust enough to operate safely in complex scenarios such as mixed urban traffic,
adverse weather conditions, unmapped roads, or areas with unreliable connectivity [8]. Under these circumstances, it
is still hard for existing detectors to perceive all traffic participants (vehicles, pedestrians, traffic signs, etc.) accurately,
robustly, and in real-time. The impact of autonomous driving in the future promises to be important due to their
potential to improve road safety, reduce traffic, and decrease pollution [9]. However, many aspects require significant
progress before this technology can fully substitute human driving.
In this work, the aim is to enhance the 2D object detection accuracy in the images obtained from the on-board
cameras of autonomous vehicles. The goal of this detection task is to determine the presence of objects from given
categories and return the spatial location of each instance through a bounding box [10]. In recent literature, the main
trend in object detection is to develop increasingly sophisticated architectures to improve the performance over the
general-purpose COCO (Common Objects in Context) benchmark [11]. However, the effectiveness of such generic
object detectors when applied to particular applications is still far from optimal [12]. For this reason, this study
proposes several modifications to the popular Faster R-CNN detection framework to better adapt it to the specific
context of self-driving cars. The novelty of this work lies in two main aspects that are considered for improving the
performance of the original model: optimizing the anchor generation procedure and modifying the learning process
to improve accuracy over minority instances.
The uniform anchor generation procedure of Faster R-CNN is not suitable for the autonomous driving scenario.
The default configuration, which has proven to be effective for generic object detection, produces anchors with the
same scale and aspect ratios at each location of the feature map. However, due to the perspective projection of
on-board cameras in the vehicles, the scale of objects has a strong correlation with their position in the image in
this context. This implies that in regions where objects tend to be very large, producing small scale anchors is not
appropriate, and vice versa. To overcome this anchor mismatch issue, our proposal is to divide the images into several
regions and optimize each of them independently. With the help of a clustering study, key regions in the images
that have objects with significantly different dimensions are obtained. Then, a methodology based on evolutionary
algorithms is presented in order to search for optimal values of scale and aspect ratio for the prior anchors of each
region. Furthermore, we modify the second-stage header network introducing spatial properties extracted from the
region of interest (ROI) proposals of the first-stage. The spatial features of ROIs (size and position in the image) are
concatenated to the convolutional features extracted from the backbone network to improve localization accuracy.
Another important issue is that the default training scheme of Faster R-CNN results in a significant performance
drop in minority classes and difficult instances. In the literature, the learning process of detectors has been given
less attention compared to the development of architectures [13]. However, a balanced learning scheme is crucial for
this multi-class scenario due to the presence of elements, such as pedestrians or cyclists, that are less frequent than
vehicles. In this study, an extensive analysis of different approaches to address foreground-foreground class imbalance
is performed. Several alternatives are explored, such as assigning different weights according to the class distribution
and the use of focal loss, which has been traditionally used in one-stage detectors. Finally, an ensemble model based
on non-maximum suppression and test-time augmentation is designed, combining the different training strategies to
increase the robustness of the detector.
The recently released Waymo Open Dataset [14] is used for evaluating the proposal, which is the largest and most
diverse up to date in terms of geographic coverage and weather conditions. Waymo is 15 times more diverse than
other existing benchmarks such as KITTI [15]. In this dataset, the object detection task has objects from three classes
(vehicles, pedestrians, and cyclists) that are divided into two difficulty levels. To the best of our knowledge, this is
the first study that addresses anchor optimization and class imbalance in a multi-class 2D detection problem in the
context of autonomous vehicles. The proposed methodology can easily be extended to other anchor-based detection
frameworks with different backbone networks, since it does not rely on the specific implementation carried out in this
study.
In summary, the main contributions of this work can be compiled as follows:
• A novel region-based anchor optimization methodology using evolutionary algorithms for 2D object detection
for autonomous driving
• A module that enhances the second-stage header network of Faster R-CNN by including the spatial features of
ROIs produced by the region proposal network.
• A thorough study of different training procedures to address severe foreground-foreground class imbalance in
two-stage object detectors.
• An ensemble model combining the strengths of the different learning strategies to improve detection precision.
The rest of the paper is organized as follows: Section 2 presents a review of related work; in Section 3 the materials
used and the methods proposed in the study are described; Section 4 reports and discusses the results obtained; Section
5 presents the conclusions and potential future work.
