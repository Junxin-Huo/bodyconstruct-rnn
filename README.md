# bodyconstruct-rnn
RNN, Tensorflow

function: predict elbow position according to hand position and rotation.

input: hand position(x, y, z) and hand rotation(x1, y1, z1, x2, y2, z2).
output: elbow position(x, y, z).

x1, y1, z1 are the global position with localPosition = (0, 0, 1) 
x2, y2, z2 are the global position with localPosition = (0, 1, 0)
These data collected from Unity and Oculus rift, and you can also use HTC vive.

# net.py
Tensorflow net constraction.

# loader.py
Read input data and output data.

# train.py
Train the net.

# test.py
Test tne net.

# addition
when you run the train.py, you can find a training_infomation file in ./graph/train/. 
switch into it
   > cd graph/train/
   
run tensorboard
   > tensorboard --logdir=.
   
open the url from output infomation such as http://0.0.0.0:6006
