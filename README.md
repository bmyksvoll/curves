[![Build Status](https://travis-ci.org/equinor/curves.svg?branch=master)](https://travis-ci.org/equinor/curves)

# Curves
Smooth Forward Price Curve builder and Monte Carlo Simulation for Python. 

**_Your feedback matters_** - This library is still in development. Any feedback regarding improvements or errors in the curve builder is very much appreciated! 

# Theory

This library is based on theory from multiple sources (see Credits)



# Credits

This package is based on the brilliant work of of others:

- Bjerksund, P., Rasmussen, H., Stensland, G. (2010). Valuation and Risk Management in the Norwegian Electricity Market. In: Bjørndal, E., Bjørndal, M., Pardalos, P., Rönnqvist, M. (eds) Energy, Natural Resources and Environmental Economics. Energy Systems. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-12067-1_11
- Joachim Blaafjell Holwech, notably his Curvy https://github.com/equinor/curvy package. For a tutorial see https://holwech.github.io/blog/curvy/. Based on "[Constructing forward price curves in electricity
markets](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.470.8485&rep=rep1&type=pdf)" by Fleten and Lemming. The curve is created by solving a constrained optimization problem that ensures that the curve maintains the correct average value for each price period while keeping its smooth and continuous properties.

- Previous Excel VBA implementation by author
- etrm package in R by Anders Sleire https://github.com/sleire/etrm


# Contribution
Bugs or suggestions? Please don't hesitate to post an issue on it!

Maintainer: Bjarte Myksvoll


# Develop & Build
The project is set up using[SetupTools]( https://setuptools.pypa.io/en/latest/userguide/quickstart.html) using flat-layout
(also known as “adhoc”)

The package folder(s) are placed directly under the project root:

pip install --editable .

python -m build


