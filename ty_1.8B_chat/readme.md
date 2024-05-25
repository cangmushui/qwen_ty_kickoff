# 环境

python 3.8(必须)
pytroch+cuda11.8
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
requirements.txt
加快transformers的运算速度:(从github上下载后安装失败了)
pip install flash-attn --no-build-isolation --use-pep517
安装layernorm(使flashattention的速度更快)
git clone https://github.com/Dao-AILab/flash-attention
cd flash-attention
pip install csrc/layer_norm
使用量化技术:
pip install optimum
pip install auto-gptq
使用魔搭下载模型
pip install modelscope
基本框架是多卡并行, 进一步利用zero参数服务器, 按照zero等级层层深入, 逐层将模型参数、梯度、优化器状态拆到多卡上
， 也可以引入GPU显存交换技术，将闲置的不用的数据暂放到CPU, huggingface和modelscope底层应该都是基于ds
pip install deepspeed
微调算法框架peft
pip install peft
安装mpi4py
pip install mpi4py

# 运行微调

epoch设为2, batch_size设为4, 注意核对下deepspeed的配置
bash finetune_qlora_single_gpu_240521.sh -m ~/.cache/modelscope/hub/qwen/Qwen-1_8B-Chat-Int4 -d train.txt
显存占用大约10多G, 训练好的Q-lora模型放在当前目录的output_qwen下

# 问题

triton 报错RuntimeError: Triton Error [CUDA]: device kernel image is invalid
https://github.com/triton-lang/triton/issues/1955#issuecomment-1929908209
用这个办法也没解决, 只好安装老版本的triton2.1.0解决
pip install triton==2.1.0
