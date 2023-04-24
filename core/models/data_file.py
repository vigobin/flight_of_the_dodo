#!/usr/bin/env python3

from pathlib import Path

class DataRetrieverTool:
    """UTILITY CLASS TO RETRIEVE CONTENTS OF EXTERNAL DATAFILE"""
    FNF_ERROR_MESSAGE = '{} "{}" DOES NOT EXIST.'

    @classmethod
    def get_file_data(cls, name=""):
        file_obj = Path(name)
        if not file_obj.exits():
            raise FileNotFoundError(
                FNF_ERROR_MESSAGE.format(
                    purpose,
                    name
                )
            )
        else:
            return file_obj.read_text()
