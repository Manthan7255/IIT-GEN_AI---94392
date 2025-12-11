# Count Even and Odd Numbers

# Take a list of numbers as input (comma-separated).

# Count how many are even and how many are odd.

# Print results.

# Example Input:
# 10, 21, 4, 7, 8

def count_even_odd():
    numbers = input("Enter a list of numbers (comma-separated): ")
    num_list = [int(num.strip()) for num in numbers.split(',')]
    
    even_count = sum(1 for num in num_list if num % 2 == 0)
    odd_count = sum(1 for num in num_list if num % 2 != 0)
    
    print("Count of even numbers:", even_count)
    print("Count of odd numbers:", odd_count)

