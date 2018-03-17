# Matt's Utility Functions

These are a few utility functions I've developed during grad school to support my research.

`geo.weighted_overlay`: Performs a weighted overlay, for instance to summarize disaggregate accessibility metrics to aggregate units. Takes the source geometry, target geometry, weights (e.g. block populations) of the source geometries, and a data frame of values to aggregate, and returns aggregated values. When the values are some block-level attribute, the source geometries are blocks, and the weights are populations, the aggregated result is the average value of the attributes experienced by people living in the aggregated area. For instance, if the values are accessibility, and the data is being aggregated to tracts, and there is a rapid transit station on the east side of the tract and an open space preserve with low accessibility on the west side, the aggregated average will reflect the area where most people live on the east side.
