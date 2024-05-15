# Copyright 2024 SLAPaper
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import typing as tg

import qianfan
import qianfan.resources
import yaml

from ..config import QIANFAN_CONFIG, reload_config

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
)
ch.setFormatter(formatter)
logger.addHandler(ch)


def set_env():
    """Set environment vars"""
    reload_config()

    os.environ["QIANFAN_ACCESS_KEY"] = QIANFAN_CONFIG.get("iam_ak")
    os.environ["QIANFAN_SECRET_KEY"] = QIANFAN_CONFIG.get("iam_sk")


set_env()


class Chat:
    """
    QianFan Chat Node
    SDK doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/xlmokikxe

    Class methods
    -------------
    INPUT_TYPES (dict):
        Tell the main program input parameters of nodes.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of each element in the output tulple.
    RETURN_NAMES (`tuple`):
        Optional: The name of each output in the output tulple.
    FUNCTION (`str`):
        The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run Example().execute()
    OUTPUT_NODE ([`bool`]):
        If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
        The backend iterates on these output nodes and tries to execute all their parents if their parent graph is properly connected.
        Assumed to be False if not present.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    execute(s) -> tuple || None:
        The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
        For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Return a dictionary which contains config for all input fields.
        Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
        Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
        The type can be a list for selection.

        Returns: `dict`:
            - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
            - Value input_fields (`dict`): Contains input fields config:
                * Key field_name (`string`): Name of a entry-point method's argument
                * Value field_config (`tuple`):
                    + First value is a string indicate the type of field or a list for selection.
                    + Secound value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "model": (
                    [
                        "DEFAULT",
                        *sorted(qianfan.ChatCompletion.models()),
                        "ENDPOINT",
                    ],
                ),
                "messages_yaml": (
                    "STRING",
                    {
                        "multiline": True,  # True if you want the field to look like the one on the ClipTextEncode node
                        "default": r"""- role: user
  content: 请想象一幅包含 春暖花开 的画面，并用详尽的语言向我描述这幅画面的内容。""",
                    },
                ),
            },
            "optional": {
                "endpoint": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "history_yaml": (
                    "STRING",
                    {
                        "multiline": True,  # True if you want the field to look like the one on the ClipTextEncode node
                        "default": r"""- role: user
  content: 你是一名幻想家，请帮助我想象一个场景，并描述这个场景。
- role: assistant
  content: 好的，我会帮助你的，请告诉我你需要怎样的场景。""",
                    },
                ),
            },
        }

    # INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(
        s,
        model: str,
        messages_yaml: str,
        endpoint: str | None,
        history_yaml: str | None,
    ) -> tg.Literal[True] | str:
        """self defined validation function"""
        if model == "ENDPOINT" and not endpoint:
            return "endpoint model requires an endpoint"

        try:
            _ = yaml.safe_load(messages_yaml)
        except Exception as e:
            return f"error parsing messages_yaml: {repr(e)}"

        if history_yaml:
            try:
                _ = yaml.safe_load(history_yaml)
            except Exception as e:
                return f"error parsing history_yaml: {repr(e)}"

        return True

    RETURN_TYPES = ("STRING", "STRING")

    RETURN_NAMES = ("result", "history_yaml")
    # OUTPUT_IS_LIST = (True, )

    FUNCTION = "chat"

    # OUTPUT_NODE = False

    CATEGORY = "QianFan"

    def chat(
        self,
        model: str,
        messages_yaml: str,
        endpoint: str | None,
        history_yaml: str | None,
    ) -> tuple[str]:
        """Execute appbuilder playground model"""
        set_env()

        chat_comp = qianfan.ChatCompletion()

        messages: list[dict] = yaml.safe_load(messages_yaml)
        if history_yaml:
            history: list[dict] = yaml.safe_load(history_yaml)
            messages = history + messages

        match model:
            case "DEFAULT":
                resp = chat_comp.do(messages=messages)
            case "ENDPOINT":
                resp = chat_comp.do(endpoint=endpoint, messages=messages)
            case _:
                resp = chat_comp.do(model=model, messages=messages)

        res: str = resp["result"]

        new_history = messages + [{"role": "assistant", "content": res}]

        return (
            res,
            yaml.safe_dump(new_history, allow_unicode=True),
        )


class Completion:
    """
    QianFan Completion Node
    SDK doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/vlmokjd30

    Class methods
    -------------
    INPUT_TYPES (dict):
        Tell the main program input parameters of nodes.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of each element in the output tulple.
    RETURN_NAMES (`tuple`):
        Optional: The name of each output in the output tulple.
    FUNCTION (`str`):
        The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run Example().execute()
    OUTPUT_NODE ([`bool`]):
        If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
        The backend iterates on these output nodes and tries to execute all their parents if their parent graph is properly connected.
        Assumed to be False if not present.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    execute(s) -> tuple || None:
        The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
        For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Return a dictionary which contains config for all input fields.
        Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
        Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
        The type can be a list for selection.

        Returns: `dict`:
            - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
            - Value input_fields (`dict`): Contains input fields config:
                * Key field_name (`string`): Name of a entry-point method's argument
                * Value field_config (`tuple`):
                    + First value is a string indicate the type of field or a list for selection.
                    + Secound value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "model": (
                    [
                        "DEFAULT",
                        *sorted(qianfan.Completion.models()),
                        "ENDPOINT",
                    ],
                ),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,  # True if you want the field to look like the one on the ClipTextEncode node
                        "default": r"""请想象一幅包含 春暖花开 的画面，并用详尽的语言向我描述这幅画面的内容。画面：""",
                    },
                ),
            },
            "optional": {
                "endpoint": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
            },
        }

    # INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(
        s,
        model: str,
        prompt: str,
        endpoint: str | None,
    ) -> tg.Literal[True] | str:
        """self defined validation function"""
        if model == "ENDPOINT" and not endpoint:
            return "ENDPOINT model requires an endpoint"

        return True

    RETURN_TYPES = ("STRING",)

    RETURN_NAMES = ("result",)
    # OUTPUT_IS_LIST = (True, )

    FUNCTION = "completion"

    # OUTPUT_NODE = False

    CATEGORY = "QianFan"

    def completion(
        self,
        model: str,
        prompt: str,
        endpoint: str | None,
    ) -> tuple[str]:
        """Execute appbuilder playground model"""
        set_env()

        comp = qianfan.Completion()

        match model:
            case "DEFAULT":
                resp = comp.do(prompt=prompt)
            case "ENDPOINT":
                resp = comp.do(endpoint=endpoint, prompt=prompt)
            case _:
                resp = comp.do(model=model, prompt=prompt)

        res: str = resp["result"]

        return (res,)


_NODE_CLASS_MAPPINGS = {
    "QianFan Chat": Chat,
    "QianFan Completion": Completion,
}

_NODE_DISPLAY_NAME_MAPPINGS = {
    "QianFan Chat": "QianFan Chat",
    "QianFan Completion": "QianFan Completion",
}

__all__ = ["_NODE_CLASS_MAPPINGS", "_NODE_DISPLAY_NAME_MAPPINGS"]
