# Perform a weighted overlay, e.g. to aggregate figures from blocks to block groups weighting by population

import numpy as np
import pandas as pd
from tqdm import tqdm
from .projections import aea

def _intersectingFractions (target_geom, source_geoms, sindex):
     # spatial index will overselect but that's okay as we do an actual intersection below
    relevantSourceGeoms = list(sindex.intersection(target_geom.bounds))
    out = np.zeros(len(source_geoms))
    # weights are the fraction of area of a source geom that is within the target geom
    # geoms are already projected to an equal area projection
    out[relevantSourceGeoms] = source_geoms.iloc[relevantSourceGeoms]\
        .intersection(target_geom).area / source_geoms.iloc[relevantSourceGeoms].area
    return out

def weighted_overlay (source_geoms, target_geoms, weights, vals, quiet=False, tqdm=tqdm, scaleInvariantVariables=True):
    """
    vals should be a data frame with all values to aggregate. If scaleInvariantVariables is False, a weighted sum rather than average will be returned.
    This is useful for variables that vary with area. For instance, half of a census block would be expected to have
    roughly the same population density as the full block---population density is a scale invariant variable.
    However, you would expect half a census block to have half the total population of the full Census block; this is a scale-variant variable.
    By passing scaleInvariantVariables=False, it will be treated correctly, and partially overlapping areas will be scaled accordingly.
    """
    if weights is None:
        weights = np.ones(len(vals))

    def log (*args, **kwargs):
        if not quiet:
            print(*args, **kwargs)

    log('Projecting geometries')
    source_geoms = source_geoms.to_crs(aea)
    target_geoms = target_geoms.to_crs(aea)

    log('Building spatial index')
    # https://github.com/gboeing/urban-data-science/blob/master/19-Spatial-Analysis-and-Cartography/rtree-spatial-indexing.ipynb
    sindex = source_geoms.sindex

    out = pd.DataFrame({col: np.zeros(len(target_geoms)) for col in vals.columns}, index=target_geoms.index)

    log('Performing overlay')

    it = tqdm(list(zip(target_geoms.index, target_geoms))) if not quiet else zip(target_geoms.index, target_geoms)
    for idx, target_geom in it:
        frac = _intersectingFractions(target_geom, source_geoms, sindex)
        targetWeights = weights * frac
        if scaleInvariantVariables:
            targetWeights /= np.sum(targetWeights)
        for col in vals.columns:
            out.loc[idx, col] = np.sum(vals[col] * targetWeights)

    return out
