def count_even_odd():
    numbers = input("Enter a list of numbers (comma-separated): ")
    num_list = [int(num.strip()) for num in numbers.split(',')]
    
    even_count = sum(1 for num in num_list if num % 2 == 0)
    odd_count = sum(1 for num in num_list if num % 2 != 0)
    
    print("Count of even numbers:", even_count)
    print("Count of odd numbers:", odd_count)

