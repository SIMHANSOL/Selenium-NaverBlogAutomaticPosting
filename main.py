from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import subprocess
import pyperclip
import time

subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[
    0]  # 크롬드라이버 버전 확인
try:
    driver = webdriver.Chrome(
        f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(
        f'./{chrome_ver}/chromedriver.exe', options=option)

driver.implicitly_wait(3)

postTitle = '입력될 제목입니다.'
postDescription = '입력될 내용입니다.'
userId = 'naverId'  # 네이버 계정 아이디
userPw = 'naverPassword'  # 네이버 계정 패스워드


def naver_login():
    # 네이버 로그인 페이지로 이동
    driver.get(
        'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
    print("로그인 페이지 이동")
    time.sleep(.5)

    # 아이디 입력폼
    tag_id = driver.find_element_by_name('id')
    # 패스워드 입력폼
    tag_pw = driver.find_element_by_name('pw')

    # id 입력
    # 입력폼 클릭 -> paperclip에 선언한 userId 내용 복사 -> 붙여넣기
    tag_id.click()
    tag_id.send_keys(Keys.CONTROL, 'a')
    tag_id.send_keys(Keys.DELETE)
    pyperclip.copy(userId)
    tag_id.send_keys(Keys.CONTROL, 'v')
    print("아이디 입력 완료")

    # pw 입력 # 입력폼 클릭 -> paperclip에 선언한 userPw 내용 복사 -> 붙여넣기
    tag_pw.click()
    tag_pw.send_keys(Keys.CONTROL, 'a')
    tag_pw.send_keys(Keys.DELETE)
    pyperclip.copy(userPw)
    tag_pw.send_keys(Keys.CONTROL, 'v')
    print("비밀번호 입력 완료")

    # 로그인 버튼 클릭
    login_btn = driver.find_element_by_id('log.login')
    login_btn.click()
    print("로그인 버튼 클릭")
    time.sleep(1)


def naver_crolling():
    driver.execute_script('window.open("https://www.naver.com", "_blank");')
    print("새탭 열기")
    time.sleep(1)
    driver.switch_to_window(driver.window_handles[1])


def naver_blog():
    driver.get('https://blog.naver.com/' + userId + '?Redirect=Write')
    print("블로그 이동")
    time.sleep(1)

    frame = driver.find_element_by_id("mainFrame")  # iframe 태그 엘리먼트 찾기
    driver.switch_to.frame(frame)  # 프레임 이동
    print("프레임 변경")
    time.sleep(1)

    # 기존 작성 글
    try:
        cancel = driver.find_element_by_css_selector(
            '.se-popup-button.se-popup-button-cancel')
        if cancel:
            cancel.click()
    except:
        pass
    print("기존 작성 글 닫기")
    time.sleep(1)

    # 제목 부분
    title = driver.find_element_by_css_selector(
        '.se-placeholder.__se_placeholder.se-fs32')
    action = ActionChains(driver)
    action.move_to_element(title).pause(
        1).click().send_keys(postTitle).perform()
    action.reset_actions()
    print("제목 작성 완료")
    time.sleep(.5)

    # 내용 부분
    description = driver.find_element_by_css_selector(
        '.se-component.se-text.se-l-default')
    description.click()
    action = ActionChains(driver)
    action.send_keys(postDescription).pause(1).send_keys(
        Keys.ENTER).send_keys(Keys.ENTER).perform()
    action.reset_actions()
    time.sleep(.5)
    print("내용 작성 완료")


naver_login()
naver_crolling()
naver_blog()
print("프로그램 종료")
