import torch
from torch import nn
import torch.nn.functional as func

from network.spec.denses.standard_dense import DenseModel
from network.spec.extractor.standard_conv import ExtractionModel


class SpecModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.extractor = ExtractionModel()
        self.dense = DenseModel()

    def forward(self, input_tensor: torch.Tensor):
        output = self.extractor(input_tensor)
        output = self.dense(output)
        return output
