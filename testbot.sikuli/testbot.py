"""Slingo Adventure Test Bot, containing low level functions.

Test suites rely on this framework to perform system setup
and game play controlling.

Sample functions:
    setup_chrome()
    close_chrome()

Deprecated functions (such as setupChrome()) are all at the bottom of the file.

"""
from sikuli import *
import os
import time
import sys
import re
import inspect
import shutil
import setup
import dialogs
import maps
import levels
import CustomExceptions
from create_json import *

sys.path.insert(0, r"C:\Users\Charlie Guan\Code\sikuliScripts' \
                '\sikuliTestBotV2.sikuli\sikuliTestBotV2.py")

# Global Variables
global reg
reg = Screen(0)
global app_screen  # the monitor chrome is running on
app_screen = SCREEN

fbUser1 = "automation_qfhrcjq_test@tfbnw.net"
fbPassword1 = "test123"
URLQA = r"https://apps.facebook.com/qa-one-slingo/"

def take_screenshot(filename='moment_before_click.png'):
    """Take a screenshot and save it in /adventure_canvas/screenshots folder."""
    screenshotsDir = "screenshots"
    img = capture(reg)
    shutil.move(img, os.path.join(
        screenshotsDir, filename))

def setup_testing(os="MAC",
                  fb_username=fbUser1, 
                  fb_password=fbPassword1, 
                  envURL=URLQA):
    """Uses setup module to setup the test environment. Passes along variables
       from testsuite."""
    reg = setup.setup_chrome(os,fb_username, fb_password, envURL)
    dialogs.reg = maps.reg = setup.reg = levels.reg = reg

def check_load_slingo():
    global reg
    reg = setup.check_load_slingo()
    dialogs.reg = Region(reg)
    maps.reg = Region(reg)
    setup.reg = Region(reg)
    levels.reg = Region(reg)

def check_reset_progress():
    setup.reset_player_progress()

def check_spinner_store(spins):
    """Check if spinners can be bought, and if the total is expected."""
    costDict = {20:Pattern("spinner_store_price_399-1.png").similar(0.95).targetOffset(89,2),30:Pattern("spinner_store_price_499-1.png").similar(0.95).targetOffset(89,2),90:Pattern("spinner_store_price_999-1.png").similar(0.95).targetOffset(89,2),200:Pattern("spinner_store_price_1999-1.png").similar(0.95).targetOffset(93,1),600:Pattern("spinner_store_price_4999-1.png").similar(0.95).targetOffset(95,-1)}
    try:
        dialogs.clear_dialogs()
    except:
        raise CustomExceptions.UIError("Sikuli can't close dialogs.")

    setup.set_top_bar(hearts = 0, coins = 0, spinners = (1000 - spins))    
    assert reg.exists(Pattern("TopBarSpinners-2.png").similar(0.60).targetOffset(46,2),3)
    click(reg.getLastMatch())

    assert reg.exists(costDict[spins],3)
    click(reg.getLastMatch())
    wait(2)
    dialogs.click_thru_fb_buy()
    reg.wait("1467072782461-1.png",10)
    
    assert reg.exists(Pattern("TopBarSpinners-2.png").similar(0.60),5).exists(Pattern("topbar_spinner_total_1000-1.png").similar(0.90),3)

def check_coins_store(coins,spins):
    """ Checks if x coins can be bought for y spinners. """
    costDict = {5:Pattern("coins_store_spinner_cost_5-1.png").similar(0.90),8:Pattern("CoinsStore8Spinner-1.png").similar(0.90),14:Pattern("CoinsStore14Spinner-1.png").similar(0.90),20:Pattern("coins_store_spinner_cost_20-1.png").similar(0.90)}
    try: 
        dialogs.clear_dialogs()
    except:
        pass

    setup.set_top_bar(hearts = 0, coins = (40001 - coins), spinners = spins)
    
    assert reg.exists(Pattern("coinsTopBar-2.png").similar(0.60).targetOffset(69,-1),5)
    click(reg.getLastMatch())
    
    assert reg.exists(costDict[spins],3)
    click(reg.getLastMatch())
    wait(2)
    assert reg.exists(Pattern("coinsTopBar-2.png").similar(0.60).targetOffset(69,-1),10).exists(Pattern("top_bar_coins_total_40001-1.png").similar(0.90),3)
    assert reg.exists(Pattern("TopBarSpinners-1.png").similar(0.60),3).exists(Pattern("top_bar_spinner_total_0-1.png").similar(0.90),3)
    
def check_refill_hearts():
    """Checks if hearts can be refilled with Golden Spinners on the map. 
       Aborts if HHH is Active."""
    if reg.exists("HHHStore-2.png",2):
        print 'Hearts Happy Hour is active'
        return False

    setup.set_top_bar(4, 1, 5)
    assert reg.exists(Pattern("HeartsStore-2.png").targetOffset(54, 1), 5)
    click(reg.getLastMatch())
    assert reg.exists("RefillHeartsSpinnersButton-2.png", 8)
    click(reg.getLastMatch())
    assert reg.exists(Pattern("HeartsFull-2.png").similar(0.90), 2)
    assert reg.exists("TopBarSpinnerIcon-2.png", 10).right().exists(
        Pattern("SpinnerTotal0-2.png").similar(0.90))

def check_refill_hearts_level():
    """Checks if hearts can be refilled with spinners during a level.
    Abort if HHH is active."""
    if reg.exists("HHHStore-2.png", 2):
        print('Hearts Happy Hour is active')
        return False

    setup.set_top_bar(4, 1, 5)
    maps.select_level(1)
    levels.verify_level_load()
    assert reg.exists(Pattern("HeartsStore-1.png").targetOffset(54, 1), 5)
    click(reg.getLastMatch())
    assert reg.exists("RefillHeartsSpinnersButton-2.png", 8)
    click(reg.getLastMatch())
    assert reg.exists(Pattern("HeartsFull-2.png").similar(0.90), 2)
    assert reg.exists("TopBarSpinnerIcon-1.png", 10).right().exists(
        Pattern("SpinnerTotal0-1.png").similar(0.90))
    levels.exit_level()

def check_PUP_store():
    """Loads a level with a power up equipped, then check if power up
    is present in level, and coin balance is correct."""
    try:
        dialogs.clear_dialogs()
    except:
        raise CustomExceptions.UIError("Sikuli can't close dialogs.")

    setup.set_top_bar(5, 6500, 5)
    maps.select_level(4)

    assert reg.exists(pupDict["extraspins4"], 2)
    click(reg.getLastMatch())
    assert reg.exists("PUPStoreExtraSpins-1.png", 2)
    reg.click("PUPStoreBuyButton-1.png")

    assert reg.exists("CoinStoreIcon-1.png", 10).right().exists(
        Pattern("CoinTotal500-1.png").similar(0.90), 3)
    levels.verify_level_load()
    wait(3)
    assert reg.exists("CoinStoreIcon-1.png", 10).right().exists(
        Pattern("CoinTotal500-1.png").similar(0.90), 3)
    setup.set_top_bar(5, 6500, 5)
    wait(2)
    levels._spin_and_daub()
    assert reg.exists(pupDict["jokerplus"])
    click(reg.getLastMatch())
    assert reg.exists("PUPStoreJokerPlus-1.png", 3)
    reg.click("PUPStoreBuyButton-1.png")

    assert reg.exists("CoinStoreIcon-1.png", 10).right().exists(
        Pattern("CoinTotal500-1.png").similar(0.90), 3)
    levels._spin_and_daub()

    levels.exit_level()

def check_FTU_level_1(rush=False):
    """Checks first time user level 1 experience.

    Args:
        rush:   True to skip the 45 sec animation;
                False to wait for it to end.

    """
    assert reg.exists("FTUBannerNewPlayerSpecial-1.png", 30)
    dialogs.close_dialog()
    levels.check_spin_button(8)
    click(reg.getLastMatch())
    wait(4)
    assert reg.exists(Pattern("FTULvl1Tile10-1.png").similar(0.90), 4)
    click(reg.getLastMatch())

    levels._spin_and_daub()
    levels.check_spin_button(3)
    click(reg.getLastMatch())
    wait(3)

    levels._repeat_spin_and_daub(5)
    wait(3)
    levels._spin_and_daub()
    assert reg.exists("NISSkipButton-2.png", 10)
    if rush is True:
        # skip the 45sec animation
        click(reg.getLastMatch())
        assert reg.exists("sign_out_next_button-2.png", 5)
        click(reg.getLastMatch())
        wait(2)
    else:
        assert reg.exists("sign_out_next_button-2.png", 45)
        wait(1)
        click(reg.getLastMatch())
        wait(2)

def check_FTU_level_2(rush=False):
    """Check level 2 first time user experience."""
    assert reg.exists(Pattern("FTULevel2Node-1.png").similar(0.90), 3)
    click(reg.getLastMatch())
    assert reg.exists("PUPStorePlayButton-1.png", 3)
    click(reg.getLastMatch())
    wait(5)
    # only appears on the first level 2 play through
    assert reg.exists("NISSkipButton-2.png", 10)
    if rush is True:
        click(reg.getLastMatch())
    levels.check_spin_button(15)
    click(reg.getLastMatch())
    wait(3)
    levels._daub_matrix()

    levels._repeat_spin_and_daub(3)

    levels.check_spin_button(3)
    click(reg.getLastMatch())
    wait(3)

    levels._repeat_spin_and_daub(4)
    assert reg.exists("sign_out_next_button-1.png", 20)
    wait(1)
    click(reg.getLastMatch())
    wait(2)


def check_FTU_level_3():
    """Check level 3 FTUE."""
    maps.select_level(3)
    reg.click("PUPStorePlayButton-1.png")

    levels.check_spin_button(30)
    click(reg.getLastMatch())
    wait(3)
    levels._daub_matrix()

    levels._repeat_spin_and_daub(16)
    wait(3)
    assert reg.exists("TutorialClaimFreeSpinnersButton-1.png", 3)
    click(reg.getLastMatch())

    levels._repeat_spin_and_daub(4)
    assert reg.exists("sign_out_next_button-1.png", 20)
    wait(1)
    click(reg.getLastMatch())
    wait(2)


def check_FTU_level_4(rush=False):
    """Check level 4 FTUE"""
    # TODO: add rush mode
    maps.select_level(4)
    assert reg.exists("FTUEExtraSpins-1.png", 3)
    click(reg.getLastMatch())
    wait(1.5)
    reg.click("PUPStorePlayButton-1.png")

    levels.check_spin_button(30)
    click(reg.getLastMatch())
    wait(3)
    assert reg.exists("FTUELVL4JokerPlusIcon-1.png", 10)
    click(reg.getLastMatch())
    wait(0.5)
    click(reg.getLastMatch())

    levels.check_spin_button(30)
    click(reg.getLastMatch())
    wait(3)
    levels._daub_matrix()

    levels._repeat_spin_and_daub(13)
    wait(3)
    assert reg.exists("MiniGameBet10Button-1.png", 6)
    wait(2)
    click(reg.getLastMatch())
    wait(5)

    levels.check_spin_button(10)
    click(reg.getLastMatch())
    wait(3)
    levels._daub_matrix()

    levels._repeat_spin_and_daub(6)

    levels.check_spin_button(30)
    click(reg.getLastMatch())
    wait(3)
    levels._daub_matrix()

    levels._spin_and_daub()
    assert reg.exists("sign_out_next_button-1.png", 20)
    wait(1)
    click(reg.getLastMatch())
    wait(2)
    dialogs.clear_dialogs()

def check_level_range(start_lvl, end_lvl, spend=False):
    """ Progress through levels in the specified range"""
    maps.play_level_range(start_lvl, end_lvl, p_spend=spend)

def check_reward_video_coins(cadence = 5):
    """Ad testing methods. Reward video tests all ads specified in the expected 
       cadence can be viewed. """
    
    clearDialogs()
    
    for index in range(cadence):
        print "Trying ad: " + str(index + 1)
        assert reg.exists(Pattern("coinsTopBar-2.png").similar(0.80).targetOffset(70,0),3)
        click(reg.getLastMatch())
    
        if reg.exists("RewardVideoCoinsButton-1.png"):
            print "Earn button available. Proceeding..."
            click(reg.getLastMatch())
        elif reg.exists("RewardVideoCheckBackBanner-1.png"):
            print "No ads available!"
            assert False, "Ad not available when expected"
            break
        
        assert exists("RewardVideoCoinsBanner-1.png",5)

        """
        global found_button
        found_button = False
        reg_playbutton_observe = Region(reg)
        reg_playbutton_observe.onAppear("RewardVideoPlayButton-1.png",reward_play_button)
        #reg_playbutton_observe.onAppear("RewardVideoPlaybutton1-1.png",reward_play_button)
        reg_playbutton_observe.observe(10)

        if found_button == False:
            print "No Play button found"
            assert False, "No play button detected on ad"
        """
        
        if reg.exists("RewardVideoPlayButton-1.png",10):
            click(reg.getLastMatch())
        elif reg.exists("RewardVideoPlaybutton1-1.png",2):
            click(reg.getLastMatch())
        else:
            print "Play button not found!"
            assert False, "No play button detected on ad"

        start_time = time.time()
    
        assert reg.exists("RewardVideoCoinsSuccess-1.png",120)
        print "Ad took: " + str(time.time() - start_time)
        
        assert exists("RewardVideoCloseButton-1.png")
        click(getLastMatch())
        clearDialogs()

def check_rva_finalspins(cadence = 3, numtests = 2):
    absent_ads = 0
    clearDialogs()
        
    for index in range(numtests):
        if reg.exists(Pattern("TopbarHeartsValue0-1.png").similar(0.98)):
                print "Out of hearts. Refilling..."
                admin_adjust_player(100009124185968, 
                                    hearts=5, 
                                    reset_rva_coins=False, 
                                    envURL=r"http://slingo-appob.bstage.ca/slingo/console/index.htm")
        selectLevel(41)
        handle_daily_deal()
        verifyLevelLoad()
        playLevel(wait_for_finalspins = True)
        print "Final spins reached"
        if reg.exists("RewardVideoFinalSpins-1.png",3):
            print "Final Spins Reward Video present"
            check_finalspins_ad()
        else:
            print "Final Spins Reward Video absent!"
            absent_ads += 1
            clearDialogs()
            wait(3)
            handleAdInterstitial()
            clearDialogs()

    if absent_ads > 0:
        assert False, "During some level ends ads were not present"
    else:
        assert True

def check_finalspins_ad():
    reg_finalspins_rva_observe = reg
    #reg_finalspins_rva_observe.onAppear(,observe_finalspins_ad)
    
    reg.click(Pattern("RewardVideoFinalSpins-1.png").targetOffset(229,3))

def reward_play_button(event):
    global found_button
    found_button = True
    assert True
    click(event.region.getLastMatch())

### Interstitial ads tests.
def check_inter_ad(cadence = 3,numtests = 2):
    reg_ad_observe = reg
    reg_ad_observe.onAppear("AdBanner-1.png",observe_inter_ad)

    clearDialogs()
    
    for num in range(numtests):
        for index in range(cadence):
            if reg.exists(Pattern("TopbarHeartsValue0-1.png").similar(0.98)):
                print "Out of hearts. Refilling..."
                admin_adjust_player(100009124185968,
                                    hearts=5,
                                    reset_rva_coins=False, 
                                    envURL=r"http://slingo-appob.bstage.ca/slingo/console/index.htm")
            selectLevel(1)
            handle_daily_deal()
            verifyLevelLoad()
            levels.exit_level()
            clearDialogs()
            reg_ad_observe.observe(10,False)
        
def observe_inter_ad(event):
        print "Interstitial Ad Found"
        start_time = time.time()
        reg.waitVanish("AdBanner-1.png",60)
        print "Ad time: " + str(time.time() - start_time)
        clearDialogs()


# The following functions are for setting up cord information for level nodes.
def displayNodePositions():
    reg.findAll("1432594286365.png")
    nodes = reg.getLastMatches()
    while nodes.hasNext():
        currentNode = nodes.next()
        print(str(currentNode.x) + "," + str(currentNode.y))


def _hover_node(first, last):
    for item in Cord.lvlList[first:last]:
        hover(reg.getTopLeft().offset(item.x, item.y))

def _print_mouse_pos():
    print(str(Env.getMouseLocation().x - reg.getTopLeft().x) + "," +
          str(Env.getMouseLocation().y - reg.getTopLeft().y))


def _record_mouse_pos(pos_number):
    reg.highlight(1)
    wait(1)
    reg.highlight(1)
    wait(1)
    for i in range(pos_number):
        reg.highlight(3)
        _print_mouse_pos()

def record_node_pos():
    maps.select_map(7)

    """
    maps.set_map_area(1)
    _record_mouse_pos(11)
    maps.set_map_area(2)
    _record_mouse_pos(14)
    maps.set_map_area(3)
    _record_mouse_pos(11)
    maps.set_map_area(4)
    _record_mouse_pos(14)
    maps.set_map_area(5)    
    _record_mouse_pos(12)
    """
    maps.set_map_area(6)
    _record_mouse_pos(13)
    """
    maps.set_map_area(7)
    _record_mouse_pos(11)
    maps.set_map_area(8)
    _record_mouse_pos(14)
    """


def main():
    pass

if __name__ == '__main__':
    main()