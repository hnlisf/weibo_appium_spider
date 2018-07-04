import time
from random import choice
from PIL import Image
from traceback import format_exc
from app_conner import Apper
from chaojiying import Chaojiying_Client
from loggers import MyLogger


platformName = 'Android'
platformVersion = '4.4.2'
deviceName = 'Android Emulator'
appPackage = 'com.sina.weibo'
appActivity = 'com.sina.weibo.SplashActivity'
comments_file=open('reason_comments.txt',mode='r',encoding='utf-8')
comments_list=comments_file.readlines()
comments_file.close()

class AppLoginer:
    def __init__(self):
        self.apper =  Apper(platformName, platformVersion, deviceName, appPackage, appActivity)
        self.driver= self.apper.driver
        # 打码平台客户端
        self.chaojiying = Chaojiying_Client('用户名', '密码', '软件id')
        self.logger = MyLogger('weibo','./weibog_log.txt')

    # 登录用户
    def login(self,username,password):
        login_status = True
        self.driver.implicitly_wait(20)
        # 点击登录按钮，进入登录页面
        self.driver.find_element_by_id('com.sina.weibo:id/titleSave').click()

        # 等待点击登录的出现，最长等待10秒
        self.driver.implicitly_wait(20)
        #点击文本框，删除文本框内容
        username_input= self.driver.find_element_by_id('com.sina.weibo:id/etLoginUsername')
        username_input.click()
        context= username_input.get_attribute('text')
        self.driver.keyevent(123)
        for i in range(0,len(context)):
            self.driver.keyevent(67)

        # 输入用户名
        username_input.send_keys(username)

        # 清空密码框
        password_input = self.driver.find_element_by_id('com.sina.weibo:id/etPwd')
        password_input.clear()

        # 输入密码
        password_input.send_keys(password)

        # 点击登录，进行登录
        self.driver.find_element_by_id('com.sina.weibo:id/bnLogin').click()
        # 等待点击验证码元素的出现，最长等待20秒
        self.driver.implicitly_wait(20)

        # 获得和输入验证码
        self._input_code()

        error_account_tags = self.driver.find_elements_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.TextView')
        # 是否存在异常账号：
        if len(error_account_tags) > 0:
            print(error_account_tags[0].text)
            if len(error_account_tags[0].text) == 4:
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.TextView[1]').click()
                login_status = False
            # 评分界面
            if len(error_account_tags[0].text) == 5:
                self.driver.find_element_by_id( 'com.sina.weibo:id/btn_3').click()

        if login_status:
                # 点击进入微博
                login_tags = self.driver.find_elements_by_id('com.sina.weibo:id/iv_navigater_clickable')
                if len(login_tags)>0:
                    self.driver.find_element_by_id('com.sina.weibo:id/iv_navigater_clickable').click()
                self.driver.implicitly_wait(20)

                # 取消更新app
                # self.apper.driver.keyevent(4)
                update_tags = self.driver.find_elements_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.TextView[1]')
                if len(update_tags)>0:
                    self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.TextView[1]').click()

                self.driver.implicitly_wait(20)
        return login_status
    # 注销用户
    def login_out(self):
        # 点击我的资料
        self.driver.find_element_by_xpath('//android.view.View[@content-desc="我的资料"]').click()
        self.driver.implicitly_wait(20)

        # 点击设置
        self.driver.find_element_by_id('com.sina.weibo:id/titleSave').click()
        self.driver.implicitly_wait(20)

        # 点击账号管理
        self.driver.find_element_by_id('com.sina.weibo:id/accountLayout').click()
        self.driver.implicitly_wait(20)

        # 点击注销账号
        self.driver.find_element_by_id('com.sina.weibo:id/exitAccountContent').click()
        self.driver.implicitly_wait(20)

        # 点击确认退出
        self.driver.find_element_by_xpath('	/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout'
                                          '/android.widget.FrameLayout/android.widget.LinearLayout/'
                                          'android.widget.LinearLayout[2]/android.widget.TextView[2]').click()
        self.driver.implicitly_wait(10)
    # 点击获取app验证码图片和输入验证码
    def _input_code(self):
        pic_id = '1'
        while len(self.driver.find_elements_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/'
                                          'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]'
                                          '/android.widget.TextView[2]'))>0 or pic_id=='1':
                title=self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.TextView').text

                if len(title)==4:
                    self.logger.write('info','当前用户账号异常')
                    break
                if pic_id !='1':
                    print('验证码%s错误'%pic_id)
                    self.logger.write('info','验证码%s错误'%pic_id)
                    self.chaojiying.ReportError(pic_id)
                    time.sleep(0.5)
                # 点击换验证码
                self.driver.find_element_by_id('com.sina.weibo:id/tv_change_image').click()

                time.sleep(1)
                # 验证码截图
                self.driver.save_screenshot('./screen.png')
                # 验证码图片显示标签
                code_image_element = self.driver.find_element_by_id('com.sina.weibo:id/iv_access_image')
                time.sleep(0.5)
                # 标签位置
                location = code_image_element.location
                # 标签大小
                size = code_image_element.size
                # 验证码图片在屏幕的四个坐标
                box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])


                # 截取图片
                image = Image.open('./screen.png')
                newImage = image.crop(box)
                newImage.save('./code.png')

                # 获得打码平台验证码
                pic_id,code = self._get_code()
                if code:
                    # 输入验证码
                    self.driver.find_element_by_id('com.sina.weibo:id/et_input').send_keys(code)

                # 点击确认按钮
                self.driver.find_element_by_xpath('	/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/'
                                                  'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]'
                                                  '/android.widget.TextView[2]').click()
                time.sleep(0.5)
                self.driver.implicitly_wait(20)
    # 获得打码平台验证码
    def _get_code(self):

        im = open('code.png', 'rb').read()
        code_json=self.chaojiying.PostPic(im, 1902)
        code = code_json.get('pic_str')
        pic_id = code_json.get('pic_id')
        return pic_id,code

    # 转发操作
    def repost(self):
        repost_tags=self.driver.find_elements_by_xpath('//android.view.View[@content-desc="转发"]')
        if len(repost_tags)>0:
            repost_tags[0].click()

        repost_text_tags=self.driver.find_elements_by_id('com.sina.weibo:id/et_mblog')
        if len(repost_text_tags)>0:
            repost_text_tags[0].click()
            old_repost_text=repost_text_tags[0].text
            print(old_repost_text)
            add_str= choice(comments_list)
            repost_text=add_str.strip('\n')+old_repost_text
            print(repost_text)
            time.sleep(3)

        repost_btn_tags = self.driver.find_elements_by_id('com.sina.weibo:id/titleSave')
        if len(repost_btn_tags)>0:
            repost_btn_tags[0].click()

        self.driver.implicitly_wait(20)
    # 运行流程
    def run(self,username,password):
        print('用户%s准备登录'%username)
        self.logger.write('info','用户%s准备登录'%username)
        # 登录
        login_status=self.login(username,password)
        if not login_status:
            print('用户%s登录操作失败' % (username))
            self.logger.write('info','用户%s登录操作失败' % (username))
            # 关闭app
            self.driver.close_app()
            return

        # 滑动屏幕一下,模拟用户操作
        self.apper.swipeDown(400)
        # #转发微博
        # self.repost()
        # # 滑动屏幕一下,模拟用户操作
        # self.apper.swipeDown(400)
        print('休息10秒')
        # 休息10秒
        time.sleep(10)

        # 注销账号登录
        self.login_out()
        print('用户%s注销成功'% username)
        self.logger.write('info','用户%s注销成功'% username)
        print('用户%s登录流程执行成功' % username)
        self.logger.write('info', '用户%s登录流程执行成功' % username)
        #关闭app
        self.driver.close_app()


if __name__ == '__main__':

    userinfo_file = './user.txt'
    with open(userinfo_file, mode='r', encoding='utf-8') as f:
        for line in f:
            username = line.split('----')[0]
            password = line.split('----')[1]

            try:
                loginer = AppLoginer()
                loginer.run(username,password)
            except Exception as e:
                print('%s----用户%s登录操作失败：%s' % (format_exc(), username, str(e)))
               
