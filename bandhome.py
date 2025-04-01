



# 밴드 가이드, 데스크톱 메뉴 테스트
def test_002_bandmainlink(self):
    # 밴드 가이드 버튼 클릭
    driver.find_element(By.CLASS_NAME, 'btnOption._linkGuideBand').click()
    time.sleep(2)

    # URL 검증
    url = driver.current_url
    check.equal(url, 'https://band.us/band/62396709')

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
    check.equal(url, 'https://band.us/cs/notice/1301')

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
    check.equal(url, 'https://band.us/open-feed')

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
        infobutton = driver.find_element(By.CLASS_NAME, 'buttonIntroMore').is_displayed()
        check.is_true(infobutton)
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
        check.equal(url, 'https://band.us/discover')

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
    check.equal(url, 'https://band.us/cs/notice')

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
    check.equal(url, 'https://band.us/policy/privacy')

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
    check.equal(url, 'https://band.us/cs/help')

    # 도움말 목록 타이틀 확인
    title = driver.find_element(By.CLASS_NAME, 'sectionTitle.-bg').text
    check.equal(title, '자주 묻는 질문')

    closenewtab()