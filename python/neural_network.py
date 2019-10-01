"""Implementation of a neural network using numpy."""

import numpy as np


# Sigmoid Function
def sigmoid(x):
    return 1/(1 + np.exp(-x))


# Derivative of Sigmoid Function
def derivatives_sigmoid(x):
    return x * (1 - x)


class Neural_network:
    """Represents an instance of a neural network."""

    def __init__(self, input_n, hidden_n, output_n, lr=0.1):
        """Initialize the neural networks neuron layers."""
        # Validate input
        for n in [input_n, hidden_n, output_n]:
            e1 = "Must use integer values for neuron, not {}".format(type(n))
            assert isinstance(n, int), e1
            e2 = "Must use interger value greater than 0, not {}".format(n)
            assert n > 0, e2
        e3 = "Learning rate must be a number, not {}".format(type(lr))
        assert isinstance(lr, (int, float)), e3

        self.input_n = input_n
        self.hidden_n = hidden_n
        self.output_n = output_n
        self.lr = lr

        # Create weight and bias matrices
        self.wh = np.random.uniform(size=(self.input_n, self.hidden_n))
        self.bh = np.random.uniform(size=(1, self.hidden_n))
        self.wout = np.random.uniform(size=(self.hidden_n, self.output_n))
        self.bout = np.random.uniform(size=(1, self.output_n))

    def guess(self, X):
        """Give an output for a given set of inputs."""
        hidden_layer_input1 = np.dot(X, self.wh)
        hidden_layer_input = hidden_layer_input1 + self.bh
        hiddenlayer_activations = sigmoid(hidden_layer_input)
        output_layer_input1 = np.dot(hiddenlayer_activations, self.wout)
        output_layer_input = output_layer_input1 + self.bout
        output = sigmoid(output_layer_input)
        return output

    def train(self, X, y):
        """Train the neural network given an input and an expected output.

        X can be a vector or an mx1 array
        y can be a vector or an mx1 arrawy
        """
        hidden_layer_input1 = np.dot(X, self.wh)
        hidden_layer_input = hidden_layer_input1 + self.bh
        hiddenlayer_activations = sigmoid(hidden_layer_input)
        output_layer_input1 = np.dot(hiddenlayer_activations, self.wout)
        output_layer_input = output_layer_input1 + self.bout
        output = sigmoid(output_layer_input)

        # Backpropagation
        error = y - output
        slope_output_layer = derivatives_sigmoid(output)
        slope_hidden_layer = derivatives_sigmoid(hiddenlayer_activations)
        d_output = error * slope_output_layer
        error_at_hidden_layer = d_output.dot(self.wout.T)
        d_hiddenlayer = error_at_hidden_layer * slope_hidden_layer
        self.wout += hiddenlayer_activations.T.dot(d_output) * self.lr
        self.bout += np.sum(d_output, axis=0, keepdims=True) * self.lr
        self.wh += np.outer(X, d_hiddenlayer) * self.lr
        self.bh += np.sum(d_hiddenlayer, axis=0, keepdims=True) * self.lr

        print(output)

# Make it so that is accepts lists
X1 = np.array([1, 0, 1, 0])
y1 = np.array([1])
nn = Neural_network(4, 3, 1)
nn.train(X1, y1)
