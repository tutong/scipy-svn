# pylint: disable-msg=W0611, W0612, W0511,R0201
"""Tests suite for MaskedArray.
Adapted from the original test_ma by Pierre Gerard-Marchant

:author: Pierre Gerard-Marchant
:contact: pierregm_at_uga_dot_edu
:version: $Id: test_timeseries.py 2578 2007-01-17 19:25:10Z mattknox_ca $
"""
__author__ = "Pierre GF Gerard-Marchant ($Author: mattknox_ca $)"
__version__ = '1.0'
__revision__ = "$Revision: 2578 $"
__date__     = '$Date: 2007-01-17 14:25:10 -0500 (Wed, 17 Jan 2007) $'

import numpy as N
from numpy import bool_, complex_, float_, int_, object_
import numpy.core.fromnumeric  as fromnumeric
import numpy.core.numeric as numeric
from numpy.testing import NumpyTest, NumpyTestCase
from numpy.testing.utils import build_err_msg

import maskedarray
from maskedarray import masked_array, masked, nomask

import maskedarray.testutils
from maskedarray.testutils import assert_equal, assert_array_equal, approx

from timeseries import tcore

class test_funcs(NumpyTestCase):
    
    def __init__(self, *args, **kwds):
        NumpyTestCase.__init__(self, *args, **kwds)
        self.mask = [1,0,1,0,0,1,1,0,0,0]
        self.data = numeric.arange(10)
        self.test_array = masked_array(self.data, mask=self.mask)

    def test_backward_fill (self):
        result = masked_array(self.data, mask=self.mask)
        result[0] = 1
        result[2] = 3
       
        assert_equal(tcore.backward_fill(self.test_array, maxgap=1), result)
        
        result[5] = 7
        result[6] = 7
        
        assert_equal(tcore.backward_fill(self.test_array), result)

    def test_forward_fill (self):
        result = masked_array(self.data, mask=self.mask)
        result[2] = 1
       
        assert_equal(tcore.forward_fill(self.test_array, maxgap=1), result)
        
        result[5] = 4
        result[6] = 4
        
        assert_equal(tcore.forward_fill(self.test_array), result)

    def test_interp_fill(self):
        result_lin = masked_array(self.data).astype(float_)
        result_lin[0] = masked
        
        approx(tcore.interp_masked1d(self.test_array.astype(float_), kind='linear'), result_lin)
        
        
###############################################################################
#------------------------------------------------------------------------------
if __name__ == "__main__":
    NumpyTest().run()        