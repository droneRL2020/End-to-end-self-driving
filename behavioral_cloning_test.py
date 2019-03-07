import datetime
import numpy as np
import tensorflow as tf
import binarynet_classifier as bc
# import mobilenet_classifier as mc
tf.set_random_seed(777)  # reproducibility


csv_path_test = tf.train.string_input_producer(['demo2/roll_record/straight_pwm_test.csv'],
                                         shuffle=False,
                                         name='csv_path')

reader = tf.TextLineReader()
key_test, value_test = reader.read(csv_path_test)


record_defaults = [[0],[""],[0.],[0.]]
_, im_name_test, label_test, _ = tf.decode_csv(value_test, record_defaults=record_defaults)


# load images from image_path above
im_content_test = tf.read_file(im_name_test)
image_test = tf.image.decode_png(im_content_test, channels=3)
image_test = tf.cast(image_test, tf.float32)
image_test = tf.image.resize_images(image_test, [64, 64])

test_x_batch, test_y_batch = \
    tf.train.batch([image_test, label_test], batch_size=100)

learning_rate = 0.0001
batch_size = 100
num_classes = 1
num_batch = 290 // batch_size


X_ph = tf.placeholder(tf.float32, [None, 64, 64, 3])    
Y_ph = tf.placeholder(tf.float32, [None, num_classes])

hypothesis, probs, _ = bc.binarynet(X_ph, 1)
print("hello wrold")
cost = tf.reduce_mean(tf.square(hypothesis - Y_ph))
# print(tf.trainable_variables())  ## Check trainable variables
optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(cost)
# optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate).minimize(cost)
                      
# initialize
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
sess = tf.InteractiveSession(config=config)
sess.run(tf.global_variables_initializer())

# Start populating the filename queue.
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)


restore_vars = [var for var in tf.global_variables() if
               var.name.startswith('binary_classifier')]
saver = tf.train.Saver(restore_vars)
saver.restore(sess, "saved_networks/2018-11-18_16_11")

x_batch, y_batch = sess.run([test_x_batch, test_y_batch]) # Since, we can't feed tensor

hy_val = sess.run([hypothesis], feed_dict={X_ph: x_batch})
print("prediction:", hy_val, "label:", y_batch)

print("Learning Done!")
coord.request_stop()
coord.join(threads)