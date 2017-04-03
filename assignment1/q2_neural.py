#!/usr/bin/env python

import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive


def forward_backward_prop(data, labels, params, dimensions):
    """
    Forward and backward propagation for a two-layer sigmoidal network

    Compute the forward propagation and for the cross entropy cost,
    and backward propagation for the gradients for all parameters.

    Arguments:
    data -- M x Dx matrix, where each row is a training example.
    labels -- M x Dy matrix, where each row is a one-hot vector.
    params -- Model parameters, these are unpacked for you.
    dimensions -- A tuple of input dimension, number of hidden units
                  and output dimension
    """

    ### Unpack network parameters (do not modify)
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2])

    W1 = np.reshape(params[ofs:ofs+ Dx * H], (Dx, H))
    ofs += Dx * H
    b1 = np.reshape(params[ofs:ofs + H], (1, H))
    ofs += H
    W2 = np.reshape(params[ofs:ofs + H * Dy], (H, Dy))
    ofs += H * Dy
    b2 = np.reshape(params[ofs:ofs + Dy], (1, Dy))

    T = data.shape[0]

    ### YOUR CODE HERE: forward propagation
    z1 = np.dot(data, W1) + b1	# MxH + 1xH = MxH
    h = sigmoid(z1)		
    z2 = np.dot(h, W2) + b2	# MxDy + 1xDy = MxDy
    y_ = softmax(z2)		# MxDy
    cost = -1*np.sum(np.log(y_)*labels)/T
    #raise NotImplementedError
    ### END YOUR CODE

    ### YOUR CODE HERE: backward propagation
    dz2 = (y_ - labels)/T	# MxDy
    db2 = np.sum(dz2, axis=0)	# 1xDy
    dh	= np.dot(dz2, W2.T)	# MxH
    dW2	= np.dot(h.T, dz2)	# HxDy
    dz1 = h*(1-h)*dh		# MxH 
    db1 = np.sum(dz1, axis=0)	# 1xH
    dW1	= np.dot(data.T, dz1)	# Dx x H

    gradb2 = db2
    gradW2 = dW2
    gradb1 = db1
    gradW1 = dW1
    #raise NotImplementedError
    ### END YOUR CODE

    ### Stack gradients (do not modify)
    grad = np.concatenate((gradW1.flatten(), gradb1.flatten(),
        gradW2.flatten(), gradb2.flatten()))

    #print "Cost: %f \t grad[0] %f, grad[1] %f" % (cost, grad[0], grad[1])

    return cost, grad


def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using
    gradcheck.
    """
    print "Running sanity check..."

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # each row will be a datum
    labels = np.zeros((N, dimensions[2]))
    for i in xrange(N):
        labels[i, random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], )

    gradcheck_naive(lambda params:
        forward_backward_prop(data, labels, params, dimensions), params)


def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print "Running your sanity checks..."
    N = 20
    dimensions = [20, 25, 10]
    # dimensions = [1, 2, 2]
    data = np.random.randn(N, dimensions[0])   # each row will be a     datum
    labels = np.zeros((N, dimensions[2]))
    for i in xrange(N):
        labels[i, random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] +     (
        dimensions[1] + 1) * dimensions[2], )

    gradcheck_naive(lambda params:
        forward_backward_prop(data, labels, params, dimensions), params)
    print 'PASSED (Y)'

    ### YOUR CODE HERE
#raise NotImplementedError
    ### END YOUR CODE


if __name__ == "__main__":
    sanity_check()
    your_sanity_checks()
