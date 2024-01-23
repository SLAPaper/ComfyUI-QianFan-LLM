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

import appbuilder
import json

from .common import set_env


class DialogSummary:
    """
    QianFan AppBuilder DialogSummary Node
    SDK doc: https://cloud.baidu.com/doc/AppBuilder/s/Elqgd1hfp
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Return a dictionary which contains config for all input fields.
        """
        return {
            "required": {
                "model": (["eb-turbo-appbuilder", "ernie-bot-4"],),
                "dialog": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": r"""用户:喂我想查一下我的话费
坐席:好的女士您话费余的话还有87.49元钱
用户:好的知道了谢谢
坐席:嗯不客气祝您生活愉快再见""",
                    },
                ),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "needs",
        "response",
        "solution",
        "raw_response",
    )

    FUNCTION = "dialog_summary"

    CATEGORY = "QianFan/AppBuilder"

    def dialog_summary(
        self,
        model: str,
        dialog: str,
    ) -> tuple[str, str, str, str]:
        """Execute appbuilder dialog_summary model"""
        set_env()

        ds = appbuilder.DialogSummary(model=model)
        params = appbuilder.Message(dialog)
        resp = ds(params, stream=False)
        data = json.loads(resp.content)

        return (
            data["诉求"],
            data["回应"],
            data["解决情况"],
            resp.content,
        )
