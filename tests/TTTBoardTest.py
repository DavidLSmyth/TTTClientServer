import unittest
from python_files.TTTBoard import TTTBoard


class TestTTTBoard(unittest.TestCase):
    def setUp(self):
        self.my_board = TTTBoard()

    def test_make_move(self):
        self.assertEqual(self.my_board.get_board(), [i for i in range(9)])
        self.assertTrue(self.my_board.make_move(0, b'X'))
        self.assertEqual(self.my_board.get_board(), [b'X'] + [i+1 for i in range(8)])
        self.assertFalse(self.my_board.make_move(0, b'O'))

    def test_get_printable_board(self):
        self.assertEqual(self.my_board.get_printable_board(),
                         '''
 --- --- --- 
| 0 | 1 | 2 | 
 --- --- --- 
| 3 | 4 | 5 | 
 --- --- --- 
| 6 | 7 | 8 | 
 --- --- --- 
''')
        self.assertTrue(self.my_board.make_move(0, b'X'))
        self.assertEqual(self.my_board.get_printable_board(),
                         '''
 --- --- --- 
| X | 1 | 2 | 
 --- --- --- 
| 3 | 4 | 5 | 
 --- --- --- 
| 6 | 7 | 8 | 
 --- --- --- 
''')
        self.assertTrue(self.my_board.make_move(1, b'O'))
        self.assertEqual(self.my_board.get_printable_board(),
                         '''
 --- --- --- 
| X | O | 2 | 
 --- --- --- 
| 3 | 4 | 5 | 
 --- --- --- 
| 6 | 7 | 8 | 
 --- --- --- 
''')
        self.assertTrue(self.my_board.make_move(7, b'X'))
        self.assertEqual(self.my_board.get_printable_board(),
                         '''
 --- --- --- 
| X | O | 2 | 
 --- --- --- 
| 3 | 4 | 5 | 
 --- --- --- 
| 6 | X | 8 | 
 --- --- --- 
''')

    def test_make_multiple_moves(self):
        self.assertTrue(self.my_board.make_move(0, b'X'))
        self.assertEqual(self.my_board.get_board(), [b'X'] + [i+1 for i in range(8)])
        self.assertTrue(self.my_board.make_move(1, b'O'))
        self.assertEqual(self.my_board.get_board(), [b'X', b'O'] + [i+2 for i in range(7)])
        self.assertTrue(self.my_board.make_move(2, b'X'))
        self.assertEqual(self.my_board.get_board(), [b'X', b'O', b'X'] + [i+3 for i in range(6)])

    def test_winner_horiz(self):
        self.my_board.make_move(0, b'X')
        self.assertFalse(self.my_board.detect_winner())
        self.my_board.make_move(1, b'X')
        self.assertFalse(self.my_board.detect_winner())
        self.my_board.make_move(2, b'X')
        self.assertEqual(self.my_board.detect_winner(), b'X')

    def test_winner_vert(self):
        self.my_board.make_move(0, b'O')
        self.assertFalse(self.my_board.detect_winner())
        self.my_board.make_move(3, b'O')
        self.assertFalse(self.my_board.detect_winner())
        self.my_board.make_move(6, b'O')
        self.assertEqual(self.my_board.detect_winner(), b'O')

    def test_winner_diag(self):
        self.my_board.make_move(2, b'X')
        self.assertFalse(self.my_board.detect_winner())
        self.my_board.make_move(4, b'X')
        self.assertFalse(self.my_board.detect_winner())
        self.my_board.make_move(6, b'X')
        # print(self.my_board.get_printable_board())
        self.assertEqual(self.my_board.detect_winner(), b'X')


if __name__ == '__main__':
    unittest.main()
