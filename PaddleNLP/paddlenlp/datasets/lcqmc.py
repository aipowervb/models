# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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

import copy
import collections
import io
import os
import warnings

from paddle.io import Dataset
from paddle.dataset.common import md5file
from paddle.utils.download import get_path_from_url
from paddlenlp.utils.env import DATA_HOME

from .dataset import TSVDataset

__all__ = ['LCQMC']


class LCQMC(TSVDataset):
    """
    LCQMC:A Large-scale Chinese Question Matching Corpus
    More information please refer to `https://www.aclweb.org/anthology/C18-1166/`


    """

    URL = "https://bj.bcebos.com/paddlehub-dataset/lcqmc.tar.gz"
    MD5 = "62a7ba36f786a82ae59bbde0b0a9af0c"
    MODE_INFO = collections.namedtuple(
        'MODE_INFO', ('file', 'md5', 'field_indices', 'num_discard_samples'))
    MODES = {
        'train': MODE_INFO(
            os.path.join('lcqmc', 'train.tsv'),
            '2193c022439b038ac12c0ae918b211a1', (0, 1, 2), 1),
        'dev': MODE_INFO(
            os.path.join('lcqmc', 'dev.tsv'),
            'c5dcba253cb4105d914964fd8b3c0e94', (0, 1, 2), 1),
        'test': MODE_INFO(
            os.path.join('lcqmc', 'test.tsv'),
            '8f4b71e15e67696cc9e112a459ec42bd', (0, 1, 2), 1)
    }

    def __init__(self,
                 mode='train',
                 data_file=None,
                 return_all_fields=False,
                 **kwargs):
        if return_all_fields:
            segments = copy.deepcopy(self.__class__.MODES)
            mode_info = list(modes[mode])
            mode_info[2] = None
            modes[mode] = self.MODE_INFO(*mode_info)
            self.MODES = segments

        self._get_data(data_file, mode, **kwargs)

    def _get_data(self, data_file, mode, **kwargs):
        default_root = DATA_HOME
        filename, data_hash, field_indices, num_discard_samples = self.MODES[
            mode]
        fullname = os.path.join(
            default_root, filename) if data_file is None else os.path.join(
                os.path.expanduser(data_file), filename)
        if not os.path.exists(fullname) or (data_hash and
                                            not md5file(fullname) == data_hash):
            if data_file is not None:  # not specified, and no need to warn
                warnings.warn(
                    'md5 check failed for {}, download {} data to {}'.format(
                        filename, self.__class__.__name__, default_root))
            path = get_path_from_url(self.URL, default_root, self.MD5)
            fullname = os.path.join(default_root, filename)
        super(LCQMC, self).__init__(
            fullname,
            field_indices=field_indices,
            num_discard_samples=num_discard_samples,
            **kwargs)

    def get_labels(self):
        """
        Return labels of the LCQMC object.
        """
        return ["0", "1"]


if __name__ == "__main__":
    ds = LCQMC('train', return_all_fields=True)

    for idx, data in enumerate(ds):
        if idx >= 3:
            break
        print(data)
