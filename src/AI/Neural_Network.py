import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleNN(nn.Module):
    def __init__(self, input_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_size)
        self.dropout = nn.Dropout(0.2) 
    def forward(self, x):
        x = F.leaky_relu(self.fc1(x), negative_slope=0.01)
        x = self.dropout(x)
        x = F.leaky_relu(self.fc2(x), negative_slope=0.01)
        x = self.fc3(x)
        x = torch.tanh(x)
        return x

# class SimpleNN(nn.Module):
#     def __init__(self, input_size, output_size):
#         super(SimpleNN, self).__init__()
#         self.fc1 = nn.Linear(input_size, 256)
#         self.fc2 = nn.Linear(256, 128)
#         self.fc3 = nn.Linear(128, 64)
#         self.fc4 = nn.Linear(64, output_size)
#         self.dropout = nn.Dropout(p=0.5)
#         self.activations = None
#     def forward(self, x):
#         x = F.leaky_relu(self.fc1(x), negative_slope=0.01)  # Usando LeakyReLU
#         x = self.dropout(x)
#         x = F.elu(self.fc2(x))  # Usando ELU
#         x = self.dropout(x)
#         x = F.relu(self.fc3(x))  # Manteniendo ReLU para la última capa oculta
#         self.activations = x.detach().numpy().reshape(1, -1)
#         self.activations = (self.activations - self.activations.min()) / (self.activations.max() - self.activations.min())
#         x = self.fc4(x)
#         return x