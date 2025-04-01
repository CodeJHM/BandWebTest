from selenium import webdriver
from selenium.common import NoSuchElementException, UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.action_chains import ActionChains
import pytest, sys, logging
from pytest_html_reporter import attach
import pytest_check as check
from selenium.webdriver.support.select import Select
from twocaptcha import TwoCaptcha
import datetime
import pyautogui

checkurl = 'qa1.band.us'
moveurl = ''

# 시작 함수
@pytest.fixture(scope="session")
def setup():
    global driver
    options = Options()
    # recapcha 확장 프로그램 불러오기
    options.add_extension('0626.crx')
    #options.add_extension('reCAPTCHA-Solver-auto-captcha-bypass.crx')
    #options.add_extension('Captcha-Solver-Auto-captcha-solving-service.crx')
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    baseurl = 'https://'+checkurl+'/home'
    driver.get(baseurl)
    driver.implicitly_wait(5)


# 검증 실패시 스크린샷 첨부해주는 함수
@pytest.fixture(autouse=True)
def screen_capture():
    attach(data=driver.get_screenshot_as_png())


def newtab():
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])
    time.sleep(2)


def closenewtab():
    driver.close()
    tabs = driver.window_handles
    driver.switch_to.window(tabs[0])
    time.sleep(2)


def scrollelement(element):
    element = driver.find_element(By.CLASS_NAME, element)
    actions = ActionChains(driver)
    actions.scroll_to_element(element)
    actions.perform()
    time.sleep(2)


def urlcheck(url):
    nowurl = driver.current_url
    check.equal(nowurl, url)


@pytest.mark.usefixtures("setup")
class TestBand():
    # 밴드 로그인 테스트
    def test_001_login(self):
        # 로그인 버튼 클릭
        driver.find_element(By.CLASS_NAME, 'button._loginBtn').click()
        time.sleep(1)

        # 이메일 로그인 버튼 클릭
        driver.find_element(By.ID, 'email_login_a').click()
        time.sleep(2)

        # ID 입력
        driver.find_element(By.ID, 'input_email').send_keys('nv_map_07@naver.com')
        driver.find_element(By.CLASS_NAME, 'uBtn.-tcType.-confirm').click()
        time.sleep(2)

        # PW 입력
        driver.find_element(By.ID, 'pw').send_keys('Test1234')
        driver.find_element(By.CLASS_NAME, 'uBtn.-tcType.-confirm').click()
        time.sleep(2)

        # reCAPTCHA resolver code
        #solver = TwoCaptcha('6Lcky20fAAAAAEb1Ej1bTBENV80CSh1N5UVRW-NC')
        #response = solver.solve_captcha(site_key=solver, page_url='https://auth.band.us/continue_email_login?login_type=')
        #code = response['code']

        # 확장 프로그램으로 실행이라 50초 대기 (가끔씩 오래 걸리는 경우 대비)
        wait = WebDriverWait(driver, 120)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'bandCreate._link')))

        # 메인 탭 이동
        #driver.find_element(By.CLASS_NAME, '_tabMyMission.tab').click()
        #time.sleep(2)
        #driver.find_element(By.CLASS_NAME, '_tabMyLocalMeetup.tab').click()
        #time.sleep(2)
        #driver.find_element(By.CLASS_NAME, '_tabMyBandList.tab').click()
        #time.sleep(2)

        # 각 텍스트 확인 (밴드홈은 클릭되어 있는 상태로 체크)
        mybandtext = driver.find_element(By.CLASS_NAME, '_tabMyBandList.tab.-active').text
        #missiontext = driver.find_element(By.CLASS_NAME, '_tabMyMission.tab').text
        #localtext = driver.find_element(By.CLASS_NAME, '_tabMyLocalMeetup.tab').text

        # 이동 잘되었는지 텍스트로 체크
        check.equal(mybandtext, '내 밴드')
        #check.equal(missiontext, '미션')
        #check.equal(localtext, '소모임')

        #driver.get('https://band.us/band/88122841/member')
        #driver.get('https://band.us/discover')
        time.sleep(2)
    # ------------------------------------------- 밴드홈 -------------------------------------------
    # 밴드 가이드, 데스크톱 메뉴 테스트
    '''
    def test_002_bandmainlink(self):
        # 밴드 가이드 버튼 클릭
        driver.find_element(By.CLASS_NAME, 'btnOption._linkGuideBand').click()
        time.sleep(2)

        # URL 검증
        url = driver.current_url
        check.equal(url, 'https://qa1.band.us/band/62396709')

        # 밴드 타이틀 검증
        titletext = driver.find_element(By.CLASS_NAME, 'uriText').text
        check.equal(titletext, '공식 밴드BAND 가이드')

        driver.back()
        time.sleep(2)

        # 밴드 데스크탑 다운로드 버튼 클릭
        driver.find_elements(By.CLASS_NAME, 'btnOption')[3].click()
        time.sleep(4)

        newtab()

        # URL 검증
        url = driver.current_url
        check.equal(url, 'https://qa1.band.us/cs/notice/1301')

        headtitle = driver.find_element(By.CLASS_NAME, 'cBx.listView.-detailPage').find_element(By.CLASS_NAME, 'head').text
        check.equal(headtitle, 'PC에서도 편리한 BAND 데스크톱 버전 출시!')

        closenewtab()

    # 메인탭 오늘의 인기글 테스트
    def test_003_mainpopular(self):
        # 최하단까지 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # 인기글 개수 카운트 검증
        count = len(driver.find_elements(By.CLASS_NAME, 'textContents'))
        check.equal(count, 4)

        href = driver.find_elements(By.CLASS_NAME, 'popularBandContents')[1].get_attribute('href')
        driver.find_elements(By.CLASS_NAME, 'textContents')[1].click()
        time.sleep(2)

        # 인기글 포스트로 이동하여 URL로 검증
        newtab()
        posturl = driver.current_url
        check.is_in(href, posturl)

        # 새 탭 닫고 현재 탭으로 복귀
        closenewtab()

        # 인기글 모두보기로 이동 후 검증
        driver.find_element(By.CLASS_NAME, 'openBandList').find_element(By.CLASS_NAME, 'optionText').click()
        time.sleep(2)

        url = driver.current_url
        check.equal(url, 'https://qa1.band.us/open-feed')

        # 인기글 탭 활성화 검증 / 인기글 포스트 보이는지 검증
        openfeedtab = driver.find_element(By.CLASS_NAME, 'tab._tabOpenFeed.-active').is_displayed()
        openfeedpost = driver.find_element(By.CLASS_NAME, 'cContentsCard._postMainWrap').is_displayed()
        check.is_true(openfeedtab)
        check.is_true(openfeedpost)

        driver.back()
        time.sleep(2)

    # 메인탭 이런 밴드는 어때요 테스트
    def test_004_maindiscover(self):
        flag = len(driver.find_elements(By.CLASS_NAME, 'discoverBandList'))

        if flag > 0:
            # 이런 밴드는 어때요 항목으로 스크롤
            element = driver.find_element(By.CLASS_NAME, 'discoverBandList')
            actions = ActionChains(driver)
            actions.scroll_to_element(element)
            actions.perform()
            time.sleep(2)

            # 10개 개수 노출 검증
            count = len(driver.find_elements(By.CLASS_NAME, 'bandLink._bandLink'))
            check.equal(count, 10)

            contentbandname = driver.find_elements(By.CLASS_NAME, 'text._bandLink')[2].text

            driver.find_elements(By.CLASS_NAME, 'bandLink._bandLink')[2].click()
            time.sleep(2)

            newtab()

            # 가입 버튼, 소개 버튼 노출 / 밴드 이름 일치하는지 검증
            joinbutton = driver.find_element(By.CLASS_NAME, 'uButton.-sizeL.-confirm._btnJoinBand').is_displayed()
            check.is_true(joinbutton)
            #infobutton = driver.find_element(By.CLASS_NAME, 'buttonIntroMore').is_displayed()
            #check.is_true(infobutton)
            bandname = driver.find_element(By.CLASS_NAME, 'uriText').text

            # 공백 이슈가 있어 공백 제거 후 밴드 이름 검증
            contentbandname = contentbandname.replace(' ', '')
            bandname = bandname.replace(' ', '')

            check.equal(contentbandname, bandname)

            closenewtab()

            # 6번째 추천글 클릭
            driver.find_elements(By.CLASS_NAME, 'moreBandLink._tagLink')[5].click()
            time.sleep(2)

            newtab()

            # 밴드 페이지 활성화 탭 검증
            activemenutab = driver.find_element(By.CLASS_NAME, 'findTopMenuItemLink._searchLnbMenu.-active').is_displayed()
            check.is_true(activemenutab)

            # 검색 결과 텍스트 노출 검증
            titletext = driver.find_element(By.CLASS_NAME, 'sectionTitle._totalBandListHead').text
            check.is_in('검색 결과', titletext)

            # 리스트 잘 노출되는지 검증
            lists = driver.find_element(By.CLASS_NAME, 'cCoverList').is_displayed()
            check.is_true(lists)

            closenewtab()

            # 모두보기 텍스트 클릭
            driver.find_element(By.CLASS_NAME, 'discoverBandList').find_element(By.CLASS_NAME, 'optionText').click()
            time.sleep(2)

            # 찾기 화면으로 이동되는지 URL로 검증
            url = driver.current_url
            check.equal(url, 'https://qa1.band.us/discover')

            driver.back()
            time.sleep(2)

    # 맨 위로 버튼 동작 테스트
    def test_005_topbutton(self):
        # 푸터 영역으로 스크롤 이동
        scrollelement('copyMenuListItem')

        # 맨 위로 버튼 동작 버튼 클릭
        driver.find_element(By.CLASS_NAME, 'buttonGotoTop._btnGoToTop').click()
        time.sleep(2)

        # 밴드 만들기 버튼 보이는지 검증
        createbtn = driver.find_element(By.CLASS_NAME, 'bandCreate._link').is_displayed()
        check.is_true(createbtn)

    # 푸터 링크 이동 테스트
    def test_006_footer(self):
        # footer 영역까지 스크롤 이동
        scrollelement('copyMenuList')

        # 블로그 푸터 링크 클릭
        driver.find_elements(By.CLASS_NAME, 'copyMenuLink')[0].click()
        time.sleep(2)

        newtab()

        # 밴드 블로그 URL 확인
        url = driver.current_url
        check.equal(url, 'https://blog.naver.com/bandapp')

        closenewtab()

        # 공지사항 푸터 링크 클릭
        driver.find_elements(By.CLASS_NAME, 'copyMenuLink')[1].click()
        time.sleep(2)

        newtab()

        # 공지사항 URL 확인
        url = driver.current_url
        check.equal(url, 'https://'+checkurl+'/cs/notice')

        # 타이틀 공지사항 확인
        title = driver.find_element(By.CLASS_NAME, 'sectionTitle').text
        check.equal(title, '공지사항')

        closenewtab()

        # 개인정보처리방침 푸터 클릭
        driver.find_elements(By.CLASS_NAME, 'copyMenuLink')[5].click()
        time.sleep(2)

        newtab()

        # 개인정보처리방침 URL 확인
        url = driver.current_url
        check.equal(url, 'https://'+checkurl+'/policy/privacy')

        # 타이틀 확인
        title = driver.find_element(By.CLASS_NAME, 'titWrap').text
        check.equal(title, '개인정보처리방침')

        closenewtab()

        # 도움말 푸터 링크 클릭
        driver.find_elements(By.CLASS_NAME, 'copyMenuLink')[12].click()
        time.sleep(2)

        newtab()

        # 공지사항 URL 확인
        url = driver.current_url
        check.equal(url, 'https://'+checkurl+'/cs/help')

        # 도움말 목록 타이틀 확인
        title = driver.find_element(By.CLASS_NAME, 'sectionTitle.-bg').text
        check.equal(title, '자주 묻는 질문')

        closenewtab()
    # ------------------------------------------- 미션 탭 -------------------------------------------
    # 미션 탭 노출 영역 테스트
    def test_007_missiontab(self):
        # 미션 탭 이동
        driver.find_element(By.CLASS_NAME, '_tabMyMission.tab').click()
        time.sleep(2)

        # URL 체크
        urlcheck('https://'+checkurl+'/mission')

        # 각 타이틀 텍스트 확인
        missionlist = driver.find_elements(By.CLASS_NAME, 'titleMainHome')[0].text
        missionlist = missionlist[:-2]
        badge = driver.find_elements(By.CLASS_NAME, 'titleMainHome')[1].text
        badge = badge[0:6]
        missioncountlist = driver.find_elements(By.CLASS_NAME, 'titleMainHome')[2].text
        missioncountlist = missioncountlist[0:8]

        #check.equal(missionlist, '인증할 미션이 없네요')
        check.equal(badge, '메달과 배지')
        check.equal(missioncountlist, '나의 인증 기록')

    # 미션 목록 영역 테스트
    def test_008_missioncard(self):
        zerocase = len(driver.find_elements(By.CLASS_NAME, 'makeMission.gMat24._linkMissionLfgBandCreate'))
        completecase = len(driver.find_elements(By.CLASS_NAME, 'todayMissionComplete'))
        missionnum = len(driver.find_elements(By.CLASS_NAME, 'number._missionCount'))

        if missionnum > 0:
            missioncount = driver.find_element(By.CLASS_NAME, 'number._missionCount').text

        # 미션 만들기 버튼 클릭
        # 미션 생성된게 0개인 경우
        if zerocase > 0:
            driver.find_element(By.CLASS_NAME, 'makeMission.gMat24._linkMissionLfgBandCreate').click()
            newtab()
        # 금일 미션을 모두 완료한 경우
        elif completecase > 0:
            driver.find_element(By.CLASS_NAME, 'createMission.-iconPlus._linkMissionLfgBandCreate').click()
        else:
            if int(missioncount) > 2:
                driver.find_element(By.CLASS_NAME, 'next._btnNextMission').click()
                time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'createMission.-iconPlus._btnMissionLfgBandCreate').click()
        time.sleep(2)

        # 3번째 운동 카테고리 선택
        driver.find_elements(By.CLASS_NAME, 'typeButton._categoryBtn')[2].click()
        time.sleep(2)

        # 미션명 입력
        driver.find_element(By.CLASS_NAME, '_inputBandName').send_keys('mission gogo test!!')
        time.sleep(2)

        # 미션 설명 (30자 이상) 입력
        driver.find_element(By.CLASS_NAME, '_missionDescription').send_keys('123456789012345678901234567890haha')
        time.sleep(2)

        # 확인 버튼 클릭
        driver.find_element(By.CLASS_NAME, '_btnConfirm.uButton.-sizeXL.-confirm').click()
        time.sleep(2)

        # 미션 밴드 바로 시작 텍스트 클릭
        driver.find_element(By.CLASS_NAME, 'startRightAwayButton._btnConvertToGroup').click()
        time.sleep(2)

        # 확인 버튼 클릭
        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        moveurl = driver.current_url

        if zerocase > 0:
            closenewtab()

        # 미션 밴드 생성 후 미션 탭 새로고침
        driver.get('https://'+checkurl+'/mission')
        time.sleep(2)

        missioncount = driver.find_element(By.CLASS_NAME, 'number._missionCount').text

        # 미션 인증 버튼 클릭
        driver.find_elements(By.CLASS_NAME, 'postWriteMission.swiper-no-swiping._linkMissionConfirm')[0].click()
        time.sleep(2)

        # 글 작성 완료 버튼 클릭
        driver.find_element(By.CLASS_NAME, 'uButton.-sizeM.-confirm._btnSubmitPost').click()
        time.sleep(2)

        # 미션 완료 팝업 닫기
        driver.find_element(By.CLASS_NAME, 'uButton.-iconClose.btnLyClose._btnClose').click()
        time.sleep(2)

        # 미션 탭으로 이동하기 위해 이전 페이지 이동
        driver.back()
        time.sleep(2)

        # 미션 인증 완료 영역 노출 검증
        if zerocase > 0 or completecase > 0:
            missioncomplete = driver.find_element(By.CLASS_NAME, 'todayMissionComplete').is_displayed()
            check.is_true(missioncomplete)
        else:
            completeafter = driver.find_element(By.CLASS_NAME, 'number._missionCount').text
            check.equal(int(completeafter), int(missioncount)-1)

    # 미션 통계 영역 테스트
    def test_009_missionstats(self):
        driver.find_elements(By.CLASS_NAME, 'helpButton._btnHelp')[0].click()
        time.sleep(2)

        firsthelp = driver.find_elements(By.CLASS_NAME, 'bubble._helpLayer')[0].is_displayed()
        secondhelp = driver.find_elements(By.CLASS_NAME, 'bubble._helpLayer')[1].is_displayed()

        check.is_true(firsthelp)
        check.is_false(secondhelp)

        driver.find_elements(By.CLASS_NAME, 'btnLyClose._btnHelpLayerClose')[0].click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'helpButton._btnHelp')[1].click()
        time.sleep(2)

        firsthelp = driver.find_elements(By.CLASS_NAME, 'bubble._helpLayer')[0].is_displayed()
        secondhelp = driver.find_elements(By.CLASS_NAME, 'bubble._helpLayer')[1].is_displayed()

        check.is_false(firsthelp)
        check.is_true(secondhelp)

        driver.find_elements(By.CLASS_NAME, 'btnLyClose._btnHelpLayerClose')[1].click()
        time.sleep(2)

        scrollelement('chartMissionCertificate')

        gold = driver.find_element(By.CLASS_NAME, 'iconGold').is_displayed()
        join = driver.find_element(By.CLASS_NAME,'iconJoin').is_displayed()

        check.is_true(gold)
        check.is_true(join)

        chart = driver.find_element(By.CLASS_NAME, 'chartMissionCertificate').is_displayed()
        check.is_true(chart)

    # 미션 추천 리스트 테스트
    def test_010_missionchallengelist(self):
        scrollelement('categorySlider._missionKeywordScrollWrapper')

        activetext = driver.find_element(By.CLASS_NAME, 'tab._tabMissionKeyword.-active').text
        check.equal(activetext, '전체')

        driver.find_elements(By.CLASS_NAME, 'tab._tabMissionKeyword')[4].click()
        time.sleep(2)

        activetext = driver.find_element(By.CLASS_NAME, 'tab._tabMissionKeyword.-active').text
        check.is_in('스터디', activetext)

        scrollelement('bandFindWrap')

        title = driver.find_element(By.CLASS_NAME, 'sectionTitle._title').text
        check.is_in('스터디', title)

        scrollelement('categorySlider._missionKeywordScrollWrapper')

        driver.find_element(By.CLASS_NAME, '_filterSelect').click()
        time.sleep(2)

        select = Select(driver.find_element(By.CLASS_NAME, '_filterSelect'))
        select.select_by_index(1)

        time.sleep(2)

        text = driver.find_elements(By.CLASS_NAME, 'missionDesc')[0].text
        check.is_in('명이 더 모이면 미션이 시작됩니다.', text)

    # ------------------------------------------- 찾기 페이지 -------------------------------------------
    # 찾기탭 주제별 밴드를 찾아보세요 테스트
    def test_011_searchsection(self):
        driver.get('https://'+checkurl+'/discover')
        time.sleep(2)
        # 첫번째 주제 클릭
        onetext = driver.find_elements(By.CLASS_NAME, 'inner._itemLink')[0].text

        driver.find_elements(By.CLASS_NAME, 'inner._itemLink')[0].click()
        time.sleep(2)

        # 클릭하여 진입한 주제가 해당 주제가 맞는지 체크
        sectiontitle = driver.find_element(By.CLASS_NAME, 'sectionTitle').text
        check.equal(onetext, sectiontitle[:-9])

        popularactive = driver.find_element(By.CLASS_NAME, '_keywordName.-active._active').is_displayed()
        check.is_true(popularactive)

        # 검색 결과 검증
        searchlist = driver.find_element(By.CLASS_NAME, 'cCoverList').is_displayed()
        searchresult = driver.find_elements(By.CLASS_NAME, 'cCoverItem')[1].is_displayed()
        searchsubtitle = driver.find_elements(By.CLASS_NAME, 'pSubTxt.-multiLine')[5].is_displayed()

        check.is_true(searchlist)
        check.is_true(searchresult)
        check.is_true(searchsubtitle)

        driver.back()
        time.sleep(2)

        # 5번째 주제 클릭
        fivetext = driver.find_elements(By.CLASS_NAME, 'inner._itemLink')[4].text

        driver.find_elements(By.CLASS_NAME, 'inner._itemLink')[4].click()
        time.sleep(2)

        # 타이틀 검증
        sectiontitle = driver.find_element(By.CLASS_NAME, 'sectionTitle').text
        check.equal(fivetext, sectiontitle[:-9])

        # 검색 결과 검증
        searchlist = driver.find_element(By.CLASS_NAME, 'cCoverList').is_displayed()
        searchresult = driver.find_elements(By.CLASS_NAME, 'cCoverItem')[2].is_displayed()
        searchsubtitle = driver.find_elements(By.CLASS_NAME, 'pSubTxt.-multiLine')[4].is_displayed()

        check.is_true(searchlist)
        check.is_true(searchresult)
        check.is_true(searchsubtitle)

        driver.back()
        time.sleep(2)

    # 찾기탭 오늘의 인기글 테스트
    def test_012_searchpopular(self):
        # 오늘의 인기글 항목으로 스크롤
        try:
            element = driver.find_element(By.CLASS_NAME, 'todayBest')
            actions = ActionChains(driver)
            actions.scroll_to_element(element)
            actions.perform()
            time.sleep(2)

            count = len(driver.find_elements(By.CLASS_NAME, 'body._postLink'))
            check.equal(count, 2)

            href = driver.find_elements(By.CLASS_NAME, 'body._postLink')[0].get_attribute('href')
            driver.find_elements(By.CLASS_NAME, 'body._postLink')[0].click()
            time.sleep(2)

            # 인기글 포스트로 이동하여 URL로 검증
            newtab()
            posturl = driver.current_url
            check.is_in(href, posturl)

            # 새 탭 닫고 현재 탭으로 복귀
            closenewtab()

            driver.find_element(By.CLASS_NAME, 'todayBest').find_element(By.CLASS_NAME, 'more._moreLink').click()
            time.sleep(2)

            url = driver.current_url
            check.equal(url, 'https://' + checkurl + '/open-feed')

            openfeedtab = driver.find_element(By.CLASS_NAME, 'tab._tabOpenFeed.-active').is_displayed()
            openfeedpost = driver.find_element(By.CLASS_NAME, 'cContentsCard._postMainWrap').is_displayed()
            check.is_true(openfeedtab)
            check.is_true(openfeedpost)

            driver.back()
            time.sleep(2)
        except NoSuchElementException:
            print('인기글 미노출')
    # 찾기탭 소모임 추천글 테스트
    #UI 변경으로 추후 변경 진행
    def test_013_searchlocal(self):
        scrollelement('localMeetupBand')

        # 메인탭 소개와 밴드 상세 소개 비교 (너무 긴 경우 잘림으로 검증)
        onetext = driver.find_elements(By.CLASS_NAME, 'localMeetupContDesc.gMat6')[2].text.replace(' ', '')
        onearea = driver.find_elements(By.CLASS_NAME, 'tagItem.-local._itemRegionBtn')[2].text
        onecategory = driver.find_elements(By.CLASS_NAME, 'tagItem._itemKeywordBtn')[2].text

        if len(onetext) > 17:
            onetext = onetext[0:15]

        driver.find_elements(By.CLASS_NAME, 'localMeetupContentLink._itemBandLink')[2].click()
        time.sleep(2)

        newtab()

        twotext = driver.find_element(By.CLASS_NAME, 'cBandIntroDetail').get_attribute('textContent').replace(' ', '').lstrip()
        twoarea = driver.find_element(By.CLASS_NAME, 'keywordButton').text
        twocategory = driver.find_element(By.CLASS_NAME, 'keywordButton._btnLocalKeyword').text

        if len(twotext) > 17:
            twotext = twotext[0:15]

        check.equal(onetext, twotext)
        check.equal(onearea, twoarea)
        check.equal(onecategory, twocategory)

        closenewtab()
    # 찾기탭 추천 페이지 테스트
    def test_014_searchpage(self):
        # 추천 페이지 영역으로 스크롤
        scrollelement('invitePage')

        # 구독 텍스트 검증
        subtext = driver.find_elements(By.CLASS_NAME, 'btnPageSubscription._subscribeBtn')[0].text
        readmember = driver.find_elements(By.CLASS_NAME, 'readMember')[2].text

        check.equal(subtext, '구독')
        check.is_in('구독 중', readmember)

        # 2번째 추천 페이지 진입
        driver.find_element(By.CLASS_NAME, 'invitePage').find_elements(By.CLASS_NAME, 'bandLink._pageBandLink')[1].click()
        time.sleep(2)

        newtab()

        # 구독하기, 메시지, 최신글 탭 활성화 검증
        subbutton = driver.find_element(By.CLASS_NAME, 'roundButton.-full.-subscribe._btnJoinPage').is_displayed()
        msgbutton = driver.find_element(By.CLASS_NAME, 'roundButton._chatToPageBtn').is_displayed()
        newtabactive = (driver.find_element(By.CLASS_NAME, 'pageLnb').
                        find_element(By.CLASS_NAME, 'lnbItemLink._lnbLink.active').is_displayed())

        check.is_true(subbutton)
        check.is_true(msgbutton)
        check.is_true(newtabactive)

        # 홈 탭으로 이동
        driver.find_elements(By.CLASS_NAME, 'lnbItemLink._lnbLink')[0].click()
        time.sleep(2)

        # 이 페이지 공유하기 버튼 검증
        pagesharebutton = driver.find_element(By.CLASS_NAME, 'buttonShare._sharePageBand').is_displayed()
        check.is_true(pagesharebutton)

        closenewtab()

        # 구독 버튼 클릭
        driver.find_elements(By.CLASS_NAME, 'btnPageSubscription._subscribeBtn')[1].click()
        time.sleep(2)

        length = len(driver.find_elements(By.CLASS_NAME, 'desc.gPab11'))
        msg = len(driver.find_elements(By.CLASS_NAME, 'headingMsg'))

        # 프로필 여러개인 경우
        if length > 0:
            subtitle = driver.find_element(By.CLASS_NAME, 'desc.gPab11').text
            check.equal(subtitle, '선택한 프로필의 사진을 이 페이지 구독자들도 볼 수 있게 돼요.')

            driver.find_element(By.CLASS_NAME, 'uButton.-confirm.-sizeL._confirmBtn').click()
            time.sleep(2)
        # 구독하려는 페이지가 광고성 페이지인 경우
        elif msg > 15:
            subtitle = driver.find_element(By.CLASS_NAME, 'headingMsg').text
            check.equal(subtitle, '이 페이지를 구독하면 페이지 운영자로부터 광고성 알림 푸시를 받을 수 있습니다.')

            driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
            time.sleep(2)
        elif msg < 10:
            subtitle = driver.find_element(By.CLASS_NAME, 'headingMsg').text
            check.equal(subtitle, '페이지를 구독합니다.')

            driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
            time.sleep(2)

        # 구독 버튼 클릭 후 구독 중 변경되는지 검증
        subfin = driver.find_element(By.CLASS_NAME, 'btnPageSubscription.-disabled._subscribeBtn').text
        check.equal(subfin, '구독 중')

        # click 동작하지 않아서 변경
        driver.find_element(By.CLASS_NAME, 'invitePage').find_elements(By.CLASS_NAME, 'bandLink._pageBandLink')[1].send_keys(Keys.ENTER)
        time.sleep(2)

        newtab()

        # 구독 후 구독 설정으로 변경되는지 검증
        subtext = driver.find_element(By.CLASS_NAME, 'roundButton.-full._btnSettingSubscribe').text
        check.equal(subtext, '구독 설정')

        closenewtab()

        # 모두보기 텍스트 클릭
        driver.find_element(By.CLASS_NAME, 'invitePage').find_element(By.CLASS_NAME, 'more._moreLink').click()
        time.sleep(2)

        # 추천페이지 모두보기 URL 검증
        currenturl = driver.current_url
        check.equal(currenturl, 'https://'+checkurl+'/discover/recommended-page')

        # 주요 노출 영역 검증
        maintitle = driver.find_element(By.CLASS_NAME, 'sectionTitle.gPab0.gMat10').text
        guidetext = driver.find_element(By.CLASS_NAME, 'topGuideBannerLink._pageCreateLink').find_element(By.CLASS_NAME, 'guideText').text
        pagesubtextcount = len(driver.find_elements(By.CLASS_NAME, 'pSubTxt.gMat4.-multiLine'))
        pagesubbtncount = len(driver.find_elements(By.CLASS_NAME, 'btnPageSubscription._subscribeBtn'))

        check.equal(maintitle, '추천 페이지')
        check.equal(guidetext, '찾고 있는 페이지가 없다면? 직접 페이지를 만들어 보세요.')
        check.greater(pagesubtextcount, 10)
        check.greater(pagesubbtncount, 10)

        driver.back()
        time.sleep(2)

    # 찾기탭 미션 인증글 테스트
    def test_015_searchmission(self):
        scrollelement('missionBand')

        driver.find_elements(By.CLASS_NAME, 'missionInfo')[2].click()
        time.sleep(2)

        newtab()

        missiontab = driver.find_elements(By.CLASS_NAME, 'btn.sf_color._btnMissionInfoTab')[1].text
        check.equal(missiontab, '미션 인증글')

        missiontext = (driver.find_elements(By.CLASS_NAME, 'missionContentBox')[0]
                       .find_element(By.CLASS_NAME, 'missionSubTitle').text)
        check.equal(missiontext, '인증 규칙')

        #driver.find_elements(By.CLASS_NAME, 'btn.sf_color._btnMissionInfoTab')[1].click()
        #time.sleep(2)

        #missionpost = len(driver.find_elements(By.CLASS_NAME, 'missionCertification._missionInfo'))
        #print(missionpost)
        #check.is_true(missionpost > 0)

        closenewtab()

        driver.find_element(By.CLASS_NAME, 'missionBand').find_element(By.CLASS_NAME, 'more._moreLink').click()
        time.sleep(2)

        url = driver.current_url
        check.equal(url, 'https://'+checkurl+'/discover/recommended-mission')

        alltab = driver.find_element(By.CLASS_NAME, 'tab._tabMissionKeyword.-active').text
        check.equal(alltab, '전체')

        missioncreatebutton = driver.find_element(By.CLASS_NAME, 'uButton.-confirm').is_displayed()
        check.is_true(missioncreatebutton)

        missionlist = len(driver.find_elements(By.CLASS_NAME, 'bandLink._bandLink'))
        check.is_true(missionlist > 0)

        driver.back()

    def test_missionbanddel(self):
        driver.get(moveurl)
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'bandSettingLink').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-sizeS.-confirm2.-colorError._btnDeleteBand').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        current_url = driver.get()
        check.equal(current_url, 'https://qa1.band.us/')

    # ------------------------------------------- 개별밴드 -------------------------------------------
    # 밴드 만들기 테스트
    def test_016_bandcreate(self):
        driver.get('https://'+checkurl+'/band-create')
        time.sleep(2)

        #22.0 이전 만들기
        driver.find_element(By.CLASS_NAME, 'bandCreate._link').click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, '직접 만들기').click()
        time.sleep(2)
        
        # 비공개 밴드로 선택하여 생성
        driver.find_element(By.ID, 'ex_name').send_keys('selenium autoband')
        driver.find_element(By.ID, 'secret').click()
        driver.find_element(By.CLASS_NAME, '_btnConfirm.uButton.-sizeXL.-confirm').click()
        time.sleep(2)
     
        #22.0 이후 만들기
        driver.find_element(By.CLASS_NAME, 'typeItem._privateBtn').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'buttonConfirmMakeType._nextBtn').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'typeItem._secretBandBtn').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'buttonConfirmMakeType._nextBtn').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'interestItem._usecaseItemBtn')[7].click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'buttonConfirmMakeType._nextBtn').click()
        time.sleep(2)

        driver.find_element(By.ID, 'band_name').send_keys('selenium autoband')
        driver.find_element(By.CLASS_NAME, 'buttonConfirmMakeType._createBtn').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'buttonConfirmMakeType._goGroupBandHomeBtn').click()
        time.sleep(2)

        # 밴드이름, 글쓰기 버튼 노출, 게시글/사진첩 탭 노출 유무 검증
        bandname = driver.find_element(By.CLASS_NAME, 'uriText').text
        writebtn = driver.find_element(By.CLASS_NAME, 'uButton.-sizeL.-confirm.sf_bg._btnPostWrite').text
        menulist = driver.find_elements(By.CLASS_NAME, 'lnbTopMenuItemText')

        check.equal(bandname, 'selenium autoband')
        check.equal(writebtn, '글쓰기')
        check.equal(menulist[0].text, '게시글')
        check.equal(menulist[1].text, '사진첩')

    # 밴드 일반 글쓰기 테스트
    def test_017_bandwrite(self):
        driver.find_element(By.CLASS_NAME, 'uButton.-sizeL.-confirm.sf_bg._btnPostWrite').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'postWriteForm._postWriteForm.-standby').click()
        (driver.find_element(By.CSS_SELECTOR, 'div.postWriteForm._postWriteForm.-standby > div:nth-child(2)')
         .send_keys('python selenium autotest'))

        driver.find_element(By.CLASS_NAME, 'uButton.-sizeM._btnSubmitPost.-confirm').click()
        time.sleep(2)

        posttxt = driver.find_element(By.CLASS_NAME, 'txtBody').text
        check.equal(posttxt, 'python selenium autotest')

    # 밴드 작성글 수정 테스트
    def test_018_postedit(self):
        driver.find_element(By.CLASS_NAME, 'postMain').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'postSet._btnPostMore')[1].send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, 'div.lyMenu._postMoreMenu > ul > li:nth-child(1) > a').click()
        time.sleep(2)

        # driver.find_element(By.CSS_SELECTOR, 'div.postWriteForm._postWriteForm.-standby > div').send_keys(Keys.COMMAND + 'a', Keys.BACKSPACE)
        driver.find_element(By.CSS_SELECTOR, 'div.postWriteForm._postWriteForm.-standby > div').clear()
        time.sleep(2)
        # driver.find_element(By.CSS_SELECTOR, 'div.postWriteForm._postWriteForm.-standby > div > p').click()
        # driver.find_element(By.CSS_SELECTOR, 'div.postWriteForm._postWriteForm.-standby > div > p').send_keys('post edit')
        driver.find_element(By.CSS_SELECTOR,
                            'div.postWriteForm._postWriteForm.-standby > div:nth-child(2)').send_keys(
            'post edit')
        driver.find_element(By.CLASS_NAME, 'uButton.-sizeM._btnSubmitPost.-confirm').click()
        time.sleep(2)

        posttxt = driver.find_element(By.CLASS_NAME, 'txtBody').text
        check.equal(posttxt, 'post edit')

    # 작성글 댓글 추가 테스트
    def test_019_postcomment(self):
        driver.find_element(By.CLASS_NAME, 'commentWrite._use_keyup_event._messageTextArea').send_keys(
            'comment test')
        #driver.find_element(By.CLASS_NAME, 'writeSubmit.uButton._sendMessageButton.-active').click()
        driver.find_element(By.CLASS_NAME, 'btnCommentSubmit._sendMessageButton.-active').click()
        time.sleep(2)

        firstcomment = driver.find_element(By.CLASS_NAME, 'txt._commentContent').text
        check.equal(firstcomment, 'comment test')

        driver.find_element(By.CLASS_NAME, 'commentWrite._use_keyup_event._messageTextArea').send_keys(
            'comment test two')
        driver.find_element(By.CLASS_NAME, 'btnCommentSubmit._sendMessageButton.-active').click()
        #driver.find_element(By.CLASS_NAME, 'writeSubmit.uButton._sendMessageButton.-active').click()
        time.sleep(2)

        firstcomment = driver.find_elements(By.CLASS_NAME, 'txt._commentContent')[0].text
        secondcomment = driver.find_elements(By.CLASS_NAME, 'txt._commentContent')[1].text

        check.equal(firstcomment, 'comment test')
        check.equal(secondcomment, 'comment test two')

        commentcount = driver.find_element(By.CSS_SELECTOR,
                                           'span.comment._commentCountBtn.gCursorDefault > span').text
        check.equal(commentcount, '2')

    # 댓글 수정 테스트
    def test_020_commentedit(self):
        driver.find_elements(By.CLASS_NAME, 'commentEdit')[0].click()
        driver.find_element(By.CSS_SELECTOR, 'div.feedback > div > ul > li:nth-child(1) > a').send_keys(Keys.ENTER)
        time.sleep(2)

        # driver.find_element(By.CLASS_NAME, 'commentWrite._modificationTextarea._use_keyup_event').send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
        driver.find_element(By.CLASS_NAME, 'commentWrite._modificationTextarea._use_keyup_event').clear()
        # driver.find_element(By.CLASS_NAME, 'commentWrite._modificationTextarea._use_keyup_event').send_keys(Keys.LEFT_SHIFT, Keys.HOME, Keys.BACKSPACE)
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'commentWrite._modificationTextarea._use_keyup_event').send_keys(
            'comment change')
        #driver.find_element(By.CLASS_NAME, 'buttonCommentModi.buttonPoint._submitButton').click()
        driver.find_element(By.CLASS_NAME, 'btnCommentSave.gMar6._submitButton').click()

        time.sleep(2)

        firstcomment = driver.find_elements(By.CLASS_NAME, 'txt._commentContent')[0].text
        check.equal(firstcomment, 'comment change')

    # 댓글 삭제 테스트
    def test_021_commentdel(self):
        driver.find_elements(By.CLASS_NAME, 'commentEdit')[0].click()
        driver.find_element(By.CSS_SELECTOR, 'div.feedback > div > ul > li:nth-child(3) > a').send_keys(Keys.ENTER)

        driver.switch_to.alert.accept()
        time.sleep(2)

        firstcomment = driver.find_element(By.CLASS_NAME, 'txt._commentContent').text
        check.equal(firstcomment, 'comment test two')

        commentcount = driver.find_element(By.CSS_SELECTOR,
                                           'span.comment._commentCountBtn.gCursorDefault > span').text
        check.equal(commentcount, '1')

    # 작성글 삭제 테스트
    def test_022_postdel(self):
        driver.find_elements(By.CLASS_NAME, 'postSet._btnPostMore')[1].send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, 'div.lyMenu._postMoreMenu > ul > li:nth-child(7) > a').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        emptytitle = driver.find_element(By.CLASS_NAME, 'uEmptyTitle').is_displayed()
        emptypost = driver.find_element(By.CLASS_NAME, 'uEmptyDesc').is_displayed()
        check.is_true(emptytitle)
        check.is_true(emptypost)

        #삭제 후 버그가 있어서 긴급 코드 추가 (추후 확인 필요)
        driver.refresh()

    # 투표 첨부글 테스트
    def test_023_pollpost(self):
        driver.find_element(By.CLASS_NAME, 'vote._showToolTip._popupOpenShortly').click()
        time.sleep(2)

        driver.find_element(By.ID, 'pollTitle').send_keys('poll_Title test')
        time.sleep(1)

        driver.find_element(By.ID, 'poll_item_0').send_keys('number one item')
        time.sleep(1)

        driver.find_element(By.ID, 'poll_item_1').send_keys('number two item')
        time.sleep(1)

        driver.find_element(By.ID, 'poll_item_2').send_keys('number three item')
        time.sleep(1)

        driver.find_element(By.ID, 'poll_item_3').send_keys('number four item')
        time.sleep(1)

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnComplete').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-sizeM._btnSubmitPost.-confirm').click()
        time.sleep(2)

        polltitle = driver.find_element(By.CLASS_NAME, 'addTitle').text
        check.equal(polltitle, 'poll_Title test')

        items = driver.find_element(By.CLASS_NAME, 'pollQuestionList.-more').find_elements(By.CSS_SELECTOR, 'li')
        check.equal(items[0].text, 'number one item')
        check.equal(items[1].text, 'number two item')
        check.equal(items[2].text, 'number three item')

    # 투표글 수정 테스트
    def test_024_polledit(self):
        driver.find_element(By.CLASS_NAME, 'addTitle').click()
        time.sleep(2)

        alertmessage = driver.find_element(By.CLASS_NAME, 'alert').text
        check.equal(alertmessage, '복수선택이 가능합니다.')

        driver.find_elements(By.CLASS_NAME, 'postSet._btnPostMore')[1].send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, 'div.lyMenu._postMoreMenu > ul > li:nth-child(1) > a').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'cke_reset.cke_widget_drag_handler').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'bandWidgetBtn.uButton.-sizeS.-modify._btnModify').click()
        time.sleep(2)

        driver.find_element(By.ID, 'pollTitle').clear()
        driver.find_element(By.ID, 'pollTitle').send_keys('edit OK?')

        driver.find_element(By.ID, 'poll_item_2').clear()
        driver.find_element(By.ID, 'poll_item_2').send_keys('three item change~')

        driver.find_element(By.CLASS_NAME, 'checkInput._chkMultipleSelect').click()

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnComplete').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-sizeM.-confirm._btnSubmitPost').click()
        time.sleep(2)

        polltitle = driver.find_element(By.CLASS_NAME, 'addTitle').text
        check.equal(polltitle, 'edit OK?')

        items = driver.find_element(By.CLASS_NAME, 'pollQuestionList.-more').find_elements(By.CSS_SELECTOR, 'li')
        check.equal(items[2].text, 'three item change~')

        alertmessage = driver.find_elements(By.CLASS_NAME, 'alert')
        check.equal(len(alertmessage), 0)

        #일정으로 넘어가기 위해 투표 닫음
        driver.find_element(By.CLASS_NAME, 'btnCloseLyPost._btnClose').click()
        time.sleep(2)

    # 멤버탭 내 프로필 상세 테스트
    def test_025_memberprofile(self):
        driver.get('https://'+checkurl+'/band/88122841/member')
        # 타인 프로필 검증
        driver.find_elements(By.CLASS_NAME, 'uIconOption')[0].click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'btnListItem._btnProfile')[0].click()
        time.sleep(2)

        leftbutton = driver.find_element(By.CLASS_NAME, 'chatting._btnSendMessage').text
        rightbutton = driver.find_element(By.CLASS_NAME, 'writePost._btnGotoSearchMemberContent').text

        check.equal(leftbutton, '채팅하기')
        check.equal(rightbutton, '작성글 보기')

        driver.find_element(By.CLASS_NAME, 'closeButton._btnClose').click()
        time.sleep(2)

        # 본인 프로필 검증
        driver.find_element(By.CLASS_NAME, 'bntSetting._btnSetting').click()
        time.sleep(2)

        leftbutton = driver.find_element(By.CLASS_NAME, 'settingProfile._btnProfileEdit').text
        rightbutton = driver.find_element(By.CLASS_NAME, 'writePost._btnGotoSearchMemberContent').text

        plusbutton = driver.find_element(By.CLASS_NAME, 'addPhoto._btnPhotoUpload').is_displayed()
        check.is_true(plusbutton)

        driver.find_element(By.CLASS_NAME, 'closeButton._btnClose').click()
        time.sleep(2)

    # 프로필 차단 테스트
    def test_026_profileblock(self):
        # 멤버 선택 후 차단
        driver.find_elements(By.CLASS_NAME, 'uIconOption')[1].click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'btnListItem._btnProfile')[1].click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'moreButton._btnMore').click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, '차단하기').click()
        time.sleep(2)

        # 차단 메시지 검증
        titlemsg = driver.find_element(By.CLASS_NAME, 'headingMsg').text
        bodymsg = driver.find_element(By.CLASS_NAME, 'pText').text

        check.is_in('차단', titlemsg)
        check.equal(bodymsg, '이 멤버가 쓴 글과 댓글에 대해 알림이 오지 않고, 작성한 내용도 보이지 않게 됩니다.')

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'uIconOption')[1].click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'btnListItem._btnProfile')[1].click()
        time.sleep(2)

        # 프로필 재진입 후 차단 여부 검증
        blockbutton = driver.find_element(By.CLASS_NAME, 'unblock._unmuteMember').is_displayed()
        check.is_true(blockbutton)

        blocktext = driver.find_element(By.CLASS_NAME, 'unblock._unmuteMember').find_element(By.TAG_NAME, 'span').text
        check.equal(blocktext, '차단 해제')

        # 차단 해제 버튼 클릭하여 차단 해제
        driver.find_element(By.CLASS_NAME, 'unblock._unmuteMember').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'uIconOption')[1].click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'btnListItem._btnProfile')[1].click()
        time.sleep(2)

        # 차단 해제 후 작성글 보기 메뉴 노출 검증
        writemenu = driver.find_element(By.CLASS_NAME, 'writePost._btnGotoSearchMemberContent').is_displayed()
        check.is_true(writemenu)

    # 멤버 정렬 옵션 테스트
    def test_027_membersort(self):
        driver.get('https://'+checkurl+'/band/88122841/member')
        time.sleep(4)

        # 멤버 탭 진입 후 검색창 노출 검증
        searchtab = driver.find_element(By.CLASS_NAME, '_queryInput').is_displayed()
        check.is_true(searchtab)

        # 정렬 옵션 최신 가입순으로 정렬 후 검증
        select = Select(driver.find_element(By.ID, 'sort'))
        select.select_by_value('recently_joined')
        time.sleep(2)

        firstmember = driver.find_elements(By.CLASS_NAME, 'ellipsis')[0].text
        secondmember = driver.find_elements(By.CLASS_NAME, 'ellipsis')[1].text
        fourmember = driver.find_elements(By.CLASS_NAME, 'ellipsis')[3].text
        sixmember = driver.find_elements(By.CLASS_NAME, 'ellipsis')[5].text

        check.equal(firstmember, '두루미뚜룹뚜룹뚜룹두루미뚜룹뚜룹뚜룹두루미뚜룹뚜룹뚜룹')
        check.equal(secondmember, '모퉁이02계정')
        check.equal(fourmember, '07 hahashhahshshshshshsh')
        check.equal(sixmember, '김정환')

        # 디폴트 정렬 옵션이 이름 순으로 변경 후 검증
        select = Select(driver.find_element(By.ID, 'sort'))
        select.select_by_visible_text('이름 순')
        time.sleep(2)

        firstmember = driver.find_elements(By.CLASS_NAME, 'ellipsis')[0].text
        secondmember = driver.find_elements(By.CLASS_NAME, 'ellipsis')[1].text
        fourmember = driver.find_elements(By.CLASS_NAME, 'ellipsis')[3].text
        sixmember = driver.find_elements(By.CLASS_NAME, 'ellipsis')[5].text

        check.equal(firstmember, '07 hahashhahshshshshshsh')
        check.equal(secondmember, 'KEYBOARD!')
        check.equal(fourmember, 'Cat cat@3')
        check.equal(sixmember, '김정환')

    # 멤버 검색 테스트
    def test_028_memebersearch(self):
        # 한글 멤버 검색 후 검증
        driver.find_element(By.CLASS_NAME, '_queryInput').send_keys('모퉁이')
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'search._searchBtn').click()
        time.sleep(2)

        searchcount = len(driver.find_element(By.CLASS_NAME, '_searchResultWrap').find_elements(By.CLASS_NAME, 'uFlexItem'))
        check.equal(searchcount, 1)

        searchtext = driver.find_element(By.CLASS_NAME, 'ellipsis').text
        check.equal(searchtext, '모퉁이02계정')

        # 2개 검색결과 숫자 검증
        driver.find_element(By.CLASS_NAME, '_queryInput').clear()
        driver.find_element(By.CLASS_NAME, '_queryInput').send_keys('0')
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'search._searchBtn').click()
        time.sleep(2)

        searchcount = len(driver.find_element(By.CLASS_NAME, '_searchResultWrap').find_elements(By.CLASS_NAME,
                                                                                                'uFlexItem'))
        check.equal(searchcount, 2)

        searchtext1 = driver.find_elements(By.CLASS_NAME, 'ellipsis')[0].text
        searchtext2 = driver.find_elements(By.CLASS_NAME, 'ellipsis')[1].text

        check.equal(searchtext1, '모퉁이02계정')
        check.equal(searchtext2, '^^05^^^05^^^^05^^^')

        # 영문 뒷자리 포함 멤버 검색 검증
        driver.find_element(By.CLASS_NAME, '_queryInput').clear()
        driver.find_element(By.CLASS_NAME, '_queryInput').send_keys('ARD')
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'search._searchBtn').click()
        time.sleep(2)

        searchcount = len(driver.find_element(By.CLASS_NAME, '_searchResultWrap').find_elements(By.CLASS_NAME,
                                                                                                'uFlexItem'))
        check.equal(searchcount, 1)
        searchtext = driver.find_element(By.CLASS_NAME, 'ellipsis').text
        check.equal(searchtext, 'KEYBOARD!')

        # 검색결과 없을 때 검증
        driver.find_element(By.CLASS_NAME, '_queryInput').clear()
        driver.find_element(By.CLASS_NAME, '_queryInput').send_keys('0808')
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'search._searchBtn').click()
        time.sleep(2)

        emptytext = driver.find_element(By.CLASS_NAME, 'uEmptyDesc.gFs14.gColorGr3').text
        check.equal(emptytext, '검색 결과가 없습니다.')

    # 첨부 앨범 만들기
    def test_029_attachmentalbum(self):
        driver.get('https://'+checkurl+'/band/98191555')
        time.sleep(2)

        # 첨부 탭 이동
        driver.find_elements(By.CLASS_NAME, 'lnbTopMenuItemText')[3].click()
        time.sleep(2)

        # 폴더 만들기 버튼 클릭
        driver.find_element(By.CLASS_NAME, 'uploadButton._folderCreateBtn').click()
        time.sleep(2)

        # 폴더명 입력 후 생성
        driver.find_element(By.ID, 'promptLabelId').send_keys('attachment selenium$$^^&&')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton._confirmButton').click()
        time.sleep(2)

        # 생성 후 앨범명 검증
        title = driver.find_element(By.CLASS_NAME, 'titleText._title').text
        check.equal(title, 'attachment selenium$$^^&&')

    # 앨범명 수정 취소 테스트
    def test_030_attachfolderedit(self):
        # 삼점 버튼 클릭 > 수정 버튼 > 취소
        driver.find_element(By.CLASS_NAME, 'btnMore._menuBtn').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'btnListItem._editBtn').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'uButton.-cancel._cancelButton').click()

        # 재진입하여 앨범명 변경 후 확인
        driver.find_element(By.CLASS_NAME, 'btnMore._menuBtn').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'btnListItem._editBtn').click()
        time.sleep(2)

        driver.find_element(By.ID, 'promptLabelId').clear()
        driver.find_element(By.ID, 'promptLabelId').send_keys(';;;;attachment move////')
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'uButton._confirmButton').click()
        time.sleep(2)

        # 타이틀명 변경되었는지 검증
        title = driver.find_element(By.CLASS_NAME, 'titleText._title').text
        check.equal(title, ';;;;attachment move////')

    # 첨부 탭 파일 업로드
    def test_031_fileupload(self):
        # 테스트 이미지 파일 업로드
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys('/Users/user/PycharmProjects/pythonProject/example/check.jpg')
        time.sleep(3)
        file_input2 = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input2.send_keys('/Users/user/PycharmProjects/pythonProject/example/testExcel.xlsx')
        time.sleep(2)

        # 목록 내 업로드된 파일명 검증
        firstname = driver.find_elements(By.CLASS_NAME, 'text.-ellipsis.gFw4')[0].text
        secondname = driver.find_elements(By.CLASS_NAME, 'text.-ellipsis.gFw4')[1].text

        check.equal(firstname, 'testExcel.xlsx')
        check.equal(secondname, 'check.jpg')

        # 우측 파일 영역에 업로드된 파일명 검증
        firstname = driver.find_elements(By.CLASS_NAME, 'text._downloadLink')[0].text
        secondname = driver.find_elements(By.CLASS_NAME, 'text._downloadLink')[1].text

        check.equal(firstname, 'testExcel.xlsx')
        check.equal(secondname, 'check.jpg')

        # 파일 업로드 날짜 검증
        createdate = driver.find_elements(By.CLASS_NAME, 'creationDate')[0].text
        now = datetime.datetime.now()
        today = str(now.year) + '년 ' + str(now.month) + '월 ' + str(now.day) + '일'
        check.equal(createdate, today)

        # 파일 업로드 개수 검증
        filecount = driver.find_element(By.CLASS_NAME, 'count.sf_color._count').text
        check.equal(filecount, '2')

    # 파일 정렬 옵션 테스트
    def test_032_filesort(self):
        # 정렬 오래된 순 보기로 변경하여 검증
        select = Select(driver.find_element(By.CLASS_NAME, '_orderBy'))
        select.select_by_value('created_at_asc')
        time.sleep(2)
        firstname = driver.find_elements(By.CLASS_NAME, 'text.-ellipsis.gFw4')[0].text
        check.equal(firstname, 'check.jpg')

        # 정렬 최신순 보기로 변경하여 검증
        select = Select(driver.find_element(By.CLASS_NAME, '_orderBy'))
        select.select_by_value('created_at_desc')
        time.sleep(2)
        firstname = driver.find_elements(By.CLASS_NAME, 'text.-ellipsis.gFw4')[0].text
        check.equal(firstname, 'testExcel.xlsx')

    # 파일 이동 테스트
    def test_033_filemove(self):
        # 관리 버튼 클릭
        driver.find_element(By.CLASS_NAME, 'uButton.-text.-manage._checkableOnBtn').click()
        time.sleep(2)

        # 파일 2개 체크 이동 클릭
        driver.find_elements(By.CLASS_NAME, 'checkInput._checkbox')[0].click()
        driver.find_elements(By.CLASS_NAME, 'checkInput._checkbox')[1].click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'uButton.-text._moveBtn').click()
        time.sleep(2)

        movefoldername = 'twomove newfloder!!'

        # 파일 이동 후 확인 버튼 검증
        driver.find_element(By.CLASS_NAME, 'uploadButton._newFolderBtn').click()
        time.sleep(2)
        driver.find_element(By.ID, 'promptLabelId').send_keys(movefoldername)
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'uButton._confirmButton').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'uButton._confirmBtn').click()
        time.sleep(2)

        successmsg = driver.find_element(By.CLASS_NAME, 'headingMsg').text
        check.equal(successmsg, '파일 이동 완료!')
        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        # 이동 후 파일 0개 검증
        foldercount = driver.find_element(By.CLASS_NAME, 'count.sf_color._count').text
        check.equal(foldercount, '0')
        driver.back()

        # 첨부 탭에서 파일들 이동 폴더로 변경되었는지 검증
        firstfolder = driver.find_elements(By.CLASS_NAME, 'folderName')[0].text
        secondfolder = driver.find_elements(By.CLASS_NAME, 'folderName')[1].text

        check.equal(firstfolder, movefoldername)
        check.equal(secondfolder, movefoldername)

        # 이동한 폴더로 이동
        driver.find_elements(By.CLASS_NAME, 'cFolderItemLink')[0].click()
        time.sleep(2)

        # 이동한 폴더에 카운트 증가 검증
        foldercount = driver.find_element(By.CLASS_NAME, 'count.sf_color._count').text
        check.equal(foldercount, '2')

        # 이동한 파일명 검증
        filename1 = driver.find_elements(By.CLASS_NAME, 'text.-ellipsis.gFw4')[0].text
        filename2 = driver.find_elements(By.CLASS_NAME, 'text.-ellipsis.gFw4')[1].text

        check.equal(filename1, 'testExcel.xlsx')
        check.equal(filename2, 'check.jpg')

    # 첨부파일 삭제
    def test_034_filedelete(self):
        # 관리 버튼 클릭
        driver.find_element(By.CLASS_NAME, 'uButton.-text.-manage._checkableOnBtn').click()
        time.sleep(2)

        # 2개 모두 체크 후 삭제
        driver.find_elements(By.CLASS_NAME, 'checkInput._checkbox')[0].click()
        driver.find_elements(By.CLASS_NAME, 'checkInput._checkbox')[1].click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'uButton.-text._deleteBtn').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        # 삭제 완료 메시지 검증
        deletemsg = driver.find_element(By.CLASS_NAME, 'headingMsg').text
        check.equal(deletemsg, '파일 삭제 완료!')

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        # 파일 개수 0개 검증
        count = driver.find_element(By.CLASS_NAME, 'count.sf_color._count').text
        check.equal(count, '0')
        driver.back()
        time.sleep(2)

        # 폴더 목록에서 0개 검증
        filecount = driver.find_elements(By.CLASS_NAME, 'files')[0].text
        check.equal(filecount, '0개')
            
    # 사진첩 앨범 만들기
    def test_035_albumcreate(self):
        driver.get('https://qa1.band.us/band/98191555')
        driver.find_elements(By.CLASS_NAME, 'lnbTopMenuItemText')[1].click()
        time.sleep(2)

        # 앨범 만들기 클릭
        #driver.find_element(By.CLASS_NAME, '_createAlbum.btn.uButton.sf_color.sf_tBorderOpacity').click()
        driver.find_element(By.CLASS_NAME, 'iconPlus._createAlbum').click()
        time.sleep(2)

        driver.find_element(By.ID, 'promptLabelId').send_keys('selenium album!!')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton._confirmButton').click()
        driver.switch_to.alert.accept()
        time.sleep(2)

        albumtitle = driver.find_element(By.CLASS_NAME, 'titleText._albumNameTitle').text
        check.equal(albumtitle, 'selenium album!!')
        time.sleep(2)

        #사진 올리기 버튼 검증
        filebutton = driver.find_element(By.CLASS_NAME, 'btn.uButton.sf_tBorderOpacity.sf_color._headerPhotoInputWrap.js-fileapi-wrapper').is_displayed()
        check.is_true(filebutton)

    # 앨범명 수정하기
    def test_036_albumedit(self):
        driver.find_element(By.CLASS_NAME, 'btnMore').click()
        time.sleep(2)

        #앨범 수정 버튼 클릭
        driver.find_elements(By.CLASS_NAME, 'btnListItem')[2].click()
        time.sleep(2)

        driver.find_element(By.ID, 'promptLabelId').clear()
        time.sleep(2)
        driver.find_element(By.ID, 'promptLabelId').send_keys('album명 수정하기')
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'uButton._confirmButton').click()
        time.sleep(2)

        albumtitle = driver.find_element(By.CLASS_NAME, 'titleText._albumNameTitle').text
        check.equal(albumtitle, 'album명 수정하기')

    # 사진첩에 이미지 업로드
    def test_037_photoupload(self):
        driver.find_elements(By.CLASS_NAME, 'lnbTopMenuItemText')[1].click()
        time.sleep(2)

        #테스트 이미지 파일 업로드
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys('/Users/user/PycharmProjects/pythonProject/example/check.jpg')
        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._submitBtn').click()
        time.sleep(2)

        #여러개 중에 첫번째
        driver.find_elements(By.CLASS_NAME, 'album')[0].click()
        time.sleep(2)

        #사진 상세 확인
        imagewrap = driver.find_element(By.CLASS_NAME, 'mediaWrap._mediaWrap').is_displayed()
        fullbutton = driver.find_element(By.CLASS_NAME, 'btnCommentToggle._fullScreenButton').is_displayed()
        albumbutton = driver.find_element(By.CLASS_NAME, 'goAlbum._goAlbumButton').is_displayed()
        commentbutton = driver.find_element(By.CLASS_NAME, 'mentions-input._prevent_toggle').is_displayed()

        check.is_true(imagewrap)
        check.is_true(fullbutton)
        check.is_true(albumbutton)
        check.is_true(commentbutton)

        driver.find_element(By.CLASS_NAME, 'btnLyClose._directCloseButton').click()
        time.sleep(2)

    # 이미지 이동하기
    def test_038_uploadedit(self):
        driver.find_element(By.CLASS_NAME, 'uButton.-text.-manage._selectButton').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'checkInput._checkBoxInput').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-text._sendPhotoButton').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'makeAlbum').click()
        time.sleep(2)

        driver.find_element(By.ID, 'promptLabelId').send_keys('selenium moveAlbum')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton._confirmButton').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'footer.-tLine').find_elements(By.TAG_NAME, 'button')[1].click()
        time.sleep(2)

        #사진 이동 성공 팝업 닫기
        driver.switch_to.alert.accept()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'lnbTopMenuItemText')[1].click()
        time.sleep(2)

        #albumname = driver.find_element(By.CSS_SELECTOR, 'div.albumHeader > div > h3 > a > strong').text
        albumname = driver.find_elements(By.CLASS_NAME, 'albumName')[0].text
        check.equal(albumname, 'selenium moveAlbum')

        #albumcount = driver.find_element(By.CSS_SELECTOR, 'div.albumHeader > div > h3 > a > em').text
        albumcount = driver.find_elements(By.CLASS_NAME, 'albumInfo')[0].find_element(By.CLASS_NAME, 'count').text
        check.equal(albumcount, '1장')

    # 이미지 삭제
    def test_039_imagedelete(self):
        driver.find_elements(By.CLASS_NAME, 'albumName')[0].click()
        time.sleep(2)

        albumcount = driver.find_element(By.CLASS_NAME, 'count.sf_color._photoCountEl').is_displayed()
        check.is_true(albumcount)

        driver.find_element(By.CLASS_NAME, 'uButton.-text.-manage._selectButton').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'checkInput._checkBoxInput').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-text._deletePhotoButton').click()
        time.sleep(2)

        driver.switch_to.alert.accept()
        time.sleep(2)

        albumcount = driver.find_element(By.CLASS_NAME, 'count.sf_color._photoCountEl').is_displayed()
        check.is_false(albumcount)

    # 앨범 정렬 옵션
    def test_040_albumrange(self):
        driver.find_elements(By.CLASS_NAME, 'lnbTopMenuItemText')[1].click()
        time.sleep(2)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'albumSort._albumSortMenuWrap').click()
        time.sleep(2)
        driver.find_elements(By.CLASS_NAME, 'btnListItem._albumSortOptionButton')[2].click()
        time.sleep(2)

        firstalbum = driver.find_elements(By.CLASS_NAME, 'albumName')[0].text
        check.equal(firstalbum, 'album명 수정하기')

        driver.find_element(By.CLASS_NAME, 'albumSort._albumSortMenuWrap').click()
        time.sleep(2)
        driver.find_elements(By.CLASS_NAME, 'btnListItem._albumSortOptionButton')[3].click()
        time.sleep(2)

        firstalbum = driver.find_elements(By.CLASS_NAME, 'albumName')[0].text
        check.equal(firstalbum, 'selenium moveAlbum')

    # 앨범 삭제하기
    def test_041_albumdelete(self):

        albumcount = len(driver.find_elements(By.CLASS_NAME, 'albumInfo'))

        driver.find_elements(By.CLASS_NAME, 'albumItem')[0].click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'btnMore').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'btnListItem')[3].click()
        time.sleep(2)

        driver.switch_to.alert.accept()
        time.sleep(2)

        newcount = len(driver.find_elements(By.CLASS_NAME, 'albumInfo'))

        check.equal(albumcount-1, newcount)

    # 일정 작성 테스트
    def test_042_calcreate(self):
        driver.find_elements(By.CLASS_NAME, 'lnbTopMenuItemText')[2].click()
        time.sleep(2)

        cal_count = len(driver.find_elements(By.CLASS_NAME, 'scheduleItem._schedule'))

        driver.find_element(By.CLASS_NAME, 'uButton.sf_color.sf_tBorderOpacity._btnAddSchedule').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, '_scheduleName').send_keys('cal_title auto')
        driver.find_element(By.CLASS_NAME, '_description').send_keys('!!auto_test_gogo!!')
        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnSubmit').click()
        time.sleep(2)

        change_count = len(driver.find_elements(By.CLASS_NAME, 'scheduleItem._schedule'))
        check.equal(cal_count+1, change_count)

    # 일정 수정 테스트
    def test_043_calchange(self):
        driver.find_element(By.CLASS_NAME, 'scheduleEndTime').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'postSet._moreButton').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, '_optionMenuLink')[0].click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, '_scheduleName').clear()
        time.sleep(1)

        driver.find_element(By.CLASS_NAME, '_scheduleName').send_keys('change CAL')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnSubmit').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        title_text = driver.find_element(By.CLASS_NAME, 'contWrap').find_element(By.CLASS_NAME, 'title').text
        check.equal(title_text, 'change CAL')

    # 일정 댓글 작성 테스트
    def test_044_calcommentwrite(self):
        driver.find_element(By.CLASS_NAME, 'commentWrite._use_keyup_event._messageTextArea').send_keys('comment write test')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'btnCommentSubmit._sendMessageButton.-active').click()
        #driver.find_element(By.CLASS_NAME, 'writeSubmit.uButton._sendMessageButton.-active').click()
        time.sleep(2)

        comment_text = driver.find_element(By.CLASS_NAME, 'txt._commentContent').text
        check.equal(comment_text, 'comment write test')

    # 일정 댓글 수정 테스트
    def test_045_calcommentchange(self):
        driver.find_element(By.CLASS_NAME, 'commentEdit').click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, '댓글 수정').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'commentWrite._modificationTextarea._use_keyup_event').clear()
        driver.find_element(By.CLASS_NAME, 'commentWrite._modificationTextarea._use_keyup_event').send_keys('1234567890ASDF')
        driver.find_element(By.CLASS_NAME, 'btnCommentSave.gMar6._submitButton').click()
        #driver.find_element(By.CLASS_NAME, 'buttonCommentModi.buttonPoint._submitButton').click()
        time.sleep(2)

        comment_text = driver.find_element(By.CLASS_NAME, 'txt._commentContent').text
        check.equal(comment_text, '1234567890ASDF')

    # 일정 댓글 삭제 테스트
    def test_046_calcommentdel(self):
        commentelement = driver.find_element(By.CLASS_NAME, 'commentEdit').is_displayed()
        check.is_true(commentelement)

        driver.find_element(By.CLASS_NAME, 'commentEdit').click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, '댓글 삭제').click()
        time.sleep(2)

        driver.switch_to.alert.accept()
        time.sleep(2)

        commentelement = driver.find_elements(By.CLASS_NAME, 'commentEdit')
        check.equal(len(commentelement), 0)

    # 일정 삭제 테스트
    def test_047_caldel(self):
        cal_count = len(driver.find_elements(By.CLASS_NAME, 'scheduleItem._schedule'))

        driver.find_element(By.CLASS_NAME, 'postSet._moreButton').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, '_optionMenuLink')[6].click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-cancel._btnCancel').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'postSet._moreButton').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, '_optionMenuLink')[6].click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
        time.sleep(2)

        change_count = len(driver.find_elements(By.CLASS_NAME, 'scheduleItem._schedule'))
        check.equal(cal_count-1, change_count)

    '''  
    # ------------------ 소모임 ----------------------
    # 소모임 탭 지역 변경 테스트
    def test_070_localchange(self):
        driver.find_element(By.CLASS_NAME, '_tabMyLocalMeetup.tab').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'openKeyword._regionSelectBtn').click()
        time.sleep(2)

        driver.find_element(By.ID, 'regionSearch').send_keys('분당구 서현동')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'btnSearch.uButton.-sizeS.-default._btnSearch.-active').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'searchResultsList').click()
        time.sleep(2)

        localtext = driver.find_element(By.CLASS_NAME, 'localTitle').text
        check.equal(localtext[0:7], '서현동 소모임')

        driver.find_element(By.CLASS_NAME, 'openKeyword._regionSelectBtn').click()
        time.sleep(2)

        driver.find_element(By.ID, 'regionSearch').send_keys('정자동')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'btnSearch.uButton.-sizeS.-default._btnSearch.-active').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'searchResultsItem')[1].click()
        time.sleep(2)

        localtext = driver.find_element(By.CLASS_NAME, 'localTitle').text
        check.equal(localtext[0:7], '정자동 소모임')

    # 지역 검색 추가/삭제 테스트
    def test_071_localhistory(self):
        driver.find_element(By.CLASS_NAME, 'openKeyword._regionSelectBtn').click()
        time.sleep(2)

        #basecount = len(driver.find_elements(By.CLASS_NAME, 'searchResultsList'))

        driver.find_element(By.ID, 'regionSearch').send_keys('부산 동구')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'btnSearch.uButton.-sizeS.-default._btnSearch.-active').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'searchResultsItem')[4].click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'openKeyword._regionSelectBtn').click()
        time.sleep(2)

        driver.find_element(By.ID, 'regionSearch').send_keys('경기도 남양주시')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'btnSearch.uButton.-sizeS.-default._btnSearch.-active').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'searchResultsItem')[3].click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'openKeyword._regionSelectBtn').click()
        time.sleep(2)

        historycount = len(driver.find_elements(By.CLASS_NAME, 'searchResultsItem'))
        check.equal(historycount-1, 4)

        driver.find_elements(By.CLASS_NAME, 'buttonDelete._btnDelete')[1].click()
        time.sleep(2)

        historycount = len(driver.find_elements(By.CLASS_NAME, 'searchResultsItem'))
        check.equal(historycount-1, 3)

        secondhistory = driver.find_elements(By.CLASS_NAME, 'buttonText._btnSelect')[1].text
        check.equal(secondhistory, '분당구 정자동')

        driver.find_elements(By.CLASS_NAME, 'buttonDelete._btnDelete')[0].click()
        time.sleep(2)

        historycount = len(driver.find_elements(By.CLASS_NAME, 'searchResultsItem'))
        check.equal(historycount-1, 2)

        secondhistory = driver.find_elements(By.CLASS_NAME, 'buttonText._btnSelect')[1].text
        check.equal(secondhistory, '분당구 서현동')

        for i in range(0, 2):
            driver.find_element(By.CLASS_NAME, 'buttonDelete._btnDelete').click()
            time.sleep(2)

        flag = len(driver.find_elements(By.CLASS_NAME, 'searchResultsItem'))
        check.equal(flag, 1)

        driver.find_element(By.CLASS_NAME, 'uButton.-iconClose.btnLyClose._btnClose').click()
        time.sleep(2)

    # 소모임 밴드 만들기 테스트
    def test_072_localnewband(self):
        driver.find_element(By.CLASS_NAME, 'makeMission._recruitBtn').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'checkLabel')[0].click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._confirmBtn').click()
        time.sleep(2)

        try:
            url = driver.current_url
            check.equal(url, 'https://qa1.band.us/band-create/lfg/local')

            driver.find_element(By.ID, 'ex_name').send_keys('localmeetingCheck')
            time.sleep(2)

            driver.find_element(By.ID, 'introduction').send_keys('one two three four five six seven eight nine ten gogo')
            time.sleep(2)

            driver.find_element(By.CLASS_NAME, '_btnKeyword.addButton').click()
            time.sleep(2)

            driver.find_elements(By.CLASS_NAME, 'checkLabel')[1].click()
            time.sleep(2)

            driver.find_element(By.CLASS_NAME, 'uButton.-confirm._btnConfirm').click()
            time.sleep(2)

            driver.find_element(By.CLASS_NAME, '_btnRegion.addButton').click()
            time.sleep(2)

            driver.find_element(By.ID, 'regionSearch').send_keys('구로동')
            time.sleep(2)

            driver.find_element(By.CLASS_NAME, 'btnSearch.uButton.-sizeS.-default._btnSearch.-active').click()
            time.sleep(2)

            driver.find_element(By.CLASS_NAME, 'buttonText._btnSelect').click()
            time.sleep(2)

            driver.find_element(By.CLASS_NAME, '_btnConfirm.uButton.-sizeXL.-confirm').click()
            time.sleep(5)

            subtitle = driver.find_element(By.CLASS_NAME, 'introSubTitle').text
            check.equal(subtitle, '소모임 정보')

            localtext = driver.find_element(By.CLASS_NAME, 'keywordButton').text
            check.equal(localtext, '구로동')

            categorytext = driver.find_element(By.CLASS_NAME, 'keywordButton._btnLocalKeyword').text
            check.equal(categorytext, '등산/산악')

            driver.get('https://qa1.band.us/local-meetup')
            time.sleep(2)
        except UnexpectedAlertPresentException:
            # popuptext = driver.switch_to.alert.text
            # check.equal(popuptext, '소모임은 1일 1개, 30일 내 10개까지 모집할 수 있습니다.')
            driver.switch_to.alert.accept()

    # 소모임 밴드 상세 테스트
    def test_073_localcategory(self):
        scrollelement('uHelpGuideRound.-close')

        driver.find_elements(By.CLASS_NAME, 'localMeetupContentLink._itemBandLink')[2].click()
        time.sleep(2)

        newtab()

        subtitle = driver.find_element(By.CLASS_NAME, 'introSubTitle').text
        check.equal(subtitle, '소모임 정보')

        closenewtab()

    # 기존 밴드 소모임 모집하기 테스트
    def test_074_localexistingband(self):
        driver.get('https://'+checkurl+'/local-meetup')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'makeMission._recruitBtn').click()
        time.sleep(2)

        driver.find_elements(By.CLASS_NAME, 'checkLabel')[1].click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'uButton.-confirm._confirmBtn').click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'buttonCapsule._applyBtn').click()
        time.sleep(2)

        titletext = driver.find_element(By.CLASS_NAME, 'title').text
        check.equal(titletext, '지역 소모임 설정')

        driver.find_element(By.CLASS_NAME, 'detailView.-arrowRight').click()
        time.sleep(2)

        newtab()

        tab = driver.current_url
        check.equal(tab, 'https://band.us/cs/notice/4741')

        closenewtab()

    # 피드 메인 테스트
    def test_075_feedmain(self):
        driver.find_elements(By.CLASS_NAME, 'widgetItem')[0].click()
        time.sleep(2)

        feedactive = driver.find_element(By.CLASS_NAME, 'tab._tabMyFeed.-active').is_displayed()
        check.is_true(feedactive)

        writebutton = driver.find_element(By.CLASS_NAME, 'feedWriteButton.gContentCardShadow.gBoxHoverShadow._writeButton').is_displayed()
        check.is_true(writebutton)

        createbutton = driver.find_element(By.CLASS_NAME, 'makeBand.gBoxShadow.gBoxHoverShadow._bandCreateLink').is_displayed()
        check.is_true(createbutton)

        feedcards = driver.find_elements(By.CLASS_NAME, 'cContentsCard._postMainWrap')
        check.is_true(feedcards[0])
        check.is_true(feedcards[1])






































