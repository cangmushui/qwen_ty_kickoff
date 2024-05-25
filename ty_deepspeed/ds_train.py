import argparse
import torch
import torchvision
import deepspeed
from model import FashionModel, img_transform

#!首先需要准备一个deepspeed配置文件
##deepspeed的命令行启动参数: deepspeed ds_train.py --epoch 5 --deepspeed --deepspeed_config ds_config.json
########deepspeed训练逻辑, 每个子进程都要执行下列完整代码, 彼此共同协商训练###############
########下面是一个单机多卡的例子, 每张卡都会建立一个子进程####################
# 1. 初始化parser
parser = argparse.ArgumentParser()
# 2. 添加参数
#! local rank是每个子程序必须接受的参数, 代表该子程序的显卡序号
parser.add_argument('--local_rank', type=int, default=-1, help='local rank passed from distributed launcher')
# 后面的部分是用户自定义的参数
parser.add_argument('--epcoh', type=int, default=-1, help='epoch')
#! 使用deepspeed把deepspeed一些所需参数加入parser
parser = deepspeed.add_config_arguments(parser)
#3. 解析参数
cmd_args = parser.parse_args()

dataset = torchvision.datasets.FashionMNIST(root='./dataset', download=True, transform=img_transform)
#!这里是使用了deepspeed的一个体现, batchsize应该等于train_batch_size/gpu数量
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, num_workers=4, shuffle=True)

#定义model和loss
model = FashionModel().cuda()
loss_fn = torch.nn.CrossEntropyLoss().cuda()

#! 使用deepspeed进行训练
# 该代码拉起很多进程, 得到一个分布式模型
model, _, _, _ = deepspeed.initialize(args=cmd_args, model=model, model_parameters=model.parameters())
for epoch in range(cmd_args.epoch):
    for x, y in dataloader:
        x, y = x.cuda(), y.cuda()
        # 下面这个和model相关需要做多卡协调, 如果有进程没有完成会发生阻塞
        output = model()
        loss = loss_fn(output, y)
        model.backward(loss)
        model.step()
    print('epoch {} done'.format(epoch))
    model.save_checkpont('./check_points')
