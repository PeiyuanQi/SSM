import argparse
import unittest
from util import *


class TestSmallFile(unittest.TestCase):

    def test_small_file_compact(self):
        file_paths = []
        # create directory with random name under TEST_DIR
        source_dir = TEST_DIR + random_string() + "/"
        # create files in the above directory
        for i in range(MAX_NUMBER):
            file_paths.append(create_random_file_parallel(FILE_SIZE,
                                                          source_dir)[0])
        time.sleep(2)
        # compact rule
        rule_str = "file : path matches " + \
            "\"" + source_dir + "*\" | compact"
        rid = submit_rule(rule_str)
        # Activate rule
        start_rule(rid)
        # Submit read action to trigger rule
        # Read three times
        time.sleep(1)
        # Statue check
        while True:
            time.sleep(1)
            rule = get_rule(rid)
            if rule['numCmdsGen'] >= MAX_NUMBER:
                break
        time.sleep(5)
        delete_rule(rid)
        # delete all random files
        for i in range(MAX_NUMBER):
            cids.append(delete_file(file_paths[i]))
        wait_for_cmdlets(cids)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-size', default='1MB')
    parser.add_argument('-num', default='500')
    parser.add_argument('unittest_args', nargs='*')
    args, unknown_args = parser.parse_known_args()
    sys.argv[1:] = unknown_args
    print "The file size for test is {}.".format(args.size)
    FILE_SIZE = convert_to_byte(args.size)
    print "The file number for test is {}.".format(args.num)
    MAX_NUMBER = int(args.num)

    unittest.main()
