# bodyconstruct-rnn
RNN, Tensorflow

function: predict elbow position according to hand position and rotation.

input: hand position(x, y, z) and hand rotation(x1, y1, z1, x2, y2, z2).
output: elbow position(x, y, z).

x1, y1, z1 are the global position with localPosition = (0, 0, 1)
x2, y2, z2 are the global position with localPosition = (0, 1, 0)
These data collected from Unity and Oculus rift, and you can also use HTC vive.
