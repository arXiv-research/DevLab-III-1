Recent progress in the object detection field has been driven by novel methodologies based on deep learning, as
it has happened in many computer vision tasks [16]. Existing image object detectors in the literature can be mainly
divided into two categories: two-stage detectors such as Faster R-CNN [17], and one-stage detectors such as SSD
[18]. Generally speaking, the strength of one-stage detectors lies in their higher inference speed, while two-stage
architectures obtain higher localization accuracy.

The pioneering two-stage detector was the Regions with CNN features framework (R-CNN) [19]. R-CNN used
the selective search method to crop box proposals from the image and feed them to a convolutional network classifier.
This external proposal generation was very costly and inefficient. Faster R-CNN solved this issue by sharing features
between the region proposal network (RPN) and the detection network [17]. This approach improved accuracy and
speed and has led to a large number of follow-up works. For instance, R-FCN proposed a position-sensitive ROI
cropping that respects translation variance [20]. Later studies have focused on exploiting the multi-scale properties of
feature extractors, such as the feature pyramid networks (FPNs) with lateral connections proposed in [21]. Other works
have tried to improve this detector by including rotation-invariant and Fisher discriminative regularizers on the CNN
features. [22] Due to the cost of manually labeling bounding boxes, there are also many studies on weakly-supervised
object detection that work only with image-level labels [23]. Currently, the COCO leaderboard is led by Cascade
R-CNN methods. Cascade models build a sequence of detectors trained with increasing intersection-over-union (IoU)
thresholds, to be sequentially more selective against false positives [24].

In contrast, one-stage architectures predict class probabilities and bounding box offsets directly from the image,
without the region proposal step. The first YOLO (You Only Look Once) architecture was proposed in [25], achieving
real-time inference rates but with high localization errors. SSD combined ideas from YOLO and RPN to improve
the performance while maintaining high speed [18]. With the help of default bounding boxes, SSD detects objects
at different scales on several feature maps. More recently, an important step forward in the one-stage family was
achieved by solving the foreground-background class imbalance problem. RetinaNet proposed a novel focal loss
function that focuses on difficult objects by down-weighting the importance of well-classified samples [26]. Another
interesting approach are the anchor-free one-stage detectors, that do not require pre-defined anchor boxes. FCOS [27]
and CenterNet [28] use the center of objects to define positives and regress the four distances that build the bounding
box from that point. Other models such as ExtremeNet [29] or CornerNet [30] generate the boxes by locating several
keypoints first. Anchor-free detectors are more flexible than RetinaNet and can achieve similar performance.

The backbone network that acts as a feature extractor and its capacity to extract quality features play a very im-
portant role in all detection frameworks. Rather than the VGG network [31] used in the original Faster R-CNN paper,
deeper and more densely connected architectures have been recently proposed. Some examples include the ResNet
[32] used in the Mask R-CNN detector [33], ResNeXt [34], Res2Net [35] or HRNet [36]. The improved YOLOv3
detector includes multi-scale predictions and a new feature extractor, DarkNet-53, which uses residual blocks and skip
connections [37]. Other works such as NAS-FPN [38] introduce neural architecture search to learn optimal feature fu-
sion in the pyramid and build a stronger backbone. However, these complex networks lead to slower inference speed.
Since this is undesired in real-time applications, other researchers have focused on designing lightweight backbones
such as MobileNets [39], which are also less accurate. In general, finding the optimal speed/accuracy balance in a
backbone architecture is a difficult task that highly depends on the problem to be addressed [40].

The interest in the autonomous driving field has risen significantly in recent years. Many high-quality datasets
are becoming available for the research community to push the state-of-the-art in problems such as object detection.
After the popular KITTI benchmark [15], other datasets have been released such as NuScenes [41] or PandaSet [42].

A complete overview of existing self-driving datasets is provided in [43]. Waymo has recently released the most
extensive and diverse multi-modal dataset up to date [14]. In [44], the authors evaluate the trade-off between accuracy
and speed of several state-of-the-art detectors over the Waymo dataset. However, there are still few works that have
addressed the optimization of existing 2D object detectors in the context of autonomous vehicles. RefineNet proposed
extra regressors to further refine the candidate bounding boxes for vehicle detection [45]. The work in [46] presents an
anchor optimization methodology and ROI assignment improvement over two-stage detectors but also focusing only
on vehicles and not on other traffic participants. A CNN-based methodology to improve vehicle detection in adverse
weather conditions was presented in [47]. There are other important perception problems in autonomous driving being
addressed with deep learning such as 3D detection using LiDAR point clouds [48, 49] and object tracking [50, 51].
