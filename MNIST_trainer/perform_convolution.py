import numpy

#default_bias = 0
#sample_convolution = numpy.array([[1, 1, 1],[0, 0, 0],[-1, -1, -1]])
#print(sample_convolution)

def create_rand_conv(conv_size, num_input_channels):
    std = numpy.sqrt(2 / ((conv_size**2) * num_input_channels))
    Z = numpy.random.normal(0, std, (conv_size, conv_size))
    #print('normalisation did not crash')
    return((Z, 0))
    #zero is the bias
    #works

def initialise_conv_grad_stacks(conv_size):
    f = numpy.zeros((conv_size, conv_size))
    return((f, 0))
    #works

def convolute(M, filter, bias, filtration):
    #call store gradient function
    outputs = []
    #M is the source matrix, filter is the convolution matrix (or filter)
    fshape = numpy.shape(filter)
    M = numpy.pad(M, pad_width=((0, 1),(0, 1)), mode='constant', constant_values=0)
    cropped_M_size = len(M) - fshape[0] + 1
    #iterating through the corners of the matrices to be convoluted
    croppings = []
    negative_bools = []
    for rowi in range(0, cropped_M_size, 2):
        row = M[rowi]
        for coli in range(0, cropped_M_size, 2):
            #corner = row[coli]
            #print(corner)
            #actual operation occurs here
            cropping = M[rowi:rowi+3, coli:coli+3]
            croppings.append(cropping)
            output_raw = numpy.sum(cropping * filter)
            #add bias (same bias added to all)
            output_biased = output_raw + bias
            #relu it
            output_rel = max(0, output_biased)
            negative_bools.append(output_rel != 0)
            outputs.append(output_rel)    
    Z = numpy.reshape(outputs, ((len(M)-1) // 2, (len(M)-1) // 2))
    filtration.extend([croppings, negative_bools, numpy.shape(M)])
    return(Z, numpy.shape(Z), filtration)
    #works

#M = numpy.diag(numpy.arange(28))
#print(M)
#x, y, z = convolute(M, sample_convolution, default_bias, [sample_convolution, default_bias])
#print(x)
#print(y)
#print(z)
#print(create_rand_conv(3))
