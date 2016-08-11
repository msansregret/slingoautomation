from sikuli import *

global reg
reg = SCREEN

def close_dialog():
    """Closes the current dialog"""
    closebuttons = reg.findAll("DialogCloseButton.png")
    sortedbuttons = sorted(closebuttons, key=lambda b: b.y)

    reg.click(sortedbuttons[-1])

def clear_dialogs():
    """As long as there are dialogues with a close button is closes 
       them until no more are found"""
    while reg.exists("DialogCloseButton.png", 1):
        close_dialog()
        wait(1)

def handle_ad_interstitial():
    """If an interstitial ad is on screen it waits up to 60 
       seconds for it to close"""
    if reg.exists("AdBanner.png",3):
        print "Ad Found waiting to complete"
        reg.waitVanish("AdBanner.png",60)

def handle_spinner_prompt(time=1):
    """Helps handle the the confimation of being out of spinners"""
    if reg.exists("SpinnerStoreBanner.png", time):
        assert (reg.exists(Pattern("Spinner299BuyButton.png")
                           .similar(0.98).targetOffset(32, 2), 1))
        click(reg.getLastMatch())
        click_thru_fb_buy()
        wait(2)

def click_thru_fb_buy():
    """When fb wants you to confirm if you really want to buy golden spinner,
    click cancel."""
    temp_reg = reg.nearby(150)
    assert temp_reg.exists("buy_golden_spinner_or_cancel.png",5), "FaceBook buy confirmation missing"
    wait(3)
    temp_reg.click("buy_golden_spinner_or_cancel.png")
    temp_reg.waitVanish("buy_golden_spinner_or_cancel.png", 5)

def park_cursor():
    hover(reg.getBottomRight())
