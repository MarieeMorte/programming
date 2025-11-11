"""Модуль тестирования решателя Судоку."""

import unittest

from src.lab3.sudoku import group, get_row, get_col, get_block, find_empty_positions, find_possible_values


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

    def test_find_empty_positions(self):
        """Проверка поиска пустых позиций."""
        grid1 = [
            ['1', '2', '.'],
            ['4', '5', '6'],
            ['7', '8', '9']
        ]
        self.assertEqual(find_empty_positions(grid1), (0, 2))

        grid2 = [
            ['1', '2', '3'],
            ['4', '.', '6'],
            ['7', '8', '9']
        ]
        self.assertEqual(find_empty_positions(grid2), (1, 1))

        grid3 = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['.', '8', '9']
        ]
        self.assertEqual(find_empty_positions(grid3), (2, 0))

        grid4 = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']
        ]
        self.assertIsNone(find_empty_positions(grid4))

    def test_find_possible_values(self):
        """Проверка поиска возможных значений."""
        grid = [
            ['1', '2', '.'],
            ['.', '5', '6'],
            ['7', '8', '9']
        ]

        possible = find_possible_values(grid, (0, 2))
        self.assertEqual(possible, {'3', '4'})

        possible = find_possible_values(grid, (1, 0))
        self.assertEqual(possible, {'3', '4'})

        grid = [
            ['5', '3', '.', '.', '7', '.', '.', '.', '.'],
            ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
            ['.', '9', '8', '.', '.', '.', '.', '6', '.']
        ]

        possible = find_possible_values(grid, (0, 2))
        self.assertEqual(possible, {'1', '2', '4'})
