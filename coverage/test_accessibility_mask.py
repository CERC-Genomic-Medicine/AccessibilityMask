import unittest
from bin.accessibility_mask import make_bed
import io
import glob


class TestInterval(unittest.TestCase):
    def testinterval(self):
        input_names = glob.glob("test/*.txt.gz")
        output_names = [i[:-7]+"_out.txt" for i in input_names]
        for i in range(len(input_names)):
            input_path = input_names[i]
            output_path = "test/test_run.txt"
            column_name = "PCT_INDV_OVER_10X"
            min_percent = 0.85
            max_depth = 100
            test_out = output_names[i]
            make_bed(column_name, input_path, output_path, min_percent, max_depth)
            print("testing " + input_names[i][5:-7])
            self.assertListEqual(
                list(io.open(test_out)),
                list(io.open(output_path)))
            print(input_names[i][5:-7] +" PASS!")
        
if __name__ == '__main__':
    unittest.main()