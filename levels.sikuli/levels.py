from sikuli import *
import time
import dialogs
from cord import Cord

global reg
reg = SCREEN

global matrix_size
matrix_size = '5x5'
global level_type
level_type = 'classic'

spend = False

global play_level
play_level = False
global finalspins_wait
finalspins_wait = False
global daubing
daubing = True

pupDict = {
    "jokerplus": "PUPIconJokerPlus.png",
    "superjoker": "PUPIconSuperJoker.png",
    "pointmultiplier": "PUPIconPointMultiplier.png",
    "reelblitz": "PUPIconReelBlitz.png",
    "blockerbreaker": "PUPIconBlockerBreaker.png"

}

def check_spin_button(time_):
    """Checks if the spin button is enabled.
    Args:
        time_: wait time, in seconds, in case there is
                an animation waiting to complete.

    """
    timeout = time.time() + time_
    while True:
        # if either spinner button is preset, assert True
        if reg.exists("SpinButton.png", 0) or reg.exists(
                "SpinButtonHighlighted.png", 0):
            assert True
            break
        # if time is up, assert False.
        elif time.time() >= timeout:
            assert False, "Spin button not present in time."
            break
        # don't loop too fast
        else:
            wait(0.5)

def verify_level_load():
    """Launches the level from the sign up dialogue, wait for it to load
    correctly, and record the time."""
    start_time = time.time()
    assert reg.exists("PUPStorePlayButton.png", 5)
    wait(1)

    click(reg.getLastMatch())
    dialogs.park_cursor()
    waitVanish(Pattern("MuteButtons.png").similar(0.65),10)
    print('Level is loading...')
    assert reg.exists(Pattern("MuteButtons.png").similar(0.65),30), "Level load was not detected before timeout"
    timeout = time.time() + 30
    while True:
        if reg.exists("PUPUnlockedFUE.png", 0) or \
               reg.exists("LetsGetSpinningBanner.png", 0):
            assert True
            break

        if time.time() > timeout:
            assert False, "Level load was not detected before timeout"
            break
  
    elapsed_time = time.time() - start_time
    print("Level took: {} seconds to load.".format(str(elapsed_time)))
    wait(1)

def verify_level_exit(skip_nis=True):
    """Watches for the level to deconstruct and then waits for the map
       to construct. """
    if skip_nis:
        reg_skip_observe = reg
        reg_skip_observe.onAppear("NISSkipButton.png", event_skip_nis)
        reg_skip_observe.observe(45,True)

    start_time = time.time()
    assert reg.exists(Pattern("MuteButtons.png").similar(0.65))
    reg.waitVanish(Pattern("MuteButtons.png").similar(0.65),30)
    start_time = time.time()
    print('Map is loading...')
    assert reg.exists(Pattern("MuteButtons.png").similar(0.65),30), "Map load was not detected before timeout"
    elapsed_time = time.time() - start_time
    print("Map took: {} seconds to load.".format(str(elapsed_time)))
    wait(1)

def event_skip_nis(event):
    """ handles the observe NIS button skip event for verify_level_exit"""
    reg.click(event.pattern)

def exit_level():
    """Quits a level"""
    assert reg.exists("LevelHomeButton-1.png")
    click(reg.getLastMatch())
    wait(1)
    assert reg.exists("1422915703730.png")
    click(reg.getLastMatch())
    wait(2)
    assert reg.exists(Pattern("MuteButtons-2.png").similar(0.65),40)


def _daub_matrix():
    """Clicks each matrix tile on the game board in a pattern.

    The pattern is gotten from the Cord library of coordinates.
    It uses the matrix_size variable to choose between 5*5 or 7*7

    """
    global daubing
    daubing = True
    
    #Should be a region covering only the lower right corner
    reg_observe_spin_ready = Region(reg.x + (reg.w / 2), reg.y + (reg.h /2), reg.w / 2, reg.h / 2) 
    reg_observe_spin_ready.onAppear("SpinButton-1.png", event_daub_done)
    reg_observe_spin_ready.observe(FOREVER, True)
    
    storeDelay = Settings.MoveMouseDelay
    #Settings.MoveMouseDelay = 0.01
    Settings.MoveMouseDelay = 0.0
    if matrix_size == '5x5' and reg_observe_spin_ready.exists("spin_button_disabled.png",0):
        for tile in Cord.tiles5x5:
            if daubing:
                click(reg.getTopLeft().offset(tile.x, tile.y))
            else:
                break
    elif matrix_size == '7x7' and reg_observe_spin_ready.exists("spin_button_disabled.png",0):
        for tile in Cord.tiles7x7:
            if daubing:
                click(reg.getTopLeft().offset(tile.x, tile.y))
            else:
                break

    Settings.MoveMouseDelay = storeDelay
    reg_observe_spin_ready.stopObserver()

def event_daub_done(event):
    global daubing
    daubing = False

def _spin_and_daub():
    """If the spin button is there, it uses _daub_matrix to daub each tile."""
    check_spin_button(3)
    click(reg.getLastMatch())
    dialogs.park_cursor()
    wait(2)
    _daub_matrix()

def _repeat_spin_and_daub(repeat):
    """Repeatedly call _spin_and_daub().
    Args:
        repeat: number of times we repeat calling _spin_and_daub().
                Must be integer
    """
    for i in range(repeat):
        _spin_and_daub()

def new_play_level(m_size='5x5', finalspins=False, l_spend=False):
    global matrix_size
    matrix_size = m_size
    global play_level
    play_level = True
    global spend 
    spend = l_spend
    global finalspins_wait
    if finalspins == True:
        finalspins_wait = True
    
    playtime = 500
    
        
    reg_finalspins_observe = Region(reg)
    reg_finalspins_observe.onAppear("finalspins_dialog_banner.png", event_finalspins)
    reg_finalspins_observe.observe(playtime, True)
    

    reg_spin_observe = Region(reg.x + (reg.w / 2), reg.y + (reg.h /2), reg.w / 2, reg.h / 2)
    reg_spin_observe.onAppear("SpinButton-1.png", event_spin)
    reg_spin_observe.observe(playtime, True)


    reg_minigame_observe = Region(reg)    
    reg_minigame_observe.onAppear("MiniGameBet10Button.png", event_minigame)
    reg_minigame_observe.observe(playtime, True)
    

    reg_help_observe = Region(reg)
    reg_help_observe.onAppear("free_1.png", event_cherub_help)
    reg_help_observe.onAppear("free_2.png", event_cherub_help)
    reg_help_observe.observe(playtime, True)
    

    reg_levelend_observe = Region(reg)
    reg_levelend_observe.onAppear("level_end_banner_win.png", event_level_win)
    reg_levelend_observe.onAppear("level_end_banner_lose.png", event_level_lose)
    reg_levelend_observe.observe(playtime, True)
    

    spin_timeout = 0
    timeout = time.time() + playtime
    while play_level:
        wait(1)
        if reg_spin_observe.exists("spin_button_disabled.png",0):
            spin_timeout += 1

        if spin_timeout >= 10:
            _daub_matrix()
            spin_timeout = 0
            
        if not reg.exists(Pattern("MuteButtons-1.png").similar(0.65).targetOffset(15,-25)):
            assert False, "Slingo went missing during level play"
            break
        elif time.time() > timeout:
            assert False, "Playing level took longer than timeout"
            break

    reg_finalspins_observe.stopObserver()
    reg_spin_observe.stopObserver()
    reg_help_observe.stopObserver()
    reg_minigame_observe.stopObserver()
    reg_levelend_observe.stopObserver()
    
    verify_level_exit()
    

def event_finalspins(event):
    global play_level
    global daubing
    daubing = False
    print("Final spins found")
    if finalspins_wait:
        print("Waiting on Final Spins")
        event.region.stopObserver()
        play_level = False
    elif spend and reg.exists("1468600681405.png"):
        reg_offer_observe = Region(reg)
        reg_offer_observe.onAppear("purchase_double_up_offer.png", event_offer)
        reg_offer_observe.observe(FOREVER,True)
        print("Buying Spinners")
        assert reg.exists("finalspins_spinner_5.png")
        click(reg.getLastMatch())
        wait(3)
        dialogs.handle_spinner_prompt(2)
        reg_offer_observe.stopObserver()
        event.repeat(3)
    else:
        print("Closing out Final Spins")
        play_level = False
        wait(2)
        dialogs.clear_dialogs()
        event.region.stopObserver()

def event_offer(event):
    reg.click(Pattern("purchase_double_up_offer.png").targetOffset(288,-1))

def event_level_win(event):
    print "Level Win Detected"
    global play_level
    play_level = False

def event_level_lose(event):
    print "Level Lose Detected"
    global play_level
    play_level = False

def event_spin(event):
    _spin_and_daub()
    event.repeat()

def event_minigame(event):
    handle_mini_game()    
    event.repeat(3)

def event_cherub_help(event):
    click(event.pattern)
    event.repeat(3)


def handle_mini_game():
    """Handles shell mini game and rock, paper, scissors game.

    Since we're having problems right now, take screenshots before trying to 
    click on anything. 

    """
    print("Minigame discovered")
    assert reg.exists("MiniGameBet10Button.png")
    wait(2)
    reg.click("MiniGameBet10Button.png")
    if reg.exists("jokers_shell_game.png", 1):
        print("Play shell game")
        reg.wait("minigame_joker_cup_pickbanner.png", 10)
        wait(1)
        reg.click("minigame_joker_cup.png")

    if reg.exists("rock_paper_scissors.png", 5):
        print("Play RPS game")
        reg.click("rock.png", 20)
        # Good ol' rock, nothing beats rock.
        
    reg.waitVanish("MiniGameBet10Button.png", 20)
    wait(1.5)
    #_daub_matrix()
    print("Mini-game handling over.")

def handle_pup_unlock():
    if reg.exists("PUPUnlockedFUE-1.png"):
        assert reg.exists(Pattern("PUPStoreIcon.png").similar(0.90))     
        click(reg.getLastMatch())