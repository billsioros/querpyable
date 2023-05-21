import pytest

from linqpy.linqpy import Queryable


@pytest.fixture
def single_element_list():
    return [1]


@pytest.fixture
def flattened_list():
    return [1, 2, 2, 3, 4, 5, 5]


@pytest.fixture
def nested_list():
    return [[1, 2], [2, 3], [4, 5], [5]]


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
    result = queryable.any(lambda x: x > 5)
    assert result == False


def test_queryable_count(flattened_list):
    queryable = Queryable(flattened_list)
    result = queryable.count()
    assert result == 7


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
    assert result.to_list() == [1, 1, 2, 2, 3, 4, 5, 5]


def test_default_if_empty_empty():
    empty_list = []
    queryable = Queryable(empty_list)
    result = queryable.default_if_empty(default=-1)
    assert result.to_list() == [-1]
