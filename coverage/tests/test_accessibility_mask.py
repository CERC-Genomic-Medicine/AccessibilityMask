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
        """
        This function is testing a condition where our final bed file contains a big interval,\
        meaning that all base pairs meet the criteria for min percentage and max depth. And all\
        base pairs are continous.
        """
        
        input_path = f'{self.test_data_path}/test1.txt.gz'
        truth_path = f'{self.test_data_path}/truth1.bed'
        output_path = 'test1.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))

    def test_no_regions(self):
        """
        This function is testing a condition where our final bed file contains no interval,\
        meaning that none of base pairs meet the criteria for min percentage and max depth.
        """
        
        input_path = f'{self.test_data_path}/test2.txt.gz'
        truth_path = f'{self.test_data_path}/truth2.bed'
        output_path = 'test2.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))
    
    def test_one_no_region_one_large_region(self):
        """
        This function is testing a condition where our final bed file contains an interval\
        However, the interval doesn't start from the first base pair. Because, there is a set\
        of base pairs at the begining that doesn't meet the criteria.
        """
        
        input_path = f'{self.test_data_path}/test3.txt.gz'
        truth_path = f'{self.test_data_path}/truth3.bed'
        output_path = 'test3.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))

    def test_one_large_region_one_no_region(self):
        """
        This function is testing a condition where our final bed file contains an interval,\
        the interval starts from the first base pair but it doesn't contain a subset of base\
        pairs at the end. Because they don't meet the criteria.
        """
        
        input_path = f'{self.test_data_path}/test4.txt.gz'
        truth_path = f'{self.test_data_path}/truth4.bed'
        output_path = 'test4.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))    
    
    def test_one_no_region_one_region_one_no_region(self):
        """
        This function is testing a condition where our final bed file contains an interval.\
        However, the interval doesn't start from the first base pair and also it doesn't\
        contain a set of regions at the end.
        """
        
        input_path = f'{self.test_data_path}/test5.txt.gz'
        truth_path = f'{self.test_data_path}/truth5.bed'
        output_path = 'test5.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))
            
    def test_one_region_one_no_region_one_region(self):
        """
        This function is testing a condition where our final bed file contains two intervals.\
        one interval at the begining of base pairs set and one at the end. There is a region in\
        the middle which doesn't meet the criteria.
        """
        
        input_path = f'{self.test_data_path}/test6.txt.gz'
        truth_path = f'{self.test_data_path}/truth6.bed'
        output_path = 'test6.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))
            
    def test_two_non_continuous_regions(self):
        """
        This function is testing a condition where our final bed file contains two intervals.\
        However, the intervals are not continous. If the first interval ends at position 3 the\
        next will start at position 8.
        """
        
        input_path = f'{self.test_data_path}/test7.txt.gz'
        truth_path = f'{self.test_data_path}/truth7.bed'
        output_path = 'test7.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))
    
    def test_three_non_continuous_regions(self):
        """
        This function is testing a condition where our final bed file contains three intervals.\
        However, the intervals are not continous. As an example, if the first interval ends at \
        position 3 the next will start at position 8.
        """
        
        input_path = f'{self.test_data_path}/test8.txt.gz'
        truth_path = f'{self.test_data_path}/truth8.bed'
        output_path = 'test8.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))
    
    def test_two_non_continuous_regions_one_no_region(self):
        """
        This function is testing a condition where our final bed file contains two intervals.\
        However, the intervals are not continous. As an example, if the first interval ends at\
        position 3 the next will start at position 8. Besides there is a subset of base pairs at\
        the end that doesn't meet the criteria.
        """
        
        input_path = f'{self.test_data_path}/test9.txt.gz'
        truth_path = f'{self.test_data_path}/truth9.bed'
        output_path = 'test9.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))
    
    def test_one_no_region_two_non_continuous_regions(self):
        """
        This function is testing a condition where our final bed file contains two intervals.\
        However, the intervals are not continous. As an example, if the first interval ends at\
        position 3 the next will start at position 8. Besides there is a subset of base pairs at\
        the the begining that doesn't meet the criteria, hense our first interval doesn't start\
        from very beggining base pair.
        """
        
        input_path = f'{self.test_data_path}/test10.txt.gz'
        truth_path = f'{self.test_data_path}/truth10.bed'
        output_path = 'test10.bed'
        make_bed(self.column_name, input_path, output_path, self.min_percent, self.max_depth)
        with open(truth_path) as truth, open(output_path) as output:
            self.assertListEqual(list(truth), list(output))
            
    def tearDown(self):
        
        for f in glob.glob('test*.bed'):
            os.remove(f)