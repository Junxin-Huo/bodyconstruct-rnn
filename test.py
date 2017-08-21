from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import time
import numpy as np
import tensorflow as tf
from net import inference
from loader import loadDataLabel, FRAME_COUNT

BATCH_SIZE = 1
DATADIR = 'dataset_train'
NETPATH = 'data/net.ckpt'
# NETPATH = 'data/net_final.ckpt'
EVAL_FREQUENCY = 1000
WRITE_RESULT = False

def main(argv=None):
    if WRITE_RESULT:
        f=open('result.txt', 'w')
    print('Loading......')
    start_time = time.time()
    begin_time = start_time

    data, label = loadDataLabel(DATADIR, BATCH_SIZE)
    batch_len = label.shape[0]
    epoch_size = label.shape[1]
    train_size = batch_len * epoch_size * FRAME_COUNT
    print('Loaded %d datas.' % train_size)

    elapsed_time = time.time() - start_time
    print('Loading datas with label elapsed %.1f s' % elapsed_time)
    print('Building net......')
    start_time = time.time()

    x = tf.placeholder(tf.float32, shape=[BATCH_SIZE, 1, 9], name='data')
    keep_prob = tf.placeholder(tf.float32, name='prob')

    train_prediction, initial_state, final_state = inference(x, keep_prob, BATCH_SIZE)

    elapsed_time = time.time() - start_time
    print('Building net elapsed %.1f s' % elapsed_time)
    print('Begin testing..., train dataset size:{0}'.format(train_size))
    start_time = time.time()

    saver = tf.train.Saver()

    elapsed_time = time.time() - start_time
    print('loading net elapsed %.1f s' % elapsed_time)
    start_time = time.time()

    distances = []
    with tf.Session() as sess:
        saver.restore(sess, NETPATH)
        tf.train.write_graph(sess.graph_def, '.', 'data/train.pb', False)
        state = sess.run(initial_state)
        for step in range(epoch_size):
            batch_data = np.reshape(data[:, step, :, :], [BATCH_SIZE, FRAME_COUNT, 9])
            for j in range(FRAME_COUNT):
                data_mini = batch_data[:, j, :]
                feed_dict = {x: np.reshape(data_mini, [BATCH_SIZE, 1, 9]),
                             keep_prob: 1.0}
                for i, (c, h) in enumerate(initial_state):
                    feed_dict[c] = state[i].c
                    feed_dict[h] = state[i].h
                tp, state = sess.run([train_prediction, final_state], feed_dict=feed_dict)
                # if WRITE_RESULT:
                #     f.write(str(tp[0][0]) + ' ' + str(tp[0][1]) + ' ' + str(tp[0][2]) + ' ' + str(tp[0][3]) + ' ' + str(tp[0][4]) + ' ' + str(tp[0][5]) + '\n')
                if WRITE_RESULT:
                    f.write(str(tp[0][0]) + ' ' + str(tp[0][1]) + ' ' + str(tp[0][2]) + '\n')
                distance = np.square(np.reshape(tp, (-1)) - label[0, step, j, :])
                # distance_ave = (np.sqrt(distance[0] + distance[1] + distance[2]) + np.sqrt(distance[3] + distance[4] + distance[5])) / 2
                distance_ave = np.sqrt(distance[0] + distance[1] + distance[2])
                distances.append(distance_ave)

            if step % EVAL_FREQUENCY == 0:
                elapsed_time = time.time() - start_time
                start_time = time.time()
                print('Step %d, %.1f ms.' % (step, 1000 * elapsed_time / EVAL_FREQUENCY))
                print('Prediction: ', tp)
                print('True:       ', label[0, step, j, :])
                print('Distances: ', distance_ave)
            sys.stdout.flush()

    distances = np.asarray(distances, dtype=np.float32)
    error = np.mean(distances)
    print('Total Average Distance: ', error)

    elapsed_time = time.time() - begin_time
    print('Total time: %.1f s' % elapsed_time)

    if WRITE_RESULT:
        f.close()


if __name__ == '__main__':
    tf.app.run()
