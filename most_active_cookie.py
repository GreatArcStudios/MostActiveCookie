import argparse
import csv
import sys


class CookieProcessor:
    def __init__(self):
        # keys are the date, values are dict of the cookie and occurrences
        self.cookies_dict = {}
        # used to actually process the counts
        # essentially an inverse of cookies_dict
        # keys are the date, and values are dict of occurrences and sets of cookies
        self.count_dict = {}

    def find_active_cookies(self, date):
        """
        Looks through the count dictionary for a specified date, and return
        the corresponding cookies that have the max count.
        This implementations allows us to avoid having to process all the data again;
        we only need to essentially "query" the max
        :param date:
        :return: set of most active cookies, used in the tester
        """
        most_active_cookies = set()
        if date in self.count_dict:
            max_occurrence = max(self.count_dict[date].keys())
            most_active_cookies = self.count_dict[date][max_occurrence]
            for cookie in most_active_cookies:
                print(cookie)
        return most_active_cookies

    def process_cookies(self, log_path):
        """
        Process the cookies log CSV file.
        Process the counts here rather than in find_active_cookies() because
        we may choose to change how a "count" is defined, and find_active_cookies()
        is only responsible for finding the max of the counts.
        :param log_path: the path to the log file
        :return: void
        """
        with open(log_path, newline='') as cookie_log:
            log_reader = csv.DictReader(cookie_log)
            for log_row in log_reader:
                self.process_row(log_row)

    def process_row(self, row):
        """
        Processes a row of the CSV, making sure to update both the count
        dictionary for O(n) processing and the cookies_dictionary
        :param row: dict
        :return: void
        """
        cookie, date = row['cookie'], row['timestamp']
        date = self.process_date(date)
        # update the cookies dictionary
        if date not in self.cookies_dict:
            self.cookies_dict[date] = {cookie: 1}
        else:
            if cookie not in self.cookies_dict[date]:
                self.cookies_dict[date][cookie] = 1
            else:
                self.cookies_dict[date][cookie] += 1
        count = self.cookies_dict[date][cookie]
        # update the count dictionary
        if date not in self.count_dict:
            self.count_dict[date] = {count: set([cookie])}
        else:
            if count not in self.count_dict[date]:
                self.count_dict[date][count] = set([cookie])
            else:
                self.count_dict[date][count].add(cookie)
                if count > 1:
                    self.count_dict[date][count - 1].remove(cookie)

    def process_date(self, date):
        """
        Abstract date processing, may be extended to use datetime objects
        Currently just uses string processing to get the year, month, day
        :param date: the UTC date string we process
        :return: str of the processed date
        """
        date_parts = date.split("T")
        # return the year-month-day part of the date
        return date_parts[0]


if __name__ == '__main__':
    # use the argparse library to process the CLI
    arg_parser = argparse.ArgumentParser(
        prog='most_active_cookie.py',
        description='Program to calculate the most active cookies on a date, '
                    'given CSV with cookie and timestamp',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    arg_parser.add_argument("file_path")
    arg_parser.add_argument("--date", "-d")
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    # create a CookieProcessor and process the data
    cookie_processsor = CookieProcessor()
    cookie_processsor.process_cookies(args["file_path"])
    cookie_processsor.find_active_cookies(args["date"])
