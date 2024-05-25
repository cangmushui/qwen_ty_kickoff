#!/bin/bash
#SBATCH --job-name=Qwen-1.8B-forecast          # ��ҵ����
#SBATCH --output=Qwen.txt        # �����־���ļ���
#SBATCH --time=100000:00:00            # ִ��ʱ������Ϊ1Сʱ
#SBATCH --ntasks=1                 # ������Ϊ1
#SBATCH --cpus-per-task=2          # ÿ������ʹ��2�� CPU ����
#SBATCH --mem=64G                   # ÿ������ʹ��4G�ڴ�
#SBATCH --partition=gpujl          # ��������Ϊgpujl
#SBATCH --gres=gpu:1             # �����Ҫ��ʹ��1��GPU

echo "Hello World! Welcome to Slurm.------"
nvidia-smi                         # �鿴�������ڵ���Կ����
echo "CUDA_VISIBLE_DEVICES" $CUDA_VISIBLE_DEVICES # �鿴�Լ������䵽�������Կ��ϡ�
# cd ~/projects/diffuscene-cleaner/scripts

cmd="bash finetune_qlora_single_gpu_240521.sh -m ~/.cache/modelscope/hub/qwen/Qwen-1_8B-Chat-Int4 -d train.txt"
echo $cmd
eval $cmd

echo "Job completed successfully."
