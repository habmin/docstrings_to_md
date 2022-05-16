# Python Docstring to MD
This is a basic, quick and dirty script that retrieves the doc strings of class objects and functions in a module/file, then formats it to a MD file, including a table of contents with anchor links.

This works on one very particular form of docstrings.

For classes:
```
class Object():
    """
    Description of class

    Attributes
    ----------
    first_attribute : type
        description of attribute
    second_attribute : type
        another description

    Methods
    -------
    function_name():
        Description description
    """
```

For functions:
```
def function(arg1, arg2):
    """
    description of function

    Parameters
    ----------
    arg1 : type
        description
    arg2 : type
        description

    Raises
    ------
    ErrorType
        Raises is an optional section that can be added,
        but it must be written before Returns section
    
    Returns
    -------
    Type
        Description
    """
```
