import numpy as np

def create_random_dense_layers_old(size, num_input_channels):
    dense_layers = {}
    std = np.sqrt(2 / ((size**2) * num_input_channels))
    for i in range(10):
        dense_layers[i] = []
        for j in range(num_input_channels):
            dense_layers[i].append(np.random.normal(0, std, (size, size)))
    return(dense_layers)

#def create_random_dense_layer_new(size):
    dense_layers = np.random.rand(size, 10)
    return(dense_layers)

def initialise_dense_grad_stacks(dense_size, num_input_channels):
    dense_grad_stack = []
    for i in range(10):
        dense_grad_stack.append([])
        for j in range(num_input_channels):
            dense_grad_stack[i].append(np.zeros((dense_size, dense_size)))
    return(dense_grad_stack)

def densate(M, dense_layers):
    raw_preds = []
    x_pred_sum = 0
    #print('raw preds incoming')
    for i in range(10):
        raw_pred = 0
        for j in range(len(M)):
            raw_pred += np.sum(dense_layers[i][j] * M[j])
        raw_preds.append(raw_pred)
    x = max(raw_preds)
    x_preds = []
    for raw_pred in raw_preds:
        x_pred = np.exp(raw_pred - x)
        x_pred_sum += x_pred
        x_preds.append(x_pred)
    preds = (x_preds / x_pred_sum)
    return(preds)

#def densify(M, dense_layer):
    size = np.shape(M)[0]
    #dividing by size is an attempt to do average pooling, pretty sure this is not how its supposed to work - like this has no effect at all idt
    raw_preds = np.exp(np.sum((M @ dense_layer), 0) / size)
    raw_preds_sum = np.sum(raw_preds)
    preds = raw_preds / raw_preds_sum
    return(preds)

#old way works

#dense = create_random_dense_layers_old(7, 16)
#print('dense_shape')
#print(np.shape(dense[0]))

#M = []
#for i in range(16):
#    M.append(np.random.rand(7, 7))
#pred = (densate(M, dense))
#print(pred)