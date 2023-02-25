# -*- coding: utf-8 -*-
# @Time    : 2022/11/11 18:45
# @Author  : sunxuan
# @Site    : #处理异步http请求
# @File    : AsyncHttpRequest.py
import json
import time

import aiohttp
from aiohttp.formdata import FormData

from backend.common.enums.request_emus import BodyType


class AsyncHttpRequest(object):
    def __init__(self, url, time_out=200, **kwargs):
        self.url = url
        self.kwargs = kwargs
        self.time_out = aiohttp.ClientTimeout(total=time_out)
        self.proxy = None
        self.cookies = None

    def get_cookies(self, session):
        self.cookies = session.cookie_jar.filter_cookies(self.url)
        return {k: v.value for k, v in self.cookies.items()}

    def get_request_data(self, **kwargs):
        '''判断传过来的类型 json 就返回json'''
        if kwargs.get('json') is not None:
            result = kwargs.get('json')
        else:
            result = kwargs.get('data')
        print(f'get_result_data:{result}')
        return result

    @staticmethod
    async def handle_request_data(body):

        if isinstance(body, bytes):
            body = body.decode()
        elif isinstance(body, FormData):
            body = str(body)
        elif isinstance(body, str) or body is None:
            return body
        return json.dumps(body, ensure_ascii=False, indent=4)

    @staticmethod
    async def get_resp(resp):
        '''
        Args:
            resp (): 响应对象
        Returns:
            json格式 返回true
            其他格式 返回false
        '''
        try:
            encode_data = await  resp.json(encoding='utf-8')
            data = json.dumps(encode_data, ensure_ascii=False, indent=4)
            return data, True
        except:
            data = await  resp.text()
            return data, False

    @staticmethod
    async def handle_resp(status, request_data, status_code=200, request_headers=None, response=None,
                    response_headers=None, cookies=None, elapsed=None, msg="success", **kwargs):
        '''重新组装请求
        Args:
            status (): 200:true    other: false
            request_data (): 请求入参
            status_code ():请求结果状态码
            request_headers ():
            response (): 相应结果
            response_headers ():
            cookies ():
            elapsed (): 耗时
            msg (): 错误信息
            **kwargs ():
        Returns:
        '''
        request_headers = json.dumps({
                                         k: v for k, v in request_headers.items()
                                     } if request_headers is not None else {})

        response_headers = json.dumps({
                                          k: v for k, v in response_headers.items()
                                      } if response_headers is not None else {})
        cookies = json.dumps({k: v for k, v in cookies.items()} if cookies is not None else {})
        return {
            "status": status,
            "response": response,
            "status_code": status_code,
            "request_data": await AsyncHttpRequest.handle_request_data(request_data),
            "request_headers": request_headers,
            "response_headers": response_headers,
            "cookies": cookies,
            "msg": msg,
            "cost": elapsed,
            **kwargs

        }

    async def aio_request(self, method: str) ->dict :
        '''发送异步请求'''
        start = time.time()
        async  with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
            async with session.request(method=method, url=self.url, timeout=self.time_out,
                                       **self.kwargs) as resp:
                print('sta:',resp.status)
                response, json_is_format = await  AsyncHttpRequest.get_resp(resp)
                print(f'response:{json_is_format},{session}')
                cookie = self.get_cookies(session)
                print(f'cookies:{cookie}')

                if resp.status != 200:  # 非200状态
                    return await self.handle_resp(False, request_data=self.get_request_data(**self.kwargs), status_code=resp.status,
                                                  request_headers=resp.request_info.headers,response_headers=resp.headers,response=response,msg='http请求不为200')
                cost = "%.0fms" % ((time.time() - start) * 1000)
                # 200状态
                return await self.handle_resp(status=True, status_code=resp.status,
                                              request_data=self.get_request_data(**self.kwargs),
                                              request_headers=resp.request_info.headers,
                                              response_headers=resp.headers,
                                              response=response,
                                              cookies=cookie,
                                              json_is_format=json_is_format,
                                              cost=cost

                                              )

    async def download(self):
        async  with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
            async  with session.request('GET', self.url, time_out=self.time_out, proxy=self.proxy, ssl=False,
                                        **self.kwargs) as resp:
                if resp.status != 200:
                    raise Exception("下载失败")
                return await resp.content.read()

    @staticmethod
    async def handle_client(url: str, body_type: BodyType = BodyType.json, time_out=20, **kwargs):
        '''

        Args:
            url (): 请求url
            body_type (): 请求数据类型
            time_out ():
            **kwargs (): data headers 等等

        Returns: AsyncHttpRequest instance

        '''
        if not url.startswith('http'):
            raise Exception('请输入正确的url')
        headers = kwargs.get('headers', {})
        if body_type == BodyType.json:  # json格式
            if "Content-Type" not in headers:
                headers['Content-Type'] = 'application/json'
            try:
                json_data = kwargs.get('body')
                if json_data:
                    json_data = json.loads(json_data)
                res = AsyncHttpRequest(url=url, headers=headers, time_out=time_out, json=json_data)
            except Exception as e:
                raise Exception(f'json数据格式错误:{e}')
        elif body_type == BodyType.form:  # form格式 可上传文件
            try:
                fm=None
                form_data = kwargs.get('body')
                if form_data:
                    fm= FormData()
                    form_data = json.loads(form_data)
                    for item in form_data:
                        if item.get('type') =='TEXT':#文本类型
                            fm.add_field(item.get('key'),item.get('value',{}))
                        else:
                            pass
                    print(fm)
                res = AsyncHttpRequest(url=url,headers=headers,time_out=time_out,data=fm)
            except Exception as e:
                raise Exception(f'form数据格式错误:{e}')
        elif body_type ==BodyType.x_form:#x_form 只能以kv上传
            try:
                x_form_data =str(kwargs.get('body',"{}")) #返回一个string
                new_form_data =json.loads(x_form_data)
                print(f'new_form:{new_form_data}')
                res =AsyncHttpRequest(url=url,headers=headers,time_out=time_out,data=new_form_data)
            except Exception as e:
                raise Exception(f'x_form_data格式错误:{e}')
        else:
            #get请求
           res =AsyncHttpRequest(url=url,headers=headers,time_out=time_out,data=kwargs.get('body'))
        return  res




