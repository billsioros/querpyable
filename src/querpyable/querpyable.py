"""A Python implementation of LINQ."""

from abc import ABC, abstractmethod
from collections.abc import Callable, Generator, Iterable
from itertools import chain
from typing import Optional, TypeVar

T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")
V = TypeVar("V")


class Query(ABC):
    @abstractmethod
    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        pass


class Unary(ABC):
    @abstractmethod
    def __call__(self, source: Generator[T, None, None]) -> Generator[U, None, None]:
        pass


class Binary(ABC):
    @abstractmethod
    def __call__(
        self, source1: Generator[T, None, None], source2: Generator[U, None, None],
    ) -> Generator[T, None, None]:
        pass


class Where(Query):
    def __init__(self, predicate: Callable[[T], bool]) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        return (item for item in source if self.predicate(item))


class Select(Unary):
    def __init__(self, selector: Callable[[T], U]) -> None:
        self.selector = selector

    def __call__(self, source: Generator[T, None, None]) -> Generator[U, None, None]:
        return (self.selector(item) for item in source)


class Take(Query):
    def __init__(self, count: int) -> None:
        self.count = count

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        return (item for _, item in zip(range(self.count), source))


class Skip(Query):
    def __init__(self, count: int) -> None:
        self.count = count

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        for index, item in enumerate(source):
            if index >= self.count:
                yield item


class Distinct(Query):
    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        seen = set()
        for item in source:
            if item not in seen:
                seen.add(item)
                yield item


class SelectMany(Unary):
    def __init__(self, selector: Callable[[T], Generator[U, None, None]]) -> None:
        self.selector = selector

    def __call__(self, source: Generator[T, None, None]) -> Generator[U, None, None]:
        for item in source:
            yield from self.selector(item)


class OrderBy(Query):
    def __init__(self, key_selector: Callable[[T], U]) -> None:
        self.key_selector = key_selector

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        return (item for item in sorted(source, key=self.key_selector))


class OrderByDescending(Query):
    def __init__(self, key_selector: Callable[[T], U]) -> None:
        self.key_selector = key_selector

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        return (item for item in sorted(source, key=self.key_selector, reverse=True))


class ThenBy(Query):
    def __init__(self, key_selector: Callable[[T], U]) -> None:
        self.key_selector = key_selector

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        return (item for item in sorted(source, key=self.key_selector, reverse=False))


class ThenByDescending(Query):
    def __init__(self, key_selector: Callable[[T], U]) -> None:
        self.key_selector = key_selector

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        return (item for item in sorted(source, key=self.key_selector, reverse=True))


class Join(Binary):
    def __init__(
        self,
        inner: list[U],
        outer_key_selector: Callable[[T], K],
        inner_key_selector: Callable[[U], K],
        result_selector: Callable[[T, U], V],
    ) -> None:
        self.inner = inner
        self.outer_key_selector = outer_key_selector
        self.inner_key_selector = inner_key_selector
        self.result_selector = result_selector

    def __call__(
        self, source1: Generator[T, None, None], source2: Generator[U, None, None],
    ) -> Generator[V, None, None]:
        lookup = {self.inner_key_selector(item): item for item in self.inner}
        for item in source1:
            key = self.outer_key_selector(item)
            if key in lookup:
                yield self.result_selector(item, lookup[key])


class GroupJoin(Binary):
    def __init__(
        self,
        inner: list[U],
        outer_key_selector: Callable[[T], K],
        inner_key_selector: Callable[[U], K],
        result_selector: Callable[[T, list[U]], V],
    ) -> None:
        self.inner = inner
        self.outer_key_selector = outer_key_selector
        self.inner_key_selector = inner_key_selector
        self.result_selector = result_selector

    def __call__(
        self, source1: Generator[T, None, None], source2: Generator[U, None, None],
    ) -> Generator[V, None, None]:
        lookup = {self.inner_key_selector(item): item for item in self.inner}
        for item in source1:
            key = self.outer_key_selector(item)
            inner_items = [lookup[key]] if key in lookup else []
            yield self.result_selector(item, inner_items)


class Zip(Binary):
    def __call__(
        self, source1: Generator[T, None, None], source2: Generator[U, None, None],
    ) -> Generator[tuple[T, U], None, None]:
        return zip(source1, source2)


class All(Query):
    def __init__(self, predicate: Callable[[T], bool]) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        return all(self.predicate(item) for item in source)


class Any(Query):
    def __init__(self, predicate: Optional[Callable[[T], bool]] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        if self.predicate is None:
            return any(source)
        return any(self.predicate(item) for item in source)


class Contains(Query):
    def __init__(self, value: T) -> None:
        self.value = value

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        return self.value in source


class Count(Query):
    def __init__(self, predicate: Callable[[T], bool] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[int, None, None]:
        if self.predicate:
            return sum(1 for item in source if self.predicate(item))
        else:
            return sum(1 for _ in source)


class Sum(Query):
    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        return sum(source)


class Min(Query):
    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        return min(source)


class Max(Query):
    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        return max(source)


class Average(Query):
    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[float], None, None]:
        total = 0
        count = 0
        for item in source:
            total += item
            count += 1
        if count > 0:
            return total / count
        return None


class Aggregate(Query):
    def __init__(self, func: Callable[[T, T], T]) -> None:
        self.func = func

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        iterator = iter(source)
        try:
            result = next(iterator)
        except StopIteration:
            msg = "Sequence contains no elements."
            raise ValueError(msg)
        for item in iterator:
            result = self.func(result, item)
        return result


class Concat(Binary):
    def __call__(
        self, source1: Generator[T, None, None], source2: Generator[T, None, None],
    ) -> Generator[T, None, None]:
        yield from source1
        yield from source2


class Union(Binary):
    def __call__(
        self, source1: Generator[T, None, None], source2: Generator[T, None, None],
    ) -> Generator[T, None, None]:
        yield from set(source1).union(source2)


class Intersect(Binary):
    def __call__(
        self, source1: Generator[T, None, None], source2: Generator[T, None, None],
    ) -> Generator[T, None, None]:
        yield from set(source1).intersection(source2)


class Except(Binary):
    def __call__(
        self, source1: Generator[T, None, None], source2: Generator[T, None, None],
    ) -> Generator[T, None, None]:
        yield from set(source1).difference(source2)


class First(Query):
    def __init__(self, predicate: Optional[Callable[[T], bool]] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        if self.predicate is None:
            try:
                return next(iter(source))
            except StopIteration:
                msg = "Sequence contains no elements."
                raise ValueError(msg)
        for item in source:
            if self.predicate(item):
                return item
        msg = "Sequence contains no matching element."
        raise ValueError(msg)


class FirstOrDefault(Query):
    def __init__(
        self, predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None,
    ) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        if self.predicate is None:
            try:
                return next(iter(source))
            except StopIteration:
                return None
        for item in source:
            if self.predicate(item):
                return item
        return None


class Last(Query):
    def __init__(self, predicate: Optional[Callable[[T], bool]] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        if self.predicate is None:
            try:
                result = None
                for item in source:
                    result = item
                return result
            except StopIteration:
                msg = "Sequence contains no elements."
                raise ValueError(msg)
        for item in source:
            if self.predicate(item):
                result = item
        if result is None:
            msg = "Sequence contains no matching element."
            raise ValueError(msg)
        return result


class LastOrDefault(Query):
    def __init__(
        self, predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None,
    ) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        if self.predicate is None:
            try:
                result = None
                for item in source:
                    result = item
                return result
            except StopIteration:
                return None
        for item in source:
            if self.predicate(item):
                return item
        return None


class Single(Query):
    def __init__(self, predicate: Optional[Callable[[T], bool]] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        items = iter(source)

        if self.predicate is None:
            try:
                result = next(items)
                try:
                    next(items)
                    msg = "Sequence contains more than one element."
                    raise ValueError(msg)
                except StopIteration:
                    return result
            except StopIteration:
                msg = "Sequence contains no elements."
                raise ValueError(msg)
        match_count = 0
        result = None
        for item in source:
            if self.predicate(item):
                match_count += 1
                result = item
        if match_count == 0:
            msg = "Sequence contains no matching element."
            raise ValueError(msg)
        if match_count > 1:
            msg = "Sequence contains more than one matching element."
            raise ValueError(msg)
        return result


class SingleOrDefault(Query):
    def __init__(
        self, predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None,
    ) -> None:
        self.predicate = predicate

    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        items = iter(source)

        if self.predicate is None:
            try:
                result = next(items)
                try:
                    next(items)
                    msg = "Sequence contains more than one element."
                    raise ValueError(msg)
                except StopIteration:
                    return result
            except StopIteration:
                return None
        match_count = 0
        result = None
        for item in source:
            if self.predicate(item):
                match_count += 1
                result = item
        if match_count > 1:
            msg = "Sequence contains more than one matching element."
            raise ValueError(msg)
        return result


class ElementAt(Query):
    def __init__(self, index: int) -> None:
        self.index = index

    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        try:
            return next(item for i, item in enumerate(source) if i == self.index)
        except StopIteration:
            msg = "Sequence contains no element at the specified index."
            raise ValueError(msg)


class ElementAtOrDefault(Query):
    def __init__(self, index: int, default: Optional[T] = None) -> None:
        self.index = index

    def __call__(self, source: Generator[T, None, None]) -> Generator[Optional[T], None, None]:
        try:
            return next(item for i, item in enumerate(source) if i == self.index)
        except StopIteration:
            return None


class DefaultIfEmpty(Unary):
    def __init__(self, default_value: Optional[T] = None) -> None:
        self.default_value = default_value

    def __call__(self, source: Generator[T, None, None]) -> Generator[T, None, None]:
        try:
            first_item = next(iter(source))
        except StopIteration:
            if self.default_value is not None:
                yield self.default_value
            return
        yield first_item
        yield from source


class ToDictionary(Query):
    def __init__(
        self, key_selector: Callable[[T], K], value_selector: Optional[Callable[[T], V]] = None,
    ) -> None:
        self.key_selector = key_selector
        self.value_selector = value_selector

    def __call__(self, source: Generator[T, None, None]) -> Generator[dict[K, V], None, None]:
        if self.value_selector is None:
            return {self.key_selector(item): item for item in source}
        return {self.key_selector(item): self.value_selector(item) for item in source}


class OfType(Query):
    def __init__(self, type_filter: type[U]) -> None:
        self.type_filter = type_filter

    def __call__(self, source: Generator[T, None, None]) -> Generator[U, None, None]:
        return (item for item in source if isinstance(item, self.type_filter))


class Queryable(Iterable[T]):
    def __init__(self, collection: Iterable[T]) -> None:
        self.collection = collection

    def __call__(self) -> Generator[T, None, None]:
        return iter(self)

    def __iter__(self) -> Generator[T, None, None]:
        yield from self.collection

    @classmethod
    def range(cls, start: int, stop: int, step: int = 1) -> "Queryable":
        return cls(range(start, stop, step))

    @classmethod
    def empty() -> "Queryable":
        return cls([])

    def query(self) -> "Queryable":
        return Queryable(self)

    def where(self, predicate: Callable[[T], bool]) -> "Queryable":
        return Queryable(Where(predicate)(self))

    def select(self, selector: Callable[[T], U]) -> "Queryable":
        return Queryable(Select(selector)(self))

    def distinct(self) -> "Queryable":
        return Queryable(Distinct()(self))

    def skip(self, count: int) -> "Queryable":
        return Queryable(Skip(count)(self))

    def take(self, count: int) -> "Queryable":
        return Queryable(Take(count)(self))

    def of_type(self, type_filter: type[U]) -> "Queryable":
        return Queryable(OfType(type_filter)(self))

    def select_many(self, selector: Callable[[T], Iterable[U]]) -> "Queryable":
        return Queryable(SelectMany(selector)(self))

    def order_by(self, key_selector: Callable[[T], U]) -> "Queryable":
        return Queryable(OrderBy(key_selector)(self))

    def order_by_descending(self, key_selector: Callable[[T], U]) -> "Queryable":
        return Queryable(OrderByDescending(key_selector)(self))

    def then_by(self, key_selector: Callable[[T], U]) -> "Queryable":
        return Queryable(ThenBy(key_selector)(self))

    def then_by_descending(self, key_selector: Callable[[T], U]) -> "Queryable":
        return Queryable(ThenByDescending(key_selector)(self))

    def concat(self, other: Iterable[T]) -> "Queryable[T]":
        return Queryable(chain(self, other))

    def aggregate(self, func: Callable[[T, T], T]) -> T:
        return Queryable(Aggregate(func)(self))

    def union(self, other: Iterable[T]) -> "Queryable[T]":
        return Queryable(Union()(self, other))

    def intersect(self, other: Iterable[T]) -> "Queryable[T]":
        return Queryable(Intersect()(self, other))

    def all(self, predicate: Callable[[T], bool]) -> bool:
        return All(predicate)(self)

    def any(self, predicate: Callable[[T], bool] = None) -> bool:
        return Any(predicate)(self)

    def count(self, predicate: Callable[[T], bool] = None) -> int:
        return Count(predicate)(self)

    def except_for(self, other: Iterable[T]) -> "Queryable[T]":
        return Queryable(Except()(self, other))

    def first(self, predicate: Callable[[T], bool] = None) -> T:
        return First(predicate)(self)

    def first_or_default(
        self, predicate: Callable[[T], bool] = None, default: Optional[T] = None,
    ) -> T:
        return FirstOrDefault(predicate, default)(self)

    def last(self, predicate: Callable[[T], bool] = None) -> T:
        return Last(predicate)(self)

    def last_or_default(
        self, predicate: Callable[[T], bool] = None, default: Optional[T] = None,
    ) -> T:
        return LastOrDefault(predicate, default)(self)

    def single(self, predicate: Callable[[T], bool] = None) -> T:
        return Single(predicate)(self)

    def single_or_default(
        self, predicate: Callable[[T], bool] = None, default: Optional[T] = None,
    ) -> T:
        return SingleOrDefault(predicate, default)(self)

    def element_at(self, index: int) -> T:
        return ElementAt(index)(self)

    def element_at_or_default(self, index: int, default: Optional[T] = None) -> T:
        return ElementAtOrDefault(index, default)(self)

    def default_if_empty(self, default: T) -> "Queryable[T]":
        query = DefaultIfEmpty(default)
        return Queryable(query(self))

    def join(
        self,
        inner: list[U],
        outer_key_selector: Callable[[T], K],
        inner_key_selector: Callable[[U], K],
        result_selector: Callable[[T, U], V],
    ) -> "Queryable":
        return Queryable(
            Join(inner, outer_key_selector, inner_key_selector, result_selector)(self, inner),
        )

    def to_list(self) -> list[T]:
        return list(self)
