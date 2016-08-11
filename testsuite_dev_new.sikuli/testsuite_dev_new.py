### This script is meant to run daily and cover the elements of a smoke test ###

import os
import time
import sys
import re
from emailer import sendMailAttach
import testbot as bot
import unittest
import HTMLTestRunner
reload(HTMLTestRunner)

# Variables used for the test environment. Such as file paths for test reports and user names and passwords for log ins. They can be called in methods locally within this script.
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

URLQA = r"https://apps.facebook.com/qa-one-slingo/"
URLDEV = r"https://apps.facebook.com/dev-one-slingo/"
URLPROD = r"https://apps.facebook.com/slingoadventure/"

##################      Test Suites      ###################
class SetupTesting(unittest.TestCase):
    def test1_LoadChrome(self):
        bot.setup_testing(os="MAC",fb_username=fbUser1, fb_password=fbPassword1, envURL=URLQA)
        
    def test2_LoadSlingo(self):
        bot.check_load_slingo()

class FirstTimeUserTests(unittest.TestCase):
    def test0_ResetPlayerProgress(self):
        bot.check_reset_progress()

    def test1_TutorialLevel1(self):
        bot.check_FTU_level_1()

    def test2_TutorialLevel2(self):
        bot.check_FTU_level_2()

    def test3_TutorialLevel3(self):
        bot.check_FTU_level_3()

    def test4_TutorialLevel4(self):
        bot.check_FTU_level_4()


class SpinnerPurchaseTests(unittest.TestCase):
    def test1_Buy20Spinners(self):
        bot.check_spinner_store(20)
        
    def test2_Buy30Spinners(self):
        bot.check_spinner_store(30)

    def test3_Buy90Spinners(self):
        bot.check_spinner_store(90)

    def test4_Buy200Spinners(self):
        bot.check_spinner_store(200)

    def test5_Buy600Spinners(self):
        bot.check_spinner_store(600)

class CoinPurchaseTests(unittest.TestCase):
    def test1_Buy5000Coins(self):
        bot.check_coins_store(5000,5)

    def test2_Buy12000Coins(self):
        bot.check_coins_store(12000,8)

    def test3_Buy25000Coins(self):
        bot.check_coins_store(25000,14)

    def test4_Buy40000Coins(self):
        bot.check_coins_store(40000,20)
        
class HeartPurchaseTests(unittest.TestCase):    
    def test1_RefillHeartsMap(self):
        bot.check_refill_hearts()
        
    def test2_RefillHeartsLevel(self):
        bot.check_refill_hearts_level()

class PowerUpPurchaseTests(unittest.TestCase):
    def test1_PUPStorePurchase(self):
        bot.checkPUPStore()
        
class LevelProgression(unittest.TestCase):
    def test1_PlayLevels601to700(self):
        bot.check_level_range(5, 26, spend=True)

class TestNewPlayLevel(unittest.TestCase):
    def test1_NewPlayLevel(self):
        bot.select_level(5)
        verify_level_load()
        handle_pup_unlock()
        new_play_level()

class RecordNodes(unittest.TestCase):
    def test1_recordmousepos(self):
        bot.record_node_pos()
        
def main():
    dir = "/Volumes/UserShares/msansregret/HTMLTestRunner_Daily"
    #recipients = ['msansregret@gamehouse.com', 'munruh@gamehouse.com', 'dustinv@blastworksinc.com']
    recipients = ['msansregret@gamehouse.com']
    filename = 'test.html'
    filepath = os.path.join(dir, filename)

    #HTMLTestReport sets up the HTML format report file.
    #suite = unittest.TestLoader().loadTestsFromTestCase(LevelProgression) 
    suite = unittest.TestLoader().loadTestsFromTestCase(SetupTesting) #First test to be ran
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(FirstTimeUserTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SpinnerPurchaseTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CoinPurchaseTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(HeartPurchaseTests)) #Additional tests can be added with this pattern
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestNewPlayLevel))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PowerUpPurchaseTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LevelProgression))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(RecordNodes))

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

    sendMailAttach('noreply@gamehouse.com', recipients, 'Testbot Dev Report: Canvas', body, filename, filepath)
    #f.close()

def buildEmailBody(report):
	result = re.findall(r'</strong>(.*)</p>',report)
	
	body = 'TEST RESULT SUMMARY' + '\r' + '\r' + 'Start Time:' + result[0] + '\r' + 'Duration:' + result[1] + '\r' + 'Status:' + result[2] + '\r' + '\r' + 'See attachment for full test report'
	return body

if __name__ == '__main__':
    main()