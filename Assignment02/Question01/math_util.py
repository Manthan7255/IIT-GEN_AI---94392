def area_of_circle(radius):
    pi = 3.14159
    return pi * radius * radius

def area_of_rectangle(length, width):
    return length * width

def area_of_triangle(base, height):
    return 0.5 * base * height

def area_of_square(side):
    return side * side  

if __name__ == "__main__":
    # Test the functions
    print("Area of circle with radius 5:", area_of_circle(5))
    print("Area of rectangle with length 4 and width 6:", area_of_rectangle(4, 6))
    print("Area of triangle with base 3 and height 7:", area_of_triangle(3, 7))
    print("Area of square with side 4:", area_of_square(4))