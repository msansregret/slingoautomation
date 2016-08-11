from sikuli import *
import time
import dialogs

global reg
reg = SCREEN

def setup_chrome(os, fb_username, fb_password, envURL):
    """Opens Chrome, opens an ingocnito tab, and then loads the Slingo URL
    Args:
        os: the operating system you're on. Only support "MAC" and "WIN".
    Return:
        returns a region of the screen where chrome was found.
    """
    global os_type
    os_type = os
    if os_type == "MAC":
        chrome = App('Google Chrome')
    elif os_type == "WIN":
        chrome = App('C:\\Program Files (x86)\\Google\\Chrome\\' +
                     'Application\\chrome.exe')
    else:
        raise OSError('The OS you specified: {} is not supported!'.format(os))

    # TODO: handle open() failure.
    chrome.open()
    wait(2)

    global reg
    if os_type == "MAC":
        # There is no process here trying to determining where Chrome is,
        # not because Mac has no such problem,
        # but because Mike's Mac only has 1 monitor.
        assert exists("ChromeButtons_mac.png", 10)
    else:
        # Find out which monitor chrome is at,
        # and set that monitor to app_screen.
        if Screen(0).exists("chrome_buttons_win.png", 5):
            reg = Screen(0)
        elif Screen(1).exists("chrome_buttons_win.png", 5):
            reg = Screen(1)
        else:
            raise
        (CustomExceptions.AppOpenError("Sikuli seems to have trouble" +
                                       "finding an open Chrome window."))

    wait(1)
    if os_type == "MAC":
        type("n", KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type("n", KeyModifier.CTRL + KeyModifier.SHIFT)

    assert reg.exists("ChromeIncognitoIcon.png", 5)
    login_facebook_(fb_username, fb_password)
    wait(1)
    if os_type == "MAC":
        type("l", KeyModifier.CMD)
    else:
        type("l", KeyModifier.CTRL)
    wait(1)
    paste(envURL)
    type(Key.ENTER)
    wait(1)
    return reg

def close_chrome():
    """Closes Google Chrome.

    Args:
        os: "MAC" or "WIN".

    """
    if os_type == "MAC":
        chrome = App('Google Chrome')
    else:
        chrome = App(
            (r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'))
    chrome.focus()
    chrome.close()
    wait(2)

def openTabChrome():
    """Open chrome tab"""
    type("n",Key.CMD + Key.SHIFT)
    assert exists("ChromeIncognitoIcon.png",5)

def closeTabChrome():
    """Closes chrome tab"""
    if os_type == "MAC":
        type("w",Key.CMD)
    else:
        type("w".Key.CTRL)
        
    wait(1)

def login_facebook_(fb_user, fb_password):
    """ Type in facebook.com, login using provided parameters.

    Args:
        fb_user: facebook username
        fb_password: facebook password
        os: operating system, "MAC" or "WIN".

    Return:
        It doesn't return anything
    """
    type("l", KeyModifier.CTRL)
    type("facebook.com")
    type(Key.ENTER)
    assert reg.exists("FacebookLoginPageLogo.png",10)
    type("0", KeyModifier.CTRL)
    if os_type == "MAC":
        assert reg.exists("FacebookLoginFields.png", 10)
    else:
        assert reg.exists("login_incognito_win.png", 10)
    wait(1)
    if os_type == "MAC":
        reg.click(
            (Pattern("FacebookLoginFields.png").targetOffset(-163, -3)))
    else:
        reg.click(
            (Pattern("login_incognito_win.png").targetOffset(-155, 1)))
    paste(fb_user)
    type(Key.TAB)
    wait(1)
    paste(fb_password)
    type(Key.ENTER)
    wait(1)
    assert exists("facebook_logged_in.png",5)
    wait(2)

def load_slingo_env(URL):
    """Pastes the URL for slingo QA1, DEV1, PROD, etc...
       Then executes the browser to load that page"""
    type("l",Key.CMD)
    paste(URL)
    type(Key.ENTER)
    wait(2)

def check_load_slingo():
    """Checks if slingo loads and tries to report how much time it took. 
       Also if it loads it sets up the Region for all further tests
       """
    global reg
    start_time = time.time()
    if reg.exists(Pattern("MuteButtons.png").similar(0.65),40):
        assert True
        reg = _set_slingo_reg()
    else: 
        if exists(Pattern("fb_enjoying_check.png").targetOffset(142,2),1):
            click(getLastMatch())
            if exists(Pattern("MuteButtons.png").similar(0.65)):
                assert True
                reg = _set_slingo_reg()
            else:
                assert False, "Slingo not able to be found"
        else:
            assert False, "Slingo not able to be found"
 
    elapsed_time = time.time() - start_time
    print "Slingo took: " + str(elapsed_time) + " seconds to load"
    return Region(reg)


def _set_slingo_reg():
    """Finds Slingo and returns a region square around the slingo 
       flash player. This is a critical component of the reg screen 
       class,  which further image compares use to improve effeciency.
       """
    home = exists(Pattern("MuteButtons.png").similar(0.65),3)
    new_reg = Region(home.x - 731,home.y - 10,755,645)
    new_reg.highlight(1)
    return new_reg

def reset_player_progress():
    """Uses the cheat menu to delete the player then reloads 
       the page to restart slingo"""
    assert reg.exists(Pattern("MuteButtons-1.png").similar(0.65).targetOffset(15,-25),3)
    click(reg.getLastMatch())
    type("c")
    wait(1)
    assert reg.exists("PlayerCurrency.png")
    reg.doubleClick(Pattern("CheatDeletePlayerButton.png").similar(0.90))
    click(Pattern("ChromeButtons.png").targetOffset(-14,0))
    wait(2)
    check_load_slingo()

def set_top_bar(hearts, coins, spinners):
    """Sets hearts, coins, and spinners to values given as variables. 
       Uses the cheat menu."""
    assert reg.exists(Pattern("MuteButtons-1.png").similar(0.65).targetOffset(15,-25),3)
    click(reg.getLastMatch())
    type("c")
    wait(1)
    assert reg.exists(Pattern("PlayerCurrency.png").targetOffset(-10,-28))
    reg.click(Pattern("PlayerCurrency.png").targetOffset(-7,-48))
    
    reg.doubleClick(Pattern("PlayerCurrency.png").targetOffset(-37,-46))
    paste(str(hearts))
    reg.click(Pattern("PlayerCurrency.png").targetOffset(-9,-10))
    reg.doubleClick(Pattern("PlayerCurrency.png").targetOffset(-42,-11))
    paste(str(coins))
    reg.click(Pattern("PlayerCurrency.png").targetOffset(37,8))
    reg.doubleClick(Pattern("PlayerCurrency.png").targetOffset(10,8))
    paste(str(spinners))
    reg.click(Pattern("PlayerCurrency.png").targetOffset(-86,44))
    type("c")

    wait(1)

def admin_adjust_player(player_fb_id, 
                        hearts=0, 
                        reset_rva_coins=False, 
                        envURL = r"http://qa1-slingo-app.bstage.ca/slingo/console/index.htm"):
    """Uses the admin page to adjust player data"""
    openTabChrome()
    load_slingo_env(envURL)
    reg_login_observe = SCREEN
    reg_login_observe.onAppear("AdminConsoleLogin.png",login_admin_page)
    reg_login_observe.observe(10,True)

    assert exists("AdminPageBanner.png",10)
    click(Pattern("AdminPageFBIDField.png").similar(0.80))
    wait(1)
    paste(str(player_fb_id))
    wait(1)
    click(Pattern("AdminPageSearchButton.png").similar(0.75))
    assert exists(Pattern("PlayerIDSkeletor.png").similar(0.98),5)

    if hearts > 0:
        count = 0
        while not exists(Pattern("AdminPageHearts.png").similar(0.95)):
            #wheel(Pattern("ChromeButtons-1.png").targetOffset(0,38),WHEEL_DOWN,3)
            type(Key.PAGE_DOWN)
            count += 1
            if count >= 10:
                break
    
        doubleClick(Pattern("AdminPageHearts.png").similar(0.95))
        wait(1)
        paste(str(hearts))
        click(Pattern("AdminPageHearts.png").similar(0.95).targetOffset(186,-1))
        assert exists("AdimPageConfirmation.png",5)
        wait(1)
        type(Key.ENTER)
        wait(2)

    if reset_rva_coins == True:
        count = 0
        while not exists(Pattern("AdminPageRewardCoinCount.png").similar(0.85)):
            type(Key.PAGE_DOWN)
            count += 1
            if count >= 10:
                break

        click(Pattern("AdminPageRewardCoinCount.png").similar(0.85).targetOffset(446,1))
        wait(1)
        doubleClick(Pattern("AdminPageRewardCoinCount.png").similar(0.85).targetOffset(192,1))
        paste("0")
        click(Pattern("AdminPageRewardCoinCount.png").similar(0.85).targetOffset(380,1))
        wait(2)
        
    closeTabChrome()
    wait(3)
    assert exists(Pattern("ChromeButtons-1.png").targetOffset(-14,0),3)
    click(getLastMatch())
    wait(3)
    checkLoadSlingo()

def login_admin_page(event):
    """If the login observer sees the login window, this 
       handles the login."""
    
    print "Logging into Admin Page"
    click("AdminConsoleLogin.png")
    wait(1)
    paste("producer")
    type(Key.TAB)
    wait(1)
    paste("stillsomejasper")
    type(Key.ENTER)

def refill_hearts():
    """ Use spinners to refill hearts; buy more spinners if needed."""
    assert reg.exists(Pattern("HeartsStore.png").targetOffset(54, 1), 2)
    click(reg.getLastMatch())
    assert reg.exists("RefillHeartsSpinnersButton.png", 8)
    click(reg.getLastMatch())
    
    dialogs.handle_spinner_prompt(2)
    assert reg.exists(Pattern("HeartsFull.png").similar(0.90), 3)