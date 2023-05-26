import pytest

from querpyable.querpyable import Queryable


@pytest.fixture
def single_element_list():
    return [1]


@pytest.fixture
def flattened_list():
    return [1, 2, 2, 3, 4, 5, 5]


@pytest.fixture
def nested_list():
    return [[1, 2], [2, 3], [4, 5], [5]]


def test_queryable_empty():
    assert len(Queryable.empty().to_list()) == 0


def test_queryable_range():
    data = Queryable.range(10).to_list()
    assert len(data) == 10
    assert 0 in data

    data = Queryable.range(1, 10).to_list()
    assert len(data) == 9
    assert 0 not in data


def test_queryable_where(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.where(lambda x: x > 2).to_list()
    assert result == [3, 4, 5, 5]


def test_queryable_select(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.select(lambda x: x * 2).to_list()
    assert result == [2, 4, 4, 6, 8, 10, 10]


def test_queryable_distinct(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.distinct().to_list()
    assert result == [1, 2, 3, 4, 5]


def test_queryable_skip(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.skip(2).to_list()
    assert result == [2, 3, 4, 5, 5]


def test_queryable_take(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.take(3).to_list()
    assert result == [1, 2, 2]


def test_queryable_of_type(flattened_list):
    mixed_data = flattened_list + ['a', 'b', 'c']
    queryable = Queryable(mixed_data)
    result = queryable.of_type(int).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5]


def test_queryable_select_many(nested_list):
    queryable = Queryable(nested_list)
    result = queryable.select_many(lambda x: x).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5]


def test_queryable_order_by(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.order_by(lambda x: x).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5]


def test_queryable_order_by_descending(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.order_by_descending(lambda x: x).to_list()
    assert result == [5, 5, 4, 3, 2, 2, 1]


def test_queryable_then_by(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.order_by(lambda x: -x).then_by(lambda x: x).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5]


def test_queryable_then_by_descending(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.order_by(lambda x: x).then_by_descending(lambda x: -x).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5]


def test_queryable_join(flattened_list):
    inner_data = [1, 3, 5, 7, 9]
    queryable = Queryable(flattened_list)
    result = queryable.join(inner_data, lambda x: x, lambda x: x, lambda x, y: x * y).to_list()
    assert result == [1, 9, 25, 25]


def test_group_join():
    persons = [
        {'id': 1, 'name': 'John', 'country_id': 1},
        {'id': 2, 'name': 'Alice', 'country_id': 2},
        {'id': 3, 'name': 'Bob', 'country_id': 1},
        {'id': 4, 'name': 'Emily', 'country_id': 3},
        {'id': 5, 'name': 'David', 'country_id': 2},
    ]

    countries = [
        {'id': 1, 'name': 'USA'},
        {'id': 2, 'name': 'Canada'},
        {'id': 3, 'name': 'Australia'},
    ]

    queryable_persons = Queryable(persons)

    result = queryable_persons.group_join(
        countries,
        outer_key_selector=lambda person: person['country_id'],
        inner_key_selector=lambda country: country['id'],
        result_selector=lambda person, countries: {
            'person_name': person['name'],
            'countries': [country['name'] for country in countries],
        },
    )

    expected_result = [
        {'person_name': 'John', 'countries': ['USA']},
        {'person_name': 'Alice', 'countries': ['Canada']},
        {'person_name': 'Bob', 'countries': ['USA']},
        {'person_name': 'Emily', 'countries': ['Australia']},
        {'person_name': 'David', 'countries': ['Canada']},
    ]

    assert list(result) == expected_result


def test_zip():
    numbers = [1, 2, 3, 4, 5]
    letters = ['A', 'B', 'C', 'D', 'E']

    queryable_numbers = Queryable(numbers)

    result = queryable_numbers.zip(letters)

    expected_result = [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')]

    assert list(result) == expected_result


def test_queryable_concat(flattened_list):
    queryable1 = Queryable(flattened_list)
    queryable2 = Queryable([6, 7, 7, 8])
    result = queryable1.concat(queryable2).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5, 6, 7, 7, 8]


def test_queryable_union(flattened_list):
    queryable1 = Queryable(flattened_list)
    queryable2 = Queryable([5, 6, 7, 7, 8])
    result = queryable1.union(queryable2).to_list()
    assert result == [1, 2, 3, 4, 5, 6, 7, 8]


def test_queryable_intersect(flattened_list):
    queryable1 = Queryable(flattened_list)
    queryable2 = Queryable([3, 4, 5, 6, 6])
    result = queryable1.intersect(queryable2).to_list()
    assert result == [3, 4, 5]


def test_queryable_except(flattened_list):
    queryable1 = Queryable(flattened_list)
    queryable2 = Queryable([2, 3, 6, 6])
    result = queryable1.except_for(queryable2).to_list()
    assert result == [1, 4, 5]


def test_queryable_all(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.all(lambda x: x > 0)
    assert result == True


def test_queryable_any(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.any()
    assert result == True


def test_queryable_any_predicate(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.any(lambda x: x > 5)
    assert result == False


def test_queryable_contains(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.contains(1)
    assert result == True
    result = queryable.contains(0)
    assert result == False


def test_queryable_count(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.count()
    assert result == 7


def test_queryable_sum(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.sum()
    assert result == 22


def test_sum():
    numbers = [1, 2, 3, 4, 5]
    queryable = Queryable(numbers)

    result = queryable.sum()
    expected_result = 15

    assert result == expected_result


def test_min():
    numbers = [5, 3, 9, 1, 7]
    queryable = Queryable(numbers)

    result = queryable.min()
    expected_result = 1

    assert result == expected_result


def test_max():
    numbers = [5, 3, 9, 1, 7]
    queryable = Queryable(numbers)

    result = queryable.max()
    expected_result = 9

    assert result == expected_result


def test_average():
    numbers = [1, 2, 3, 4, 5]
    queryable = Queryable(numbers)

    result = queryable.average()
    expected_result = 3.0

    assert result == expected_result


def test_aggregate_sum(flattened_list):
    queryable = Queryable(flattened_list)

    result = queryable.aggregate(lambda x, y: x + y)

    assert result == 22


def test_aggregate_multiply():
    numbers = [1, 2, 3, 4, 5]
    queryable = Queryable(numbers)

    result = queryable.aggregate(lambda x, y: x * y)
    expected_result = 120

    assert result == expected_result


def test_first(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.first()
    assert result == 1


def test_first_or_default(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.first_or_default(default=-1)
    assert result == 1


def test_last(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.last()
    assert result == 5


def test_last_or_default(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.last_or_default(default=-1)
    assert result == 5


def test_single(single_element_list):
    queryable = Queryable(single_element_list)
    result = queryable.single()
    assert result == 1


def test_single_or_default(single_element_list):
    queryable = Queryable(single_element_list)
    result = queryable.single_or_default(default=-1)
    assert result == 1


def test_element_at(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.element_at(index=1)
    assert result == 2


def test_element_at_or_default(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.element_at_or_default(index=3, default=-1)
    assert result == 3


def test_default_if_empty_not_empty(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.default_if_empty(default=-1)
    assert result.to_list() == [1, 2, 2, 3, 4, 5, 5]


def test_default_if_empty_empty():
    empty_list = []
    queryable = Queryable(empty_list)
    result = queryable.default_if_empty(default=-1)
    assert result.to_list() == [-1]


def test_to_dictionary():
    data = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}, {'name': 'Mike', 'age': 35}]
    queryable = Queryable(data)

    result = queryable.to_dictionary(lambda x: x['name'], lambda x: x['age'])
    expected_result = {'John': 30, 'Jane': 25, 'Mike': 35}

    assert result == expected_result
