import pytest

from linqpy import Queryable


@pytest.fixture
def sample_data():
    # Sample data for testing
    return [1, 2, 2, 3, 4, 5, 5]


def test_queryable_where(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.where(lambda x: x > 2).to_list()
    assert result == [3, 4, 5, 5]


def test_queryable_select(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.select(lambda x: x * 2).to_list()
    assert result == [2, 4, 4, 6, 8, 10, 10]


def test_queryable_distinct(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.distinct().to_list()
    assert result == [1, 2, 3, 4, 5]


def test_queryable_skip(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.skip(2).to_list()
    assert result == [2, 3, 4, 5, 5]


def test_queryable_take(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.take(3).to_list()
    assert result == [1, 2, 2]


def test_queryable_of_type(sample_data):
    mixed_data = sample_data + ['a', 'b', 'c']
    queryable = Queryable(mixed_data)
    result = queryable.of_type(int).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5]


def test_queryable_select_many(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.select_many(lambda x: [x, x + 1]).to_list()
    assert result == [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]


def test_queryable_order_by(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.order_by(lambda x: x).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5]


def test_queryable_order_by_descending(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.order_by_descending(lambda x: x).to_list()
    assert result == [5, 5, 4, 3, 2, 2, 1]


def test_queryable_then_by(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.order_by(lambda x: x).then_by(lambda x: -x).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5]


def test_queryable_then_by_descending(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.order_by(lambda x: x).then_by_descending(lambda x: x).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5]


def test_queryable_join(sample_data):
    inner_data = [1, 3, 5, 7, 9]
    queryable = Queryable(sample_data)
    result = queryable.join(inner_data, lambda x: x, lambda x: x, lambda x, y: x * y).to_list()
    assert result == [1, 9, 25, 49, 81]


def test_queryable_concat(sample_data):
    queryable1 = Queryable(sample_data)
    queryable2 = Queryable([6, 7, 7, 8])
    result = queryable1.concat(queryable2).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 5, 6, 7, 7, 8]


def test_queryable_union(sample_data):
    queryable1 = Queryable(sample_data)
    queryable2 = Queryable([5, 6, 7, 7, 8])
    result = queryable1.union(queryable2).to_list()
    assert result == [1, 2, 2, 3, 4, 5, 6, 7, 8]


def test_queryable_intersect(sample_data):
    queryable1 = Queryable(sample_data)
    queryable2 = Queryable([3, 4, 5, 6, 6])
    result = queryable1.intersect(queryable2).to_list()
    assert result == [3, 4, 5]


def test_queryable_except(sample_data):
    queryable1 = Queryable(sample_data)
    queryable2 = Queryable([2, 3, 6, 6])
    result = queryable1.except_(queryable2).to_list()
    assert result == [1, 4, 5, 5]


def test_queryable_all(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.all(lambda x: x > 0)
    assert result == True


def test_queryable_any(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.any(lambda x: x > 5)
    assert result == True


def test_queryable_count(sample_data):
    queryable = Queryable(sample_data)
    result = queryable.count()
    assert result == 7
