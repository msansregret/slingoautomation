import os
import time
import sys
import re
from emailer import sendMailAttach
from sikuliTestBotV2 import *
import unittest
import HTMLTestRunner
reload(HTMLTestRunner)

fbUser1 = "automation_qfhrcjq_test@tfbnw.net"
fbPassword1 = "test123"

fbUser2 = "automation_xnzemdf_two@tfbnw.net"
fbPassword2 = "test123"

fbUser3 = "automation_wicxbhy_three@tfbnw.net"
fbPassword3 = "test123"

fbUser4 = "automation_wwjankw_four@tfbnw.net"
fbPassword4 = "test123"

fbUser5 = "automation_smzecuc_five@tfbnw.net"
fbPassword5 = "test123"        
##################      Test Suites      ###################
class SetupTesting(unittest.TestCase):
    def test1_LoadChrome(self):
        setupChrome()
        
    def test2_FacebookLogin(self):
        loginFacebook(fbUser3,fbPassword3)
        
    def test3_LoadSlingo(self):
        checkLoadSlingo()

class FirstTimeUserTests(unittest.TestCase):
    def test0_ResetPlayerProgress(self):
        resetPlayerProgress()

    def test1_TutorialLevel1(self):
        checkFTULevel1()

    def test2_TutorialLevel2(self):
        checkFTULevel2()

    def test3_TutorialLevel3(self):
        checkFTULevel3()

    def test4_TutorialLevel4(self):
        checkFTULevel4()


class SpinnerPurchaseTests(unittest.TestCase):
    def test1_Buy15Spinners(self):
        checkBuySpinners15()

    def test2_Buy30Spinners(self):
        checkBuySpinners30()

    def test3_Buy65Spinners(self):
        checkBuySpinners65()

    def test4_Buy150Spinners(self):
        checkBuySpinners150()

    def test5_Buy400Spinners(self):
        checkBuySpinners400()

class CoinPurchaseTests(unittest.TestCase):
    def test1_Buy5000Coins(self):
        checkBuyCoins5000()

    def test2_Buy12000Coins(self):
        checkBuyCoins12000()

    def test3_Buy25000Coins(self):
        checkBuyCoins25000()

    def test4_Buy40000Coins(self):
        checkBuyCoins40000()
        
class HeartPurchaseTests(unittest.TestCase):    
    def test1_RefillHeartsMap(self):
        checkRefillHearts()
        
    def test2_RefillHeartsLevel(self):
        checkRefillHeartsLevel()

class PowerUpPurchaseTests(unittest.TestCase):
    def test1_PUPStorePurchase(self):
        checkPUPStore()
        
class LevelProgression(unittest.TestCase):
    def test1_PlayLevels5to6(self):
        setSlingoReg()
        playLevelRange(5,11, spend = True)

def main():
    dir = "/Volumes/UserShares/msansregret/HTMLTestRunner_iMac-01"
    #recipients = ['msansregret@gamehouse.com', 'munruh@gamehouse.com', 'dustinv@blastworksinc.com']
    recipients = ['msansregret@gamehouse.com']
    filename = 'test.html'
    filepath = os.path.join(dir, filename)

    #HTMLTestReport sets up the HTML format report file.
    #suite = unittest.TestLoader().loadTestsFromTestCase(LevelProgression) 
    suite = unittest.TestLoader().loadTestsFromTestCase(SetupTesting) #First test to be ran
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(FirstTimeUserTests))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SpinnerPurchaseTests))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CoinPurchaseTests))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(HeartPurchaseTests)) #Additional tests can be added with this pattern
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PowerUpPurchaseTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LevelProgression)) 

    fp = open(os.path.join(dir, "test.html"), "w")
    runner = HTMLTestRunner.HTMLTestRunner(stream = fp, verbosity=2, dirTestScreenshots = dir)
    runner.run(suite) 
    fp.close()

    fp = open(filepath,'r')
    body = buildEmailBody(''.join(fp))
    fp.close()
    #email report details
    #f = open(r"C:/Sikuli/HTMLTestRunner/test.html", 'r') #Windows Path
    #f = open(os.path.join(dir, "test.html"), 'r') #Mac path
    #sendMail('noreply@gamehouse.com', recipients, 'Testbot Report', f)

    sendMailAttach('noreply@gamehouse.com', recipients, 'Testbot Daily Report: Canvas', body, filename, filepath)
    #f.close()

def buildEmailBody(report):
	result = re.findall(r'</strong>(.*)</p>',report)
	
	body = 'TEST RESULT SUMMARY' + '\r' + '\r' + 'Start Time:' + result[0] + '\r' + 'Duration:' + result[1] + '\r' + 'Status:' + result[2] + '\r' + '\r' + 'See attachment for full test report'
	return body

if __name__ == '__main__':
    main()