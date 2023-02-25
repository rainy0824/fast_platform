#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/7/8 15:03 
# ide： PyCharm
from typing import Union, List, Dict

from fastapi import status
from fastapi.responses import JSONResponse, Response


def resp_result(*, code=200,data: Union[list, dict, str]=None,message="Success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': code,
            'message': message,
            'data': data,
            'detail':message
        }
    )

def resp_failed(*, status_code=400,data: Union[list, dict, str]=None,message="failed") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': status_code,
            'message': message,
            'data': data,
        }
    )