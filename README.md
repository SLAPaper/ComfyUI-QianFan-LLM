# ComfyUI-QianFan-LLM

ComfyUI nodes utilizing LLM models on QianFan Platform （百度智能云千帆大模型平台）

## NOTICE: This Project is WIP, send issue if you want some missing features

## Pre-requisites

1. Clone into `custom_nodes` folder of ComfyUI
2. Install SDK(s) by running `python -m pip install -U -r requirements.txt`
3. Run ComfyUI first, and then edit `config.yaml` to fill in your own credentials
    1. [AppBuilder Credentials](https://cloud.baidu.com/doc/AppBuilder/s/Flpv3oxup)
    2. [QianFan Credentials](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/3lmokh7n6#%E3%80%90%E6%8E%A8%E8%8D%90%E3%80%91%E4%BD%BF%E7%94%A8%E5%AE%89%E5%85%A8%E8%AE%A4%E8%AF%81aksk%E9%89%B4%E6%9D%83%E8%B0%83%E7%94%A8%E6%B5%81%E7%A8%8B)

## Modules

### appbuilder （千帆AppBuilder）

Document: [千帆AppBuilder-SDK](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz)

Implemented: PlayGround

#### PlayGround

Inputs:

- model: selection of use model
- prompt_template: use in `str.format` to fill in params
- params: yaml format, parse into dict and send to `str.format`

![Snipaste_2024-01-22_01-47-43](https://github.com/SLAPaper/ComfyUI-QianFan-LLM/assets/7543632/1e42bb59-136d-49c0-b599-c7ee969fb673)

### qianfan （千帆大模型平台）

Document: [千帆大模型平台-SDK](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/wlmhm7vuo)

Implemented: Chat

#### Chat

Inputs:

- model: selection of use model
- current message: yaml format, list of dicts, `role` and `content` are required
- endpoint: optional, only activate when model set to ENDPOINT
- history messages: optional, yaml format, like current message

actually will concatenate history messages and current message, then send to model

![Snipaste_2024-01-22_01-46-53](https://github.com/SLAPaper/ComfyUI-QianFan-LLM/assets/7543632/618fad3c-ccff-4b26-82d1-02681f826076)

#### Completion

Document: [千帆大模型平台-SDK](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/vlmokjd30)

Inputs:

- model: selection of use model
- prompt: prompt text
- endpoint: optional, only activate when model set to ENDPOINT

![Snipaste_2024-01-22_03-48-08](https://github.com/SLAPaper/ComfyUI-QianFan-LLM/assets/7543632/a541431d-c872-4f1a-bcd2-48114fbe96d9)
