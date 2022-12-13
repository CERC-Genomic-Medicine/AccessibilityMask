import unittest
from bin.accessibility_mask import make_bed
import os
import glob


class TestInterval(unittest.TestCase):
    
    def setUp(self):
        self.test_data_path = 'tests/data'
        self.column_name = 'PCT_INDV_OVER_10X'
        self.min_percent = 0.85
        self.max_depth = 100

    def test_one_large_region(self):
        input_path = f'{self.test_data_path}/test1.txt.gz'
        truth_path = f'{self.test_data_path}/truth1.bed'
        output_path = 'test1.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))

    def test_no_regions(self):
        input_path = f'{self.test_data_path}/test2.txt.gz'
        truth_path = f'{self.test_data_path}/truth2.bed'
        output_path = 'test2.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))

    def tearDown(self):
        for f in glob.glob('test*.bed'):
            os.remove(f)


'''    
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
''' 

if __name__ == '__main__':
    unittest.main()
