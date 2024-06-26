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

from .dialog_summary import DialogSummary
from .playground import PlayGround

_NODE_CLASS_MAPPINGS = {
    "QianFan AB Playground": PlayGround,
    "QianFan AB Dialog Summary": DialogSummary,
}

_NODE_DISPLAY_NAME_MAPPINGS = {
    "QianFan AB Playground": "QianFan AppBuilder Playground",
    "QianFan AB Dialog Summary": "QianFan AppBuilder Dialog Summary",
}

__all__ = ["_NODE_CLASS_MAPPINGS", "_NODE_DISPLAY_NAME_MAPPINGS"]
