"""
编写服务端接口
"""
from django.http import JsonResponse
from django.shortcuts import render


def login_page(request):
    return render(request, 'login.html')


# 定义一个服务器接口，访问index.html文件
def go_index(request):
    """
    render函数：django提供的方法，实现访问某个页面， 核心参数：
    1.request
    2.页面访问路径
    """
    return render(request, 'index.html')
