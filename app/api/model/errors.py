# coding:utf-8
from enum import Enum, unique
from flask import jsonify

@unique
class ResponseCode(Enum):
    OK = {"200": "成功"}
    SUCCESS = {"000001": "成功"}
    FAIL = {"000000": "失败"}
    PARAM_IS_NULL = {"000002": "请求参数为空"}
    PARAM_ILLEGAL = {"000003": "请求参数非法"}
    JSON_PARSE_FAIL = {"000004": "JSON转换失败"}
    REPEATED_COMMIT = {"000005": "重复提交"}
    SQL_ERROR = {"000006": "数据库异常"}
    NOT_FOUND = {"000007": "无记录"}
    NETWORK_ERROR = {"000015": "网络异常"}
    UNKNOWN_ERROR = {"000099": "未知异常"}
    LOGIN_ERROR = {"000100": "用户名或者密码错误"}
    PHONE_EXIST_ERROR = {"000101": "手机号已存在"}
    PASSWORD_ERROR = {"000102": "原始密码错误"}

    def get_code(self):
        """
        根据枚举名称取状态码code
        :return: 状态码code
        """
        return list(self.value.keys())[0]

    def get_msg(self):
        """
        根据枚举名称取状态说明message
        :return: 状态说明message
        """
        return list(self.value.values())[0]

# 状态码以及默认的信息
class ResponseResult:

    # 处理成功
    @staticmethod
    def success(data=None,page=None,responseCode = ResponseCode.OK):
        return {
            'data': data,
            'page':page,
            'msg': responseCode.get_msg(),
            'code': responseCode.get_code()
        }

    # 异常
    @staticmethod
    def error(responseCode = ResponseCode.FAIL):
        return {
            'msg': responseCode.get_msg(),
            'code': responseCode.get_code()
        }

    @staticmethod
    def lay_success(data,count):
        return {
            'code':0,
            'data':data,
            'count':count
        }



if __name__ == "__main__":
    print(ResponseResult.success())
