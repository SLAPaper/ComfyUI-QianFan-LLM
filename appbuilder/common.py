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

import appbuilder

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

    os.environ["APPBUILDER_TOKEN"] = QIANFAN_CONFIG.get("appbuilder_api_key")


set_env()


def get_model_list(api_type_filter=list[str]) -> list[str]:
    """Get model list from AppBuilder"""
    set_env()

    res = [
        "ERNIE-4.0-8K",
        "ERNIE-3.5-8K",
        "ERNIE-Speed-8K",
        "ERNIE-Speed-128K（预览版）",
        "ERNIE-Lite-8K",
        "ERNIE-Tiny-8K",
        "ERNIE-Character-8K",
        "ERNIE-Functions-8K",
        "ERNIE Speed-AppBuilder",
        "ERNIE-Bot 4.0",
        "ERNIE-Bot",
        "ERNIE-Speed",
        "EB-turbo-AppBuilder专用版",
    ]

    try:
        return sorted(
            model
            for model in appbuilder.get_model_list(
                api_type_filter=api_type_filter, is_available=True
            )
        )
    except Exception as e:
        logging.warn(
            f"Failed to get model list, will return default model list, reason: {repr(e)}"
        )

    return res
