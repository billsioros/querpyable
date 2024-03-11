import pytest

from querpyable import Queryable


# Returns a Queryable instance representing a range of integers from start to stop with a step of 1.
def test_range_with_step():
    result = Queryable.range(1, 10, 2)
    assert list(result) == [1, 3, 5, 7, 9]


# Returns an empty Queryable instance if start and stop are the same.
def test_range_empty():
    result = Queryable.range(5, 5)
    assert list(result) == []


# Returns a new Queryable instance with an empty list.
def test_empty_returns_new_queryable_with_empty_list():
    # Arrange
    expected_collection = []

    # Act
    result = Queryable.empty()

    # Assert
    assert result.collection == expected_collection


# The empty list is the only argument passed to the constructor of the new Queryable instance.
def test_empty_list_passed_to_constructor():
    # Arrange
    expected_collection = []

    # Act
    result = Queryable.empty()

    # Assert
    assert result.collection == expected_collection


# Returns a new Queryable containing elements that satisfy the given predicate.
def test_where_returns_new_queryable():
    # Arrange
    data = Queryable([1, 2, 3, 4, 5])

    def is_even(n):
        return n % 2 == 0

    # Act
    result = data.where(is_even)

    # Assert
    assert isinstance(result, Queryable)
    assert list(result) == [2, 4]


# Returns an empty Queryable if the original Queryable is empty.
def test_where_returns_empty_queryable():
    # Arrange
    data = Queryable([])

    # Act
    result = data.where(lambda x: x > 0)

    # Assert
    assert isinstance(result, Queryable)
    assert list(result) == []


# Selecting from a Queryable with multiple elements returns a new Queryable with the same number of elements.
def test_select_multiple_elements():
    # Arrange
    data = Queryable([1, 2, 3, 4, 5])

    def double(x):
        return x * 2

    # Act
    result = data.select(double)

    # Assert
    assert list(result) == [2, 4, 6, 8, 10]


# Selecting from a Queryable with a selector function that raises an exception raises the same exception.
def test_select_exception():
    # Arrange
    data = Queryable([1, 2, 3, 4, 5])

    def raise_exception(x):
        raise ValueError("Test Exception")

    # Act & Assert
    with pytest.raises(ValueError):
        data.select(raise_exception).to_list()


# Returns a new Queryable with distinct elements.
def test_distinct_returns_new_queryable_with_distinct_elements():
    # Arrange
    data = [1, 2, 2, 3, 4, 4, 5]
    queryable_data = Queryable(data)

    # Act
    distinct_queryable = queryable_data.distinct()

    # Assert
    assert list(distinct_queryable) == [1, 2, 3, 4, 5]


# Returns an empty Queryable if the original collection is empty.
def test_distinct_returns_empty_queryable_if_original_collection_is_empty():
    # Arrange
    data = []
    queryable_data = Queryable(data)

    # Act
    distinct_queryable = queryable_data.distinct()

    # Assert
    assert list(distinct_queryable) == []


# Given a Queryable with n elements, when skip is called with a count less than n, then a new Queryable is returned containing the remaining elements after skipping the specified number of elements.
def test_skip_with_count_less_than_n():
    # Create a Queryable with elements [1, 2, 3, 4, 5]
    queryable = Queryable([1, 2, 3, 4, 5])

    # Skip the first 2 elements
    result = queryable.skip(2)

    # The result should contain elements [3, 4, 5]
    assert list(result) == [3, 4, 5]


# Given a Queryable with no elements, when skip is called, then an empty Queryable is returned.
def test_skip_with_empty_queryable():
    # Create an empty Queryable
    queryable = Queryable([])

    # Skip elements
    result = queryable.skip(2)

    # The result should be an empty Queryable
    assert list(result) == []


# Returns a new Queryable containing the first 'count' elements of the current Queryable.
def test_take_returns_new_queryable_with_first_count_elements():
    # Arrange
    data = Queryable([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    count = 3

    # Act
    result = data.take(count)

    # Assert
    assert list(result) == [1, 2, 3]


# Returns empty if count is negative.
def test_take_returns_empty_if_count_is_negative():
    # Arrange
    data = Queryable([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    count = -3

    # Act and Assert
    assert data.take(count).to_list() == []


# Returns a new Queryable containing only elements of the specified type.
def test_of_type_returns_new_queryable_with_specified_type():
    # Arrange
    data = [1, "two", 3.0, "four", 5]
    queryable_data = Queryable(data)

    # Act
    result = queryable_data.of_type(str)

    # Assert
    assert isinstance(result, Queryable)
    assert result.to_list() == ["two", "four"]


# Returns an empty Queryable if the original Queryable is empty.
def test_of_type_returns_empty_queryable_for_empty_queryable():
    # Arrange
    data = []
    queryable_data = Queryable(data)

    # Act
    result = queryable_data.of_type(int)

    # Assert
    assert isinstance(result, Queryable)
    assert result.to_list() == []


# Should return a new Queryable instance containing the flattened sequence
def test_select_many_return_new_queryable_instance():
    # Arrange
    def get_digits(n: int):
        return (int(digit) for digit in str(n))

    numbers = Queryable([123, 456, 789])

    # Act
    result = numbers.select_many(get_digits)

    # Assert
    assert isinstance(result, Queryable)
    assert list(result) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


# Should raise an exception if the selector function is None
def test_select_many_raise_exception_if_selector_function_is_none():
    # Arrange
    numbers = Queryable([1, 2, 3])

    # Act & Assert
    with pytest.raises(TypeError):
        numbers.select_many(None).to_list()


# Orders a Queryable of integers in ascending order based on a key selector function
def test_order_by_order_by_ascending():
    # Initialize Queryable with a list of integers
    data = Queryable([5, 2, 8, 1, 7])

    # Order the Queryable in ascending order
    result = data.order_by(lambda x: x).to_list()

    # Assert the result is in ascending order
    assert result == [1, 2, 5, 7, 8]


# Orders an empty Queryable
def test_order_by_empty():
    # Initialize an empty Queryable
    data = Queryable.empty()

    # Order the empty Queryable
    result = data.order_by(lambda x: x).to_list()

    # Assert the result is an empty list
    assert result == []


# Sorts a list of integers in descending order based on the element itself.
def test_order_by_descending_integers_descending():
    # Initialize the Queryable object
    data = [5, 2, 8, 1, 7]
    queryable_data = Queryable(data)

    # Invoke the order_by_descending method
    result = queryable_data.order_by_descending(lambda x: x)

    # Check the result
    assert list(result) == [8, 7, 5, 2, 1]


# Sorts an empty list, returns an empty Queryable.
def test_order_by_descending_empty_list():
    # Initialize the Queryable object with an empty list
    data = []
    queryable_data = Queryable(data)

    # Invoke the order_by_descending method
    result = queryable_data.order_by_descending(lambda x: x)

    # Check the result
    assert list(result) == []


# Sorts a list of objects by a primary key and then by a secondary key.
def test_then_by_by_primary_and_secondary_key():
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    people = [
        Person("Alice", 30),
        Person("Bob", 25),
        Person("Charlie", 35),
        Person("Bob", 30),
    ]

    queryable_people = Queryable(people)

    # Sort by age in ascending order and then by name in ascending order
    sorted_people = queryable_people.order_by(lambda p: p.age).then_by(lambda p: p.name).to_list()

    assert sorted_people == sorted(people, key=lambda p: (p.age, p.name))


# The input collection is empty.
def test_then_by_empty_collection():
    queryable = Queryable([])
    sorted_queryable = queryable.then_by(lambda x: x)
    assert list(sorted_queryable) == []


# The method should sort a list of objects based on a key selector in descending order.
def test_then_by_descending_list_in_descending_order():
    # Initialize the Queryable object
    queryable = Queryable([(1, "apple"), (3, "banana"), (2, "orange")])

    # Sort the list in descending order based on the key selector
    sorted_list = queryable.then_by_descending(lambda x: x[0]).to_list()

    # Check if the list is sorted correctly
    assert sorted_list == [(3, "banana"), (2, "orange"), (1, "apple")]


# The method should work correctly with an empty list.
def test_then_by_descending_empty_list():
    # Initialize an empty Queryable object
    queryable = Queryable([])

    # Sort the empty list in descending order based on the key selector
    sorted_list = queryable.then_by_descending(lambda x: x[0]).to_list()

    # Check if the sorted list is also empty
    assert sorted_list == []

    # should join two sequences based on the specified key selectors and return a new Queryable containing the result of the group join operation


def test_group_join_success():
    # Initialize the outer sequence
    outer_sequence = Queryable([1, 2, 3, 4])

    # Initialize the inner sequence
    inner_sequence = Queryable([(1, 'a'), (2, 'b'), (2, 'c'), (3, 'd')])

    # Perform the group join operation
    result = outer_sequence.group_join(
        inner_sequence,
        outer_key_selector=lambda x: x,
        inner_key_selector=lambda x: x[0],
        result_selector=lambda outer, inner: (outer, list(inner)),
    )

    # Assert the result
    assert list(result) == [(1, [('a',)]), (2, [('b', 'c')]), (3, [('d',)]), (4, [])]


# should raise a TypeError if the outer_key_selector is not callable
def test_group_join_invalid_outer_key_selector():
    # Initialize the outer sequence
    outer_sequence = Queryable([1, 2, 3, 4])

    # Initialize the inner sequence
    inner_sequence = Queryable([(1, 'a'), (2, 'b'), (2, 'c'), (3, 'd')])

    # Define an invalid outer key selector
    invalid_outer_key_selector = "not_callable"

    # Perform the group join operation and assert that it raises a TypeError
    with pytest.raises(TypeError):
        outer_sequence.group_join(
            inner_sequence,
            outer_key_selector=invalid_outer_key_selector,
            inner_key_selector=lambda x: x[0],
            result_selector=lambda outer, inner: (outer, list(inner)),
        ).to_list()


# Zips two Queryable instances of the same length.
def test_zip_same_length():
    # Initialize two Queryable instances
    queryable1 = Queryable([1, 2, 3, 4])
    queryable2 = Queryable(['a', 'b', 'c', 'd'])

    # Zip the elements of the two Queryable instances
    result = queryable1.zip(queryable2)

    # Convert the result to a list and assert the expected output
    assert list(result) == [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]


# Zips two Queryable instances of different lengths.
def test_zip_different_length():
    # Initialize two Queryable instances
    queryable1 = Queryable([1, 2, 3, 4])
    queryable2 = Queryable(['a', 'b', 'c'])

    # Zip the elements of the two Queryable instances
    result = queryable1.zip(queryable2)

    # Convert the result to a list and assert the expected output
    assert list(result) == [(1, 'a'), (2, 'b'), (3, 'c')]


# Concatenating two non-empty iterables
def test_concat_two_non_empty_iterables():
    # Initialize the Queryable object with initial elements
    queryable1 = Queryable([1, 2, 3])

    # Another iterable to concatenate
    other_iterable = [4, 5, 6]

    # Concatenate the two iterables
    result_queryable = queryable1.concat(other_iterable)

    # Assert that the concatenated elements are correct
    assert list(result_queryable) == [1, 2, 3, 4, 5, 6]


# Concatenating a large iterable to a small iterable
def test_concat_large_iterable_to_small_iterable():
    # Initialize the Queryable object with initial elements
    queryable1 = Queryable([1, 2, 3])

    # Another iterable to concatenate (larger than the initial iterable)
    other_iterable = [4, 5, 6, 7, 8, 9]

    # Concatenate the two iterables
    result_queryable = queryable1.concat(other_iterable)

    # Assert that the concatenated elements are correct
    assert list(result_queryable) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


# Concatenating with empty list
def test_concat_with_empty_list():
    # Initialize the Queryable object
    queryable1 = Queryable([1, 2, 3])

    # Concatenate with empty list
    result_queryable = queryable1.concat([])

    # Check if the concatenated elements are correct
    assert list(result_queryable) == [1, 2, 3]


# Aggregating a list of numbers using the addition function
def test_aggregate_addition():
    # Arrange
    numbers = Queryable([1, 2, 3, 4, 5])

    # Act
    result = numbers.aggregate(lambda x, y: x + y)

    # Assert
    assert result == 15


# Aggregating an empty list raises a ValueError
def test_aggregate_empty_list():
    # Arrange
    numbers = Queryable([])

    # Act & Assert
    with pytest.raises(ValueError):
        numbers.aggregate(lambda x, y: x + y)


# Returns a new Queryable with unique elements from both sequences.
def test_union_unique_elements():
    set1 = Queryable(["apple", "banana", "cherry"])
    set2 = ["banana", "orange", "grape"]
    result = set1.union(set2)
    assert set(result) == {"apple", "banana", "cherry", "orange", "grape"}


# Returns a new Queryable with unique elements from two sequences with duplicate elements.
def test_union_duplicate_elements():
    set1 = Queryable([1, 2, 3, 4])
    set2 = [3, 4, 5, 6]
    result = set1.union(set2)
    assert list(result) == [1, 2, 3, 4, 5, 6]


# Returns a new Queryable containing common elements between two sequences.
def test_intersect_common_elements():
    set1 = Queryable(["apple", "banana", "orange"])
    set2 = ["banana", "orange", "grape"]
    result = set1.intersect(set2)
    assert list(result) == ["banana", "orange"]


# If the input sequence contains duplicates, returns a Queryable with the intersection of the unique elements.
def test_intersect_duplicates():
    set1 = Queryable(["apple", "banana", "banana", "orange"])
    set2 = ["banana", "orange", "grape"]
    result = set1.intersect(set2)
    assert set(result) == {"banana", "orange"}


# Returns True if all elements satisfy the predicate
def test_all_elements_satisfy_predicate():
    # Arrange
    numbers = Queryable([2, 4, 6, 8])

    # Act
    result = numbers.all(lambda x: x % 2 == 0)

    # Assert
    assert result == True


# Returns True if the predicate is None and all elements are truthy
def test_all_predicate_is_none_and_all_elements_are_truthy():
    # Arrange
    numbers = Queryable([2, 4, 6, 8, 9])

    # Act
    result = numbers.all(None)

    # Assert
    assert result


# Returns True if at least one element satisfies the predicate
def test_any_returns_true_if_any_element_satisfies_predicate():
    # Arrange
    numbers = Queryable([5, 8, 12, 3, 7])

    # Act
    result = numbers.any(lambda x: x > 10)

    # Assert
    assert result is True


# Returns False for an empty collection and a valid predicate
def test_any_returns_false_for_empty_collection_and_valid_predicate():
    # Arrange
    numbers = Queryable([])

    # Act
    result = numbers.any(lambda x: x > 10)

    # Assert
    assert result is False


# returns True if the value is in the sequence
def test_contains_returns_true_if_value_in_sequence():
    # Arrange
    numbers = Queryable([1, 2, 3, 4])

    # Act
    result = numbers.contains(3)

    # Assert
    assert result is True


# works with None as the value parameter
def test_contains_works_with_none_as_value_parameter():
    # Arrange
    numbers = Queryable([1, 2, 3, 4])

    # Act
    result = numbers.contains(None)

    # Assert
    assert result is False


# Count the number of elements in a non-empty sequence
def test_count_non_empty_sequence():
    # Arrange
    numbers = Queryable([1, 2, 3, 4, 5, 6])

    # Act
    result = numbers.count()

    # Assert
    assert result == 6


# Count the number of elements in a sequence with a single element
def test_count_single_element_sequence():
    # Arrange
    numbers = Queryable([1])

    # Act
    result = numbers.count()

    # Assert
    assert result == 1


# Calculates the sum of a list of positive integers
def test_sum_positive_integers():
    numbers = Queryable([1, 2, 3, 4, 5])
    result = numbers.sum()
    assert result == 15


# Calculates the sum of an empty list, which should return 0
def test_sum_empty_list():
    numbers = Queryable([])
    result = numbers.sum()
    assert result == 0


# Returns the minimum value in a sequence of integers.
def test_min_returns_minimum_value():
    numbers = Queryable([3, 1, 4, 1, 5, 9, 2])
    result = numbers.min()
    assert result == 1


# Raises a ValueError if the sequence is empty.
def test_min_raises_value_error_for_empty_sequence():
    numbers = Queryable([])
    with pytest.raises(ValueError):
        numbers.min()


# Returns the maximum value in a sequence of integers.
def test_max_returns_maximum_value():
    numbers = Queryable([3, 1, 4, 1, 5, 9, 2])
    result = numbers.max()
    assert result == 9


# Raises a ValueError when called on an empty sequence.
def test_max_raises_value_error_on_empty_sequence():
    numbers = Queryable([])
    with pytest.raises(ValueError):
        numbers.max()


# Returns the correct average of a list of integers.
def test_average_correct_average_of_integers():
    numbers = Queryable([1, 2, 3, 4, 5])
    result = numbers.average()
    assert result == 3.0


# Raises a TypeError if the Queryable object contains non-numeric values.
def test_average_raises_type_error_for_non_numeric_values():
    data = Queryable([1, 2, 'three', 4, 5])
    with pytest.raises(TypeError):
        data.average()


# Returns a new Queryable containing elements not present in the specified sequence.
def test_except_for_returns_new_queryable():
    set1 = Queryable([1, 2, 3, 4])
    set2 = [3, 4, 5, 6]
    result = set1.except_for(set2)
    assert isinstance(result, Queryable)
    assert list(result) == [1, 2]


# Excludes all elements from the specified sequence.
def test_except_for_excludes_all_elements():
    set1 = Queryable([1, 2, 3, 4])
    set2 = [1, 2, 3, 4]
    result = set1.except_for(set2)
    assert isinstance(result, Queryable)
    assert list(result) == []


# Returns the first element of a non-empty sequence without a predicate.
def test_first_returns_first_element_without_predicate():
    numbers = Queryable([1, 2, 3, 4, 5])
    result = numbers.first()
    assert result == 1


# Raises a ValueError if the sequence is empty and no predicate is given.
def test_first_raises_value_error_if_sequence_is_empty_without_predicate():
    numbers = Queryable([])
    with pytest.raises(ValueError):
        numbers.first()


# Returns the first element of the sequence when no predicate is given and the sequence is not empty.
def test_first_or_default_returns_first_element_when_no_predicate_given_and_sequence_not_empty():
    # Arrange
    numbers = Queryable([1, 2, 3, 4, 5])

    # Act
    result = numbers.first_or_default()

    # Assert
    assert result == 1


# Returns None when the sequence is empty and no default value is provided.
def test_first_or_default_returns_none_when_sequence_empty_and_no_default_value_provided():
    # Arrange
    numbers = Queryable([])

    # Act
    result = numbers.first_or_default()

    # Assert
    assert result is None


# Returns the last element of a non-empty sequence.
def test_last_returns_last_element_of_non_empty_sequence():
    # Arrange
    numbers = Queryable([1, 2, 3, 4, 5])

    # Act
    result = numbers.last()

    # Assert
    assert result == 5


# Raises ValueError if the sequence is empty and no predicate is given.
def test_last_raises_value_error_if_sequence_is_empty_and_no_predicate_given():
    # Arrange
    numbers = Queryable([])

    # Act & Assert
    with pytest.raises(ValueError):
        numbers.last()


# Returns the last element of the sequence if no predicate is given and the sequence is not empty.
def test_last_or_default_returns_last_element_if_no_predicate_given_and_sequence_not_empty():
    # Arrange
    numbers = Queryable([1, 2, 3, 4, 5])

    # Act
    result = numbers.last_or_default()

    # Assert
    assert result == 5


# Returns None if the sequence is empty and no default value is given.
def test_last_or_default_returns_none_if_sequence_empty_and_no_default_value_given():
    # Arrange
    numbers = Queryable([])

    # Act
    result = numbers.last_or_default()

    # Assert
    assert result is None


# Returns the single element of the sequence.
def test_single_returns_single_element():
    numbers = Queryable([2])
    result = numbers.single()
    assert result == 2


# Raises ValueError if the sequence is empty.
def test_single_raises_value_error_if_sequence_is_empty():
    numbers = Queryable([])
    with pytest.raises(ValueError):
        numbers.single()


# Returns the single element of the sequence satisfying the predicate.
def test_single_or_default_returns_single_element():
    numbers = Queryable([1, 2, 3, 4, 5])
    result = numbers.single_or_default(lambda x: x == 2)
    assert result == 2


# Raises ValueError if the sequence contains more than one element satisfying the predicate.
def test_single_or_default_raises_value_error():
    numbers = Queryable([1, 2, 3, 4, 5, 6])
    with pytest.raises(ValueError):
        numbers.single_or_default(lambda x: x % 2 == 0)


# Should return the element at the specified index
def test_element_at_return_element_at_specified_index():
    numbers = Queryable([1, 2, 3, 4, 5])
    result = numbers.element_at(2)
    assert result == 3


# Should raise ValueError if the sequence is empty
def test_element_at_raise_value_error_if_sequence_is_empty():
    numbers = Queryable([])
    with pytest.raises(ValueError):
        numbers.element_at(0)


# Should return the element at the specified index
def test_return_element_at_specified_index():
    numbers = Queryable([1, 2, 3, 4, 5])
    result = numbers.element_at_or_default(2)
    assert result == 3


# Should return None if the sequence is empty and no default value is provided
def test_return_none_if_sequence_empty():
    numbers = Queryable([])
    result = numbers.element_at_or_default(0)
    assert result is None


# Returns a new Queryable with the original elements if the sequence is not empty.
def test_default_if_empty_non_empty_sequence():
    # Arrange
    data = [1, 2, 3, 4, 5]
    queryable_data = Queryable(data)

    # Act
    result = queryable_data.default_if_empty(default=0).to_list()

    # Assert
    assert result == data


# The default value is None.
def test_default_if_empty_default_value_none():
    # Arrange
    empty_list = Queryable([])

    # Act
    result = empty_list.default_if_empty(default=None).to_list()

    # Assert
    assert result == [None]


# Join two non-empty sets based on common factors
def test_join_two_non_empty_sets():
    # Initialize the Queryable objects
    set1 = Queryable([1, 2, 3, 4])
    set2 = [3, 4, 5, 6]

    # Join the two sets based on common factors
    result = set1.join(
        set2,
        outer_key_selector=lambda x: x,
        inner_key_selector=lambda x: x % 3,
        result_selector=lambda x, y: (x, y),
    )

    # Assert the result is correct
    assert result.to_list() == [(1, 4), (2, 5), (3, 6)]


# Join two sets based on common factors, where the inner iterable contains duplicate keys
def test_join_with_duplicate_keys():
    # Initialize the Queryable objects
    set1 = Queryable([1, 2, 3, 4])
    set2 = [3, 4, 4, 5, 6]

    # Join the two sets based on common factors
    result = set1.join(
        set2,
        outer_key_selector=lambda x: x,
        inner_key_selector=lambda x: x % 3,
        result_selector=lambda x, y: (x, y),
    )

    # Assert the result is correct
    assert result.to_list() == [(1, 4), (1, 4), (2, 5), (3, 6)]


# Returns a list containing all elements of the Queryable.
def test_to_list_returns_list_with_all_elements():
    # Arrange
    numbers = Queryable([1, 2, 3, 4, 5])

    # Act
    result = numbers.to_list()

    # Assert
    assert result == [1, 2, 3, 4, 5]


# Returns a list with elements of different types.
def test_to_list_returns_list_with_different_types():
    # Arrange
    data = Queryable([1, "two", 3.0, "four", 5])

    # Act
    result = data.to_list()

    # Assert
    assert result == [1, "two", 3.0, "four", 5]


# Returns a dictionary with key-value pairs based on the input Queryable and key_selector function.
def test_to_dictionary_returns_dictionary_with_key_value_pairs():
    # Arrange
    data = Queryable([(1, 'one'), (2, 'two'), (3, 'three')])

    # Act
    result = data.to_dictionary(key_selector=lambda x: x[0], value_selector=lambda x: x[1])

    # Assert
    assert isinstance(result, dict)
    assert len(result) == 3
    assert result == {1: 'one', 2: 'two', 3: 'three'}


# Raises a TypeError when key_selector is not callable.
def test_to_dictionary_raises_type_error_when_key_selector_not_callable():
    # Arrange
    data = Queryable([(1, 'one'), (2, 'two'), (3, 'three')])

    # Act and Assert
    with pytest.raises(TypeError):
        data.to_dictionary(key_selector='not_callable')
