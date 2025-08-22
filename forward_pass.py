import dense_layer
import loss_function
import MNISTDataLoader
import perform_convolution
import backpropogation
import numpy as np
from array import array

def process_epoch(batch_size, train_batches, val_batches, architecture, convolutions, dense, velocity_dense, learning_rate, momentum): #50 is probably more advisable, but i find it leads to slow change (not anymore lmao)
    print('new epoch starts here')
    for i in range(4):
        print(' ')
    #print('initial convs')
    #print(convolutions)
    #print('initial dense')
    #print(dense[0])
    for b in range(225):
        print('new batch ' + str(b))
        batch = train_batches[b]
        x_trains = batch[0]
        y_trains = batch[1]
        dense_grad_stack = dense_layer.initialise_dense_grad_stacks(7, architecture[-1])
        #wait fuck are the conv grad stacks not initialised
        total_loss = 0

        for i in range(len(x_trains)):
            x_train = (np.stack(x_trains[i]) / 255)
            y_train = y_trains[i]
            loss, dense_grad_stack, convolutions = forward_pass(convolutions, x_train, y_train, dense, dense_grad_stack, True) 
            total_loss += loss
            #print(forward_pass(convolutions, x_train, y_train, dense, dense_grad_stack, False))
            #print('remember to set learning mode to true later')
        
        #end of batch updates to the dense layers and the convolutions
        #print('dense_grad_stack std: ' + str(np.std(dense_grad_stack)))
        #print('norm dense_grad_stack: ' + str(np.linalg.norm(dense_grad_stack)))
        dense, velocity_dense = dense_eob_update(dense, dense_grad_stack, velocity_dense, momentum, batch_size, learning_rate)
        convolutions = conv_eob_update(convolutions, momentum, batch_size, 3, learning_rate)

        forward_pass(convolutions, x_train, y_train, dense, dense_grad_stack, False)
        print('average loss: ' + str(total_loss / len(x_trains)))

    print(' ')
    print(' ')

    for b in range(20):
        print('val batch ' + str(b))
        batch = val_batches[b]
        x_vals = batch[0]
        y_vals = batch[1]
        total_loss = 0
        corrects = 0
        for i in range(len(x_vals)):
            x_val = (np.stack(x_vals[i]) / 255)
            y_val = y_vals[i]
            local_loss, correct = forward_pass(convolutions, x_val, y_val, dense, dense_grad_stack, False)
            total_loss += local_loss
            if correct:
                corrects += 1
        average_loss = total_loss / len(x_vals)
        accuracy = corrects / len(x_vals)
        print('average loss: ' + str(average_loss))
        print('accuracy: ' + str(accuracy))

    return(convolutions, dense, velocity_dense)

def instantiate_weights(architecture, dense_size=7, conv_size=3):
    dense = dense_layer.create_random_dense_layers_old(dense_size, architecture[-1])
    velocity_dense = dense_layer.initialise_dense_grad_stacks(dense_size, architecture[-1])
    convolutions = []
    for i in range(len(architecture)):
        convolutions.append([])
    for i in range(len(convolutions)):
        layer = convolutions[i]
        if i == 0:
            num_inputs = 1
        else:
            num_inputs = architecture[i-1]
        for j in range(architecture[i]):
            layer.append([])
        for filtration in layer:
            for k in range(num_inputs):
                filtration.append([perform_convolution.create_rand_conv(conv_size, num_inputs), perform_convolution.initialise_conv_grad_stacks(conv_size), perform_convolution.initialise_conv_grad_stacks(conv_size)])
        #for now we aren't worrying about branching convolutions so we use this simplified code to just create one convolution per layer
        #the first tuple holds the filter and bias, the second holds the velocity vector, the third holds the gradient stack (it is empty on initialisation)
    return(convolutions, dense, velocity_dense)


def dense_eob_update(dense, dense_grad_stack, velocity_dense, momentum, batch_size, learning_rate=0.01):
    #print('final eob step 0.0: ')
    #print('std: ' + str(np.std(dense_grad_stack[0][0] / batch_size)))
    #print('norm: ' + str(np.linalg.norm(dense_grad_stack[0][0] / batch_size)))
    #print('final eob step 4.8: ')
    #print('std: ' + str(np.std(dense_grad_stack[4][8] / batch_size)))
    #print('norm: ' + str(np.linalg.norm(dense_grad_stack[4][8] / batch_size)))
    for i in range(10):
        for j in range(len(dense[i])):
            g = (dense_grad_stack[i][j] / batch_size) * 10

            g_norm = np.linalg.norm(g)
            #print('g_norm' + str(g_norm))
            #print('g_std' + str(np.std(g)))
            if g_norm > 3.5:
                g = g * (3.5 / g_norm)
            
            #the momentum system here uses a moving point average to bias the system agaisnt sporadic movement - 
            velocity_dense[i][j] = (((1-momentum)*g + momentum*velocity_dense[i][j]) * learning_rate)
            dense[i][j] += velocity_dense[i][j]
    
    #print('final eob step 0.0: ')
    #print('std: ' + str(np.std(dense[0][0])))
    #print('norm: ' + str(np.linalg.norm(dense[0][0])))
    #print('final eob step 4.8: ')
    #print('std: ' + str(np.std(dense[4][8])))
    #print('norm: ' + str(np.linalg.norm(dense[4][8])))

    return(dense, velocity_dense)

def conv_eob_update(convolutions, momentum, batch_size, conv_size=3, learning_rate=0.01):
    for layer in convolutions:
        filter_shown = False
        for hell in layer:
            for devil_tuple in hell:
                #print('beginning update - devil tuple:')
                #print(devil_tuple)

                #unpacking
                filter = devil_tuple[0][0]
                bias = devil_tuple[0][1]
                velocity_filter = devil_tuple[1][0]
                velocity_bias = devil_tuple[1][1]
                filter_grad_stack = devil_tuple[2][0]
                bias_grad_stack = devil_tuple[2][1]

                #momentum based optimisation
                g_f = filter_grad_stack / batch_size

                #gradient clipping by norm because it preserves directions and clipping by value just sounds liek a stupid thing to do - good for super anomalies but this happens too often to be a super anomaly
                g_f_norm = np.linalg.norm(g_f)
                #print('bias end of batch: ' + str(bias))
                #if not filter_shown:
                #    print('filter_grad_stack norm end of batch ' + str(g_f_norm))
                #    print('filter_grad_stack std end of batch ' + str(np.std(g_f)))
                #    filter_shown = True
                #print('filter end of batch: ' + str(filter))

                if g_f_norm > 3.5:
                    g_f = g_f * (3.5 / g_f_norm) #5 is probably more advisable but i find it causes conformance

                velocity_filter = (((1-momentum)*g_f + momentum*velocity_filter) * learning_rate)
                filter += velocity_filter
                if not filter_shown:
                    #print('filter norm end of batch ' + str(np.linalg.norm(filter)))
                    #print('filter std end of batch ' + str(np.std(filter)))
                    filter_shown = True

                g_b = bias_grad_stack / batch_size
                velocity_bias = (((1-momentum)*g_b + momentum*velocity_bias) * learning_rate)
                bias += velocity_bias

                devil_tuple[:] = [(filter, bias), (velocity_filter, velocity_bias), perform_convolution.initialise_conv_grad_stacks(conv_size)] #repack and initialise the stacks
        
    return(convolutions)


def forward_pass(convolutions, x_train, y_train, dense_layers, dense_grad_stack, learning_mode):
    #print('new forward pass')
    #print(dense_layers[0][0])
    inputs = [x_train]
    true_values = loss_function.create_true_values_vector(y_train)
    #might eventually want to do that on mass in a previous looping bit but this should work for now
    post_filtering_data = [] #this is the list containing the god tuples
    for layer in convolutions:
        post_filtering_data.append([])
        post_filtering_layer = post_filtering_data[-1]
        activations = []
        ###
        # PROBLEM 1: the devil tuples are not stored in the layers - they are stored in lists of devil tuples which are stored in layers
        # PROBLEM 3: the different filtrations each have an associated gradient that they must be assigned with
        # 
        ###
        for hell_tuple in layer:

            logits = []
            if len(hell_tuple) != len(inputs):
                print('hell tuple wrong size for some reason')
            post_filtering_layer.append([])
            post_filtering_helltup = post_filtering_layer[-1]

            for input_i in range(len(inputs)):

                devil_tuple = hell_tuple[input_i]
                #print('new devil tuple')
                filter = devil_tuple[0][0]
                bias = devil_tuple[0][1]
                #print('bias during batch ' + str(bias))
                velocity_conv = devil_tuple[1]
                filter_grad_stack = devil_tuple[2][0]
                bias_grad_stack = devil_tuple[2][1]

                post_filtering_helltup.append([filter, filter_grad_stack, bias, bias_grad_stack, velocity_conv]) #add grad stacks to this
                filtration = post_filtering_helltup[-1]
                #perform the convolution using the filter
                logit, logit_shape, filtration = perform_convolution.convolute(inputs[input_i], filter, bias, filtration)
                logits.append(logit)

            activation = np.zeros(logit_shape)
            if len(logits) != len(inputs):
                print('number of logits does not match number of inputs to the layer')
            for logit in logits: 
                activation = activation + logit
            activations.append(activation) #number of activations = number of hell tuples
        if len(activations) != len(layer):
            print('number of activations does not match number of filters in layer')
        #print('activations: ')
        #print(activations)
        inputs = activations
    #print('post_filtering_data end of pass')
    #print(post_filtering_data[1][-1])
        #maybe better to use some kind of recursion here? just my intuition idk
    M = inputs
    preds = dense_layer.densate(M, dense_layers)
    if learning_mode:
        #print('post_filtering_data end of pass')
        #print(post_filtering_data)
        dense_grad_stack, convolutions = backpropogation.backpropogate(preds, true_values, dense_layers, M, 0.01, post_filtering_data, dense_grad_stack)
        loss = loss_function.compute_loss(true_values, preds)
        return(loss, dense_grad_stack, convolutions)
    else:
        print('preds std: ' + str(np.std(preds)))
        loss = loss_function.compute_loss(true_values, preds)
        answer = np.argmax(preds)
        if answer == y_train:
            correct = True
        else:
            correct = False

        return(loss, correct)

np.random.seed(42)
print('new thing starts here')
for i in range(4):
    print(' ')
train_val_ratio = 3
batch_size = 25
train_batches, val_batches, x_test, y_test = MNISTDataLoader.load_batches(batch_size, train_val_ratio)

architecture = (8, 16)
momentum = 0.9
learning_rate = 0.025
convolutions, dense, velocity_dense = instantiate_weights(architecture)

for epoch in range(2):
    convolutions, dense, velocity_dense = process_epoch(batch_size, train_batches, val_batches, architecture, convolutions, dense, velocity_dense, learning_rate, momentum)
