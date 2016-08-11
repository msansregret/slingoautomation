"""Dev tests for MAC machine."""
import unittest
import datetime
import sys
import traceback

import json
import urllib2

import sikuliTestBotV2 as bot
from test_data import *

settings = {
    'operating_system': 'MAC',
    'fb_username': 'automation_qfhrcjq_test@tfbnw.net',
    'fb_password': 'test123',
    'env_url': r'https://apps.facebook.com/qa-one-slingo/'
}


# information about test passes (iterations); different for each iteration.
# TODO: Get maximum testPassID, so we don't have to input it manually.
test_pass_data = {
    'testPassName': 'Test Suite Daily',
    'version': 'SA Canvas 16.07.25',
    'testPassID': '-1'
}

def getTestPassID():
    """Automatically set iteration number.

    Connects to nodeJS server, call endpoint to get current highest iteration,
    plus 1, and set the correct iteration number, so we don't have to input
    it manually.

    """
    catfish_url = 'http://192.168.8.167:4711/api/current-highest-iteration/'
    data = json.load(urllib2.urlopen(catfish_url))
    test_pass_data['testPassID'] = data['testPassID'] + 1

class TestSuiteDaily(unittest.TestCase):
    """Run automation tests using the tests defined in sikuliTestBotV2.

    Normally unittest should not depend on each other, so our sequencial test is
    bad practice. But for now, let's just hack function names and make it work.

    """

    def setUp(self):
        """Set up date and time value for reporting."""
        now = datetime.datetime.now()
        self.current_date = now.strftime("%Y-%m-%d")
        self.current_time = now.strftime("%H:%M")
        self.test_number = 0

    def tearDown(self):
        """Collect test result and information, and create a JSON file."""
        # if it's 0, we don't need to report it. i.e. close chrome test
        if self.test_number == 0:
            return

        this_test = TEST_DATA[str(self.test_number)]

        # if test result is E or F, this capture the traceback information
        exc_type, exc_value, exc_traceback = sys.exc_info()

        if exc_type is None:
            # Nothing happened, we pass the test!
            bot.create_test_json(test_pass_data['testPassName'],
                                 test_pass_data['testPassID'],
                                 str(self.test_number), this_test['name'],
                                 this_test['description'],
                                 self.current_date, self.current_time,
                                 test_pass_data['version'], 'pass', '') 

        elif exc_type is AssertionError:
            # Either our script has gone wrong, or the game has gone wrong!
            formatted_lines = traceback.format_exc().splitlines()
            print("*" * 50)
            print(exc_type)
            print(exc_value)
            error_message = ''
            for line in formatted_lines:
                error_message += line + '<br>'
            # now error_message contains the stacktrack message you would
            # normally see in a Python session
            bot.create_test_json(test_pass_data['testPassName'],
                                 test_pass_data['testPassID'],
                                 str(self.test_number), this_test['name'],
                                 this_test['description'],
                                 self.current_date, self.current_time,
                                 test_pass_data['version'], 'fail',
                                 error_message)
            print error_message
            
        else:
            # An error has occured. Mostly because of our script.
            formatted_lines = traceback.format_exc().splitlines()
            print("*" * 50)
            print(exc_type)
            print(exc_value)
            error_message = ''
            for line in formatted_lines:
                error_message += line + '<br>'
            bot.create_test_json(test_pass_data['testPassName'],
                                 test_pass_data['testPassID'],
                                 str(self.test_number), this_test['name'],
                                 this_test['description'],
                                 self.current_date, self.current_time,
                                 test_pass_data['version'], 'pending',
                                 error_message)
            print error_message

    def test_01_launch_chrome(self):
        """Launch chrome."""
        self.test_number = "ac1"
        bot.setup_chrome(settings['operating_system'], 
                         settings['fb_username'],
                         settings['fb_password'],
                         settings['env_url'])

    def test_02_check_load_slingo(self):
        """Log into facebook, and attempt to load slingo.

        Facebook changed its app login behaviour. Now we need to login first,
        then go to QA URL. 

        Unless server is down, or our dev environment setup has problem, 
        this test should never fail.

        """
        self.test_number = "ac2"
        bot.check_load_slingo()

    def test_03_reset_player_progress(self):
        """Attempt to reset player progress using in-game cheat."""
        self.test_number = "ac3"
        bot.reset_player_progress()

    def test_04_check_FTU_level_1(self):
        self.test_number = "ac4"
        bot.check_FTU_level_1(rush=False)

    def test_05_check_FTU_level_2(self):
        self.test_number = "ac5"
        bot.check_FTU_level_2(rush=False)

    def test_06_check_FTU_level_3(self):
        self.test_number = "ac6"
        bot.check_FTU_level_3()

    def test_07_check_FTU_level_4(self):
        self.test_number = "ac7"
        bot.check_FTU_level_4(rush=False)

    def test_08_buy_20_spinners(self):
        self.test_number = "ac8"
        bot.check_spinner_store(20)

    def test_09_buy_30_spinners(self):
        self.test_number = "ac9"
        bot.check_spinner_store(30)

    def test_10_buy_90_spinners(self):
        self.test_number = "ac10"
        bot.check_spinner_store(90)

    def test_11_buy_200_spinners(self):
        self.test_number = "ac11"
        bot.check_spinner_store(200)

    def test_12_buy_600_spinners(self):
        self.test_number = "ac12"
        bot.check_spinner_store(600)

    def test_13_buy_5000_coins(self):
        self.test_number = "ac13"
        bot.check_buy_coins(5000,5)

    def test_14_buy_12000_coins(self):
        self.test_number = "ac14"
        bot.check_buy_coins(12000,8)

    def test_15_buy_25000_coins(self):
        self.test_number = "ac15"
        bot.check_buy_coins(25000,14)

    def test_16_buy_40000_coins(self):
        self.test_number = "ac16"
        bot.check_buy_coins(40000,20)

    def test_17_refill_hearts_map(self):
        self.test_number = "ac17"
        bot.checkRefillHearts()

    def test_18_refill_hearts_level(self):
        self.test_number = "ac18"
        bot.checkRefillHeartsLevel()
        

def suite():
    """Assemble tests."""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestSuiteDaily))
    return test_suite


# before we run a new test suite, delete the existing reports first, in case
# we didn't use send_json.py last time
def delete_content():
    """Now that we've sent JSON, delete this file for future use."""
    with open('output.json', 'w'):
        pass


delete_content()
getTestPassID()
mySuite = suite()
runner = unittest.TextTestRunner()
runner.run(mySuite)
