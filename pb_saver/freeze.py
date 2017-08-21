from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from freeze_graph import freeze_graph

input_graph = '../data/train.pb'
input_saver = ''
input_binary = True
input_checkpoint = '../data/net.ckpt'
output_node_names = 'softmax/logits,output/argmax,' \
                    'output/state_0_c,output/state_0_h,' \
                    'output/state_1_c,output/state_1_h,' \
                    'output/state_2_c,output/state_2_h'
restore_op_name = "save/restore_all"
filename_tensor_name = "save/Const:0"
output_graph = "../data/joint_rnn_graph.pb"
clear_devices = True
initializer_nodes = ''

print("freezing...")
freeze_graph(input_graph, input_saver,
        input_binary, input_checkpoint,
        output_node_names, restore_op_name,
        filename_tensor_name, output_graph,
        clear_devices, "") 
