"""Модуль тестирования решателя Судоку."""

import unittest

from src.lab3.sudoku import group


class SudokuTestCase(unittest.TestCase):
    def test_group(self):
        """Проверка группировки значений в матрицу."""
        self.assertEqual(group([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3),
                         [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(group(['a', 'b', 'c', 'd'], 2),
                         [['a', 'b'], ['c', 'd']])
        self.assertEqual(group([1, 2, 3, 4, 5, 6], 3),
                         [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(group([], 3), [])
