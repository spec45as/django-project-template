# coding: utf-8

import os
from hashlib import md5


def upload_to(directory=None):
    """Загрузить файл в директорию `directory` с хешированным именем."""

    def uploader(instance, filename):
        ext = os.path.splitext(filename)[1]
        h = md5(filename.encode('utf-8')).hexdigest()
        parts = [h[:2], h[2:4], h + ext]
        if directory is not None:
            parts.insert(0, directory)
        return '/'.join(parts)

    return uploader
