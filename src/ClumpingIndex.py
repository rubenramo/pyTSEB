# This file is part of pyTSEB for calculating the canopy clumping index
# Copyright 2016 Hector Nieto and contributors listed in the README.md file.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Created on Apr 6 2015
@author: Hector Nieto (hnieto@ias.csic.es)

Modified on Jan 27 2016
@author: Hector Nieto (hnieto@ias.csic.es)

DESCRIPTION
===========
Routines for calculating the clumping index for both randomly placed canopies and
structured row crops such as vineyards.

PACKAGE CONTENTS
================
* :func:`CalcOmega0_Kustas` Nadir viewing clmping factor.
* :func:`CalcOmega_Kustas` Clumping index at an incidence angle.
"""
def CalcOmega0_Kustas(LAI, f_C,x_LAD=1,isLAIeff=True):
    ''' Nadir viewing clmping factor

    Estimates the clumping factor forcing equal gap fraction between the real canopy
    and the homogeneous case, after [Kustas1999]_.
         
    Parameters
    ----------  
    LAI : float
        Leaf Area Index, it can be either the effective LAI or the real LAI 
        , default input LAI is effective.
    f_C : float
        Apparent fractional cover, estimated from large gaps, means that
        are still gaps within the canopy to be quantified.
    x_LAD : float, optional
        Chi parameter for the ellipsoildal Leaf Angle Distribution function of 
        [Campbell1988]_ [default=1, spherical LIDF].
    isLAIeff :  bool, optional
        Defines whether the input LAI is effective or local.
    
    Returns
    -------
    omega0 : float
        clumping index at nadir.

    References
    ----------
    .. [Kustas1999] William P Kustas, John M Norman, Evaluation of soil and vegetation heat
        flux predictions using a simple two-source model with radiometric temperatures for
        partial canopy cover, Agricultural and Forest Meteorology, Volume 94, Issue 1,
        Pages 13-29, http://dx.doi.org/10.1016/S0168-1923(99)00005-2.
    .. [Campbell1998] Campbell, G. S. & Norman, J. M. (1998), An introduction to environmental
        biophysics. Springer, New York
        https://archive.org/details/AnIntroductionToEnvironmentalBiophysics.
 '''
    
    from math import sqrt,radians, tan
    import numpy as np    
    
    theta=0.0
    theta=radians(theta)    
    # Estimate the beam extinction coefficient based on a ellipsoidal LAD function
    # Eq. 15.4 of Campbell and Norman (1998)
    K_be=sqrt(x_LAD**2+tan(theta)**2)/(x_LAD+1.774*(x_LAD+1.182)**-0.733)
    if isLAIeff:
        F=LAI/f_C
    else: # The input LAI is actually the real LAI
        F=LAI.astype(float)
    # Calculate the gap fraction of our canopy
    trans = f_C*np.exp(-K_be * F)+(1.0-f_C)
    trans[trans<=0] = 1e-36
    # and then the nadir clumping factor
    omega0 = -np.log(trans)/(F*K_be)
    return omega0

def CalcOmega_Kustas(omega0,theta,wc=1):
    ''' Clumping index at an incidence angle.

    Estimates the clumping index for a given incidence angle assuming randomnly placed canopies.
    
    Parameters
    ----------
    omega0 : float
        clumping index at nadir, estimated for instance by :func:`CalcOmega0_Kustas`.
    theta : float
        incidence angle (degrees).
    wc :  float, optional
        canopy witdth to height ratio, [default = 1].

    Returns
    -------
    Omega : float
        Clumping index at an incidenc angle.

    References
    ----------
    .. [Kustas1999] William P Kustas, John M Norman, Evaluation of soil and vegetation heat
        flux predictions using a simple two-source model with radiometric temperatures for
        partial canopy cover, Agricultural and Forest Meteorology, Volume 94, Issue 1,
        Pages 13-29, http://dx.doi.org/10.1016/S0168-1923(99)00005-2.
    '''
    
    import numpy as np    
    
    wc=1.0/wc
    omega = omega0 / (omega0 + (1.0 - omega0) * np.exp(-2.2 * (np.radians(theta))**(3.8 - 0.46 * wc)))
    return omega
