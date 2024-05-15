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

import typing as tg

import appbuilder
import yaml

from .common import get_model_list, set_env


class PlayGround:
    """
    QianFan AppBuilder PlayGround Node
    SDK doc: https://cloud.baidu.com/doc/AppBuilder/s/zlqgd1ii7

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
                "model": (get_model_list(["chat"]),),
                "prompt_template": (
                    "STRING",
                    {
                        "multiline": True,  # True if you want the field to look like the one on the ClipTextEncode node
                        "default": r"请想象一幅包含 {object} 的画面，并用详尽的语言向我描述这幅画面的内容。",
                    },
                ),
                "params_yaml": (
                    "STRING",
                    {
                        "multiline": True,  # True if you want the field to look like the one on the ClipTextEncode node
                        "default": r"object: 春暖花开",
                    },
                ),
            },
        }

    # INPUT_IS_LIST = True

    # @classmethod
    # def IS_CHANGED(
    #     s,
    #     model: str,
    #     prompt_template: str,
    #     params_yaml: str,
    # ) -> tg.Hashable:
    #     """self defined input change detection function"""
    #     pass

    @classmethod
    def VALIDATE_INPUTS(
        s,
        model: str,
        prompt_template: str,
        params_yaml: str,
    ) -> tg.Literal[True] | str:
        """self defined validation function"""
        try:
            _ = yaml.safe_load(params_yaml)
        except Exception as e:
            return f"error parsing params_yaml: {repr(e)}"

        return True

    RETURN_TYPES = ("STRING",)
    # RETURN_NAMES = ("image_output_name",)
    # OUTPUT_IS_LIST = (True, )

    FUNCTION = "playground"

    # OUTPUT_NODE = False

    CATEGORY = "QianFan/AppBuilder"

    def playground(
        self,
        model: str,
        prompt_template: str,
        params_yaml: str,
    ) -> tuple[str]:
        """Execute appbuilder playground model"""
        set_env()

        play = appbuilder.Playground(prompt_template=prompt_template, model=model)
        params = appbuilder.Message(yaml.safe_load(params_yaml))
        resp = play(params, stream=False)
        return (resp.content,)
