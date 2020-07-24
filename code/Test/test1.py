# -*- coding:utf-8 _*-
""" 
@Author: John
@Email: workspace2johnwu@gmail.com
@License: Apache Licence 
@File: test1.py 
@Created: 2020/07/06
@site:  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃            ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神獸保佑    ┣┓
                ┃　永無BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""

import tensorflow as tf
import numpy as np

g = tf.Graph()
with g.as_default():
    x = tf.compat.v1.placeholder(dtype=tf.float32,
                                 shape=(None),
                                 name='X')
    w = tf.Variable(2.0, name='weight')
    b = tf.Variable(0.7, name='bias')
    z = w * x + b

    init = tf.compat.v1.global_variables_initializer()

with tf.compat.v1.Session(graph=g) as sess:
    sess.run(init)

    for t in [1.0, 0.6, -1.8]:
        print('x=%4.1f --> z=%4.1f' % (t, sess.run(z, feed_dict={x: t})))

s = tf.Graph()
with s.as_default():
    x = tf.compat.v1.placeholder(dtype=tf.float32, shape=(None, 2, 3), name='input_x')
    x2 = tf.reshape(x, shape=(-1, 6), name='x2')
    xsum = tf.reduce_sum(x2, axis=0, name='col_sum')
    xmean = tf.reduce_mean(x2, axis=0, name='col_mean')

with tf.compat.v1.Session(graph=s) as sess:
    x_array = np.arange(18).reshape((3, 2, 3))
    print('input shape: ', x_array.shape)
    print('Reshape:\n', sess.run(x2, feed_dict={x: x_array}))
    print('Column Sums:\n', sess.run(xsum, feed_dict={x: x_array}))
    print('Column Means:\n', sess.run(xmean, feed_dict={x: x_array}))

x_train, y_train = np.arange(10).reshape((10, 1)), \
                   np.array([1.0, 1.3, 3.1, 2.0, 5.0, 6.3, 6.6, 7.4, 8.0, 9.0])

class TfLinreg(object):
    def __init__(self, x_dim, learning_rate=0.01, random_seed=None):
        self.x_dim = x_dim
        self.learning_rate = learning_rate
        self.random_seed = random_seed
        self.k = tf.Graph()
        with self.k.as_default():
            tf.compat.v1.set_random_seed(random_seed)
            self.build()
            self.init_op = tf.compat.v1.global_variables_initializer()

    def build(self):
        self.X = tf.compat.v1.placeholder(dtype=tf.float32, shape=(None, self.x_dim), name='x_input')
        self.y = tf.compat.v1.placeholder(dtype=tf.float32, shape=(None), name='y_input')
        print(self.X)
        print(self.y)

        w = tf.Variable(tf.zeros(shape=(1)), name='weights')
        b = tf.Variable(tf.zeros(shape=(1)), name='bias')
        print(w)
        print(b)

        self.z_net = tf.squeeze(w*self.X + b, name='z_net')
        print(self.z_net)

        sqr_errors = tf.square(self.y - self.z_net, name='sqr_errors')
        print(sqr_errors)

        self.mean_cost = tf.reduce_mean(sqr_errors, name='mean_cost')

        optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=self.learning_rate,
                                                                name='GradientDescent')
        self.optimizer = optimizer.minimize(self.mean_cost)
