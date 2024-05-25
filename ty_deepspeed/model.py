import torch
import numpy as np

class FashionModel(torch.nn.module):
    def __init__(self):
        super().__init__()
        self.seq = torch.nn.Sequential(
            torch.nn.Linear(in_feature = 784, out_features=300), 
            torch.nn.ReLU(),
            torch.nn.Linear(in_feature=300, out_features=10)
        )

    def forward(self, batch):
        return self.seq(batch)
def img_transform(img):
    img = np.asarray(img)/255
    return torch.tensor(img,dtype=torch.float32).flatten()