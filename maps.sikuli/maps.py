from sikuli import *
import time
import dialogs
import levels
import setup
from cord import Cord\

global reg
reg = SCREEN

global matrix_size
matrix_size = '5x5'
global level_type
level_type = 'classic'
gate_found = False
map = None


pupDict = {
    "extraspins2": "ExtraSpins2.png",
    "extraspins4": "PUPIconExtraSpins.png",
    "firecrate": "PUPIconDailyFireCrate.png",
    "premiumvision": Pattern("PUPIconPremiumVision.png").similar(0.50),
    "autodaubber": Pattern("PUPIconAutoDaubber.png").similar(0.50)
}

map_dict = {
    1:{1:"area_identifier_1.png", 2:"area_identifier_2.png", 3:"area_identifier_3.png", 4:"area_identifier_4.png", 5:"area_identifier_5.png", 6:"area_identifier_6.png", 7:"area_identifier_7.png"},
    2:{1:"area_identifier_2_1.png", 2:"area_identifier_2_2.png", 3:"area_identiifer_2_3.png", 4:"area_identifier_2_4.png", 5:"area_identifier_2_5.png", 6:"area_identifier_2_6.png", 7:"area_identifier_2_7.png"},
    7:{1:Pattern("area_ident_7_1.png").similar(0.80), 2:"area_ident_7_2.png", 3:"area_ident_7_3.png", 4:Pattern("area_ident_7_4.png").similar(0.80), 5:"area_ident_7_5.png", 6:"area_ident_7_6.png", 7:"area_ident_7_7.png", 8:"area_ident_7_8.png"}
    }

def scroll_map_up():
    """Scolls the map up by one area"""
    dragDrop(reg.getTopRight().offset(-3, 115), reg.getBottomRight().offset(-3, -115))

def scroll_map_down():
    """Scrolls the map down by one area."""
    dragDrop(reg.getBottomRight().offset(-3, -115), reg.getTopRight().offset(-3, 115))

def reset_map_position():
    """Try to see the map, then scroll it down to reset its position.

    Sometimes interstitial ad appears; this function wait for it to complete.
    If the whole operation takes more than 60 seconds, halt.

    Logics seem to be not very clear and concise; can use some optimization.

    """
    timeout = time.time() + 60

    while True:
        if reg.exists("AreaOneVillage.png") or \
           reg.exists("AreaOneVillageSnow.png"):
            break        
        elif not reg.exists(Pattern("MuteButtons.png").similar(0.65)):
            assert False, "Slingo went missing during action"
            break
        elif time.time() > timeout:
            print('Action took longer than 60sec')
            assert False, "Not able to reset map position before timeout"
            break

        scroll_map_down()

    scroll_map_down()
    assert reg.exists("AreaOneVillage.png") or \
        reg.exists("AreaOneVillageSnow.png")

def _detect_map():
    """ Sets up the global map variable which tells other
       functions what map area we are currently in. Important
       to the code that switches maps.
       """
    global map
    for map_key, map_value in map_dict.items():
        for area_key, area_value in map_value.items():
            if reg.exists(area_value, 0):
                map = map_key
                return

    assert False, "Map area could not be detected"
        
def select_map(new_map):
    if map is None:
        _detect_map()

    while not new_map == map:
        timeout = time.time() + 60
        if new_map > map:
            while not reg.exists("map_change_up_button.png"):
                scroll_map_up()
                if time.time() > timeout:
                    assert False, 'Action took longer than 60sec'
                    break   
        elif new_map < map:
            while not reg.exists("map_change_down_button.png"):
                scroll_map_down()
                if time.time() > timeout:
                    assert False, 'Action took longer than 60sec'
                    break

        click(reg.getLastMatch())
        reg.waitVanish(Pattern("MuteButtons.png").similar(0.65),10)
        assert reg.exists(Pattern("MuteButtons.png").similar(0.65),30)
        dialogs.clear_dialogs()
        _detect_map()
        
            
def set_map_area(area):
    ### Seeks to find the area desired and then positions 
    ### the map so that area is in the middle.
    
    timeout = time.time() + 60
    map_position = None
    while not reg.exists(map_dict[map][area]): 
        #While our area is not on screen.
        
        if map_position is None:
            #If we haven't found out where on the map we are yet.
            #We're going to iterate through all the items until we find one.
            for key,value in map_dict[map].items(): 
                if reg.exists(value, 0):
                    map_position = key
                    break

        #If we know where we are now go up or down or if not just down.
        if map_position < area:
            scroll_map_up()
        elif map_position > area:
            scroll_map_down()
        else:
            print "Unkown map position"
            scroll_map_down()

        if time.time() > timeout:
            print 'Action took longer than 60sec'
            assert False
            break

    ### Now that the desired area is on screen we move the map up and down until
    ### we have the area identifier lined up to within 5pix of the middle of the reg
    delta_of_area_from_center = _setup_area_delta(map_dict[map][area])
        
    timeout = time.time() + 60
    while abs(delta_of_area_from_center) > 5:
        dragDrop(reg.getTopRight().offset(-15, reg.h / 2), reg.getTopRight().offset(-15, (reg.h / 2) + delta_of_area_from_center))
        wait(0.5)
        delta_of_area_from_center = _setup_area_delta(map_dict[map][area])
        
        if time.time() > timeout:
            print 'Action took longer than 60sec'
            assert False
            break

def _setup_area_delta(area):
    dead_zone_comp = 0
    
    delta = reg.getCenter().y - reg.find(area).getCenter().y
    if delta > 0:
        delta += dead_zone_comp
    elif delta < 0:
        delta -= dead_zone_comp

    return delta

def select_level(lvl):
    """Clicks on a specified level node and the sets level parameters."""

    if lvl <= 100:
        select_map(1)
        if lvl <= 10:
            set_map_area(1)
        elif lvl <= 25:
            set_map_area(2)
        elif lvl <= 40:
            set_map_area(3)
        elif lvl <= 55:
            set_map_area(4)
        elif lvl <= 70:
            set_map_area(5)
        elif lvl <= 85:
            set_map_area(6)
        elif lvl <= 100:
            set_map_area(7)
            
    elif lvl <= 200:
        select_map(2)
        if lvl <= 115:
            set_map_area(1)
        elif lvl <= 130:
            set_map_area(2)
        elif lvl <= 145:
            set_map_area(3)
        elif lvl <= 160:
            set_map_area(4)
        elif lvl <= 175:
            set_map_area(5)
        elif lvl <= 190:
            set_map_area(6)
        elif lvl <= 200:
            set_map_area(7)

    elif lvl <= 300:
        select_map(3)

    elif lvl <= 400:
        select_map(4)
        
    elif lvl <= 500:
        select_map(5)

    elif lvl <= 600:
        select_map(6)
    
    elif lvl <= 700:
        select_map(7)
        if lvl <= 611:
            set_map_area(1)
        elif lvl <= 625:
            set_map_area(2)
        elif lvl <= 636:
            set_map_area(3)
        elif lvl <= 650:
            set_map_area(4)
        elif lvl <= 662:
            set_map_area(5)
        elif lvl <= 675:
            set_map_area(6)
        elif lvl <= 686:
            set_map_area(7)
        elif lvl <= 700:
            set_map_area(8)

            
    listAdjLvl = lvl - 1

    hover(reg.getTopLeft().offset(
        Cord.lvlList[listAdjLvl].x, Cord.lvlList[listAdjLvl].y))
    reg.mouseDown(Button.LEFT)
    reg.mouseUp(Button.LEFT)
    dialogs.park_cursor()
    assert reg.exists("PUPStorePlayButton.png", 3)

def _handle_ringo_gate_tut():
    """If the Ringo gate requirement FTUE is ocrruring,
    this handle it."""
    if reg.exists("RingoGateUnlockTut.png"):
        assert reg.exists("TutGotIt.png")
        click(reg.getLastMatch())

def handle_daily_deal():
    daily_deal_observe = reg
    daily_deal_observe.onAppear("DailyDealBanner.png",daily_deal_dismiss)
    daily_deal_observe.observe(10,True)

def daily_deal_dismiss(event):
    print "Daily Deal found. Dismissing..."
    dialogs.close_dialog()

def _set_level_type():
    """Observes the presence of the Cascade mode icon on the signup dialogue,
    and sets the level type variable."""
    global level_type

    if reg.exists(Pattern("SignUpDialogCascadeIcon.png").similar(0.95)):
        level_type = 'cascade'
    else:
        level_type = 'classic'


def _set_matrix_size():
    """Detects level signup icons and then sets
       global variable matrix_size. That variable is
       depended upon by _daub_matrix"""
    global matrix_size
    if reg.exists(Pattern("SignUpDialog5x5.png").similar(0.95)):
        matrix_size = '5x5'
        print('Level is 5x5')
    elif reg.exists(Pattern("SignUpDialog7x7.png").similar(0.95)):
        matrix_size = '7x7'
        print('Level is 7x7')

def _set_signup(pup='None'):
    """Equip one specific power up; if insucfficient currenty, buy them here.

    Call this during a script that goes through the signup dialogue.

    """
    _handle_PUP_unlocks_signup()
    if pup != 'None':
        reg.click(pupDict[pup])
        if reg.exists("PUPStoreBuyButton.png", 2):
            reg.click(reg.getLastMatch())
            wait(1)
            if reg.exists("AddCoins.png"):
                assert reg.exists("CoinsStore8Spinner.png")
                click(reg.getLastMatch())
                
            dialogs.handle_spinner_prompt(1)

        assert reg.exists("PUPequippedCheck.png")
        wait(1)

def _handle_PUP_unlocks_signup():
    """If a power up unlocked moment is happening on the sign up screen,
    this handles it, by checking which one it is, and then equipping it.
    """
    if reg.exists("PowerUpUnlockedBannerSignUp.png", 2):
        print("PUP Unlock moment found")
        unlockBanner = reg.getLastMatch()
        pupSelect = reg.find("SignUpSelectPUPsBanner.png")
        for item in pupDict:
            print("Checking for PUP...")
            if unlockBanner.below(300).exists(pupDict[item]):
                print("Found PUP")
                pupSelect.below().click(pupDict[item])
                break

    wait(2)

def handle_gate_unlock():
    """Uses the signpost on gates to check if the gate can be interacted
    if it can it proceeds to try and unlock the gate.
    """
    global gate_found
    if reg.exists(Pattern("gate_signpost.png").targetOffset(95,57)) or reg.exists("gate_01.png"):
        print("Gate post found. Checking for gate unlock")
        sign_list = [Pattern("gate_signpost.png").targetOffset(91,57), Pattern("gate_signpost_left.png").targetOffset(-130,69), "gate_01.png"]
        reg_skip_observe = Region(reg)
        reg_skip_observe.onAppear("NISSkipButton.png", event_skip)
        reg_skip_observe.observe(30, True)
        
        gate_found = False
        for item in sign_list:
            if reg.exists(item):
                click(reg.getLastMatch())
                
                if waitVanish(item, 3):
                    print("Gate found unlocking...")
                    if reg.exists("gate_dialog_unlocknow_button.png"):
                        gate_found = True
                        click(reg.getLastMatch())
                        break
                    elif reg.exists("GateDialogBanner.png"):
                        gate_found = True
                        if reg.exists("gate_dialog_buy_button.png"):
                            click(reg.getLastMatch())
                            wait(1)
                            dialogs.handle_spinner_prompt(3)
                        if reg.exists("GateUnlockTutFreeButton.png", 8):
                            click(reg.getLastMatch())
                        break
                    else:
                        dialogs.clear_dialogs()
        
        if gate_found:            
            if not reg.exists("AreaUnlockDialogBanner.png", 30):
                print("Gate unlock confirmation missing")
                dialogs.clear_dialogs()
        else:
            print("Gate dialog not found")
            dialogs.clear_dialogs()

        reg_skip_observe.stopObserver()

def event_skip(event):
    global gate_found
    gate_found = True
    reg.click(event.pattern)


def play_level_range(start, last, p_spend=False):
    """Loads and plays levels in a range specifed by
    a starting and ending level."""
    reg_pup_unlock_observe = Region(reg)
    reg_pup_unlock_observe.onAppear("PowerUpUnlockedBannerSignUp.png", event_handle_pup_unlocks)
    
    adjLast = last + 1
    for i in range(start, adjLast):
        win = False
        while not win:
            dialogs.clear_dialogs()
            if reg.exists(Pattern("topbar_hearts_value_0.png").similar(0.90), 2):
                print('Out of Hearts. Getting More...')
                setup.refill_hearts()
                
            print('Playing level ' + str(i))
            select_level(i)
            reg_pup_unlock_observe.observe(FOREVER, True)

            _set_level_type()
            _set_matrix_size()
            
            # This is where we take actions based on level type as a standard 
            # method of increasing our chances of beating the level.
            if level_type == 'classic' and p_spend is True:
                _set_signup('extraspins4')
            else:
                _set_signup('None')

            reg_pup_unlock_observe.stopObserver()
            levels.verify_level_load()
            levels.handle_pup_unlock()
            levels.new_play_level(m_size=matrix_size, l_spend=p_spend)
            dialogs.handle_ad_interstitial()

            if reg.exists("SignOutDialogWin.png", 3):
                print('Beat level ' + str(i))
                win = True
                dialogs.clear_dialogs()
                dialogs.handle_ad_interstitial()
                _handle_ringo_gate_tut()
                handle_gate_unlock()

            elif reg.exists("SignOutDialogLose.png", 3):
                print('Lost level ' + str(i) + '. Retrying...')
                win = False

        dialogs.clear_dialogs()

def event_handle_pup_unlocks(event):
    _handle_PUP_unlocks_signup()
    event.region.stopObserver()