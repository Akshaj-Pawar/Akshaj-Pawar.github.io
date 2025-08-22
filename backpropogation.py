import numpy as np
import dense_layer
#for now, these are built to account for networks with only one neuron per layer

def dense_desend(prediction, true_value, dense, M, learning_rate, dense_grad_stack):
    x = (prediction - true_value)
    dL_wrt_A = []
    #print('example of a dense gradient increment computed in response to a sample')
    #print('std' + str(np.std((-1) * x[0] * M[0]))
    for input_i in range(len(M)):
        dL_wrt_A.append(np.zeros((np.shape(M[input_i]))))
        #print('empty dense gradients')
        #print(dL_wrt_A)
        for i in range(10):
            dL_wrt_A[input_i] += x[i] * dense[i][input_i]
            dense_grad_stack[i][input_i] -= (x[i] * M[input_i])
    #gradients coming out of dense layer are healthy until the filters commit suicide'
    return(dense_grad_stack, dL_wrt_A)

def conv_descend(negative_bool, dL_wrt_A_local, filter, filter_grad_stack, cropping, bias, bias_grad_stack, learning_rate, new_dL_wrt_A):
    #this needs to take a loss and the gradient function after a forward pass, and use these to copute an adjustment and then apply the change
    #works btw given valid inputs
    if negative_bool: #dont worry this is being used right
        new_dL_wrt_A.append(dL_wrt_A_local * filter)
        filter_grad_stack -= dL_wrt_A_local * cropping
        bias_grad_stack -= dL_wrt_A_local
        #gotta adjust to make this return and increment the aggregate rather than the actual
    else:
        new_dL_wrt_A.append(np.zeros((3, 3)))
    return(filter_grad_stack, bias_grad_stack, new_dL_wrt_A)

def respool_unspooled_conv(spoolables, spooled_shape, fshape=(3,3)):
    #works given appropriate input
    #this function was revealed to me in a dream idk why everything is spools
    spooled = np.zeros((spooled_shape)) #spooled shape should be the post padding shape
    spoolables_i = 0
    cropped_spooled_size = spooled_shape[0] - fshape[0] + 1
    for rowi in range(0, cropped_spooled_size, 2):
        for coli in range(0, cropped_spooled_size, 2):
            #print('spooling data: spoolables_i = ' + str(spoolables_i))
            #print((rowi, coli))
            spooled[rowi:rowi+3, coli:coli+3] += spoolables[spoolables_i]
            spoolables_i += 1
    return(spooled[0:-1, 0:-1]) #cropped because original was padded


def backpropogate(prediction, true_value, dense, final_layer_input, learning_rate, filters_data, dense_grad_stack):
    
    #cycles backwards along the list of computations and applies the above functions
    #print(dense)
    #print(final_layer_input)
    dense_grad_stack, dL_wrt_A = dense_desend(prediction, true_value, dense, final_layer_input, learning_rate, dense_grad_stack)
    #note that dL_wrt_A is now a list
    new_dL_wrt_A_list = []
    convolutions = []
    filters_data.reverse()

    for layer in filters_data:

        convolutions.append([])
        conv_layer = convolutions[-1]
        new_grads = [] 
        for i in range(len(layer[0])): #ie len(filtrations)
            new_grads.append(None)

        for output_i in range(len(layer)):

            filtrations = layer[output_i]
            dL_wrt_A_regional = np.ndarray.flatten(dL_wrt_A[output_i])
            conv_layer.append([])
            conv_hell = conv_layer[-1]

            for input_i in range(len(filtrations)):
                #does mutating one god tuple somehow mutate all the god_tuples?

                god_tuple = filtrations[input_i]
                #unpacking - inefficent but presented this way to help the programmer keep track
                filter = god_tuple[0] #this is a 3x3 matrix, the filter
                filter_grad_stack = god_tuple[1] #this is the gradient pool where all the gradients are aggregated - it is 3x3
                bias = god_tuple[2] #this is a scalar
                bias_grad_stack = god_tuple[3] #this is a scalar in which the bias gradients are aggregated
                velocity_conv = god_tuple[4] #meanignless trash tuple (its actually very important)
                croppings = god_tuple[5] #this is a list of 3x3 input matrices
                negative_bools = god_tuple[6] #this is a list of booleans
                layer_input_shape = god_tuple[7] #this is a tuple containing the shape of the input to this layer POST PADDING
                #later might be good to do a more efficent unpacking - this should be a dictionary!

                for i in range(len(croppings)):
                    cropping = croppings[i]
                    negative_bool = negative_bools[i]
                    dL_wrt_A_local = dL_wrt_A_regional[i]
                    filter_grad_stack, bias_grad_stack, new_dL_wrt_A_list = conv_descend(negative_bool, dL_wrt_A_local, filter, filter_grad_stack, cropping, bias, bias_grad_stack, learning_rate, new_dL_wrt_A_list)
                
                #filter_grad_stack = filter_grad_stack / len(croppings)
                #bias_grad_stack = bias_grad_stack / len(croppings) #this is not necessary btw - network performs slightly ebtter without it - helps break symmetry

                #print('filter_grad_stack after operation, std: ' + str(np.std(filter_grad_stack)) + ' and norm end of filtration: ' + str(np.linalg.norm(filter_grad_stack)))
                #these grads are no longer sus

                conv_hell.append([(filter, bias), velocity_conv, (filter_grad_stack.copy(), bias_grad_stack)])
                #behold the most disusting thing you've ever seen in your life \/
                #each god tuple needs a return which is an aggregation across all filtrations. for each loop we only adjust the part of the list that pertains to the god_tuple in question
                if new_grads[input_i] is None: #subtle catch - is checks object identity, = runs into problems with ambiguous arrays
                    new_grads[input_i] = respool_unspooled_conv(new_dL_wrt_A_list, layer_input_shape)
                else:
                    new_grads[input_i] += respool_unspooled_conv(new_dL_wrt_A_list, layer_input_shape)
                
        #print('gradients coming out of conv layer')
        #print(np.std(new_grads))
        #print(np.linalg.norm(new_grads))
        dL_wrt_A = new_grads

    convolutions.reverse()

    return(dense_grad_stack, convolutions)

#def backpropogate2(prediction, true_value, dense, final_layer_input, learning_rate, filters_data, dense_grad_stack):
    #cycles backwards along the list of computations and applies the above functions
    #print(dense)
    #print(final_layer_input)
    dense_grad_stack, dL_wrt_A = dense_desend(prediction, true_value, dense, final_layer_input, learning_rate, dense_grad_stack)
    new_dL_wrt_A_list = []
    convolutions = []
    filters_data.reverse()

    for layer in filters_data:
        convolutions.append([])
        conv_layer = convolutions[-1]
        dL_wrt_A = np.ndarray.flatten(dL_wrt_A)
        new_dL_wrt_A = None
        for filtration in layer:
            #unpacking - inefficent but presented this way to help the programmer keep track
            filter = filtration[0] #this is a 3x3 matrix, the filter
            bias = filtration[1] #this is a scalar
            croppings = filtration[2] #this is a list of 3x3 input matrices
            negative_bools = filtration[3] #this is a list of booleans
            layer_input_shape = filtration[4] #this is a tuple containing the shape of the input to this layer POST PADDING
            #later might be good to do a more efficent unpacking
            for i in range(len(croppings)):
                cropping = croppings[i]
                negative_bool = negative_bools[i]
                dL_wrt_A_local = dL_wrt_A[i]
                filter, bias, new_dL_wrt_A_list = conv_descend(negative_bool, dL_wrt_A_local, filter, cropping, bias, learning_rate, new_dL_wrt_A_list)
            conv_layer.append((filter, bias))
            #behold the most disusting thing you've ever seen in your life \/
            if new_dL_wrt_A == None:
                new_dL_wrt_A = respool_unspooled_conv(new_dL_wrt_A_list, layer_input_shape)
            else:
                new_dL_wrt_A += respool_unspooled_conv(new_dL_wrt_A_list, layer_input_shape)
        dL_wrt_A = new_dL_wrt_A
    convolutions.reverse()
    return(dense_grad_stack, convolutions)



#some debugging bs lies beyond

def dense_eob_update(dense, dense_grad_stack, velocity_dense, momentum, batch_size):
    #currently only works on the outdated input form
    for i in range(10):
        for j in range(len(dense[i])):
            g = dense_grad_stack[i][j] / batch_size

            g_norm = np.linalg.norm(g)
            if g_norm > 7:
                g_f = g_f * (7 / g_norm)
            
            #the momentum system here uses a moving point average to bias the system agaisnt sporadic movement - 
            velocity_dense[i][j] = ((1-momentum)*g + momentum*velocity_dense[i][j])
            dense[i][j] += velocity_dense[i][j]
    return(dense, velocity_dense)

def test_dense():
    print('new test stats here')
    for i in range(5):
        print(' ')
    dense = dense_layer.create_random_dense_layers_old(7, 2)
    prediction = np.array([0.95, 0.05, 0.35, 0.9, 0.25, 0.1, 0.1, 0, 0.3, 0])
    true_value = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    final_layer_input = []
    for i in range(2):
        final_layer_input.append(np.random.rand(7, 7))
    dense_grad_stack = dense_layer.initialise_dense_grad_stacks(7, 2)
    velocity_dense = dense_grad_stack
    learning_rate = 0.1
    for i in range(1):
        dense_grad_stack, dL_wrt_A = dense_desend(prediction, true_value, dense, final_layer_input, learning_rate, dense_grad_stack)
        print('dl_wrt_A incoming')
        print(dL_wrt_A)
    print('dense:' + str(np.shape(dense)))
    print('dense_grad_stack:' + str(np.shape(dense_grad_stack)))
    dense, velocity_dense = dense_eob_update(dense, dense_grad_stack, velocity_dense, 0.9, 1) 
    print('final :')
    print(dense[0])