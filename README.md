Follower
========

Follow 1st order distribution of a data stream.

## density_follower.py

A quick hack of the algorithm. Needs sensible variable names, and general documenting.

A Density_1D object is an estimate of the probability density of an incoming stream. Method “adapt” adapts the quantile boundaries in response to the next data point.
Method “whiten” does not adapt the quantile boundaries, but uses maps a value in the input space to an interpolated quantised value, assuming linear interpolation. 

## density_animation_test.py

An animated demo of density following.

Shows that there are issues with the last few quantiles. They are unstable and jump around wildly.