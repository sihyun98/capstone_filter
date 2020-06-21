
import os
import glob
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import time
import threading

import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image


# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

def get_num_classes(pbtxt_fname):
    from object_detection.utils import label_map_util
    label_map = label_map_util.load_labelmap(pbtxt_fname)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=200, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    #print(len(category_index.keys()))
    return len(category_index.keys())

# test_record_fname = '/Users/yangsuyeong/Desktop/WebCapstone/webproject/object_detection_capstone/data/annotations/test.record'
# train_record_fname = '/Users/yangsuyeong/Desktop/WebCapstone/webproject/object_detection_capstone/data/annotations/train.record'
# label_map_pbtxt_fname = '/Users/yangsuyeong/Desktop/WebCapstone/webproject/object_detection_capstone/data/annotations/label_map.pbtxt'
# coco_label_map_fname  = '/Users/yangsuyeong/Desktop/WebCapstone/webproject/object_detection_capstone/data/annotations/mscoco_label_map.pbtxt'

base_path = '/home/sihyun/바탕화면/Demo/copy/object_detection_capstone/'
test_record_fname = base_path + 'data/annotations/test.record'
train_record_fname = base_path + 'data/annotations/train.record'
label_map_pbtxt_fname = base_path + 'data/annotations/label_map.pbtxt'
coco_label_map_fname  = base_path + 'data/annotations/mscoco_label_map.pbtxt'

num_classes = get_num_classes(label_map_pbtxt_fname)
coco_num_classes = get_num_classes(coco_label_map_fname)

import os
import glob

# Path to frozen detection graph. This is the actual model that is used for the object detection.

# pb_fname = '/Users/yangsuyeong/Desktop/WebCapstone/webproject/object_detection_capstone/frozen_inference_graph_12000_ssdlite.pb'
# pb_fname2 = '/Users/yangsuyeong/Desktop/WebCapstone/webproject/object_detection_capstone/frozen_inference_graph_coco.pb'

pb_fname = base_path + 'frozen_inference_graph_12000_ssdlite.pb'
pb_fname2 = base_path + 'frozen_inference_graph_coco.pb'

CKPT_list = []

PATH_TO_CKPT = pb_fname
PATH_TO_CKPT2 = pb_fname2

CKPT_list.append(PATH_TO_CKPT)
CKPT_list.append(PATH_TO_CKPT2)

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = label_map_pbtxt_fname
COCO_PATH_TO_LABELS = coco_label_map_fname

# If you want to test the code with your images, just add images files to the PATH_TO_TEST_IMAGES_DIR.
#PATH_TO_TEST_IMAGES_DIR =  os.path.join("./", "test")

assert os.path.isfile(pb_fname)
assert os.path.isfile(PATH_TO_LABELS)
#TEST_IMAGE_PATHS = glob.glob(os.path.join(PATH_TO_TEST_IMAGES_DIR, "*.*"))
#assert len(TEST_IMAGE_PATHS) > 0, 'No image found in `{}`.'.format(PATH_TO_TEST_IMAGES_DIR)





# This is needed to display the images.
#%matplotlib inline


from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util

detection_graph_list = []
#start = time.time()
for i in range(len(CKPT_list)):
  detection_graph = tf.Graph()
  with detection_graph.as_default():
      od_graph_def = tf.compat.v1.GraphDef()
      with tf.gfile.GFile(CKPT_list[i], 'rb') as fid:
          serialized_graph = fid.read()
          od_graph_def.ParseFromString(serialized_graph)
          tf.import_graph_def(od_graph_def, name='')
  detection_graph_list.append(detection_graph)

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
coco_label_map =  label_map_util.load_labelmap(COCO_PATH_TO_LABELS)

categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=num_classes, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

coco_categories = label_map_util.convert_label_map_to_categories(
    coco_label_map, max_num_classes=coco_num_classes, use_display_name=True)
coco_category_index = label_map_util.create_category_index(coco_categories)

def load_image_into_numpy_array(image):
    image = image.resize((int(image.size[0]*(1/5)),int(image.size[1]*(1/5))))
    (im_width, im_height) = image.size
    #print(image.size)
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

# Size, in inches, of the output images.
#IMAGE_SIZE = (12, 8)

def run_inference_for_images(images, graph):
    with graph.as_default():
        with tf.Session() as sess:
            output_dict_array = []

            for image in images:
                # Get handles to input and output tensors
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                            tensor_name)
                if 'detection_masks' in tensor_dict:
                    detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                    # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                    real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image.shape[0], image.shape[1])
                    detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    # Follow the convention by adding back the batch dimension
                    tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                # Run inference
                output_dict = sess.run(tensor_dict,
                                       feed_dict={image_tensor: np.expand_dims(image, 0)})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]

                output_dict_array.append(output_dict)

    return output_dict_array

def trained_model(images):
    result = []
    output_dict_array = run_inference_for_images(images,detection_graph_list[0])
    for idx in range(len(output_dict_array)):
        output_dict = output_dict_array[idx]

        boxes = output_dict['detection_boxes']
        max_boxes_to_draw = boxes.shape[0]
        classes = output_dict['detection_classes']
        scores = output_dict['detection_scores']

        objects = []
        min_score_thresh = 0.5 # in order to get higher percentages you need to lower this number; usually at 0.01 you get 100% predicted objects

        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh :
                if classes[i] in category_index.keys():
                    class_name = category_index[classes[i]]['name']
                    result.append(class_name)
    return result
               
def running_coco(images):
    result = []
    output_dict_array = run_inference_for_images(images,detection_graph_list[1])
    for idx in range(len(output_dict_array)):
        output_dict = output_dict_array[idx]

        boxes = output_dict['detection_boxes']
        max_boxes_to_draw = boxes.shape[0]
        classes = output_dict['detection_classes']
        scores = output_dict['detection_scores']

        objects = []
        min_score_thresh = 0.5 # in order to get higher percentages you need to lower this number; usually at 0.01 you get 100% predicted objects

        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh :
                if classes[i] in coco_category_index.keys():
                    class_name = coco_category_index[classes[i]]['name']
                    result.append(class_name)
    return result

def detect_func(TEST_IMAGES):
    images = []
    for image in TEST_IMAGES:
        
        #image = Image.open(image_path)
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        images.append(image_np)
        #print(image)
    # Actual detection.

    # output_dict_array = []

    res = trained_model(images)
    res1 = running_coco(images)
        #  plt.figure(figsize=IMAGE_SIZE)
        #  plt.imshow(image_np)
    #print("time :", time.time() - start)
    return list(set(res+res1))


