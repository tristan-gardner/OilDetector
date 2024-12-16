# OilDetector

# OilDetector

This repo stores the code needed to train a model to detect oil on top of running water.  It also has example ground truth data.

## Sections

### Oil Detection Training

This is where the actual training occurs each data folder (train, val, and test) should have 2 empty folders named 'oil' and 'no_oil'.  This is the pattern for data seperation that the yolo model accepts.

oil_labeling.ipynb does the actual training, once data is loaded into the three categories noted above, run all the cells in this notebook.  It will train a model, then test it to see if it is accurate with unseen images.

### Pics

When raw videos are cut into images (see Raw Videos and cut_video), they are stored in this section.  Images need to be seperated into oil and no_oil categories

### Raw Videos

This is the ground truth - video of water with and without oil on it are stored here.  GT was taken as videos initially b/c its easier to capture that way.

### Yolo Proof
This section is inteded to show that the yolo model works better than a first principals approach.  It uses a standard data set (fashion mnist) to create a categorization model.  The final results end up slightly better than the model presented in class.

fashion_labeling.ipynb has the code to set up and fill the data folder and do the actual training.  Because the data set is so massive, the data itself will not and should not be pushed to github.

### Cut Video
Helper file to take GT videos and cut them into separate images

### Image Resize
Helper file which resizes all GT images, randomly shuffles them, then inserts 80% into training, 10% into test, and 10% into validation folders (this is what gets used to rain the yolo model)

## How to Use

1. (Optional) Recut the videos into images
    - If you want more GT data, or have added videos, recut the videos 
    - Alter the call at the bottom of cut_video.py if you want to adjust the frame rate
    - `python cut_video.py`
2. Resize the images
    - choose a image width and height
    - enter that into the call at the bottom of the image_resize.py
    - `python image_resize.py`
3. Check that the images have been populated
    - oil_detection_training/data/*/oil and oil_detection_training/data/*/no_oil should have images
4. Train the model
    - run all cell in the oil_labeling.ipynb notebook
