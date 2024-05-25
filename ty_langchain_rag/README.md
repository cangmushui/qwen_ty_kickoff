# rag-retrieval

RAG向量召回示例

## 依赖

先安装适合自己环境的torch，再安装项目依赖:

```
pip install langchain langchain_community langchain_openai pypdf rapidocr-onnxruntime modelscope transformers faiss-cpu tiktoken -i https://mirrors.aliyun.com/pypi/simple/
```

如果有量化相关的报错，从源码安装vllm-gpts、auto-gtpq

## 用法

1，启动vllm的openai兼容server：

```
export VLLM_USE_MODELSCOPE=True
python -m vllm.entrypoints.openai.api_server --model 'qwen/Qwen-7B-Chat-Int4' --trust-remote-code -q gptq --dtype float16 --gpu-memory-utilization 0.6
```

2、运行indexer.py，解析pdf生成向量库

```
python indexer.py
```

```
(llm) (base) baitongyuan@node02:~/llm/qwen_ty_kickoff/ty_langchain_rag$ python indexer.py 
2024-05-25 16:56:15,323 - modelscope - INFO - PyTorch version 2.3.0+cu118 Found.
2024-05-25 16:56:15,323 - modelscope - INFO - Loading ast index from /home/baitongyuan/.cache/modelscope/ast_indexer
2024-05-25 16:56:15,477 - modelscope - INFO - Loading done! Current index file version is 1.14.0, with md5 e04a9f7a2366e8981cf40ef49327d4ba and a total number of 976 components indexed
2024-05-25 16:56:20,799 - modelscope - WARNING - Model revision not specified, use revision: v1.1.0
Downloading: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████| 886/886 [00:00<00:00, 105kB/s]
Downloading: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 2.08k/2.08k [00:00<00:00, 254kB/s]
Downloading: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████| 60.7k/60.7k [00:00<00:00, 1.28MB/s]
Downloading: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 388M/388M [00:22<00:00, 18.3MB/s]
Downloading: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████| 9.71k/9.71k [00:00<00:00, 1.27MB/s]
Downloading: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 112/112 [00:00<00:00, 15.1kB/s]
Downloading: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 332/332 [00:00<00:00, 46.5kB/s]
Downloading: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 107k/107k [00:00<00:00, 1.61MB/s]
2024-05-25 16:56:46,549 - modelscope - INFO - initiate model from /home/baitongyuan/.cache/modelscope/hub/iic/nlp_corom_sentence-embedding_chinese-base
2024-05-25 16:56:46,549 - modelscope - INFO - initiate model from location /home/baitongyuan/.cache/modelscope/hub/iic/nlp_corom_sentence-embedding_chinese-base.
2024-05-25 16:56:46,550 - modelscope - INFO - initialize model from /home/baitongyuan/.cache/modelscope/hub/iic/nlp_corom_sentence-embedding_chinese-base
2024-05-25 16:56:48,572 - modelscope - WARNING - No preprocessor field found in cfg.
2024-05-25 16:56:48,572 - modelscope - WARNING - No val key and type key found in preprocessor domain of configuration.json file.
2024-05-25 16:56:48,572 - modelscope - WARNING - Cannot find available config to build preprocessor at mode inference, current config: {'model_dir': '/home/baitongyuan/.cache/modelscope/hub/iic/nlp_corom_sentence-embedding_chinese-base'}. trying to build by task and model information.
2024-05-25 16:56:48,983 - modelscope - WARNING - No preprocessor field found in cfg.
2024-05-25 16:56:48,983 - modelscope - WARNING - No val key and type key found in preprocessor domain of configuration.json file.
2024-05-25 16:56:48,983 - modelscope - WARNING - Cannot find available config to build preprocessor at mode inference, current config: {'model_dir': '/home/baitongyuan/.cache/modelscope/hub/iic/nlp_corom_sentence-embedding_chinese-base', 'sequence_length': 128}. trying to build by task and model information.
/home/baitongyuan/anaconda3/envs/llm/lib/python3.8/site-packages/transformers/modeling_utils.py:993: FutureWarning: The `device` argument is deprecated and will be removed in v5 of Transformers.
  warnings.warn(
faiss saved!
```

3、运行rag.py，开始体验RAG增强检索

```
python rag.py
```
