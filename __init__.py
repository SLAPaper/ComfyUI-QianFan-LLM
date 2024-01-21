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

from .appbuilder import (
    _NODE_CLASS_MAPPINGS as appbuilder_node_class,
    _NODE_DISPLAY_NAME_MAPPINGS as appbuilder_node_display,
)

from .qianfan import (
    _NODE_CLASS_MAPPINGS as qianfan_node_class,
    _NODE_DISPLAY_NAME_MAPPINGS as qianfan_node_display,
)

NODE_CLASS_MAPPINGS = {**appbuilder_node_class, **qianfan_node_class}
NODE_DISPLAY_NAME_MAPPINGS = {**appbuilder_node_display, **qianfan_node_display}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

