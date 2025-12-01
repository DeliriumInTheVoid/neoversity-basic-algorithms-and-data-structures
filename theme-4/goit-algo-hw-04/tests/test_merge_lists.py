from sources.merge_lists import merge_k_lists, merge_two_lists


class TestMergeKLists:
    def test_empty_list_of_lists(self):
        result = merge_k_lists([])
        assert result == []

    def test_single_empty_list(self):
        result = merge_k_lists([[]])
        assert result == []

    def test_multiple_empty_lists(self):
        result = merge_k_lists([[], [], []])
        assert result == []

    def test_single_list(self):
        result = merge_k_lists([[1, 2, 3, 4, 5]])
        assert result == [1, 2, 3, 4, 5]

    def test_three_lists_example(self):
        lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
        result = merge_k_lists(lists)
        assert result == [1, 1, 2, 3, 4, 4, 5, 6]

    def test_lists_with_negative_numbers(self):
        result = merge_k_lists([[-5, -1, 0], [-3, 2, 4], [-2, 1, 3]])
        assert result == [-5, -3, -2, -1, 0, 1, 2, 3, 4]

    def test_lists_different_lengths(self):
        result = merge_k_lists([[1], [2, 5, 7], [3, 4, 6, 8, 9, 10]])
        assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_interleaved_values(self):
        """Test with highly interleaved values."""
        result = merge_k_lists([[1, 4, 7, 10], [2, 5, 8, 11], [3, 6, 9, 12]])
        assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
