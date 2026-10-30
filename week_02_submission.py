from functools import wraps

# SAMPLE DATA
records = [
    ("ST01", "Python"),
    ("ST02", "HTML"),
    ("ST01", "Python"),
    ("ST03", "CSS"),
    ("ST02", "HTML"),
    ("ST01", "JavaScript"),
    ("ST03", "CSS"),
    ("ST01", "Python"),
]

# QUEST 1: WRITTEN EXPLANATIONS
"""
A. FUNCTION NAMES: 
`analyze_records` processes the records list and returns the total student counts, 
total activity counts, and identifies the most active student ID.

B. DATA STRUCTURES:
Dictionaries are used to tally the student IDs and activity names because:
1. They store data in key-value pairs, making it easy to associate an ID with its count.
2. Dictionary lookups have an expected time complexity of O(1), making updates extremely fast.

C. OUTPUT SHAPE:
The function returns a Tuple: (dict, dict, str).
A tuple is used because the function must return multiple different pieces of data 
(two tally dictionaries and one winning string ID) in a fixed, immutable sequence.

EXPLAIN: DICTIONARY UPDATE
When the code runs `student_counts.get(id, 0) + 1`:
1. It checks if the `id` (e.g., "ST01") already exists as a key.
2. If it does, it retrieves the current count, adds 1, and updates the key.
3. If it does NOT exist, `.get()` returns the default value of 0, adds 1, and creates the new key. 
This prevents a KeyError when encountering a student or activity for the first time.
"""

# DECORATOR & MAIN ANALYZER
def track_calls(f):
    total = 0
    @wraps(f) 
    def wrapper(*args, **kwargs):
        nonlocal total 
        total += 1
        print(f"call no: {total}")
        return f(*args, **kwargs)
    return wrapper

@track_calls
def analyze_records(records):
    student_counts = {}
    activity_counts = {}
    for id, activity in records:
        student_counts[id] = student_counts.get(id, 0) + 1
        activity_counts[activity] = activity_counts.get(activity, 0) + 1

    most_active_id, most_count = None, 0
    for id, count in student_counts.items():
        # Tie-breaking rule: if counts are equal, pick the lexicographically smaller ID
        if count > most_count or (count == most_count and (most_active_id is None or id < most_active_id)):
            most_active_id, most_count = id, count

    return student_counts, activity_counts, most_active_id


# QUEST 3: RECURSION EXPLANATION
"""
BASE CASE: 
`if not records: return 0`
The recursion stops when the list is empty, returning a count of 0.

RECURSIVE CALL: 
`count_student_records(records[1:], student_id)`
The function calls itself with a sliced version of the list (`records[1:]`), 
processing the next item while shrinking the list by one element each time.
"""

def count_student_records(records, student_id):
    if not records:
        return 0
    id = records[0][0]
    return 1 + count_student_records(records[1:], student_id) if id == student_id else 0 + count_student_records(records[1:], student_id)




# QUEST 6 & FINAL REFLECTION
"""
QUEST 6 — Defend your Big O analysis
A. Main analyzer: Expected time complexity is O(N). It loops through the N records once (O(N)), 
   doing O(1) dictionary updates. It then loops through the U unique students to find the max (O(U)). 
   Since U <= N, this simplifies to O(N).
B. Extra space: Memory use is proportional to O(U + A), where U is unique student IDs and A is 
   unique activity names, because the dictionaries only store one entry per unique item regardless 
   of how large the records list grows.
C. Recursive counter: Time complexity is O(N^2) because list slicing `records[1:]` creates a new 
   list copy at every step (taking O(K) time per step). The auxiliary space complexity is O(N) 
   because each recursive call adds a new frame to the call stack until the list is empty.
D. Hash map caveat: Dictionary operations are expected O(1) because elements are distributed via 
   a hash function. However, if a severe collision occurs (multiple keys hashing to the same bucket), 
   Python must search that specific bucket, which degrades performance to O(N) worst-case.

FINAL REFLECTION
The part I had to think hardest about was... 
determining how to maintain a persistent count inside the decorator without using global variables, 
which required understanding closures and the `nonlocal` keyword.

A Python behavior I understand better now is... 
None, tbh. it could have been how learning decorators and closures but I havent mastered it yet. 
if it there is one thing I now understand is the `functool` and `@wraps` for proper metadata

A bug I found and how I fixed it... 
the `@wraps` decorator inside my `track_calls` wrapper threw a TypeError because I forgot to 
pass the original function to it. I fixed it by changing `@wraps` to `@wraps(f)`.

If the records grew to one million entries, I would reconsider... 
the recursive `count_student_records` function. Python would hit its maximum recursion depth 
limit and crash with a RecursionError. I would replace it with an iterative loop and remove the list slicing.
"""