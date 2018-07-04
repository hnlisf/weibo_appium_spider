from appium import webdriver

class Apper:
    def __init__(self,platformName,platformVersion,deviceName,appPackage,appActivity):
        self.desired_caps = {}
        self.desired_caps['platformName'] = platformName
        self.desired_caps['platformVersion'] = platformVersion
        self.desired_caps['deviceName'] = deviceName
        self.desired_caps['appPackage'] = appPackage
        self.desired_caps['appActivity'] = appActivity

        self.driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub',desired_capabilities=self.desired_caps, proxy=None,keep_alive=False)

    # 获取屏幕的宽和高
    def get_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    # 向上滑动
    def swipeUp(self, t):
        l = self.get_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)
        self.driver.swipe(x1, y1, x1, y2, t)

    # 向左滑动
    def swipeLeft(self, t):
        l = self.get_size()
        x1 = int(l[0] * 0.75)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.25)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 向右滑动
    def swipeRight(self, t):
        l = self.get_size()
        x1 = int(l[0] * 0.25)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.75)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 向下滑动
    def swipeDown(self, t):
        l = self.get_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.25)
        y2 = int(l[1] * 0.75)
        self.driver.swipe(x1, y1, x1, y2, t)

    def clickone(self,ps):
        self.driver.tap(ps,400)


if __name__ == '__main__':
    platformName='Android'
    platformVersion='4.4.2'
    deviceName = 'Android Emulator'
    appPackage = 'com.sina.weibo'
    appActivity = 'com.sina.weibo.SplashActivity'

    apper = Apper(platformName,platformVersion,deviceName,appPackage,appActivity)
    apper.run()