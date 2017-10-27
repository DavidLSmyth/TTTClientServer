import unittest
from python_files.TTTBoard import TTTBoard


class TestTTTBoard(unittest.TestCase):
    def setUp(self):
        self.my_board = TTTBoard()

    def test_make_move(self):
        self.assertEqual(self.my_board.get_board(), [0 for i in range(9)])
        self.assertTrue(self.my_board.make_move(0, 'X'))
        self.assertEqual(self.my_board.get_board(), [1] + [0 for i in range(8)])
        self.assertFalse(self.my_board.make_move(0, 'O'))

    def test_get_printable_board(self):
        self.assertEqual(self.my_board.get_printable_board(),
                         ''' --- --- --- 
|   |   |   | 
 --- --- --- 
|   |   |   | 
 --- --- --- 
|   |   |   | 
 --- --- --- 
''')
        self.assertTrue(self.my_board.make_move(0, 'X'))
        self.assertEqual(self.my_board.get_printable_board(),
                         ''' --- --- --- 
| X |   |   | 
 --- --- --- 
|   |   |   | 
 --- --- --- 
|   |   |   | 
 --- --- --- 
''')
        self.assertTrue(self.my_board.make_move(1, 'O'))
        self.assertEqual(self.my_board.get_printable_board(),
                         ''' --- --- --- 
| X | O |   | 
 --- --- --- 
|   |   |   | 
 --- --- --- 
|   |   |   | 
 --- --- --- 
''')
        self.assertTrue(self.my_board.make_move(7, 'X'))
        self.assertEqual(self.my_board.get_printable_board(),
''' --- --- --- 
| X | O |   | 
 --- --- --- 
|   |   |   | 
 --- --- --- 
|   | X |   | 
 --- --- --- 
''')

    def test_make_multiple_moves(self):
        self.assertTrue(self.my_board.make_move(0, 'X'))
        self.assertEqual(self.my_board.get_board(), [1] + [0 for i in range(8)])
        self.assertTrue(self.my_board.make_move(1, 'O'))
        self.assertEqual(self.my_board.get_board(), [1, 2] + [0 for i in range(7)])
        self.assertTrue(self.my_board.make_move(2, 'X'))
        self.assertEqual(self.my_board.get_board(), [1, 2, 1] + [0 for i in range(6)])


if __name__ == '__main__':
    unittest.main()
