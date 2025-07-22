import math
class Vector:
    """A class representing a mathematical vector."""
    
    # Exercise 1: The __init__ method is a dunder method that is called when an instance of the class is created.    
    
    def __init__(self, data):
        """
        Initializes a Vector instance with a list of numbers.

        Parameters:
            data (list of int or float): The list of numbers to initialize the vector.

        Raises:
            ValueError: If data is not a list.
            ValueError: If any element in data is not an integer or float.
        """
        if not isinstance(data, list): raise ValueError("Data must be a list")
        if not all(isinstance(x, (int, float)) for x in data):
            raise ValueError("All elements in the list must be integers or floats")
        self._vector = data.copy()
    
    # Exercise 2: Another very useful method to write is __str__. This dunder method will enable us to print the content of the instance using the print function.     
    
    def __str__(self):
        """
        Returns a string representation of the vector in angle brackets, with elements separated by commas.
        """
        return (f"<{', '.join([str(item) for item in self._vector])}>")
    
    # Exercise 3: Implement the method dim() that returns the dimension of a vector (i.e. the number of values in a vector)
    
    def dim(self):
        """Returns the dimension of the vector."""
        return len(self._vector)
    
    #Exercise 4: Implement the following accessor and mutator:
    # • get(index) which returns the value at position index in the vector,
    # • set(index, value) which set the value at position index to the new float value. The method does not return value.
    
    def get(self, index):
        """
        Returns the value at the specified index in the vector.

        Parameters:
            index (int): The position of the element to retrieve.

        Returns:
            The value at the specified index.

        Raises:
            ValueError: If the index is not an integer.
            IndexError: If the index is out of range.
        """
        if not isinstance(index, int):
            raise ValueError("Index must be an integer")
        if index < 0 or index >= len(self._vector):
            raise IndexError("Index out of range")          
        return self._vector[index]
    
    def set(self,index, value):
        """
        Sets the value at the specified index in the vector.

        Args:
            index (int): The position in the vector to set the value.
            value (float or int): The value to assign at the specified index.

        Raises:
            ValueError: If index is not an integer.
            ValueError: If value is not a float or integer.
        """
        if not isinstance(index, int):
            raise ValueError("Index must be an integer")
        if not isinstance(value, (float, int)):
            raise ValueError("Value must be an float or integer type")
        self._vector[index] = value
        
    # Exercise 5: Let’s implement the scalar product method scalar_product(scalar) as an example.
    #The method needs only one parameter, the scalar. In addition, the method should return a new
    #Vector containing the result of the operation, but MUST NOT modify the calling instance, e.g. my_vector.scalar_product(3) must not modify the instance my_vector.
    
    def scalar_product(self, scalar):
        """
        Multiplies each element of the vector by the given scalar and returns a new Vector instance.

        Parameters:
            scalar (int or float): The value to multiply each element of the vector by.

        Returns:
            Vector: A new Vector instance with each element scaled by the given scalar.

        Raises:
            ValueError: If the scalar is not an integer or float.
        """
        if not isinstance(scalar, (int, float)):
            raise ValueError("Scalar must be an integer or float")
        return Vector([scalar * item for item in self._vector])
    
    #Exercise 6:
    #Implement the method add(other_vector) that emulate the vector addition operator. The method should return a new vector.
    #You will have to check that other_vector is a Vector instance and return None if it is not the case.
    #You must check that both vectors have the same dimension, return None if it is not the case.
    #ou must return a new Vector instance like we have done in scalar_product(scalar).
    
    def add(self, other_vector):
        """
        Adds another Vector to this Vector and returns the result as a new Vector.

        Parameters:
            other_vector (Vector): The vector to add.

        Returns:
            Vector: A new Vector representing the element-wise sum if dimensions match.
            None: If the vectors have different dimensions.
            None if other_vector is not an instance of Vector.
    
        """
      
        if not isinstance(other_vector, Vector) or self.dim() != other_vector.dim(): 
            return None
        
        return Vector([ self._vector[i] + other_vector.get(i) for i in range(self.dim()) ])
        
    # Exersoze 7: you need to implement a method equals(other_vector) 
    # that returns True if the vectors are equals (i.e. have the same value at the same position), False otherwise. 
    # As we are dealing with float values, you may want to explore what the function isclose() form the math module does
    
    def equals(self, other_vector):
        """
        Compares this vector to another object for equality.

        Parameters:
            other_vector (any): The object to compare with.

        Returns:
            bool: True if both are Vector instances with the same dimension and all corresponding elements are equal (within floating point tolerance), False otherwise.
        """
        
        if not isinstance(other_vector, Vector) or self.dim() != other_vector.dim():
            return False
       
        return all( math.isclose( self._vector[i], other_vector.get(i) ) for i in range(self.dim()) )
        
    #Exercise 8:
    # We are now able to compare two vectors, however it would be nice if we could use the operator
    # == instead of .equals(...). Fortunately Python allows to overload operators such as +, *, == and !=. 
    # To overload the operator ==, we must override the method __eq__. (for the operator !=, override the method __ne__). 
    # Implement the two methods:
    # def __eq__(self, other_vector):
    # def __ne__(self, other_vector):

    def __eq__(self, other_vector):
        """
        Determines if this vector is equal to another vector.

        Two vectors are considered equal if:
        - The other object is an instance of Vector.
        - Both vectors have the same dimension.
        - All corresponding elements are approximately equal, as determined by math.isclose.

        Args:
            other_vector (Vector): The vector to compare with.

        Returns:
            bool: True if the vectors are equal, False otherwise.
        """
        if not isinstance(other_vector, Vector) or self.dim() != other_vector.dim():
            return False
        return all(math.isclose(self._vector[i], other_vector.get(i)) for i in range(self.dim()))
    
    def __ne__(self, other_vector):
        """
        Determines if this vector is not equal to another vector.

        Args:
            other_vector (Vector): The vector to compare against.

        Returns:
            bool: True if the vectors are not equal (different types, dimensions, or any element differs),
                  False otherwise.
        """
        if not isinstance(other_vector, Vector) or self.dim() != other_vector.dim():
            return True
        return any(not math.isclose(self._vector[i], other_vector.get(i)) for i in range(self.dim()))
    
    
    #Exercise 9:  
    # # Implement all these operators overloading dunder methods.
    # Instead of using the method add(...) and scalar_product(...) we would like to overload the operators + and *.
    # 1. The vector addition operator is commutative, i.e. v1+v2 == v2+v1 
    # and we can override the method __add__ to overload the + operator.
    
    def __add__(self, other_vector):
        """
        Adds two Vector instances element-wise and returns a new Vector.

        Args:
            other_vector (Vector): The vector to add to this vector.

        Returns:
            Vector: A new vector representing the element-wise sum.

        Raises:
            ValueError: If other_vector is not a Vector instance or if the dimensions do not match.
        """
        
        if not isinstance(other_vector, Vector) or self.dim() != other_vector.dim():
            return None
            #raise ValueError("other_vector must be an instance of Vector with the same dimension")
        return Vector([self._vector[i] + other_vector.get(i) for i in range(self.dim())])
    
    # 2. When considering the multiplication, it is a little bit more complicated, 
    # 3 * v1 is allowed, but v1 * 3 is not. 
    # Investigate the methods __mul__ and __rmul__.  
    
    # The __mul__ method defines the behavior 
    # when your object appears on the left side of the * operator (e.g., vector * scalar). 
    # For a vector class, this typically means multiplying each element of the vector by the scalar and returning a new vector.
    def __mul__(self, scalar):
        """
        Multiply each element of the vector by a scalar and return a new Vector.

        Args:
            scalar (int or float): The value to multiply each element of the vector by.

        Returns:
            Vector: A new vector with each element multiplied by the scalar.

        Raises:
            ValueError: If the scalar is not an integer or float.
        """
        
        if not isinstance(scalar, (int, float)):
            raise ValueError("Scalar must be an integer or float")
        return Vector([item * scalar for item in self._vector])
    
    
    # The __rmul__ method stands for "right multiplication" 
    # and is called when your object appears on the right side of the * operator (e.g., scalar * vector). 
    # This is useful because Python will try __mul__ first, 
    # and if the left operand does not know how to multiply with your object, 
    # it will try your object's __rmul__ method. 
    def __rmul__(self, scalar):
        """
        Implements the right-side scalar multiplication for the Vector class.

        This method allows scalar multiplication when the scalar is on the left side
        of the multiplication operator (e.g., scalar * vector).

        Args:
            scalar (int or float): The scalar value to multiply each element of the vector by.

        Returns:
            Vector: A new Vector instance with each element multiplied by the scalar.

        Raises:
            ValueError: If the scalar is not an integer or float.
        """
        if not isinstance(scalar, (int, float)):
            raise ValueError("Scalar must be an integer or float")
        return Vector([item * scalar for item in self._vector])
    # 3. One other programming shortcut we could find useful is v1 += v2 for v1 = v1+v2. 
    # It can be implemented by overloading __iadd__.
    # The __iadd__ method is used to implement the in-place addition operator +=.
    def __iadd__(self, other_vector):
        """
        Implements the in-place addition operator (+=) for Vector objects.

        Adds the elements of another Vector to this Vector, element-wise.
        The operation modifies the current Vector instance.

        Args:
            other_vector (Vector): The Vector to add. Must be an instance of Vector with the same dimension.

        Raises:
            ValueError: If other_vector is not a Vector instance or if its dimension does not match this Vector.

        Returns:
            Vector: The updated Vector instance after addition.
        """
        if not isinstance(other_vector, Vector) or self.dim() != other_vector.dim():
            raise ValueError("other_vector must be an instance of Vector with the same dimension")
        self._vector = [self._vector[i] + other_vector.get(i) for i in range(self.dim())]
        return self
        
    # 4. Similarly, the shortcut v1 *= 3 for v1 = 3 * v1 can be implemented by overloading __imul__.
    
    def __imul__(self, scalar):
        """
        Implements in-place multiplication of the vector by a scalar.

        Args:
            scalar (int or float): The value to multiply each element of the vector by.

        Returns:
            Vector: The updated vector after in-place multiplication.

        Raises:
            ValueError: If the scalar is not an integer or float.
        """
        if not isinstance(scalar, (int, float)):
            raise ValueError("Scalar must be an integer or float")
        self._vector = [item * scalar for item in self._vector]
        return self