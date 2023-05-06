## Managers

Every core functionality was separated into its own manager:
- Config - loading and storing of user config
- NN Rot - loading of the neural network and image predictions
- Data - processing and managing of the cutouts
- Hash - duplicity detection, relationship management

### Config manager
Config is stored in config.json file. All components are can be set in settings (config controller). Some settings also produce signals for drop controller (nn loading, output folder). Language settings is also used for parsing the "dictionary" jsons. Loading static texts in app is done with use of "tr" object. These texts are set during app start, so change of this setting needs app restart.

### NN Rot manager
Neural network in our project is used only for image rotation prediction. We are using our model, which was build using part of the COCO dataset (2017) that was also cleared from improper images. During the research we tried EffNetV2B1, EffNetV2B2, VGG, ResNet50, but the most promised came from EffNetV2B2. Most of the computations was done with the help of Paperspace - Gradient's services. The final resolution was set at 128x128 which is not ideal (minim. res. of B2), however we couldn't fit bigger images into Gradient or Google Colab free tier's RAM and storage. Final model has around 85% accuracy (potential for improvement). One of the additional improvements was done with use of four predictions (every rotation) for every image. NN loading is asynchronous.

Sources:
- https://lmb.informatik.uni-freiburg.de/Publications/2015/FDB15/image_orientation.pdf
- https://arxiv.org/pdf/1803.07728.pdf
- https://www.cs.toronto.edu/~guerzhoy/oriviz/crv17.pdf
- https://www.sciencedirect.com/science/article/pii/S2666827021000451
- https://www.tensorflow.org/api_docs/python/tf/keras/

### Data manager
This manager is responsible for the main functionality of this app - image cutouts. Cutouts are saved after every processed input. If no cutout is found the whole input image is passed forward.
The cutting itself can be separated into 4 steps:
1. Rectangle detection

    Find at least three connected perpendicular lines in convex hull of each component. Corners are passed as result.
2. Rotation I

    Rectangular is rotated into standard orientation.
3. Cutting

    Cutting out of background. If the area spreads out of the default canvas the background is set as transparent (png) or black (jpg).
4. Rotation II

   If the NN is enabled then the predictions will also affect the final rotation.

### Hash manager
We tried multiple image duplicity detection algorithms, however the most optimal for our usage was the PHash. Its implementation ([opencv-contrib](https://docs.opencv.org/4.x/df/d4e/classcv_1_1img__hash_1_1PHash.html)) with our minor tweaks was tested on sample data and final accuracy was for our case around 99.83%. \
Every cutout is evaluated and added to the data structure (if enabled) during saving. Cutouts that are marked by user as "duplicates" are then deleted from output folder.