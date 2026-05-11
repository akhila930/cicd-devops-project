import unittest
import pandas as pd
import io


class TestApp(unittest.TestCase):

    def setUp(self):
        data = """1|25|M|engineer|12345
2|30|F|teacher|67890
3|20|M|student|11111"""

        self.df = pd.read_csv(
            io.StringIO(data),
            sep='|',
            header=None,
            names=[
                'user_id',
                'age',
                'gender',
                'occupation',
                'zip_code'
            ]
        )

    def test_total_users(self):
        self.assertEqual(len(self.df), 3)

    def test_age_groups(self):
        self.df['age_group'] = pd.cut(
            self.df['age'],
            bins=[0, 18, 25, 35, 50, 100],
            labels=['<18', '18-25', '26-35', '36-50', '50+']
        )

        age_groups = [str(x) for x in self.df['age_group']]
        self.assertIn('18-25', age_groups)
        self.assertIn('26-35', age_groups)

    def test_occupation_count(self):
        self.assertEqual(len(self.df['occupation'].unique()), 3)


if __name__ == '__main__':
    unittest.main()