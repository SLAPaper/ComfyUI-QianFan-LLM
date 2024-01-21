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


import pathlib

import yaml

# Load or create yaml config
config_path = pathlib.Path(__file__).parent / "config.yaml"

QIANFAN_CONFIG = {}


def reload_config():
    """Reload config from yaml file"""
    global QIANFAN_CONFIG

    if not config_path.exists():
        QIANFAN_CONFIG = {
            "appbuilder_api_key": "your appbuilder API key",
            "iam_ak": "your iam ak",
            "iam_sk": "your iam sk",
        }
        config_path.write_text(yaml.safe_dump(QIANFAN_CONFIG, sort_keys=False))
    else:
        with open(config_path, "r") as f:
            QIANFAN_CONFIG = yaml.safe_load(f)


reload_config()

__all__ = ["QIANFAN_CONFIG", "reload_config"]
