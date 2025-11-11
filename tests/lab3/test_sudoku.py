"""Модуль тестирования решателя Судоку."""

import unittest

from src.lab3.sudoku import group, get_row, get_col, get_block


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

    def test_get_row(self):
        """Проверка получения строки."""
        grid = [
            ['1', '2', '.'],
            ['4', '.', '6'],
            ['7', '8', '9']
        ]
        self.assertEqual(get_row(grid, (0, 0)), ['1', '2', '.'])
        self.assertEqual(get_row(grid, (1, 0)), ['4', '.', '6'])
        self.assertEqual(get_row(grid, (2, 0)), ['7', '8', '9'])

    def test_get_col(self):
        """Проверка получения столбца."""
        grid = [
            ['1', '2', '.'],
            ['4', '.', '6'],
            ['7', '8', '9']
        ]
        self.assertEqual(get_col(grid, (0, 0)), ['1', '4', '7'])
        self.assertEqual(get_col(grid, (0, 1)), ['2', '.', '8'])
        self.assertEqual(get_col(grid, (0, 2)), ['.', '6', '9'])

    def test_get_block(self):
        """Проверка получения блока."""
        grid = [
            ['1', '2', '3', '.', '.', '.'],
            ['4', '5', '6', '.', '.', '.'],
            ['7', '8', '9', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.']
        ]
        self.assertEqual(get_block(grid, (0, 0)), ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.assertEqual(get_block(grid, (1, 1)), ['1', '2', '3', '4', '5', '6', '7', '8', '9'])

