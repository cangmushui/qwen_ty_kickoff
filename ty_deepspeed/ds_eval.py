import argparse
from model import FashionModel, img_transform
import deepspeed
import torchvision
import torch

##deepspeed提供了两种推理方式, 第一种是常用的代码推理, 第二种是给定训好的模型, 直接起一个http服务, 这里采用第一种
###执行脚本: deepspeed ds_eval.py --deepspeed --deepspeed_config ds_config.json
### 部分代码所有程序都要执行
parser = argparse.ArgumentParser()
parser.add_argument('--local_rank', type=int, default=-1, help='local rank passed from distributed launcher')
parser = deepspeed.add_config_arguments(parser)
cmd_args = parser.parse_args()

model = FashionModel().cuda()
model, _, _, _ = deepspeed.initialize(args=cmd_args, model=model, model_parameters = model.parameters())
model.load_checkpoint('./checkpoints')
model.eval()

### 部分代码只有主控程序执行
if torch.distributed.get_rank() == 0:
    dataset = torchvision.datasets.FashionMNIST(root='./dataset', download=True, transform=img_transform)
    batch_x = torch.stack(dataset[0][0], dataset[1][0]).cuda()

    outputs = model(batch_x) #分布式推理
    print('分布式推理:', outputs.cpu().argmax(dim=1), [dataset[0][1], dataset[1][1]])

    ####模型转成torch单体########
    torch.save(model.module.state_dict(), 'model.pt')
    # 创建模型并单卡加载
    model = FashionModel().cuda()
    model.load_state_dict(torch.load('model.pt'))

    model.eval()
    output = model(batch_x)
    print('单体推理:', outputs.cpu().argmax(dim=1), [dataset[0][1], dataset[1][1]])


