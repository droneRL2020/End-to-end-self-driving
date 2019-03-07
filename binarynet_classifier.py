import tensorflow as tf

def binarynet(inputs,
              num_classes,
              scope='binary_classifier'):
    num_channels = 3
    filter_size_conv1 = 3
    filter_size_conv2 = 3
    filter_size_conv3 = 3
    num_filters_conv1 = 1
    num_filters_conv2 = 1
    num_filters_conv3 = 1
    fc_layer_size = 50
    
    
    def create_weights(shape):
        return tf.Variable(tf.truncated_normal(shape, stddev=0.05))
    
    def create_biases(size):
        return tf.Variable(tf.constant(0.05, shape=[size]))
    
    def create_convolutional_layer(input,
               num_input_channels, 
               conv_filter_size,        
               num_filters):  
    
        weights = create_weights(shape=[conv_filter_size, conv_filter_size, num_input_channels, num_filters])
        biases = create_biases(num_filters)
        layer = tf.nn.conv2d(input=input,
                         filter=weights,
                         strides=[1, 1, 1, 1],
                         padding='SAME')
        layer += biases 
        layer = tf.nn.max_pool(value=layer,
                                ksize=[1, 2, 2, 1],
                                strides=[1, 2, 2, 1],
                                padding='SAME')
        layer = tf.nn.relu(layer)
        return layer
    def create_flatten_layer(layer):
        layer_shape = layer.get_shape()
        num_features = layer_shape[1:4].num_elements()
        layer = tf.reshape(layer, [-1, num_features])

        return layer
    def create_fc_layer(input,          
             num_inputs,    
             num_outputs,
             use_relu=True):
        weights = create_weights(shape=[num_inputs, num_outputs])
        biases = create_biases(num_outputs)

        layer = tf.matmul(input, weights) + biases
        if use_relu:
            layer = tf.nn.relu(layer)

        return layer
    
    with tf.variable_scope(scope) as sc:
        layer_conv1 = create_convolutional_layer(input=inputs,
               num_input_channels=num_channels,
               conv_filter_size=filter_size_conv1,
               num_filters=num_filters_conv1)

        layer_conv2 = create_convolutional_layer(input=layer_conv1,
                       num_input_channels=num_filters_conv1,
                       conv_filter_size=filter_size_conv2,
                       num_filters=num_filters_conv2)

        layer_conv3= create_convolutional_layer(input=layer_conv2,
                       num_input_channels=num_filters_conv2,
                       conv_filter_size=filter_size_conv3,
                       num_filters=num_filters_conv3)

        layer_flat = create_flatten_layer(layer_conv3)

        layer_fc1 = create_fc_layer(input=layer_flat,
                             num_inputs=layer_flat.get_shape()[1:4].num_elements(),
                             num_outputs=fc_layer_size,
                             use_relu=True)

        hypothesis = create_fc_layer(input=layer_fc1,
                             num_inputs=fc_layer_size,
                             num_outputs=num_classes,
                             use_relu=False)
    
        probs = tf.nn.softmax(hypothesis, name="y_pred")
        y_pred_cls = tf.argmax(probs, dimension=1, name="y_pred_cls")
    return hypothesis, probs, y_pred_cls
        
        