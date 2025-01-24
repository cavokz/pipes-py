# Copyright 2025 Elasticsearch B.V.
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

"""Elastic Pipes component to export data from the Pipes state."""

from . import Pipe
from .util import get_field, serialize_yaml


@Pipe("elastic.pipes.core.export")
def main(pipe, dry_run=False):
    file_name = pipe.config("file")
    field = pipe.config("field", None)

    if dry_run:
        return

    if field in (None, "", "."):
        pipe.logger.info(f"exporting everything to '{file_name}'...")
    else:
        pipe.logger.info(f"exporting '{field}' to '{file_name}'...")
    value = get_field(pipe.state, field)

    with open(file_name, "w") as f:
        serialize_yaml(f, value)
