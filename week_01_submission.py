# ELITE BEGINNER CHALLENGE - submission


# QUEST 1 - recursion

# A. trace total(4)
# calls in the order they start: total(4) -> total(3) -> total(2) -> total(1)
# total(4) is not the base case, so it needs 4 + total(3) and waits for it.
# total(3) waits on total(2), and total(2) waits on total(1).
# total(1) hits the base case (n == 1) and returns 1.
# unwinding: total(2) = 2 + 1 = 3, total(3) = 3 + 3 = 6, total(4) = 4 + 6 = 10
# final return value: 10

# B. total(0) and total(-3)
# n never equals 1, so n goes 0, -1, -2, ... and the function keeps calling itself.
# python stops it after about 1000 calls and raises RecursionError.
# the fix is to handle bad inputs before the recursion starts, not to change the base case.
# non-integer input (like 2.5) raises TypeError, bool is rejected too, because
# isinstance(True, int) is True in python.
def total(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must not be negative")
    if n == 0 or n == 1:
        return n
    return n + total(n - 1)



# C. termination
# the base case is where the recursion stops: it returns an answer without calling itself.
# the recursive case is where the function calls itself on a smaller input (n - 1).
# every call must make the input smaller so the chain of calls is finite and reaches the base case.
#  every unfinished call keeps a frame on the call stack. if the base case is never
# reached, frames pile up until the stack is full and python raises RecursionError.


# D. countdown_sum: sum of odd positive integers from n down to 1
def countdown_sum(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n <= 0:
        return 0
    current = n if n % 2 != 0 else n - 1
    return current + countdown_sum(current - 1)


assert countdown_sum(5) == 9  # 5 + 3 + 1
assert countdown_sum(4) == 4  # 3 + 1
assert countdown_sum(1) == 1
assert countdown_sum(0) == 0  # edge case


# QUEST 2 - big O

# A. analyze
# has_duplicate_a: time O(n^2), space O(1).
#   the outer loop runs n times and the inner loop up to n-1 times, and the comparison
#   items[i] == items[j] runs on every pair: n(n-1)/2 comparisons with no duplicate.
#   space is O(1) because i and j are a fixed number of variables that don't grow with n
#   (range() is lazy, it doesn't build a list).
# has_duplicate_b: time O(n) expected, space O(n).
#   one loop of n iterations, each doing one `in seen` check and one seen.add(item).
#   seen is a set that grows by one element per item, so it holds up to n elements.
#   "expected" because set operations are O(1) on average, but heavy collisions can
#   push one operation toward O(n) and the worst case toward O(n^2).
# has_duplicate_c: time O(n log n), space O(n).
#   sorted() costs O(n log n), the loop after it is O(n), together O(n log n).
#   sorted() returns a brand new list of n items, so space is O(n).
#   with .sort() instead: O(1) auxiliary space in practice (timsort uses some temp
#   buffer), time still O(n log n), but it mutates the caller's list.

# B. predict before running
# a and b can return early on the list whose first two values are equal
# (a at the very first comparison, b at the second item).
# c can't return early, it has to sort the whole list before the loop starts.
# on 10,000 distinct integers, a does the most work:
# about 50 million comparisons, vs 10,000 lookups for b and about 130,000 comparisons
# in the sort for c.
# big O is not an exact stopwatch: it describes how cost grows with n, and ignores
# constants, lower-order terms and hardware. so an O(n) function with a heavy
# per-step cost can lose to an O(n^2) one on small inputs.

# C. the misconception ("b is O(1) because set membership is O(1)")
# it ignores whether you're looking up one thing or n things.
# a single `in seen` check is O(1) expected, but has_duplicate_b runs it once
# per item inside a loop of n iterations: n iterations x O(1) per iteration = O(n) total.
# the student measured the cost of one step and called it the cost of the whole function.

# D. engineering choice for millions of records
# default pick: b. it's the fastest, O(n) expected, and can exit early on a duplicate.
# its cost is O(n) memory for the set, which is fine for millions of ints.
# c with sorted() is O(n log n) and also O(n) memory, so it's strictly worse than b.
# c with .sort() is O(1) auxiliary space, so it wins when memory is tight, but it
# mutates the caller's list (or you copy first and you're back to O(n) space).
# c also has a guaranteed O(n log n) with no hashing, so heavy hash collisions
# can't hurt it. collisions push b toward O(n^2) in the worst case.
# never a: O(n^2) on millions of records is unusable.


# QUEST 3 - hashing and hash maps

def hash_key(key):
    return sum(ord(char) for char in key) % 7


# A. calculate
# 'cat': 99 + 97 + 116 = 312, 312 % 7 = 4
# 'act': 97 + 99 + 116 = 312, 312 % 7 = 4
# 'dog': 100 + 111 + 103 = 314, 314 % 7 = 6
# 'god': 103 + 111 + 100 = 314, 314 % 7 = 6

# B. collisions
# a collision is two different keys landing in the same slot.
# 'cat' and 'act' collide in slot 4, 'dog' and 'god' collide in slot 6.
# different strings can map to the same index because the hash function squeezes
# unlimited possible keys into only 7 slots. this one sums character codes, and
# addition ignores order, so anagrams always collide.
# a matching index doesn't prove two keys are equal. the hash function only groups
# keys into buckets, the index only says which bucket to search.
# example: if slot 4 holds ('cat', 1) and you call get('act'), the hash sends
# you to slot 4, but trusting the index alone would return cat's value. so you scan
# the bucket and compare each stored key to 'act' with ==.


# C. implement (separate chaining, 7 slots, no dict or set)
class HashMap:
    def __init__(self):
        self.buckets = [[], [], [], [], [], [], []]

    # put: compute the index, scan that bucket comparing keys with ==,
    # replace the pair if the key matches and stop, otherwise append (key, value).
    def put(self, key, value):
        bucket = self.buckets[hash_key(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)  # tuples can't be edited, so replace the pair
                return
        bucket.append((key, value))

    # get: compute the index, scan that bucket comparing keys with ==,
    # return the value on a match. None goes after the loop, so one
    # non-matching pair doesn't end the search early.
    def get(self, key):
        bucket = self.buckets[hash_key(key)]
        for stored_key, stored_value in bucket:
            if stored_key == key:
                return stored_value
        return None

    # delete: compute the index, scan that bucket, remove only the one pair whose
    # key matches. other pairs in the same bucket stay (delete('cat') must not
    # touch 'act'). missing key: do nothing and return False.
    def delete(self, key):
        bucket = self.buckets[hash_key(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                return True
        return False



# D. analyze
# expected time for put/get/delete is O(1) under reasonable hashing assumptions
# (keys spread roughly evenly, few keys per bucket).
# worst case is O(n) when every key lands in one bucket, because that bucket is
# just a list you scan.
# a bigger table spreads keys over more buckets, so on average each bucket holds
# fewer keys and scans are shorter.
# it doesn't guarantee O(1) because it's only an average: the hash function
# still decides where keys go ('cat' and 'act' collide whether there are 7 slots
# or 7,000, since their sums are identical), and clustered keys can still overload
# one bucket.


# QUEST 4 - decorators

# A. predict output (exact order)
# Decorator is running
# Program started
# Before function
# Multiplying
# After function
# Answer: 12
# "Decorator is running" prints before "Program started" because @announce above
# multiply means multiply = announce(multiply). that runs the moment python reaches
# the def multiply line, so announce's body (and its first print) runs right then.
# print("Program started") is further down the file and hasn't run yet.

# B. explain the parts
# @announce is the same as multiply = announce(multiply): it replaces multiply
# with whatever announce returns.
# wrapper wraps extra behavior around the original function.
# *args and **kwargs: the wrapper doesn't know in advance what arguments the
# original takes, so *args collects any positional ones and **kwargs any keyword ones,
# and func(*args, **kwargs) passes them on unchanged. one wrapper works for any function.
# two different returns: `return wrapper` (in announce) hands back the new
# function that replaces multiply. `return result` (in wrapper) hands the original
# function's answer (12) back to whoever called multiply(3, 4).

# C. repair a bug
# if wrapper calls func(*args, **kwargs) but doesn't return the result, the
# wrapper function ends with nothing, and a function that ends with nothing gives
# back None. so answer becomes None. the fix is `return result` at the end of wrapper.
def announce(func):
    print("Decorator is running")

    def wrapper(*args, **kwargs):
        print("Before function")
        result = func(*args, **kwargs)
        print("After function")
        return result

    return wrapper


@announce
def multiply(a, b):
    print("Multiplying")
    return a * b


print("Program started")
answer = multiply(3, 4)
print("Answer:", answer)


# D. count_calls
# the counter can't be created inside wrapper: that would be a fresh local on
# every call, starting from 0 each time, so we never get past 1.
# it has to live outside the per-call scope. here it's an attribute on wrapper.
def count_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


@count_calls
def add(a, b):
    return a + b


print(add(1, 2))   # 3
print(add(3, 4))   # 7
print(add(5, 6))   # 11
print("calls:", add.calls)  # calls: 3
assert add.calls == 3


# QUEST 5 - reflection and debugging

# hardest concept: hash maps.
# first incorrect assumption: i thought a collision meant two keys having the same
# value. it actually means two different keys landing in the same slot.
# evidence that changed my mind: 'cat' and 'act' are different strings, but both
# sum to 312, and 312 % 7 = 4, so both go to slot 4.
# a test that would catch the same mistake: put 'cat', then call get('act').
# it must return None even though both keys are in slot 4.
# edge case: get('act') after only put('cat', 1).
# predicted output: None.
# why it's correct: get scans the bucket and compares each stored key to 'act' with ==,
# and 'cat' != 'act', so nothing matches and it returns None.
m2 = HashMap()
m2.put("cat", 1)
assert hash_key("cat") == hash_key("act")
assert m2.get("act") is None