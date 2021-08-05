# User-management

# Used Packages

![python](https://www.python.org/static/img/python-logo-large.c36dccadd999.png?1576869008) 
![numpy](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/NumPy_logo.svg/320px-NumPy_logo.svg.png) 
![opencv](https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/195px-OpenCV_Logo_with_text_svg_version.svg.png)
![sqlite3](https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Sqlite-square-icon.svg/240px-Sqlite-square-icon.svg.png)

for python >= 3.9 you should do following process:

in primes.py you have to change the content because in python 3.9 GCD belongs to math instead of fractions

primes.py-dir : C:\python39\Lib\site-packages\basehash\primes.py


---------- OLD ----------


def gcd(*n):
    from fractions import gcd
    return abs(reduce(gcd, n))


---------- NEW ----------


def gcd(*n):
    from math import gcd
    return abs(reduce(gcd, n))
