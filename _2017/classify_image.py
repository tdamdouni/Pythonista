# https://gist.github.com/harvitronix/57e2f626dfbbe76fbd5bbc4dd5c6bddc

def get_labels():
    """Get the labels our retraining created."""
    with open('./inception/retrained_labels.txt', 'r') as fin:
        labels = [line.rstrip('\n') for line in fin]
        return labels

def predict_on_image(image, labels):

    # Unpersists graph from file
    with tf.gfile.FastGFile("./inception/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        # Read in the image_data
        image_data = tf.gfile.FastGFile(image, 'rb').read()

        try:
            predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
            prediction = predictions[0]
        except:
            print("Error making prediction.")
            sys.exit()

        # Return the label of the top classification.
        prediction = prediction.tolist()
        max_value = max(prediction)
        max_index = prediction.index(max_value)
        predicted_label = labels[max_index]
        
        return predicted_label
