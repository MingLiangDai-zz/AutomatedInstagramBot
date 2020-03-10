from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
pw = ""  # ENTER YOUR PASSWORD IN THE QUOTATIONS
username = ""  # ENTER YOUR INSTAGRAM USER NAME IN THE QUOTATIONS
email = ""  # ENTER YOUR LOGIN EMAIL IN THE QUOTATIONS
# with open("password.txt", 'r') as f:
#    pw = f.readline()


class InstaBot:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.pw = password
        self.driver = webdriver.Chrome("chromedriver")
        self.driver.get("https://instagram.com")
        time.sleep(2)
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[6]/button").click()
        time.sleep(2)
        # self.driver.find_element_by_xpath(
        #   "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[6]/button/span[2]").click()
        email_elem = self.driver.find_element_by_id("email")
        password_elem = self.driver.find_element_by_id("pass")
        login_button = self.driver.find_element_by_id("loginbutton")

        email_elem.send_keys(self.email)
        password_elem.send_keys(self.pw)
        login_button.click()
        time.sleep(3)
        self.driver.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]").click()

    def search(self, name):
        search_bar = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
        search_bar.send_keys(name)
        time.sleep(1)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(1)
        search_bar.send_keys(Keys.ENTER)

    def unfollow(self):
        time.sleep(2)
        following = self.driver.find_element_by_xpath(
            "//button[contains(text(), 'Following')]")
        following.click()
        time.sleep(1)

        unfollow = self.driver.find_element_by_xpath(
            "//button[contains(text(), 'Unfollow')]")
        time.sleep(1)
        unfollow.click()

    def profile(self):
        time.sleep(1)
        icon = self.driver.find_element_by_xpath(
            "//a[contains(@href, '/{}')]".format(self.username))
        icon.click()

    def get_unfollowers(self):
        time.sleep(1)
        following = self.driver.find_element_by_xpath(
            "//a[contains(@href, '/following')]")
        following.click()
        followings = self.get_names()
        print(followings)
        print('\n')
        time.sleep(1)
        follower = self.driver.find_element_by_xpath(
            "//a[contains(@href, '/followers')]")
        follower.click()
        followers = self.get_names()
        print(followers)
        print('\n')
        bad_guys = []
        for following in followings:
            if (following not in followers):
                bad_guys.append(following)
        return bad_guys

    def get_names(self):
        time.sleep(1)
        scroll = self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]")
        prev = 0
        curr = 1
        while (prev != curr):
            prev = curr
            time.sleep(1)
            curr = self.driver.execute_script(
                "arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll)
        following_list = scroll.find_elements_by_tag_name('a')
        names = [name.text for name in following_list if name.text != ""]
        self.driver.get("https://instagram.com/{}".format(self.username))
        return names


my_bot = InstaBot(username, email, pw)
my_bot.profile()
bad_dudes = my_bot.get_unfollowers()
for i in bad_dudes:
    my_bot.search(str(i))
    my_bot.unfollow()
print(bad_dudes)
