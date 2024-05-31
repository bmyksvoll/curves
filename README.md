[![Build Status](https://travis-ci.org/equinor/curves.svg?branch=master)](https://travis-ci.org/equinor/curves)

# Curves
Smooth Forward Price Curve builder for Python. 


# Installing

# Credits

This package is based on the brilliant work  of Joachim Blaafjell Holwech, notably his Curvy https://github.com/equinor/curvy package. For a tutorial see https://holwech.github.io/blog/curvy/

Other sources include

- Previous Excel VBA implementation
- etrm package in R by Anders Sleire https://github.com/sleire/etrm
 

**_Your feedback matters_** - This library is still in development. Any feedback regarding improvements or errors in the curve builder is very much appreciated! 

# Theory
This library is based on theory from 


"[Constructing forward price curves in electricity
markets](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.470.8485&rep=rep1&type=pdf)" by Fleten and Lemming. The curve is created by solving a constrained optimization problem that ensures that the curve maintains the correct average value for each price period while keeping its smooth and continuous properties.


### Using

# Contribution
Bugs or suggestions? Please don't hesitate to post an issue on it!

Maintainer: Bjarte Myksvoll
