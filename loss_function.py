import numpy as np
from array import array 
#in general take the prediction dictionary (which should be a list) and subtract it from the true values list

def create_true_values_vector(label):
    #labels refers to a flat 1D array of labels, true values is a list of lists, where the inner lists are either 1s or 0's corresponding to the truth value of each digit
    true_values = np.zeros((10))
    true_values[label] = 1
    return(true_values)


def compute_loss(true_value, pred):
    #true values and preds should be lists of size 10, idk if they are arrays or not thoussing cross enthalpy loss
    #using cross entropy loss
    loss = -1 * np.sum(true_value * np.log2(pred))
    return(loss)

#y_train = array("B", [1, 7, 0, 0, 4])
#true_values = create_true_values_vector(y_train)
#print(true_values)
#batch_size = 5
#preds = [np.array([0.12538313, 0.47692714, 0.0015981, 0.14928662, 0.17750872, 0.05212745, 0.0019878, 0.00083522, 0.0101167, 0.00422911])]
#for i in range(batch_size):
#    print(compute_loss(true_values[i], preds[0]))