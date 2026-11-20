# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Loops and conditionals — Python practice
#
# Practise repeating actions, counting and making decisions in Python.
# No packages, files or setup code are needed.
#
# Run each example and read the output. Predict what will happen when you
# change it, then try the exercise. Use the self-check section at the end
# after attempting the exercises. If an output differs, compare the colon,
# indentation, numbers and condition carefully.

# %% [markdown]
# ## 1. Repeat an action with a for loop
#
# A `for` loop runs its indented instructions once for each item. Here the
# items are three colours. On the first pass, `colour` is `red`; on the next,
# it is `green`, then `blue`.

# %% tags=["example"]
# It's common in python to try to make your for loops human readable
# In this case, the object `colour` takes its value from the list of colours.

for colour in ["red", "green", "blue"]:
    print(colour)

# %% [markdown]
# The colon starts the loop body. The indentation puts `print()` inside it. `colour` is a variable name we choose; it refers to one item at a time.

# %% [markdown]
# **Exercise 1.** Loop over the names Aisha, Ben and Chen. Print a greeting for each, such as `Hello Aisha`. Use `print('Hello', name)` inside the loop.

# %% exercise=1 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 2. Count up with range
#
# `range(1, 6)` supplies 1, 2, 3, 4 and 5. The start is included; the stop
# value is **not**. A loop lets us use each number in turn.

# %% tags=["example"]
import time # This is used for the pausing below

for loop_iteration in range(1,6):
    print("This is iteration number:", loop_iteration)
    time.sleep(1) # This pauses the computer for 1 . This helps illustrate what's happening. Each loop is an indepdendent chunk of code being run.

# %% [markdown]
# With one argument, `range(3)` starts at zero and supplies 0, 1 and 2. It gives three values, not the numbers 1 to 3.

# %% [markdown]
# **Exercise 2.** Print the numbers 1 to 10, with one number on each line. Which stop value do you need? Note: you do *not* need to pause the count.

# %% exercise=2 tags=["student-task"]
# Write your code here.

# %% [markdown]
# **Exercise 3.** Print `Hello` three times using `range(3)`. You do not have to print the loop variable.

# %% exercise=3 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 3. Count down
#
# `range(start, stop, step)` has a third argument for the size and direction
# of each step. A step of `-1` moves down by one.

# %% tags=["example"]
for number in range(5, 0, -1):
    print(number)
print("Go!")

# %% [markdown]
# This prints 5 down to 1, then `Go!`. Zero is excluded. The final print is not indented, so it runs once after the loop has finished.

# %% [markdown]
# **Exercise 4.** Print a countdown from 10 to 1, followed by `Finished` once. Keep the final print outside the loop.

# %% exercise=4 tags=["student-task"]
# Write your code here.

# %% [markdown]
# **Exercise 5.** Print the numbers 5 down to 0, including zero. Change the stop value so that zero is reached before the loop stops.

# %% exercise=5 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 4. Test a condition
#
# A comparison produces `True` or `False`.
#
# | Comparison | Meaning |
# |---|---|
# | `==` | equal to |
# | `!=` | not equal to |
# | `>` | greater than |
# | `<` | less than |
# | `>=` | greater than or equal to |
# | `<=` | less than or equal to |

# %% tags=["example"]
print(4 > 2)
print(4 == 2)
print(4 != 2)

# %% [markdown]
# Remember: `number = 4` assigns a value. `number == 4` tests whether the current value equals 4.

# %% [markdown]
# **Exercise 6.** Predict each result, then print these three comparisons: `8 >= 8`, `3 < 1`, and `'blue' == 'green'`.

# %% exercise=6 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 5. Run an instruction only if a condition is true
#
# The instruction under `if` runs only when its condition is true. A false
# condition skips that instruction. It does not stop the rest of the program.

# %% tags=["example"]
number = 7
if number > 5:
    print("Greater than five")
print("Finished checking")

# %% [markdown]
# Change `number` to 3 and run the cell again. The final message still appears because its print is outside the if block.

# %% [markdown]
# **Exercise 7.** Set `temperature = 12`. Print `Cold` only if temperature is below 15. Then try 20. Should anything print in that case?

# %% exercise=7 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 6. Choose between two actions with else
#
# `else` gives an alternative when the condition is false. Exactly one of
# these two messages is printed. The if and else lines have the same indentation.

# %% tags=["example"]
number = 4
if number >= 5:
    print("Five or more")
else:
    print("Below five")

# %% [markdown]
# **Exercise 8.** Set `stock = 0`. If stock is greater than zero, print `Available`; otherwise print `Sold out`. Try stock values 0 and 3.

# %% exercise=8 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 7. Choose between more than two actions with elif
#
# `elif` means 'otherwise, if'. Python checks conditions from top to bottom
# and runs the first matching branch. `else` handles what remains.

# %% tags=["example"]
number = 0
if number > 0:
    print("Positive")
elif number < 0:
    print("Negative")
else:
    print("Zero")

# %% [markdown]
# **Exercise 9.** Write the same test, starting with `number = -4`. Then try 0 and 8. Make sure every value prints exactly one message.

# %% exercise=9 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 8. Test each number inside a loop
#
# A loop visits every item; an if decides what to do with the current one.
# Here the if is indented inside the loop, and the print is indented inside
# the if. Only numbers that pass the test are printed.

# %% tags=["example"]
for number in range(1, 6):
    if number > 3:
        print(number)

# %% [markdown]
# **Exercise 10.** Visit the numbers 1 to 10. Print only those greater than or equal to 5. The loop should still visit all ten numbers.

# %% exercise=10 tags=["student-task"]
# Write your code here.

# %% [markdown]
# **Exercise 11.** Count down from 3 to 1. Print `Last one!` instead of the number when it equals 1. Use if/else inside the loop.

# %% exercise=11 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 9. Count how many items pass a test
#
# Printing a value does not keep a running count. Start a counter at zero
# **before** the loop. Add one only when an item passes the condition.

# %% tags=["example"]
count = 0
for number in [2, 7, 4, 9]:
    if number > 5:
        count = count + 1
print(count)

# %% [markdown]
# Two values pass, so the counter ends at 2. `count = count + 1` reads the old value, adds one, and stores the new value. Resetting count inside the loop would lose earlier progress.

# %% [markdown]
# **Exercise 12.** Count how many values in `[-3, 4, 0, -1, 8]` are negative. Print the final count once, after the loop.

# %% exercise=12 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 10. Add values to a running total
#
# A counter adds one per item. A total adds the value of the item itself.
# Start the total before the loop and print it after the loop.

# %% tags=["example"]
total = 0
for number in range(1, 6):
    total = total + number
print(total)

# %% [markdown]
# **Exercise 13.** Add the numbers 1 to 10 with a loop and print the final total. Explain why `total = total + number` is different from `total = total + 1`.

# %% exercise=13 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## 11. Fix the indentation
#
# This code is intended to print `Start` three times and `Done` once,
# but Done is currently inside the loop:
#
# ```python
# for number in range(3):
#     print("Start")
#     print("Done")
# ```

# %% [markdown]
# **Exercise 14.** Copy the code and change only the indentation to get the intended result. How many lines would the original code print?

# %% exercise=14 tags=["student-task"]
# Write your code here.

# %% [markdown]
# ## Before checking your work
#
# Can you explain:
#
# - Which values a range supplies, including its final value?
# - Which instructions repeat, and which run once afterwards?
# - Why a false condition can correctly produce no output?
# - The difference between printing, counting and adding values?

# %% [markdown]
# ## Self-check answers
#
# Compare your code and output after trying each exercise. Different variable names can be equally correct.

# %% [markdown]
# ### Exercise 1
#
# ```python
# for name in ['Aisha', 'Ben', 'Chen']:
#     print('Hello', name)
# ```
#
# Expected output:
#
# ```text
# Hello Aisha
# Hello Ben
# Hello Chen
# ```
#
# The same instruction runs three times. print adds a space between the two values.

# %% [markdown]
# ### Exercise 2
#
# ```python
# for number in range(1, 11):
#     print(number)
# ```
#
# Expected output:
#
# ```text
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
# ```
#
# Use 11 as the stop because that value is excluded.

# %% [markdown]
# ### Exercise 3
#
# ```python
# for number in range(3):
#     print('Hello')
# ```
#
# Expected output:
#
# ```text
# Hello
# Hello
# Hello
# ```
#
# The loop takes three passes. Its body can print a fixed message rather than the current number.

# %% [markdown]
# ### Exercise 4
#
# ```python
# for number in range(10, 0, -1):
#     print(number)
# print('Finished')
# ```
#
# Expected output:
#
# ```text
# 10
# 9
# 8
# 7
# 6
# 5
# 4
# 3
# 2
# 1
# Finished
# ```
#
# Indenting the final print would repeat Finished on every pass.

# %% [markdown]
# ### Exercise 5
#
# ```python
# for number in range(5, -1, -1):
#     print(number)
# ```
#
# Expected output:
#
# ```text
# 5
# 4
# 3
# 2
# 1
# 0
# ```
#
# The stop is -1. That value is excluded, so zero is the final value printed.

# %% [markdown]
# ### Exercise 6
#
# ```python
# print(8 >= 8)
# print(3 < 1)
# print('blue' == 'green')
# ```
#
# Expected output:
#
# ```text
# True
# False
# False
# ```
#
# Equality is included in >=. Strings can also be compared for equality.

# %% [markdown]
# ### Exercise 7
#
# ```python
# temperature = 12
# if temperature < 15:
#     print('Cold')
# ```
#
# Expected output:
#
# ```text
# Cold
# ```
#
# At 12 the condition is true. At 20 it is false, so this program prints nothing. No output is the intended result for that case.

# %% [markdown]
# ### Exercise 8
#
# ```python
# stock = 0
# if stock > 0:
#     print('Available')
# else:
#     print('Sold out')
# ```
#
# Expected output:
#
# ```text
# Sold out
# ```
#
# Zero takes the else branch. Changing stock to 3 prints Available.

# %% [markdown]
# ### Exercise 9
#
# ```python
# number = -4
# if number > 0:
#     print('Positive')
# elif number < 0:
#     print('Negative')
# else:
#     print('Zero')
# ```
#
# Expected output:
#
# ```text
# Negative
# ```
#
# The three cases print Negative, Zero and Positive respectively. Once a branch matches, the remaining branches are skipped.

# %% [markdown]
# ### Exercise 10
#
# ```python
# for number in range(1, 11):
#     if number >= 5:
#         print(number)
# ```
#
# Expected output:
#
# ```text
# 5
# 6
# 7
# 8
# 9
# 10
# ```
#
# The condition selects what gets printed; it does not change the values supplied by range.

# %% [markdown]
# ### Exercise 11
#
# ```python
# for number in range(3, 0, -1):
#     if number == 1:
#         print('Last one!')
#     else:
#         print(number)
# ```
#
# Expected output:
#
# ```text
# 3
# 2
# Last one!
# ```
#
# Every pass takes one branch. The last pass prints the message instead of printing 1.

# %% [markdown]
# ### Exercise 12
#
# ```python
# count = 0
# for number in [-3, 4, 0, -1, 8]:
#     if number < 0:
#         count = count + 1
# print(count)
# ```
#
# Expected output:
#
# ```text
# 2
# ```
#
# Only -3 and -1 pass. Zero is neither negative nor positive.

# %% [markdown]
# ### Exercise 13
#
# ```python
# total = 0
# for number in range(1, 11):
#     total = total + number
# print(total)
# ```
#
# Expected output:
#
# ```text
# 55
# ```
#
# Adding number produces 1 + 2 + ... + 10. Adding 1 ten times would count the items and finish at 10.

# %% [markdown]
# ### Exercise 14
#
# ```python
# for number in range(3):
#     print('Start')
# print('Done')
# ```
#
# Expected output:
#
# ```text
# Start
# Start
# Start
# Done
# ```
#
# The original prints six lines: Start and Done on each of three passes. Moving Done outside the loop makes it print once at the end.
