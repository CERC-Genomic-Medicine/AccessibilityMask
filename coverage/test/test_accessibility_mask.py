import unittest
import sys
sys.path.insert(1, '/path/to/Coverage_Pipline/coverage/bin')

from accessibility_mask import make_bed
import io



class TestInterval(unittest.TestCase):
    def testinterval(self):
        input_path = "/path/to/Coverage_Pipline/coverage/test/test10.txt.gz"
        output_path = "/path/to/Coverage_Pipline/coverage/test/test_run.txt"
        column_name = "PCT_INDV_OVER_10X"
        min_percent = 0.85
        max_depth = 100
        test_out = "/path/to/Coverage_Pipline/coverage/test/test10_out.txt"
        make_bed(column_name, input_path, output_path, min_percent, max_depth)
        self.assertListEqual(
            list(io.open(test_out)),
            list(io.open(output_path)))
        
if __name__ == '__main__':
    unittest.main()