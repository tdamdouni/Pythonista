# https://gist.github.com/harvitronix/ffb20345e873c93dfade72feccbba3d6

def get_labels():
    """Get a list of labels so we can see if it's an ad or not."""
    with open('../inception/retrained_labels.txt', 'r') as fin:
        labels = [line.rstrip('\n') for line in fin]
    return labels

def run_classification(labels):
    """Stream images off the camera and process them."""

    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 2
    rawCapture = PiRGBArray(camera, size=(320, 240))

    # Warmup...
    time.sleep(2)
    
    # Unpersists graph from file
    with tf.gfile.FastGFile("../inception/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        for i, image in enumerate(
                camera.capture_continuous(
                    rawCapture, format='bgr', use_video_port=True
                )
            ):
            # Get the numpy version of the image.
            decoded_image = image.array

            # Make the prediction. Big thanks to this SO answer:
            # http://stackoverflow.com/questions/34484148/feeding-image-data-in-tensorflow-for-transfer-learning
            predictions = sess.run(softmax_tensor, {'DecodeJpeg:0': decoded_image})
            prediction = predictions[0]

            # Get the highest confidence category.
            prediction = prediction.tolist()
            max_value = max(prediction)
            max_index = prediction.index(max_value)
            predicted_label = labels[max_index]

            print("%s (%.2f%%)" % (predicted_label, max_value * 100))

            # Reset the buffer so we're ready for the next one.
            rawCapture.truncate(0)
