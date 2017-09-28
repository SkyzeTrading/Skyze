'''
Created on 05/09/2017

@author: michaelnew
'''
# 3rd Party Libraries
import os
import sys
import unittest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import pandas as pd
from pandas   import ExcelWriter
from dateutil import parser
from datetime import datetime


# Skyze Libraries
import settings
from Market import Market




class UnitTestSkyzeAbstract(unittest.TestCase):
    '''
    classdocs

    1. Creates a list of assertion errors rather than stopping after each error.
       See https://stackoverflow.com/questions/4732827/continuing-in-pythons-unittest-when-an-assertion-fails

    '''
    def setUp(self):
        self.assertion_errors = []
        self.start_time = datetime.now()
        self.target_columns_market = [  "Date", "Open","High", "Low", "Close",
                                        "Volume", "MarketCap"]



    def tearDown(self):
        print("\n\n\n")
        try:
            self.assertEqual([], self.assertion_errors)
        except AssertionError as err:
            # Assertion Failure
            print("=== Test Failed === === === === === ")
            print("List of Assertion Errors:")
            for assertion_error in self.assertion_errors:
                print("\n\n=== Name: "+assertion_error[0])
                print(assertion_error[1])
        else:
            # Assertion Passed
            print("=== Test Passed === === === === === ")
            print("PASS: ALL TESTS .. You Rock :)")

        print("\n\nLeft = test results ..... Right = target results")
        return




    def getTestAndResultData(  self,
                                p_path,
                                p_test_file,
                                p_target_file,
                                p_target_columns):
        # Get the Market data
        mkt = Market.fromTesting(p_test_file)
        mkt_data = mkt.readMarketDataCSV(p_testing=True)
        print("Rows in mkt data: "+str(len(mkt_data)))

        # Read in the target results
        target_data = self.readTargetResults(   p_path + p_target_file,
                                                p_target_columns)
        print("\n\n")

        # Format boolean columns
        # None

        return mkt_data, target_data

    def series_assert(self, p_name, p_test_results, p_target_results):
        ''' Asserts two series on the same column name
            Stores errors (exceptions) in a list so that all tests are run '''

        try:
            assert_series_equal(   p_test_results[p_name],
                                    p_target_results[p_name],
                                    check_exact = False,
                                    check_less_precise = False
                               )

        except AssertionError as e:
            # Assertion Failure
            self.assertion_errors.append([p_name,str(e)])
            print("\n--- FAIL: "+p_name)

            # Get the rows that are different
            diffs = pd.DataFrame({'test':p_test_results[p_name], 'target':p_target_results[p_name]})
            diffs["Different"] = diffs["test"] != diffs["target"]
            print(diffs.loc[diffs.Different == True])
        else:
            # Assertion Passed
            print("\n+++ PASS: "+p_name)

        return





    def dataframe_assert(self, p_name, p_test_results, p_target_results):
        ''' Asserts two dataframes
            Stores errors (exceptions) in a list so that all tests are run '''

        try:
            assert_frame_equal(p_test_results, p_target_results)
        except AssertionError as err:
            # Assertion Failure
            self.assertion_errors.append([p_name,str(err)])
            print("DATAFRAME FAIL: "+p_name)
        else:
            # Assertion Passed
            print("DATAFRAME PASS: "+p_name)

        return





    def printTestHeader(self, p_test_file, p_target_file, p_test_columns):
        ''' Prints the test info '''
        print("\n\n======= This is a test of SUPERTREND INDICATOR ==============")
        print("Start time: "+str(self.start_time))
        print("Test data: " + p_test_file + "    \nTarget data: " + p_target_file)
        print("Columns: " + str(len(p_test_columns)) + " ... "+ str(p_test_columns))
        print("Parameters: ")

        return





    def printTestInfo(self, p_output, p_mkt_data, p_target_data, p_file_name):
        if p_output:
            print("\n\n\n=== Target_data . head  === === === === === ")
            print(p_target_data.head(5))
            print()
            print("=== Target_data . tail === === === === === ")
            print(p_target_data.tail(5))

            print();print();print(); print("=== Test Results . head === === === === === ")
            print(p_mkt_data.head(5))
            print(); print("=== Test Results . tail === === === === === ")
            print(p_mkt_data.tail(5))

            # Save market data to excel
            #self.saveTestResults(p_mkt_data, "Test-Output-"+p_file_name, p_testing = True)
        return




    def assertBySeries(self, p_output, p_mkt_data, p_target_data, p_target_columns):
        if p_output:
            print(); print()
            print("=== Series Assertion === === === === === ")

            # loop through the series
            for test_column in p_target_columns:
                self.series_assert(test_column, p_mkt_data, p_target_data)




    def readTargetResults(self, p_results_file, p_column_names):
        "Opens the file and reads the data"

        # Create the path name
        file_path = os.path.join(settings.results_file_path, "%s.csv" % p_results_file)

        # Add the standard market columns to the beginning of the column list
        column_names = self.target_columns_market + p_column_names
        print(column_names)
        try:
            # Read the target results into a dataframe
            target_results = pd.read_csv(
                                            file_path,
                                            header=None ,
                                            names = column_names,
                                            index_col=False,
                                            skiprows = 1
                                       )
        except IOError as err:
            print("File Error:   " + file_path)
            raise IOError ("FileNotFound","EXCEPTION UnitTestSkyzeAbstract::readTargetResults .... IOError File does not exist")
            return
        except:
            print("AN EXCEPTION - UnitTestSkyzeAbstract::readTargetResults(p_market)")
            print("File path:   " + file_path)
            print(sys.exc_info())
            return
        else:
            # Convert the date column to a date ! ...... Not needed now date is the index
            #target_results['Date'] = pd.to_datetime(target_results['Date'].astype(str), format='%Y%m%d')

            # Move the date column to the index
            target_results.index = [parser.parse(str(d)) for d in target_results["Date"]]
            del target_results["Date"]

            return target_results






    def saveTestResults (  self, p_results,
                            p_file_name,
                            p_file_path = "",
                            p_testing = False
                       ):
        ''' Export to excel file '''

        # set file path
        file_path = p_file_path
        if p_file_path == "":
            if p_testing:
                file_path = settings.testing_file_path
            else:
                file_path = settings.data_file_path

        # Write to Excel
        print("Test Output: "+file_path+"/"+p_file_name+".xlsx")
        writer = ExcelWriter(file_path+"/"+p_file_name+".xlsx")
        p_results.to_excel(writer, 'Results')
        writer.save()

        return
