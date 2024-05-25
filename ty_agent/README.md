# agent

基于qwen的agent demo，支持历史对话, agent能使用的工具是一个免费搜索工具, 基于阿里云百炼的通义千问200B大模型(做agent的参数量70B起步)

# 依赖

基于阿里云百炼的通义千问200B大模型
pip install broadscope_bailian

现在这个模型访问貌似要收费了?从这个demo中学习一下代码怎么写还有prompt怎么写就好

# 分析

作者的正常返回大概是这样

```
question: 青岛明天天气如何?

...等待LLM返回, 请求prompt如下...

Today is 2024-05-25. Please Answer the following questions as best you can. You have access to the following tools:

tavily_search_results_json: 这是一个类似谷歌和百度的搜索引擎，搜索知识、天气、股票、电影、小说、百科等都是支持的哦，如果你不确定就应该搜索一下，谢谢！s,args: [{"name": "query", "description": "search query to look up", "type": "string"}]

These are chat history before:


Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [tavily_search_results_json]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

question: 青岛明天天气如何?


...LLM返回轮数一, 根据用户的query构造上述模板的prompt, 然后请求LLM得到...
Thought:需要查询青岛明天的天气预报
Action: tavily_search_results_json
Action Input:{"query":"青岛 明日 天气预报”}
...工具使用,并打印结果
Observation: xxxxxxxxxxxxxxxxxxxxxxxxxxx(很长, 很乱, 很杂)

...(实际情况可能有多轮请求)...

...LLM返回轮数二, 将上一步得到的Thought, Action, Action Input, Observation加到prompt并再次请求LLM...
Thought: 根据搜索结果, 我可以得到青岛的天气预报
Final Answer: 青岛明天(2024年02月2日)的天气预报显示为多云，气温较低，最低温度约为'℃ 最高温度为·2℃ 风力为4.5级。由于天气寒冷且风力较强，请注意保暖并考虑在室内进行活动。

...进入下一个用户问题...
question:

```
