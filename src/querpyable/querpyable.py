from collections.abc import Callable, Hashable, Iterable, Iterator
from itertools import chain
from typing import Optional, Protocol, Tuple, TypeVar, Union, cast

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class ComparableHashable(Hashable, Protocol):
    def __lt__(self, other: "ComparableHashable") -> bool: ...


U = TypeVar("U", bound=ComparableHashable)


class Queryable(Iterable[T]):
    def __init__(self, collection: Iterable[T]) -> None:
        """Initializes a Queryable object.

        Args:
            collection (Iterable[T]): The collection to be queried.

        Returns:
            None: This method does not return any value.

        Example:
            ```python
            # Example Usage:
            data = [1, 2, 3, 4, 5]
            queryable_data = Queryable(data)
            ```
        """
        self.collection = collection

    def __iter__(self) -> Iterator[T]:
        yield from self.collection

    @classmethod
    def range(cls, start: int, stop: Optional[int] = None, step: int = 1) -> "Queryable[int]":
        """Create a Queryable instance representing a range of integers.

        Args:
            start (int): The starting value of the range.
            stop (Optional[int]): The end value (exclusive) of the range. If None, start is considered as the stop, and start is set to 0.
            step (int): The step between each pair of consecutive values in the range. Default is 1.

        Returns:
            Queryable[int]: A Queryable instance representing the specified range of integers.

        Example:
            ```python
            result = Queryable.range(1, 5, 2)
            print(result)
            Queryable([1, 3])

            result = Queryable.range(3)
            print(result)
            Queryable([0, 1, 2])
            ```
        """
        if stop is None:
            start, stop = 0, start

        return cast(Queryable[int], cls(cast(T, i) for i in range(start, stop, step)))

    @classmethod
    def empty(cls) -> "Queryable[T]":
        """Create an empty instance of the Queryable class.

        This class method returns a new Queryable instance initialized with an empty list.

        Returns:
            Queryable[T]: A new Queryable instance with an empty list.

        Examples:
            ```python
            empty_queryable = Queryable.empty()
            print(empty_queryable)  # Output: Queryable([])
            ```
        """
        return cls([])

    def where(self, predicate: Callable[[T], bool]) -> "Queryable[T]":
        """Filters the elements of the Queryable based on a given predicate.

        Args:
            predicate (Callable[[T], bool]): A function that takes an element of the Queryable
                and returns a boolean indicating whether the element should be included in the result.

        Returns:
            Queryable[T]: A new Queryable containing the elements that satisfy the given predicate.

        Example:
            ```python
            # Create a Queryable with numbers from 1 to 5
            numbers = Queryable([1, 2, 3, 4, 5])

            # Define a predicate to filter even numbers
            def is_even(n):
                return n % 2 == 0

            # Use the 'where' method to filter even numbers
            result = numbers.where(is_even)

            # Display the result
            print(list(result))
            # Output: [2, 4]
            ```
        """
        return Queryable(item for item in self if predicate(item))

    def select(self, selector: Callable[[T], U]) -> "Queryable[U]":
        """Projects each element of the Queryable using the provided selector function.

        Args:
            selector (Callable[[T], U]): A function that maps elements of the Queryable to a new value.

        Returns:
            Queryable[U]: A new Queryable containing the results of applying the selector function to each element.

        Example:
            ```python
            # Example usage of select method
            def double(x):
                return x * 2

            data = Queryable([1, 2, 3, 4, 5])
            result = data.select(double)

            # The 'result' Queryable will contain [2, 4, 6, 8, 10]
            ```
        """
        return Queryable(selector(item) for item in self)

    def distinct(self) -> "Queryable[T]":
        """Returns a new Queryable containing distinct elements from the original
        Queryable.

        Returns:
            Queryable[T]: A new Queryable with distinct elements.

        Example:
            ```python
            data = [1, 2, 2, 3, 4, 4, 5]
            queryable_data = Queryable(data)

            distinct_queryable = queryable_data.distinct()

            # Result: Queryable([1, 2, 3, 4, 5])
            ```
        """
        return Queryable(set(self))

    def skip(self, count: int) -> "Queryable[T]":
        """Skips the specified number of elements from the beginning of the Queryable.

        Args:
            count (int): The number of elements to skip.

        Returns:
            Queryable[T]: A new Queryable object containing the remaining elements after skipping.

        Example:
            ```python
            # Create a Queryable with elements [1, 2, 3, 4, 5]
            queryable = Queryable([1, 2, 3, 4, 5])

            # Skip the first 2 elements
            result = queryable.skip(2)

            # The result should contain elements [3, 4, 5]
            assert list(result) == [3, 4, 5]
            ```
        """
        return Queryable(item for index, item in enumerate(self) if index >= count)

    def take(self, count: int) -> "Queryable[T]":
        """Returns a new Queryable containing the first 'count' elements of the current
        Queryable.

        Parameters:
        - count (int): The number of elements to take from the current Queryable.

        Returns:
        - Queryable[T]: A new Queryable containing the first 'count' elements.

        Example:
        ```python
        # Example usage of take method
        data = Queryable([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        result = data.take(3)

        print(result.to_list())  # Output: [1, 2, 3]
        ```
        """
        return Queryable(item for _, item in zip(range(count), self))

    def of_type(self, type_filter: type[U]) -> "Queryable[U]":
        """Filters the elements of the Queryable to include only items of a specific
        type.

        Args:
            type_filter (type): The type to filter the elements by.

        Returns:
            Queryable[U]: A new Queryable containing only elements of the specified type.

        Example:
            ```python
            # Create a Queryable with mixed types
            data = [1, "two", 3.0, "four", 5]

            # Create a Queryable instance
            queryable_data = Queryable(data)

            # Filter the Queryable to include only integers
            result = queryable_data.of_type(int)

            # Print the filtered result
            print(result)  # Output: Queryable([1, 5])
            ```
        """
        return Queryable(item for item in self if isinstance(item, type_filter))

    def select_many(self, selector: Callable[[T], Iterable[U]]) -> "Queryable[U]":
        """Projects each element of the sequence to an iterable and flattens the
        resulting sequences into one sequence.

        Args:
            selector (Callable[[T], Iterable[U]]): A function that transforms each element of
                the sequence into an iterable.

        Returns:
            Queryable[U]: A new Queryable instance containing the flattened sequence.

        Example:
            ```python
            # Example usage:
            def get_digits(n: int) -> Iterable[int]:
                return (int(digit) for digit in str(n))

            numbers = Queryable([123, 456, 789])
            result = numbers.select_many(get_digits)

            print(list(result))
            # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
            ```
        """

        def _() -> Iterator[U]:
            for item in self:
                yield from selector(item)

        return Queryable(_())

    def order_by(self, key_selector: Callable[[T], U]) -> "Queryable[T]":
        """Orders the elements of the Queryable based on a key selector function.

        Args:
            key_selector (Callable[[T], U]): A function that takes an element of the Queryable
                and returns a value used for sorting.

        Returns:
            Queryable[T]: A new Queryable containing the elements sorted based on the key selector.

        Example:
            ```python
            # Create a Queryable with a list of tuples
            data = Queryable([(1, "apple"), (3, "banana"), (2, "orange")])

            # Order the Queryable based on the first element of each tuple (numeric order)
            result = data.order_by(lambda x: x[0]).to_list()

            # Output: [(1, 'apple'), (2, 'orange'), (3, 'banana')]
            print(result)
            ```
        """
        return Queryable(item for item in sorted(self, key=key_selector, reverse=False))

    def order_by_descending(self, key_selector: Callable[[T], U]) -> "Queryable[T]":
        """Orders the elements of the Queryable in descending order based on the
        specified key selector.

        Args:
            key_selector (Callable[[T], U]): A function that extracts a comparable key from each element.

        Returns:
            Queryable[T]: A new Queryable with elements sorted in descending order.

        Example:
            ```python
            # Example usage of order_by_descending method
            data = [5, 2, 8, 1, 7]
            queryable_data = Queryable(data)

            # Sorting the data in descending order based on the element itself
            result = queryable_data.order_by_descending(lambda x: x)

            # Result: Queryable([8, 7, 5, 2, 1])
            ```

            ```python
            # Another example with custom key selector
            class Person:
                def __init__(self, name, age):
                    self.name = name
                    self.age = age

            people = [Person("Alice", 25), Person("Bob", 30), Person("Charlie", 22)]
            queryable_people = Queryable(people)

            # Sorting people by age in descending order
            result = queryable_people.order_by_descending(lambda person: person.age)

            # Result: Queryable([Person('Bob', 30), Person('Alice', 25), Person('Charlie', 22)])
            ```
        """
        return Queryable(item for item in sorted(self, key=key_selector, reverse=True))

    def then_by(self, key_selector: Callable[[T], U]) -> "Queryable[T]":
        """Applies a secondary sorting to the elements of the Queryable based on the
        specified key_selector.

        Args:
            key_selector (Callable[[T], U]): A function that extracts a key from each element for sorting.

        Returns:
            Queryable[T]: A new Queryable with the elements sorted first by the existing sorting criteria,
                       and then by the specified key_selector.

        Example:
            ```python
            class Person:
                def __init__(self, name, age):
                    self.name = name
                    self.age = age

            people = [
                Person("Alice", 30),
                Person("Bob", 25),
                Person("Charlie", 35),
            ]

            queryable_people = Queryable(people)

            # Sort by age in ascending order and then by name in ascending order
            sorted_people = queryable_people.order_by(lambda p: p.age).then_by(lambda p: p.name).to_list()

            # Result: [Bob(25), Alice(30), Charlie(35)]
            ```
        """
        return Queryable(item for item in sorted(self, key=key_selector, reverse=False))

    def then_by_descending(self, key_selector: Callable[[T], U]) -> "Queryable[T]":
        """Sorts the elements of the Queryable in descending order based on the
        specified key selector.

        Args:
            key_selector (Callable[[T], U]): A function that takes an element of the Queryable and
                returns a value used for sorting.

        Returns:
            Queryable[T]: A new Queryable with elements sorted in descending order based on the key selector.

        Example:
            ```python
            # Example usage of then_by_descending method
            from typing import List

            class Person:
                def __init__(self, name: str, age: int):
                    self.name = name
                    self.age = age

                def __repr__(self):
                    return f"Person(name={self.name}, age={self.age})"

            people: List[Person] = [
                Person("Alice", 30),
                Person("Bob", 25),
                Person("Charlie", 35),
            ]

            # Create a Queryable from a list of Person objects
            queryable_people = Queryable(people)

            # Sort the people by age in descending order
            sorted_people = queryable_people.then_by_descending(lambda person: person.age)

            # Display the sorted list
            print(sorted_people)
            ```
            Output:
            ```
            [Person(name=Charlie, age=35), Person(name=Alice, age=30), Person(name=Bob, age=25)]
            ```
        """
        return Queryable(item for item in sorted(self, key=key_selector, reverse=True))

    def group_join(
        self,
        inner: Iterable[U],
        outer_key_selector: Callable[[T], K],
        inner_key_selector: Callable[[U], K],
        result_selector: Callable[[T, Iterable[U]], V],
    ) -> "Queryable[V]":
        """Performs a group join operation between two sequences.

        Args:
            inner (Iterable[U]): The inner sequence to join with the outer sequence.
            outer_key_selector (Callable[[T], K]): A function to extract the key from elements in the outer sequence.
            inner_key_selector (Callable[[U], K]): A function to extract the key from elements in the inner sequence.
            result_selector (Callable[[T, Iterable[U]], V]): A function to create a result element from an outer element
                                                            and its corresponding inner elements.

        Returns:
            Queryable[V]: A new Queryable containing the result of the group join operation.

        Example:
            ```python
            # Example usage of group_join

            # Define two sequences
            outer_sequence = Queryable([1, 2, 3, 4])
            inner_sequence = Queryable([(1, 'a'), (2, 'b'), (2, 'c'), (3, 'd')])

            # Perform a group join based on the first element of each tuple
            result = outer_sequence.group_join(
                inner_sequence,
                outer_key_selector=lambda x: x,
                inner_key_selector=lambda x: x[0],
                result_selector=lambda outer, inner: (outer, list(inner))
            )

            # Display the result
            for item in result:
                print(item)

            # Output:
            # (1, [('a',)])
            # (2, [('b', 'c')])
            # (3, [('d',)])
            # (4, [])
            ```
        """

        def _() -> Iterator[V]:
            lookup = {inner_key_selector(item): item for item in inner}
            for item in self:
                key = outer_key_selector(item)
                inner_items = [lookup[key]] if key in lookup else []
                yield result_selector(item, inner_items)

        return Queryable(_())

    def zip(self, other: Iterable[U]) -> "Queryable[Tuple[T, U]]":
        """Zips the elements of the current Queryable instance with the elements of
        another iterable.

        Args:
            other (Iterable[T]): The iterable to zip with the current Queryable.

        Returns:
            Queryable[Tuple[T, U]]: A new Queryable instance containing tuples of zipped elements.

        Example:
            ```python
            queryable1 = Queryable([1, 2, 3, 4])
            queryable2 = Queryable(['a', 'b', 'c', 'd'])
            result = queryable1.zip(queryable2)

            list(result)
            [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
            ```
        """
        return Queryable(zip(self, other))

    def concat(self, other: Iterable[T]) -> "Queryable[T]":
        """Concatenates the elements of the current Queryable with the elements from
        another iterable.

        Args:
            other (Iterable[T]): Another iterable whose elements will be appended to the current Queryable.

        Returns:
            Queryable[T]: A new Queryable containing the concatenated elements.

        Example:
            ```python
            # Create a Queryable with initial elements
            queryable1 = Queryable([1, 2, 3])

            # Another iterable to concatenate
            other_iterable = [4, 5, 6]

            # Concatenate the two iterables
            result_queryable = queryable1.concat(other_iterable)

            # Result Queryable contains elements from both iterables
            assert list(result_queryable) == [1, 2, 3, 4, 5, 6]
            ```
        """
        return Queryable(chain(self, other))

    def aggregate(self, func: Callable[[T, T], T]) -> T:
        """Aggregates the elements of the sequence using a specified binary function.

        Args:
            func (Callable[[T, T], T]): A binary function that takes two elements of the
                sequence and returns a single aggregated result.

        Returns:
            T: The result of aggregating the elements using the specified function.

        Raises:
            ValueError: If the sequence is empty and cannot be aggregated.

        Example:
            ```python
            # Example 1: Aggregating a list of numbers using the addition function
            numbers = [1, 2, 3, 4, 5]
            result = aggregate(numbers, lambda x, y: x + y)
            print(result)  # Output: 15

            # Example 2: Aggregating a list of strings using the concatenation function
            words = ["Hello", " ", "World", "!"]
            result = aggregate(words, lambda x, y: x + y)
            print(result)  # Output: Hello World!
            ```
        """
        iterator = iter(self)

        try:
            result = next(iterator)
        except StopIteration:
            msg = "Sequence contains no elements."
            raise ValueError(msg)

        for item in iterator:
            result = func(result, item)

        return result

    def union(self, other: Iterable[T]) -> "Queryable[T]":
        """Returns a new Queryable containing unique elements from both sequences.

        Args:
            other (Iterable[T]): Another iterable sequence to perform the union with.

        Returns:
            Queryable[T]: A new Queryable containing unique elements from both sequences.

        Example:
            ```python
            # Example: Union of two sets of numbers
            set1 = Queryable([1, 2, 3, 4])
            set2 = [3, 4, 5, 6]
            result = set1.union(set2)
            print(result)  # Output: Queryable([1, 2, 3, 4, 5, 6])
            ```
        """
        return Queryable(set(self).union(other))

    def intersect(self, other: Iterable[T]) -> "Queryable[T]":
        """Returns a new Queryable containing common elements between two sequences.

        Args:
            other (Iterable[T]): Another iterable sequence to perform the intersection with.

        Returns:
            Queryable[T]: A new Queryable containing common elements between both sequences.

        Example:
            ```python
            # Example: Intersection of two sets of numbers
            set1 = Queryable([1, 2, 3, 4])
            set2 = [3, 4, 5, 6]
            result = set1.intersect(set2)
            print(result)  # Output: Queryable([3, 4])
            ```
        """
        return Queryable(set(self).intersection(other))

    def all(self, predicate: Callable[[T], bool]) -> bool:
        """Determines whether all elements of the sequence satisfy a given predicate.

        Args:
            predicate (Callable[[T], bool]): The predicate function to apply to each element.

        Returns:
            bool: True if all elements satisfy the predicate, False otherwise.

        Example:
            ```python
            # Example: Check if all numbers are even
            numbers = Queryable([2, 4, 6, 8])
            result = numbers.all(lambda x: x % 2 == 0)
            print(result)  # Output: True
            ```
        """
        if predicate is None:
            return all(self)

        return all(predicate(item) for item in self)

    def any(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """Determines whether any elements of the sequence satisfy a given predicate.

        Args:
            predicate (Optional[Callable[[T], bool]]): The predicate function to apply to each element.

        Returns:
            bool: True if any elements satisfy the predicate, False otherwise.

        Example:
            ```python
            # Example: Check if any numbers are odd
            numbers = Queryable([2, 4, 6, 8])
            result = numbers.any(lambda x: x % 2 != 0)
            print(result)  # Output: False
            ```
        """
        if predicate is None:
            return any(self)

        return any(predicate(item) for item in self)

    def contains(self, value: T) -> bool:
        """Determines whether the sequence contains a specific value.

        Args:
            value (T): The value to check for in the sequence.

        Returns:
            T: True if the sequence contains the value, False otherwise.

        Example:
            ```python
            # Example: Check if a list contains a specific element
            numbers = Queryable([1, 2, 3, 4])
            result = numbers.contains(3)
            print(result)  # Output: True
            ```
        """
        return value in self

    def count(self) -> int:
        """Counts the number of elements in the sequence or those satisfying a given
        predicate.

        Returns:
            int: The number of elements in the sequence or satisfying the predicate.

        Example:
            ```python
            # Example: Count the number of even numbers
            numbers = Queryable([1, 2, 3, 4, 5, 6])
            result = numbers.count()
            print(result)  # Output: 6
            ```
        """
        return sum(1 for _ in self)

    def sum(self) -> float:
        """Calculates the sum of all elements in the sequence.

        Returns:
            float: The sum of all elements in the sequence.

        Example:
            ```python
            # Example: Calculate the sum of a list of numbers
            numbers = Queryable([1, 2, 3, 4, 5])
            result = numbers.sum()
            print(result)  # Output: 15
            ```
        """
        return sum(cast(float, item) for item in self)

    def min(self) -> int:
        """Finds the minimum value among the elements in the sequence.

        Returns:
            int: The minimum value in the sequence.

        Example:
            ```python
            # Example: Find the minimum value in a list of numbers
            numbers = Queryable([3, 1, 4, 1, 5, 9, 2])
            result = numbers.min()
            print(result)  # Output: 1
            ```
        """
        return min(self)

    def max(self) -> int:
        """Finds the maximum value among the elements in the sequence.

        Returns:
            int: The maximum value in the sequence.

        Example:
            ```python
            # Example: Find the maximum value in a list of numbers
            numbers = Queryable([3, 1, 4, 1, 5, 9, 2])
            result = numbers.max()
            print(result)  # Output: 9
            ```
        ```
        ```
        """
        return max(self)

    def average(self) -> float:
        """Calculates the average of all elements in the sequence.

        Returns:
            float: The average of all elements in the sequence.

        Example:
            ```python
            # Example: Calculate the average of a list of numbers
            numbers = Queryable([1, 2, 3, 4, 5])
            result = numbers.average()
            print(result)  # Output: 3
            ```
        """
        return self.sum() / self.count()

    def except_for(self, other: Iterable[T]) -> "Queryable[T]":
        """Returns a new Queryable containing elements that are not in the specified
        sequence.

        Args:
            other (Iterable[T]): Another iterable sequence to exclude from the current sequence.

        Returns:
            Queryable[T]: A new Queryable containing elements not present in the specified sequence.

        Example:
            ```python
            # Example: Exclude common elements from two sets of numbers
            set1 = Queryable([1, 2, 3, 4])
            set2 = [3, 4, 5, 6]
            result = set1.except_for(set2)
            print(result)  # Output: Queryable([1, 2])
            ```
        """
        return Queryable(set(self).difference(other))

    def first(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        """Returns the first element of the sequence satisfying the optional predicate.

        Args:
            predicate (Optional[Callable[[T], bool]]): The optional predicate function to filter elements.

        Returns:
            T: The first element of the sequence satisfying the predicate.

        Raises:
            ValueError: If the sequence is empty or no element satisfies the predicate.

        Example:
            ```python
            # Example: Find the first even number in a list
            numbers = Queryable([1, 2, 3, 4, 5])
            result = numbers.first(lambda x: x % 2 == 0)
            print(result)  # Output: 2
            ```
        """
        if predicate is None:
            try:
                return next(iter(self))
            except StopIteration:
                msg = "Sequence contains no elements."
                raise ValueError(msg)

        for item in self:
            if predicate(item):
                return item

        msg = "Sequence contains no matching element."
        raise ValueError(msg)

    def first_or_default(
        self,
        predicate: Optional[Callable[[T], bool]] = None,
        default: Optional[T] = None,
    ) -> Optional[T]:
        """Returns the first element of the sequence satisfying the optional predicate,
        or a default value.

        Args:
            predicate (Optional[Callable[[T], bool]]): The optional predicate function to filter elements.
            default (Optional[T]): The default value to return if no element satisfies the predicate.

        Returns:
            Optional[T]: The first element of the sequence satisfying the predicate, or the default value if none found.

        Example:
            ```python
            # Example: Find the first odd number in a list or return 0 if none found
            numbers = Queryable([2, 4, 6, 8])
            result = numbers.first_or_default(lambda x: x % 2 != 0, default=0)
            print(result)  # Output: 0
            ```
        """
        if predicate is None:
            try:
                return next(iter(self))
            except StopIteration:
                return default

        for item in self:
            if predicate(item):
                return item

        return default

    def last(self, predicate: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        """Returns the last element of the sequence satisfying the optional predicate.

        Args:
            predicate (Optional[Callable[[T], bool]]): The optional predicate function to filter elements.

        Returns:
            Optional[T]: The last element of the sequence satisfying the predicate.

        Raises:
            ValueError: If the sequence is empty or no element satisfies the predicate.

        Example:
            ```python
            # Example: Find the last even number in a list
            numbers = Queryable([1, 2, 3, 4, 5])
            result = numbers.last(lambda x: x % 2 == 0)
            print(result)  # Output: 4
            ```
        """
        if predicate is None:
            try:
                result = None
                for item in self:
                    result = item
                return result
            except StopIteration:
                msg = "Sequence contains no elements."
                raise ValueError(msg)

        for item in self:
            if predicate(item):
                result = item

        if result is None:
            msg = "Sequence contains no matching element."
            raise ValueError(msg)

        return result

    def last_or_default(
        self,
        predicate: Optional[Callable[[T], bool]] = None,
        default: Optional[T] = None,
    ) -> Optional[T]:
        """Returns the last element of the sequence satisfying the optional predicate,
        or a default value.

        Args:
            predicate (Optional[Callable[[T], bool]]): The optional predicate function to filter elements.
            default (Optional[T]): The default value to return if no element satisfies the predicate.

        Returns:
            Optional[T]: The last element of the sequence satisfying the predicate, or the default value if none found.

        Example:
            ```python
            # Example: Find the last odd number in a list or return 0 if none found
            numbers = Queryable([2, 4, 6, 8])
            result = numbers.last_or_default(lambda x: x % 2 != 0, default=0)
            print(result)  # Output: 0
            ```
        """
        if predicate is None:
            try:
                result = default
                for item in self:
                    result = item
                return result
            except StopIteration:
                return default

        for item in self:
            if predicate(item):
                return item

        return default

    def single(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        """Returns the single element of the sequence satisfying the optional predicate.

        Args:
            predicate (Optional[Callable[[T], bool]]): The optional predicate function to filter elements.

        Returns:
            T: The single element of the sequence satisfying the predicate.

        Raises:
            ValueError: If the sequence is empty, contains more than one element,
                        or no element satisfies the predicate.

        Example:
            ```python
            # Example: Find the single even number in a list
            numbers = Queryable([2, 4, 6, 8])
            result = numbers.single(lambda x: x % 2 == 0)
            print(result)  # Output: 2
            ```
        """
        items = iter(self)

        if predicate is None:
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
        for item in self:
            if predicate(item):
                match_count += 1
                result = item

        if match_count == 0:
            msg = "Sequence contains no matching element."
            raise ValueError(msg)

        if match_count > 1:
            msg = "Sequence contains more than one matching element."
            raise ValueError(msg)

        return result

    def single_or_default(
        self,
        predicate: Optional[Callable[[T], bool]] = None,
        default: Optional[T] = None,
    ) -> Optional[T]:
        """Returns the single element of the sequence satisfying the optional predicate,
        or a default value if no such element is found.

        Args:
            predicate (Optional[Callable[[T], bool]]): The optional predicate function to filter elements.
            default (Optional[T]): The default value to return if no element satisfies the predicate.

        Returns:
            Optional[T]: The single element of the sequence satisfying the predicate, or the default value.

        Raises:
            ValueError: If the sequence contains more than one element satisfying the predicate.

        Example:
            ```python
            # Example: Find the single odd number in a list or return 0 if none found
            numbers = Queryable([2, 4, 6, 8])
            result = numbers.single_or_default(lambda x: x % 2 != 0, default=0)
            print(result)  # Output: 0
            ```
        """
        items = iter(self)

        if predicate is None:
            try:
                result = next(items)
                try:
                    next(items)
                    msg = "Sequence contains more than one element."
                    raise ValueError(msg)
                except StopIteration:
                    return result
            except StopIteration:
                return default

        match_count = 0
        result = default
        for item in self:
            if predicate(item):
                match_count += 1
                result = item

        if match_count > 1:
            msg = "Sequence contains more than one matching element."
            raise ValueError(msg)

        return result

    def element_at(self, index: int) -> T:
        """Returns the element at the specified index in the sequence.

        Args:
            index (int): The index of the element to retrieve.

        Returns:
            T: The element at the specified index.

        Raises:
            ValueError: If the sequence contains no element at the specified index.

        Example:
            ```python
            # Example: Get the element at index 2 in a list
            numbers = Queryable([1, 2, 3, 4, 5])
            result = numbers.element_at(2)
            print(result)  # Output: 3
            ```
        """
        try:
            return next(item for i, item in enumerate(self) if i == index)
        except StopIteration:
            msg = "Sequence contains no element at the specified index."
            raise ValueError(msg)

    def element_at_or_default(self, index: int, default: Optional[T] = None) -> Optional[T]:
        """Returns the element at the specified index in the sequence, or a default
        value if none found.

        Args:
            index (int): The index of the element to retrieve.
            default (Optional[T]): The default value to return if no element is found at the specified index.

        Returns:
            Optional[T]: The element at the specified index, or the default value if none found.

        Example:
            ```python
            # Example: Get the element at index 5 in a list or return -1 if none found
            numbers = Queryable([1, 2, 3, 4, 5])
            result = numbers.element_at_or_default(5, default=-1)
            print(result)  # Output: -1
            ```
        """
        try:
            return next(item for i, item in enumerate(self) if i == index)
        except StopIteration:
            return default

    def default_if_empty(self, default: T) -> "Queryable[T]":
        """Returns a new Queryable with a default value if the sequence is empty.

        Args:
            default (T): The default value to include in the new Queryable if the sequence is empty.

        Returns:
            Queryable[T]: A new Queryable containing the original elements or the default value.

        Example:
            ```python
            # Example: Provide a default value for an empty list
            empty_list = Queryable([])
            result = empty_list.default_if_empty(default=0).to_list()
            print(result)  # Output: [0]
            ```
        """

        def _() -> Iterator[T]:
            try:
                next(iter(self))
            except StopIteration:
                yield default
                return

            yield from self

        return Queryable(_())

    def join(
        self,
        inner: Iterable[U],
        outer_key_selector: Callable[[T], K],
        inner_key_selector: Callable[[U], K],
        result_selector: Callable[[T, U], V],
    ) -> "Queryable[V]":
        """Joins two iterables based on key selectors and applies a result selector.

        Args:
            inner (Iterable[U]): The inner iterable to join with.
            outer_key_selector (Callable[[T], K]): The key selector for the outer sequence.
            inner_key_selector (Callable[[U], K]): The key selector for the inner sequence.
            result_selector (Callable[[T, U], V]): The result selector function to apply.

        Returns:
            Queryable[T]: A new Queryable containing the joined elements based on the specified conditions.

        Example:
            ```python
            # Example: Join two sets of numbers based on common factors
            set1 = Queryable([1, 2, 3, 4])
            set2 = [3, 4, 5, 6]
            result = set1.join(set2, outer_key_selector=lambda x: x, inner_key_selector=lambda x: x % 3,
                               result_selector=lambda x, y: (x, y))
            print(result.to_list())  # Output: [(1, 4), (2, 5), (3, 6)]
            ```
        """

        def _() -> "Iterator[V]":
            lookup = {inner_key_selector(item): item for item in inner}
            for item in self:
                key = outer_key_selector(item)
                if key in lookup:
                    yield result_selector(item, lookup[key])

        return Queryable(_())

    def to_list(self) -> list[T]:
        """Converts the Queryable to a list.

        Returns:
            list[T]: A list containing all elements of the Queryable.

        Example:
            ```python
            # Example: Convert Queryable to a list
            numbers = Queryable([1, 2, 3, 4, 5])
            result = numbers.to_list()
            print(result)  # Output: [1, 2, 3, 4, 5]
            ```
        """
        return list(self)

    def to_dictionary(
        self,
        key_selector: Callable[[T], K],
        value_selector: Optional[Callable[[T], V]] = None,
    ) -> dict[K, Union[V, T]]:
        """Converts the Queryable to a dictionary using key and optional value
        selectors.

        Args:
            key_selector (Callable[[T], K]): The key selector function.
            value_selector (Optional[Callable[[T], V]]): The optional value selector function.

        Returns:
            dict[K, V]: A dictionary containing elements of the Queryable.

        Example:
            ```python
            # Example: Convert Queryable of tuples to a dictionary with the first element as the key
            pairs = Queryable([(1, 'one'), (2, 'two'), (3, 'three')])
            result = pairs.to_dictionary(key_selector=lambda x: x[0], value_selector=lambda x: x[1])
            print(result)  # Output: {1: 'one', 2: 'two', 3: 'three'}
            ```
        """
        if value_selector is None:
            return {key_selector(item): item for item in self}

        return {key_selector(item): value_selector(item) for item in self}
