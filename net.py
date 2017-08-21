from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tensorflow.contrib as con

import inspect

HIDDEN_SIZE = 64
NUM_LAYERS = 3
max_grad_norm = 2



def inference(data, prob, BATCH_SIZE, reuse=False):
    with tf.variable_scope("RNN", reuse=reuse):
        def lstm_cell():
            if 'reuse' in inspect.getargspec(con.rnn.LSTMCell.__init__).args:
                return con.rnn.LSTMCell(HIDDEN_SIZE, reuse=tf.get_variable_scope().reuse)
            else:
                return con.rnn.LSTMCell(HIDDEN_SIZE)
        cell = con.rnn.MultiRNNCell([lstm_cell() for _ in range(NUM_LAYERS)])
        _initial_state = cell.zero_state(BATCH_SIZE, tf.float32)

        data = tf.nn.dropout(data, prob)

        outputs = []
        state = _initial_state
        with tf.variable_scope("RNN", reuse=reuse):
            for time_step in range(data.shape[1]):
                if time_step > 0: tf.get_variable_scope().reuse_variables()
                (cell_output, state) = cell(data[:, time_step, :], state)
                outputs.append(cell_output)


    with tf.variable_scope("softmax", reuse=reuse):
        output = tf.reshape(tf.concat(outputs, 1), [-1, HIDDEN_SIZE])
        softmax_w = tf.get_variable(name='softmax_w', shape=[HIDDEN_SIZE, 3], dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=0.1))
        softmax_b = tf.get_variable(name='softmax_b', shape=[3], dtype=tf.float32, initializer=tf.constant_initializer(0.0))
        logits = tf.add(tf.matmul(output, softmax_w), softmax_b, name='logits')


    with tf.variable_scope("output", reuse=reuse):
        argmax = tf.nn.softmax(logits, name='argmax')
        state_0_c = tf.multiply(state[0].c, 1, name='state_0_c')
        state_0_h = tf.multiply(state[0].h, 1, name='state_0_h')
        state_1_c = tf.multiply(state[1].c, 1, name='state_1_c')
        state_1_h = tf.multiply(state[1].h, 1, name='state_1_h')
        state_2_c = tf.multiply(state[2].c, 1, name='state_2_c')
        state_2_h = tf.multiply(state[2].h, 1, name='state_2_h')
        # state_3_c = tf.multiply(state[3].c, 1, name='state_3_c')
        # state_3_h = tf.multiply(state[3].h, 1, name='state_3_h')

    return logits, _initial_state, state


def total_loss(logits, labels):
    labels = tf.reshape(labels, (-1, 3))
    logits = tf.reshape(logits, (-1, 3))
    _entropy = tf.sqrt(tf.reduce_sum(tf.square(logits - labels), 1))
    return tf.reduce_mean(_entropy)

def myTrain(loss, learning_rate, batch):
    tvars = tf.trainable_variables()
    grads, _ = tf.clip_by_global_norm(tf.gradients(loss, tvars), max_grad_norm)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train_op = optimizer.apply_gradients(zip(grads, tvars), global_step=batch)
    return train_op

def train(loss, learning_rate, batch):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    return optimizer.minimize(loss, global_step=batch)


