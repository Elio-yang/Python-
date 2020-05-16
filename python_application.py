# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import requests
# ========================= 信息 =================================
username = "yangyang1519"                   # 账号
pwd = "Yang882323"                          # 密码
recv_qq = "2925539854"                      # 接收反馈的QQ
loading_time = 5                            # 预留页面加载时间5秒 
# ========================= url ===================================
login_url = "https://ehall.jlu.edu.cn/jlu_portal/login"             # 登录url
remind_url = "https://ehall.jlu.edu.cn/taskcenter/workflow/done"    # 登录url
# ========================= xpath =================================
uid_xpath = './/input[@name="username"]'                        # 账号xpath
pwd_xpath = './/input[@name="password"]'                        # 密码xpath
button_xpath = './/input[@name="login_submit"]'                 # 登录按钮xpath
stu_xpath ='.//*[@id="cont_one_1"]/li[4]/a'                     # 本科生健康打卡按钮xpath
handle_xpath = './/*[@id="service_guide"]/div/div/input[3]'     # 我要办理按钮xpath
checkbox_xpath = './/*[@id="V1_CTRL82"]'                        # 承诺按钮xpath
confirm_xpath = './/*[@id="form_command_bar"]/li[1]'            # 确认按钮xpath
ok_xpath = './/button[1]'                                       # 好按钮xpath
# ========================= 驱动 ===================================
global driver
driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")  # 设置Chrome驱动
 
 
def web_init():
    driver.maximize_window()                    # 最大化窗口
    driver.implicitly_wait(6)                   # 隐式等待
    driver.get(login_url)                       # 获取网页
 
 
def web_close():
    driver.quit()                               # 关闭所有关联的窗口
 
 
def web_load():
    time.sleep(loading_time)                    # 预留页面加载时间5秒
 
 
def auto_login(username_, pwd_, uid_xpath_, pwd_xpath_, button_xpath_):
    web_load()
    driver.find_element_by_xpath(uid_xpath_).clear()                    # 清空已存在内容
    driver.find_element_by_xpath(uid_xpath_).send_keys(username_)       # 传入用户名
    web_load()
    driver.find_element_by_xpath(pwd_xpath_).clear()                    # 清空已存在内容
    driver.find_element_by_xpath(pwd_xpath_).send_keys(pwd_)            # 传入密码
    web_load()
    driver.find_element_by_xpath(button_xpath_).click()                 # 通过登录按钮并单击登录
 
 
def submit(stu_xpath_, handle_xpath_, checkbox_xpath_, confirm_xpath_, ok_xpath_):
    driver.find_element_by_xpath(stu_xpath_).click()                    # 本科生健康状况申报
    web_load()
    driver.find_element_by_xpath(handle_xpath_).click()                 # 我要办理
    web_load()
    driver.switch_to.window(driver.window_handles[1])                   # 切换窗口句柄至最新窗口
    web_load()
    driver.find_element_by_xpath(checkbox_xpath_).click()               # 本人承诺以上填写内容均真实可靠
    web_load()
    driver.find_element_by_xpath(confirm_xpath_).click()                # 确认填报
    web_load()
    time.sleep(4) 
    driver.find_element_by_xpath(ok_xpath_).click()                     # 好
    
    web_load()
 
 
def remind(remind_url_, recv_qq_):
    driver.get(remind_url_)                                             # 获取网页
    web_load()
    row = driver.find_elements_by_tag_name('tr')
    result_list = []
    for i in row:
        j = i.find_elements_by_tag_name('td')
        for item in j:
            text = item.text
            result_list.append(text)
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    result_msg = today+'杨扬打卡完成，本人和亲属未有计划48小时内从境外返回长春'
    print(result_msg)
    send_private_msg(recv_qq_, result_msg)                              # 发送最近的一条打卡记录
 
 
def send_private_msg(qq, msg):
    func = "send_private_msg"
    qq_url = "http://localhost:5700/" + func
    params = {
        'user_id': qq,
        'message': msg,
    }
    req = requests.get(qq_url, params)                                  # 调用酷Q发送消息至接收用户
    print(req.status_code)                              
 
 
if __name__ == '__main__':
    web_init()                                                                  # 驱动初始化
    auto_login(username, pwd, uid_xpath, pwd_xpath, button_xpath)               # 登录操作
    submit(stu_xpath, handle_xpath, checkbox_xpath, confirm_xpath, ok_xpath)    # 提交操作
    remind(remind_url, recv_qq)                                                 # 发送提醒信息
    web_close()                                                                 # 测试结束