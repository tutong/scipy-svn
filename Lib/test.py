# Copyright (C) 2003-2005 Peter J. Verveer
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# 3. The name of the author may not be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import unittest
import math
import numpy as numarray
import scipy.nd_image as nd_image
import numpy.dft as dft
#import numarray.numinclude as numinclude

eps = 1e-12

def diff(a, b):
    if not isinstance(a, numarray.ndarray):
        a = numarray.asarray(a)
    if not isinstance(b, numarray.ndarray):
        b = numarray.asarray(b)
    if (0 in a.shape) and (0 in b.shape):
        return 0.0
    if (a.dtype in [numarray.complex64, numarray.complex128] or
        b.dtype in [numarray.complex64, numarray.complex128]):
        a = numarray.asarray(a, numarray.complex128)
        b = numarray.asarray(b, numarray.complex128)
        t = ((a.real - b.real)**2).sum() + ((a.imag - b.imag)**2).sum()
    else:
        a = numarray.asarray(a)
        a = a.astype(numarray.float64)
        b = numarray.asarray(b)
        b = b.astype(numarray.float64)
        t = ((a - b)**2).sum()
    return math.sqrt(t)


class NDImageTest(unittest.TestCase):

    def setUp(self):
        # list of numarray data types
        self.types = [numarray.int8, numarray.uint8, numarray.int16,
                      numarray.uint16, numarray.int32, numarray.uint32,
                      numarray.int64, numarray.uint64,
                      numarray.float32, numarray.float64]
##      if numinclude.hasUInt64:
##          self.types.append(numarray.UInt64)

        # list of boundary modes:
        self.modes = ['nearest', 'wrap', 'reflect', 'constant']

    def test_correlate01(self):
        "correlation 1"
        array = numarray.array([1, 2])
        weights = numarray.array([2])
        true = [2, 4]
        output = nd_image.correlate(array, weights)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.convolve(array, weights)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.correlate1d(array, weights)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.convolve1d(array, weights)
        self.failUnless(diff(output, true) < eps)

    def test_correlate02(self):
        "correlation 2"
        array = numarray.array([1, 2, 3])
        kernel = numarray.array([1])
        output = nd_image.correlate(array, kernel)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.convolve(array, kernel)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.correlate1d(array, kernel)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.convolve1d(array, kernel)
        self.failUnless(diff(array, output) < eps)

    def test_correlate03(self):
        "correlation 3"
        array = numarray.array([1])
        weights = numarray.array([1, 1])
        true = [2]
        output = nd_image.correlate(array, weights)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.convolve(array, weights)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.correlate1d(array, weights)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.convolve1d(array, weights)
        self.failUnless(diff(output, true) < eps)

    def test_correlate04(self):
        "correlation 4"
        array = numarray.array([1, 2])
        tcor = [2, 3]
        tcov = [3, 4]
        weights = numarray.array([1, 1])
        output = nd_image.correlate(array, weights)
        self.failUnless(diff(output, tcor) < eps)
        output = nd_image.convolve(array, weights)
        self.failUnless(diff(output, tcov) < eps)
        output = nd_image.correlate1d(array, weights)
        self.failUnless(diff(output, tcor) < eps)
        output = nd_image.convolve1d(array, weights)
        self.failUnless(diff(output, tcov) < eps)

    def test_correlate05(self):
        "correlation 5"
        array = numarray.array([1, 2, 3])
        tcor = [2, 3, 5]
        tcov = [3, 5, 6]
        kernel = numarray.array([1, 1])
        output = nd_image.correlate(array, kernel)
        self.failUnless(diff(tcor, output) < eps)
        output = nd_image.convolve(array, kernel)
        self.failUnless(diff(tcov, output) < eps)
        output = nd_image.correlate1d(array, kernel)
        self.failUnless(diff(tcor, output) < eps)
        output = nd_image.convolve1d(array, kernel)
        self.failUnless(diff(tcov, output) < eps)

    def test_correlate06(self):
        "correlation 6"
        array = numarray.array([1, 2, 3])
        tcor = [9, 14, 17]
        tcov = [7, 10, 15]
        weights = numarray.array([1, 2, 3])
        output = nd_image.correlate(array, weights)
        self.failUnless(diff(output, tcor) < eps)
        output = nd_image.convolve(array, weights)
        self.failUnless(diff(output, tcov) < eps)
        output = nd_image.correlate1d(array, weights)
        self.failUnless(diff(output, tcor) < eps)
        output = nd_image.convolve1d(array, weights)
        self.failUnless(diff(output, tcov) < eps)

    def test_correlate07(self):
        "correlation 7"
        array = numarray.array([1, 2, 3])
        true = [5, 8, 11]
        weights = numarray.array([1, 2, 1])
        output = nd_image.correlate(array, weights)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.convolve(array, weights)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.correlate1d(array, weights)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.convolve1d(array, weights)
        self.failUnless(diff(output, true) < eps)

    def test_correlate08(self):
        "correlation 8"
        array = numarray.array([1, 2, 3])
        tcor = [1, 2, 5]
        tcov = [3, 6, 7]
        weights = numarray.array([1, 2, -1])
        output = nd_image.correlate(array, weights)
        self.failUnless(diff(output, tcor) < eps)
        output = nd_image.convolve(array, weights)
        self.failUnless(diff(output, tcov) < eps)
        output = nd_image.correlate1d(array, weights)
        self.failUnless(diff(output, tcor) < eps)
        output = nd_image.convolve1d(array, weights)
        self.failUnless(diff(output, tcov) < eps)

    def test_correlate09(self):
        "correlation 9"
        array = []
        kernel = numarray.array([1, 1])
        output = nd_image.correlate(array, kernel)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.convolve(array, kernel)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.correlate1d(array, kernel)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.convolve1d(array, kernel)
        self.failUnless(diff(array, output) < eps)

    def test_correlate10(self):
        "correlation 10"
        array = [[]]
        kernel = numarray.array([[1, 1]])
        output = nd_image.correlate(array, kernel)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.convolve(array, kernel)
        self.failUnless(diff(array, output) < eps)

    def test_correlate11(self):
        "correlation 11"
        array = numarray.array([[1, 2, 3],
                                [4, 5, 6]])
        kernel = numarray.array([[1, 1],
                                 [1, 1]])
        output = nd_image.correlate(array, kernel)
        self.failUnless(diff([[4, 6, 10], [10, 12, 16]], output) < eps)
        output = nd_image.convolve(array, kernel)
        self.failUnless(diff([[12, 16, 18], [18, 22, 24]], output) < eps)

    def test_correlate12(self):
        "correlation 12"
        array = numarray.array([[1, 2, 3],
                                [4, 5, 6]])
        kernel = numarray.array([[1, 0],
                                 [0, 1]])
        output = nd_image.correlate(array, kernel)
        self.failUnless(diff([[2, 3, 5], [5, 6, 8]], output) < eps)
        output = nd_image.convolve(array, kernel)
        self.failUnless(diff([[6, 8, 9], [9, 11, 12]], output) < eps)

    def test_correlate13(self):
        "correlation 13"
        kernel = numarray.array([[1, 0],
                                 [0, 1]])
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [4, 5, 6]], type1)
            for type2 in self.types:
                output = nd_image.correlate(array, kernel,
                                                    output = type2)
                error = diff([[2, 3, 5], [5, 6, 8]], output)
                self.failUnless(error < eps and output.dtype.type == type2)
                output = nd_image.convolve(array, kernel,
                                                   output = type2)
                error = diff([[6, 8, 9], [9, 11, 12]], output)
                self.failUnless(error < eps and output.dtype.type == type2)

    def test_correlate14(self):
        "correlation 14"
        kernel = numarray.array([[1, 0],
                                 [0, 1]])
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [4, 5, 6]], type1)
            for type2 in self.types:
                output = numarray.zeros(array.shape, type2)
                nd_image.correlate(array, kernel,
                                                        output = output)
                error = diff([[2, 3, 5], [5, 6, 8]], output)
                self.failUnless(error < eps and output.dtype.type == type2)
                nd_image.convolve(array, kernel, output = output)
                error = diff([[6, 8, 9], [9, 11, 12]], output)
                self.failUnless(error < eps and output.dtype.type == type2)

    def test_correlate15(self):
        "correlation 15"
        kernel = numarray.array([[1, 0],
                                 [0, 1]])
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [4, 5, 6]], type1)
            output = nd_image.correlate(array, kernel,
                                                output = numarray.float32)
            error = diff([[2, 3, 5], [5, 6, 8]], output)
            self.failUnless(error < eps and
                            output.dtype.type == numarray.float32)
            output = nd_image.convolve(array, kernel,
                                               output = numarray.float32)
            error = diff([[6, 8, 9], [9, 11, 12]], output)
            self.failUnless(error < eps and
                            output.dtype.type == numarray.float32)

    def test_correlate16(self):
        "correlation 16"
        kernel = numarray.array([[0.5, 0  ],
                                 [0,   0.5]])
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [4, 5, 6]], type1)
            output = nd_image.correlate(array, kernel,
                                                output = numarray.float32)
            error = diff([[1, 1.5, 2.5], [2.5, 3, 4]], output)
            self.failUnless(error < eps and
                            output.dtype.type == numarray.float32)
            output = nd_image.convolve(array, kernel,
                                               output = numarray.float32)
            error = diff([[3, 4, 4.5], [4.5, 5.5, 6]], output)
            self.failUnless(error < eps and
                            output.dtype.type == numarray.float32)

    def test_correlate17(self):
        "correlation 17"
        array = numarray.array([1, 2, 3])
        tcor = [3, 5, 6]
        tcov = [2, 3, 5]
        kernel = numarray.array([1, 1])
        output = nd_image.correlate(array, kernel, origin = -1)
        self.failUnless(diff(tcor, output) < eps)
        output = nd_image.convolve(array, kernel, origin = -1)
        self.failUnless(diff(tcov, output) < eps)
        output = nd_image.correlate1d(array, kernel, origin = -1)
        self.failUnless(diff(tcor, output) < eps)
        output = nd_image.convolve1d(array, kernel, origin = -1)
        self.failUnless(diff(tcov, output) < eps)

    def test_correlate18(self):
        "correlation 18"
        kernel = numarray.array([[1, 0],
                                 [0, 1]])
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [4, 5, 6]], type1)
            output = nd_image.correlate(array, kernel,
                                        output = numarray.float32,
                                        mode = 'nearest', origin = -1)
            error = diff([[6, 8, 9], [9, 11, 12]], output)
            self.failUnless(error < eps and
                            output.dtype.type == numarray.float32)
            output = nd_image.convolve(array, kernel,
                output = numarray.float32, mode = 'nearest', origin = -1)
            error = diff([[2, 3, 5], [5, 6, 8]], output)
            self.failUnless(error < eps and
                            output.dtype.type == numarray.float32)

    def test_correlate19(self):
        "correlation 19"
        kernel = numarray.array([[1, 0],
                                 [0, 1]])
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [4, 5, 6]], type1)
            output = nd_image.correlate(array, kernel,
                                    output = numarray.float32,
                                    mode = 'nearest', origin = [-1, 0])
            error = diff([[5, 6, 8], [8, 9, 11]], output)
            self.failUnless(error < eps and
                            output.dtype.type == numarray.float32)
            output = nd_image.convolve(array, kernel,
                                    output = numarray.float32,
                                    mode = 'nearest', origin = [-1, 0])
            error = diff([[3, 5, 6], [6, 8, 9]], output)
            self.failUnless(error < eps and
                            output.dtype.type == numarray.float32)

    def test_correlate20(self):
        "correlation 20"
        weights = numarray.array([1, 2, 1])
        true = [[5, 10, 15], [7, 14, 21]]
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [2, 4, 6]], type1)
            for type2 in self.types:
                output = numarray.zeros((2, 3), type2)
                nd_image.correlate1d(array, weights, axis = 0,
                                              output = output)
                self.failUnless(diff(output, true) < eps)
                nd_image.convolve1d(array, weights, axis = 0,
                                              output = output)
                self.failUnless(diff(output, true) < eps)

    def test_correlate21(self):
        "correlation 21"
        array = numarray.array([[1, 2, 3],
                                [2, 4, 6]])
        true = [[5, 10, 15], [7, 14, 21]]
        weights = numarray.array([1, 2, 1])
        output = nd_image.correlate1d(array, weights, axis = 0)
        self.failUnless(diff(output, true) < eps)
        output = nd_image.convolve1d(array, weights, axis = 0)
        self.failUnless(diff(output, true) < eps)

    def test_correlate22(self):
        "correlation 22"
        weights = numarray.array([1, 2, 1])
        true = [[6, 12, 18], [6, 12, 18]]
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [2, 4, 6]], type1)
            for type2 in self.types:
                output = numarray.zeros((2, 3), type2)
                nd_image.correlate1d(array, weights, axis = 0,
                                            mode = 'wrap', output = output)
                self.failUnless(diff(output, true) < eps)
                nd_image.convolve1d(array, weights, axis = 0,
                                            mode = 'wrap', output = output)
                self.failUnless(diff(output, true) < eps)

    def test_correlate23(self):
        "correlation 23"
        weights = numarray.array([1, 2, 1])
        true = [[5, 10, 15], [7, 14, 21]]
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [2, 4, 6]], type1)
            for type2 in self.types:
                output = numarray.zeros((2, 3), type2)
                nd_image.correlate1d(array, weights, axis = 0,
                                         mode = 'nearest', output = output)
                self.failUnless(diff(output, true) < eps)
                nd_image.convolve1d(array, weights, axis = 0,
                                         mode = 'nearest', output = output)
                self.failUnless(diff(output, true) < eps)

    def test_correlate24(self):
        "correlation 24"
        weights = numarray.array([1, 2, 1])
        tcor = [[7, 14, 21], [8, 16, 24]]
        tcov = [[4, 8, 12], [5, 10, 15]]
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [2, 4, 6]], type1)
            for type2 in self.types:
                output = numarray.zeros((2, 3), type2)
                nd_image.correlate1d(array, weights, axis = 0,
                           mode = 'nearest', output = output, origin = -1)
                self.failUnless(diff(output, tcor) < eps)
                nd_image.convolve1d(array, weights, axis = 0,
                           mode = 'nearest', output = output, origin = -1)
                self.failUnless(diff(output, tcov) < eps)

    def test_correlate25(self):
        "correlation 25"
        weights = numarray.array([1, 2, 1])
        tcor = [[4, 8, 12], [5, 10, 15]]
        tcov = [[7, 14, 21], [8, 16, 24]]
        for type1 in self.types:
            array = numarray.array([[1, 2, 3],
                                    [2, 4, 6]], type1)
            for type2 in self.types:
                output = numarray.zeros((2, 3), type2)
                nd_image.correlate1d(array, weights, axis = 0,
                             mode = 'nearest', output = output, origin = 1)
                self.failUnless(diff(output, tcor) < eps)
                nd_image.convolve1d(array, weights, axis = 0,
                             mode = 'nearest', output = output, origin = 1)
                self.failUnless(diff(output, tcov) < eps)

    def test_gauss01(self):
        "gaussian filter 1"
        input = numarray.array([[1, 2, 3],
                                [2, 4, 6]], numarray.float32)
        output = nd_image.gaussian_filter(input, 0)
        self.failUnless(diff(output, input) < eps)

    def test_gauss02(self):
        "gaussian filter 2"
        input = numarray.array([[1, 2, 3],
                                [2, 4, 6]], numarray.float32)
        output = nd_image.gaussian_filter(input, 1.0)
        self.failUnless(input.dtype == output.dtype and
                        input.shape == output.shape)

    def test_gauss03(self):
        "gaussian filter 3"
        input = numarray.arange(100 * 100).astype(numarray.float32)
        input.shape = (100, 100)
        output = nd_image.gaussian_filter(input, [1.0, 1.0])

        self.failUnless(input.dtype == output.dtype and
                        input.shape == output.shape and
                        output.sum(dtype='d') - input.sum(dtype='d') < eps and
                        diff(input, output) > 1.0)

    def test_gauss04(self):
        "gaussian filter 4"
        input = numarray.arange(100 * 100).astype(numarray.float32)
        input.shape = (100, 100)
        otype = numarray.float64
        output = nd_image.gaussian_filter(input, [1.0, 1.0],
                                                            output = otype)
        self.failUnless(output.dtype.type == numarray.float64 and
                        input.shape == output.shape and
                        diff(input, output) > 1.0)

    def test_gauss05(self):
        "gaussian filter 5"
        input = numarray.arange(100 * 100).astype(numarray.float32)
        input.shape = (100, 100)
        otype = numarray.float64
        output = nd_image.gaussian_filter(input, [1.0, 1.0],
                                                 order = 1, output = otype)
        self.failUnless(output.dtype.type == numarray.float64 and
                        input.shape == output.shape and
                        diff(input, output) > 1.0)

    def test_gauss06(self):
        "gaussian filter 6"
        input = numarray.arange(100 * 100).astype(numarray.float32)
        input.shape = (100, 100)
        otype = numarray.float64
        output1 = nd_image.gaussian_filter(input, [1.0, 1.0],
                                                            output = otype)
        output2 = nd_image.gaussian_filter(input, 1.0,
                                                            output = otype)
        self.failUnless(diff(output1, output2) < eps)

    def test_prewitt01(self):
        "prewitt filter 1"
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = nd_image.correlate1d(array, [-1.0, 0.0, 1.0], 0)
            t = nd_image.correlate1d(t, [1.0, 1.0, 1.0], 1)
            output = nd_image.prewitt(array, 0)
            self.failUnless(diff(t, output) < eps)


    def test_prewitt02(self):
        "prewitt filter 2"
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = nd_image.correlate1d(array, [-1.0, 0.0, 1.0], 0)
            t = nd_image.correlate1d(t, [1.0, 1.0, 1.0], 1)
            output = numarray.zeros(array.shape, type)
            nd_image.prewitt(array, 0, output)
            self.failUnless(diff(t, output) < eps)

    def test_prewitt03(self):
        "prewitt filter 3"
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = nd_image.correlate1d(array, [-1.0, 0.0, 1.0], 1)
            t = nd_image.correlate1d(t, [1.0, 1.0, 1.0], 0)
            output = nd_image.prewitt(array, 1)
            self.failUnless(diff(t, output) < eps)

    def test_prewitt04(self):
        "prewitt filter 4"
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = nd_image.prewitt(array, -1)
            output = nd_image.prewitt(array, 1)
            self.failUnless(diff(t, output) < eps)

    def test_sobel01(self):
        "sobel filter 1"
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = nd_image.correlate1d(array, [-1.0, 0.0, 1.0], 0)
            t = nd_image.correlate1d(t, [1.0, 2.0, 1.0], 1)
            output = nd_image.sobel(array, 0)
            self.failUnless(diff(t, output) < eps)

    def test_sobel02(self):
        "sobel filter 2"
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = nd_image.correlate1d(array, [-1.0, 0.0, 1.0], 0)
            t = nd_image.correlate1d(t, [1.0, 2.0, 1.0], 1)
            output = numarray.zeros(array.shape, type)
            nd_image.sobel(array, 0, output)
            self.failUnless(diff(t, output) < eps)

    def test_sobel03(self):
        "sobel filter 3"
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = nd_image.correlate1d(array, [-1.0, 0.0, 1.0], 1)
            t = nd_image.correlate1d(t, [1.0, 2.0, 1.0], 0)
            output = numarray.zeros(array.shape, type)
            output = nd_image.sobel(array, 1)
            self.failUnless(diff(t, output) < eps)

    def test_sobel04(self):
        "sobel filter 4"
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = nd_image.sobel(array, -1)
            output = nd_image.sobel(array, 1)
            self.failUnless(diff(t, output) < eps)

    def test_laplace01(self):
        "laplace filter 1"
        for type in [numarray.int32, numarray.float32, numarray.float64]:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = nd_image.correlate1d(array, [1, -2, 1], 0)
            tmp2 = nd_image.correlate1d(array, [1, -2, 1], 1)
            output = nd_image.laplace(array)
            self.failUnless(diff(tmp1 + tmp2, output) < eps)

    def test_laplace02(self):
        "laplace filter 2"
        for type in [numarray.int32, numarray.float32, numarray.float64]:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = nd_image.correlate1d(array, [1, -2, 1], 0)
            tmp2 = nd_image.correlate1d(array, [1, -2, 1], 1)
            output = numarray.zeros(array.shape, type)
            nd_image.laplace(array, output = output)
            self.failUnless(diff(tmp1 + tmp2, output) < eps)

    def test_gaussian_laplace01(self):
        "gaussian laplace filter 1"
        for type in [numarray.int32, numarray.float32, numarray.float64]:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = nd_image.gaussian_filter(array, 1.0, [2, 0])
            tmp2 = nd_image.gaussian_filter(array, 1.0, [0, 2])
            output = nd_image.gaussian_laplace(array, 1.0)
            self.failUnless(diff(tmp1 + tmp2, output) < eps)

    def test_gaussian_laplace02(self):
        "gaussian laplace filter 2"
        for type in [numarray.int32, numarray.float32, numarray.float64]:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = nd_image.gaussian_filter(array, 1.0, [2, 0])
            tmp2 = nd_image.gaussian_filter(array, 1.0, [0, 2])
            output = numarray.zeros(array.shape, type)
            nd_image.gaussian_laplace(array, 1.0, output)
            self.failUnless(diff(tmp1 + tmp2, output) < eps)

    def test_generic_laplace01(self):
        "generic laplace filter 1"
        def derivative2(input, axis, output, mode, cval, a, b):
            sigma = [a, b / 2.0]
            input = numarray.asarray(input)
            order = [0] * input.ndim
            order[axis] = 2
            return nd_image.gaussian_filter(input, sigma, order,
                                           output, mode, cval)
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = numarray.zeros(array.shape, type)
            tmp = nd_image.generic_laplace(array, derivative2,
                    extra_arguments = (1.0,), extra_keywords = {'b': 2.0})
            nd_image.gaussian_laplace(array, 1.0, output)
            self.failUnless(diff(tmp, output) < eps)

    def test_gaussian_gradient_magnitude01(self):
        "gaussian gradient magnitude filter 1"
        for type in [numarray.int32, numarray.float32, numarray.float64]:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = nd_image.gaussian_filter(array, 1.0, [1, 0])
            tmp2 = nd_image.gaussian_filter(array, 1.0, [0, 1])
            output = nd_image.gaussian_gradient_magnitude(array,
                                                                       1.0)
            true = tmp1 * tmp1 + tmp2 * tmp2
            numarray.sqrt(true, true)
            self.failUnless(diff(true, output) < eps)

    def test_gaussian_gradient_magnitude02(self):
        "gaussian gradient magnitude filter 2"
        for type in [numarray.int32, numarray.float32, numarray.float64]:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = nd_image.gaussian_filter(array, 1.0, [1, 0])
            tmp2 = nd_image.gaussian_filter(array, 1.0, [0, 1])
            output = numarray.zeros(array.shape, type)
            nd_image.gaussian_gradient_magnitude(array, 1.0,
                                                           output)
            true = tmp1 * tmp1 + tmp2 * tmp2
            numarray.sqrt(true, true)
            self.failUnless(diff(true, output) < eps)

    def test_generic_gradient_magnitude01(self):
        "generic gradient magnitude 1"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [5, 8, 3, 7, 1],
                                [5, 6, 9, 3, 5]], numarray.float64)
        def derivative(input, axis, output, mode, cval, a, b):
            sigma = [a, b / 2.0]
            input = numarray.asarray(input)
            order = [0] * input.ndim
            order[axis] = 1
            return nd_image.gaussian_filter(input, sigma, order,
                                        output, mode, cval)
        tmp1 = nd_image.gaussian_gradient_magnitude(array, 1.0)
        tmp2 = nd_image.generic_gradient_magnitude(array,
                derivative, extra_arguments = (1.0,),
                extra_keywords = {'b': 2.0})
        self.failUnless(diff(tmp1, tmp2) < eps)

    def test_uniform01(self):
        "uniform filter 1"
        array = numarray.array([2, 4, 6])
        size = 2
        output = nd_image.uniform_filter1d(array, size,
                                                   origin = -1)
        self.failUnless(diff([3, 5, 6], output) < eps)

    def test_uniform02(self):
        "uniform filter 2"
        array = numarray.array([1, 2, 3])
        filter_shape = [0]
        output = nd_image.uniform_filter(array, filter_shape)
        self.failUnless(diff(array, output) < eps)

    def test_uniform03(self):
        "uniform filter 3"
        array = numarray.array([1, 2, 3])
        filter_shape = [1]
        output = nd_image.uniform_filter(array, filter_shape)
        self.failUnless(diff(array, output) < eps)

    def test_uniform04(self):
        "uniform filter 4"
        array = numarray.array([2, 4, 6])
        filter_shape = [2]
        output = nd_image.uniform_filter(array, filter_shape)
        self.failUnless(diff([2, 3, 5], output) < eps)

    def test_uniform05(self):
        "uniform filter 5"
        array = []
        filter_shape = [1]
        output = nd_image.uniform_filter(array, filter_shape)
        self.failUnless(diff([], output) < eps)

    def test_uniform06(self):
        "uniform filter 6"
        filter_shape = [2, 2]
        for type1 in self.types:
            array = numarray.array([[4, 8, 12],
                                    [16, 20, 24]], type1)
            for type2 in self.types:
                output = nd_image.uniform_filter(array,
                                        filter_shape, output = type2)
                error = diff([[4, 6, 10], [10, 12, 16]], output)
                self.failUnless(error < eps and output.dtype.type == type2)

    def test_minimum_filter01(self):
        "minimum filter 1"
        array = numarray.array([1, 2, 3, 4, 5])
        filter_shape = numarray.array([2])
        output = nd_image.minimum_filter(array, filter_shape)
        self.failUnless(diff([1, 1, 2, 3, 4], output) < eps)

    def test_minimum_filter02(self):
        "minimum filter 2"
        array = numarray.array([1, 2, 3, 4, 5])
        filter_shape = numarray.array([3])
        output = nd_image.minimum_filter(array, filter_shape)
        self.failUnless(diff([1, 1, 2, 3, 4], output) < eps)

    def test_minimum_filter03(self):
        "minimum filter 3"
        array = numarray.array([3, 2, 5, 1, 4])
        filter_shape = numarray.array([2])
        output = nd_image.minimum_filter(array, filter_shape)
        self.failUnless(diff([3, 2, 2, 1, 1], output) < eps)

    def test_minimum_filter04(self):
        "minimum filter 4"
        array = numarray.array([3, 2, 5, 1, 4])
        filter_shape = numarray.array([3])
        output = nd_image.minimum_filter(array, filter_shape)
        self.failUnless(diff([2, 2, 1, 1, 1], output) < eps)

    def test_minimum_filter05(self):
        "minimum filter 5"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        filter_shape = numarray.array([2, 3])
        output = nd_image.minimum_filter(array, filter_shape)
        self.failUnless(diff([[2, 2, 1, 1, 1],
                              [2, 2, 1, 1, 1],
                              [5, 3, 3, 1, 1]], output) < eps)

    def test_minimum_filter06(self):
        "minimum filter 6"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 1, 1], [1, 1, 1]]
        output = nd_image.minimum_filter(array,
                                                 footprint = footprint)
        self.failUnless(diff([[2, 2, 1, 1, 1],
                              [2, 2, 1, 1, 1],
                              [5, 3, 3, 1, 1]], output) < eps)

    def test_minimum_filter07(self):
        "minimum filter 7"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = nd_image.minimum_filter(array,
                                                 footprint = footprint)
        self.failUnless(diff([[2, 2, 1, 1, 1],
                              [2, 3, 1, 3, 1],
                              [5, 5, 3, 3, 1]], output) < eps)

    def test_minimum_filter08(self):
        "minimum filter 8"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = nd_image.minimum_filter(array,
                                       footprint = footprint, origin = -1)
        self.failUnless(diff([[3, 1, 3, 1, 1],
                              [5, 3, 3, 1, 1],
                              [3, 3, 1, 1, 1]], output) < eps)

    def test_minimum_filter09(self):
        "minimum filter 9"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = nd_image.minimum_filter(array,
                                  footprint = footprint, origin = [-1, 0])
        self.failUnless(diff([[2, 3, 1, 3, 1],
                              [5, 5, 3, 3, 1],
                              [5, 3, 3, 1, 1]], output) < eps)

    def test_maximum_filter01(self):
        "maximum filter 1"
        array = numarray.array([1, 2, 3, 4, 5])
        filter_shape = numarray.array([2])
        output = nd_image.maximum_filter(array, filter_shape)
        self.failUnless(diff([1, 2, 3, 4, 5], output) < eps)

    def test_maximum_filter02(self):
        "maximum filter 2"
        array = numarray.array([1, 2, 3, 4, 5])
        filter_shape = numarray.array([3])
        output = nd_image.maximum_filter(array, filter_shape)
        self.failUnless(diff([2, 3, 4, 5, 5], output) < eps)

    def test_maximum_filter03(self):
        "maximum filter 3"
        array = numarray.array([3, 2, 5, 1, 4])
        filter_shape = numarray.array([2])
        output = nd_image.maximum_filter(array, filter_shape)
        self.failUnless(diff([3, 3, 5, 5, 4], output) < eps)

    def test_maximum_filter04(self):
        "maximum filter 4"
        array = numarray.array([3, 2, 5, 1, 4])
        filter_shape = numarray.array([3])
        output = nd_image.maximum_filter(array, filter_shape)
        self.failUnless(diff([3, 5, 5, 5, 4], output) < eps)

    def test_maximum_filter05(self):
        "maximum filter 5"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        filter_shape = numarray.array([2, 3])
        output = nd_image.maximum_filter(array, filter_shape)
        self.failUnless(diff([[3, 5, 5, 5, 4],
                              [7, 9, 9, 9, 5],
                              [8, 9, 9, 9, 7]], output) < eps)

    def test_maximum_filter06(self):
        "maximum filter 6"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 1, 1], [1, 1, 1]]
        output = nd_image.maximum_filter(array,
                                                 footprint = footprint)
        self.failUnless(diff([[3, 5, 5, 5, 4],
                              [7, 9, 9, 9, 5],
                              [8, 9, 9, 9, 7]], output) < eps)

    def test_maximum_filter07(self):
        "maximum filter 7"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = nd_image.maximum_filter(array,
                                                 footprint = footprint)
        self.failUnless(diff([[3, 5, 5, 5, 4],
                              [7, 7, 9, 9, 5],
                              [7, 9, 8, 9, 7]], output) < eps)

    def test_maximum_filter08(self):
        "maximum filter 8"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = nd_image.maximum_filter(array,
                                      footprint = footprint, origin = -1)
        self.failUnless(diff([[7, 9, 9, 5, 5],
                              [9, 8, 9, 7, 5],
                              [8, 8, 7, 7, 7]], output) < eps)

    def test_maximum_filter09(self):
        "maximum filter 9"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = nd_image.maximum_filter(array,
                                 footprint = footprint, origin = [-1, 0])
        self.failUnless(diff([[7, 7, 9, 9, 5],
                              [7, 9, 8, 9, 7],
                              [8, 8, 8, 7, 7]], output) < eps)

    def test_rank01(self):
        "rank filter 1"
        array = numarray.array([1, 2, 3, 4, 5])
        output = nd_image.rank_filter(array, 1, size = 2)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.percentile_filter(array, 100, size = 2)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.median_filter(array, 2)
        self.failUnless(diff(array, output) < eps)

    def test_rank02(self):
        "rank filter 2"
        array = numarray.array([1, 2, 3, 4, 5])
        output = nd_image.rank_filter(array, 1, size = [3])
        self.failUnless(diff(array, output) < eps)
        output = nd_image.percentile_filter(array, 50, size = 3)
        self.failUnless(diff(array, output) < eps)
        output = nd_image.median_filter(array, (3,))
        self.failUnless(diff(array, output) < eps)

    def test_rank03(self):
        "rank filter 3"
        array = numarray.array([3, 2, 5, 1, 4])
        output = nd_image.rank_filter(array, 1, size = [2])
        self.failUnless(diff([3, 3, 5, 5, 4], output) < eps)
        output = nd_image.percentile_filter(array, 100, size = 2)
        self.failUnless(diff([3, 3, 5, 5, 4], output) < eps)

    def test_rank04(self):
        "rank filter 4"
        array = numarray.array([3, 2, 5, 1, 4])
        true = [3, 3, 2, 4, 4]
        output = nd_image.rank_filter(array, 1, size = 3)
        self.failUnless(diff(true, output) < eps)
        output = nd_image.percentile_filter(array, 50, size = 3)
        self.failUnless(diff(true, output) < eps)
        output = nd_image.median_filter(array, size = 3)
        self.failUnless(diff(true, output) < eps)

    def test_rank05(self):
        "rank filter 5"
        array = numarray.array([3, 2, 5, 1, 4])
        true = [3, 3, 2, 4, 4]
        output = nd_image.rank_filter(array, -2, size = 3)
        self.failUnless(diff(true, output) < eps)

    def test_rank06(self):
        "rank filter 6"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [5, 8, 3, 7, 1],
                                [5, 6, 9, 3, 5]])
        true = [[2, 2, 1, 1, 1],
                [3, 3, 2, 1, 1],
                [5, 5, 3, 3, 1]]
        output = nd_image.rank_filter(array, 1, size = [2, 3])
        self.failUnless(diff(true, output) < eps)
        output = nd_image.percentile_filter(array, 17,
                                                    size = (2, 3))
        self.failUnless(diff(true, output) < eps)

    def test_rank07(self):
        "rank filter 7"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [5, 8, 3, 7, 1],
                                [5, 6, 9, 3, 5]])
        true = [[3, 5, 5, 5, 4],
                [5, 5, 7, 5, 4],
                [6, 8, 8, 7, 5]]
        output = nd_image.rank_filter(array, -2, size = [2, 3])
        self.failUnless(diff(true, output) < eps)

    def test_rank08(self):
        "median filter 8"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [5, 8, 3, 7, 1],
                                [5, 6, 9, 3, 5]])
        true = [[3, 3, 2, 4, 4],
                [5, 5, 5, 4, 4],
                [5, 6, 7, 5, 5]]
        kernel = numarray.array([2, 3])
        output = nd_image.percentile_filter(array, 50.0,
                                                    size = (2, 3))
        self.failUnless(diff(true, output) < eps)
        output = nd_image.rank_filter(array, 3, size = (2, 3))
        self.failUnless(diff(true, output) < eps)
        output = nd_image.median_filter(array, size = (2, 3))
        self.failUnless(diff(true, output) < eps)

    def test_rank09(self):
        "rank filter 9"
        true = [[3, 3, 2, 4, 4],
                [3, 5, 2, 5, 1],
                [5, 5, 8, 3, 5]]
        footprint = [[1, 0, 1], [0, 1, 0]]
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = nd_image.rank_filter(array, 1,
                                                  footprint = footprint)
            self.failUnless(diff(true, output) < eps)
            output = nd_image.percentile_filter(array, 35,
                                                    footprint = footprint)
            self.failUnless(diff(true, output) < eps)

    def test_rank10(self):
        "rank filter 10"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        true = [[2, 2, 1, 1, 1],
                [2, 3, 1, 3, 1],
                [5, 5, 3, 3, 1]]
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = nd_image.rank_filter(array, 0,
                                              footprint = footprint)
        self.failUnless(diff(true, output) < eps)
        output = nd_image.percentile_filter(array, 0.0,
                                                    footprint = footprint)
        self.failUnless(diff(true, output) < eps)

    def test_rank11(self):
        "rank filter 11"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        true = [[3, 5, 5, 5, 4],
                [7, 7, 9, 9, 5],
                [7, 9, 8, 9, 7]]
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = nd_image.rank_filter(array, -1,
                                              footprint = footprint)
        self.failUnless(diff(true, output) < eps)
        output = nd_image.percentile_filter(array, 100.0,
                                                    footprint = footprint)
        self.failUnless(diff(true, output) < eps)


    def test_rank12(self):
        "rank filter 12"
        true = [[3, 3, 2, 4, 4],
                [3, 5, 2, 5, 1],
                [5, 5, 8, 3, 5]]
        footprint = [[1, 0, 1], [0, 1, 0]]
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = nd_image.rank_filter(array, 1,
                                                  footprint = footprint)
            self.failUnless(diff(true, output) < eps)
            output = nd_image.percentile_filter(array, 50.0,
                                                     footprint = footprint)
            self.failUnless(diff(true, output) < eps)
            output = nd_image.median_filter(array,
                                                    footprint = footprint)
            self.failUnless(diff(true, output) < eps)

    def test_rank13(self):
        "rank filter 13"
        true = [[5, 2, 5, 1, 1],
                [5, 8, 3, 5, 5],
                [6, 6, 5, 5, 5]]
        footprint = [[1, 0, 1], [0, 1, 0]]
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = nd_image.rank_filter(array, 1,
                                       footprint = footprint, origin = -1)
            self.failUnless(diff(true, output) < eps)

    def test_rank14(self):
        "rank filter 14"
        true = [[3, 5, 2, 5, 1],
                [5, 5, 8, 3, 5],
                [5, 6, 6, 5, 5]]
        footprint = [[1, 0, 1], [0, 1, 0]]
        for type in self.types:
            array = numarray.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = nd_image.rank_filter(array, 1,
                                  footprint = footprint, origin = [-1, 0])
            self.failUnless(diff(true, output) < eps)

    def test_generic_filter1d01(self):
        "generic 1d filter 1"
        weights = numarray.array([1.1, 2.2, 3.3])
        def _filter_func(input, output, fltr, total):
            fltr = fltr / total
            for ii in range(input.shape[0] - 2):
                output[ii] = input[ii] * fltr[0]
                output[ii] += input[ii + 1] * fltr[1]
                output[ii] += input[ii + 2] * fltr[2]
        for type in self.types:
            a = numarray.arange(12, dtype = type)
            a.shape = (3,4)
            r1 = nd_image.correlate1d(a, weights / weights.sum(), 0,
                                              origin = -1)
            r2 = nd_image.generic_filter1d(a, _filter_func, 3,
                      axis = 0, origin = -1, extra_arguments = (weights,),
                      extra_keywords = {'total': weights.sum()})
            self.failUnless(diff(r1, r2) < eps)

    def test_generic_filter01(self):
        "generic filter 1"
        filter = numarray.array([[1.0, 2.0], [3.0, 4.0]])
        footprint = numarray.array([[1, 0], [0, 1]])
        cf = numarray.array([1., 4.])
        def _filter_func(buffer, weights, total = 1.0):
            weights = cf / total
            return (buffer * weights).sum()
        for type in self.types:
            a = numarray.arange(12, dtype = type)
            a.shape = (3,4)
            r1 = nd_image.correlate(a, filter * footprint) / 5
            r2 = nd_image.generic_filter(a, _filter_func,
                            footprint = footprint, extra_arguments = (cf,),
                            extra_keywords = {'total': cf.sum()})
            self.failUnless(diff(r1, r2) < eps)

    def test_extend01(self):
        "line extension 1"
        array = numarray.array([1, 2, 3])
        weights = numarray.array([1, 0])
        true_values = [[1, 1, 2],
                       [3, 1, 2],
                       [1, 1, 2],
                       [0, 1, 2]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate1d(array, weights, 0,
                                                   mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)

    def test_extend02(self):
        "line extension 2"
        array = numarray.array([1, 2, 3])
        weights = numarray.array([1, 0, 0, 0, 0, 0, 0, 0])
        true_values = [[1, 1, 1],
                       [3, 1, 2],
                       [3, 3, 2],
                       [0, 0, 0]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate1d(array, weights, 0,
                                                   mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)

    def test_extend03(self):
        "line extension 3"
        array = numarray.array([1, 2, 3])
        weights = numarray.array([0, 0, 1])
        true_values = [[2, 3, 3],
                       [2, 3, 1],
                       [2, 3, 3],
                       [2, 3, 0]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate1d(array, weights, 0,
                                                   mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)

    def test_extend04(self):
        "line extension 4"
        array = numarray.array([1, 2, 3])
        weights = numarray.array([0, 0, 0, 0, 0, 0, 0, 0, 1])
        true_values = [[3, 3, 3],
                       [2, 3, 1],
                       [2, 1, 1],
                       [0, 0, 0]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate1d(array, weights, 0,
                                                   mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)


    def test_extend05(self):
        "line extension 5"
        array = numarray.array([[1, 2, 3],
                                [4, 5, 6],
                                [7, 8, 9]])
        weights = numarray.array([[1, 0], [0, 0]])
        true_values = [[[1, 1, 2], [1, 1, 2], [4, 4, 5]],
                       [[9, 7, 8], [3, 1, 2], [6, 4, 5]],
                       [[1, 1, 2], [1, 1, 2], [4, 4, 5]],
                       [[0, 0, 0], [0, 1, 2], [0, 4, 5]]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate(array, weights,
                                                 mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)


    def test_extend06(self):
        "line extension 6"
        array = numarray.array([[1, 2, 3],
                                [4, 5, 6],
                                [7, 8, 9]])
        weights = numarray.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
        true_values = [[[5, 6, 6], [8, 9, 9], [8, 9, 9]],
                       [[5, 6, 4], [8, 9, 7], [2, 3, 1]],
                       [[5, 6, 6], [8, 9, 9], [8, 9, 9]],
                       [[5, 6, 0], [8, 9, 0], [0, 0, 0]]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate(array, weights,
                                                 mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)


    def test_extend07(self):
        "line extension 7"
        array = numarray.array([1, 2, 3])
        weights = numarray.array([0, 0, 0, 0, 0, 0, 0, 0, 1])
        true_values = [[3, 3, 3],
                       [2, 3, 1],
                       [2, 1, 1],
                       [0, 0, 0]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate(array, weights,
                                                 mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)

    def test_extend08(self):
        "line extension 8"
        array = numarray.array([[1], [2], [3]])
        weights = numarray.array([[0], [0], [0], [0], [0], [0], [0],
                                  [0], [1]])
        true_values = [[[3], [3], [3]],
                       [[2], [3], [1]],
                       [[2], [1], [1]],
                       [[0], [0], [0]]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate(array, weights,
                                                 mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)

    def test_extend09(self):
        "line extension 9"
        array = numarray.array([1, 2, 3])
        weights = numarray.array([0, 0, 0, 0, 0, 0, 0, 0, 1])
        true_values = [[3, 3, 3],
                       [2, 3, 1],
                       [2, 1, 1],
                       [0, 0, 0]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate(array, weights,
                                                 mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)

    def test_extend10(self):
        "line extension 10"
        array = numarray.array([[1], [2], [3]])
        weights = numarray.array([[0], [0], [0], [0], [0], [0], [0],
                                  [0], [1]])
        true_values = [[[3], [3], [3]],
                       [[2], [3], [1]],
                       [[2], [1], [1]],
                       [[0], [0], [0]]]
        for mode, true_value in zip(self.modes, true_values):
            output = nd_image.correlate(array, weights,
                                                 mode = mode, cval = 0)
            self.failUnless(diff(output, true_value) < eps)

    def test_fourier_gaussian_real01(self):
        "gaussian fourier filter for real transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numarray.float32, numarray.float64]:
                a = numarray.zeros(shape, type)
                a[0, 0] = 1.0
                a = dft.real_fft(a, shape[0], 0)
                a = dft.fft(a, shape[1], 1)
                a = nd_image.fourier_gaussian(a, [5.0, 2.5],
                                                       shape[0], 0)
                a = dft.inverse_fft(a, shape[1], 1)
                a = dft.inverse_real_fft(a, shape[0], 0)
                self.failUnless(diff(nd_image.sum(a), 1.0) < eps)

    def test_fourier_gaussian_complex01(self):
        "gaussian fourier filter for complex transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numarray.complex64, numarray.complex128]:
                a = numarray.zeros(shape, type)
                a[0, 0] = 1.0
                a = dft.fft(a, shape[0], 0)
                a = dft.fft(a, shape[1], 1)
                a = nd_image.fourier_gaussian(a, [5.0, 2.5], -1,
                                                       0)
                a = dft.inverse_fft(a, shape[1], 1)
                a = dft.inverse_fft(a, shape[0], 0)
                error = diff(nd_image.sum(a.real), 1.0)
                self.failUnless(error < eps)

    def test_fourier_uniform_real01(self):
        "uniform fourier filter for real transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numarray.float32, numarray.float64]:
                a = numarray.zeros(shape, type)
                a[0, 0] = 1.0
                a = dft.real_fft(a, shape[0], 0)
                a = dft.fft(a, shape[1], 1)
                a = nd_image.fourier_uniform(a, [5.0, 2.5],
                                                      shape[0], 0)
                a = dft.inverse_fft(a, shape[1], 1)
                a = dft.inverse_real_fft(a, shape[0], 0)
                self.failUnless(diff(nd_image.sum(a), 1.0) < eps)

    def test_fourier_uniform_complex01(self):
        "uniform fourier filter for complex transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numarray.complex64, numarray.complex128]:
                a = numarray.zeros(shape, type)
                a[0, 0] = 1.0
                a = dft.fft(a, shape[0], 0)
                a = dft.fft(a, shape[1], 1)
                a = nd_image.fourier_uniform(a, [5.0, 2.5], -1, 0)
                a = dft.inverse_fft(a, shape[1], 1)
                a = dft.inverse_fft(a, shape[0], 0)
                error = diff(nd_image.sum(a.real), 1.0)
                self.failUnless(error < eps)

    def test_fourier_shift_real01(self):
        "shift filter for real transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for dtype in [numarray.float32, numarray.float64]:
                true = numarray.arange(shape[0] * shape[1], dtype = dtype)
                true.shape = shape
                a = dft.real_fft(true, shape[0], 0)
                a = dft.fft(a, shape[1], 1)
                a = nd_image.fourier_shift(a, [1, 1], shape[0], 0)
                a = dft.inverse_fft(a, shape[1], 1)
                a = dft.inverse_real_fft(a, shape[0], 0)
                error1 = diff(a[1:, 1:], true[:-1, :-1])
                error2 = diff(a.imag, numarray.zeros(shape))
                self.failUnless(error1 < 1e-10 and error2 < 1e-10)

    def test_fourier_shift_complex01(self):
        "shift filter for complex transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numarray.complex64, numarray.complex128]:
                true = numarray.arange(shape[0] * shape[1],
                                       dtype = type)
                true.shape = shape
                a = dft.fft(true, shape[0], 0)
                a = dft.fft(a, shape[1], 1)
                a = nd_image.fourier_shift(a, [1, 1], -1, 0)
                a = dft.inverse_fft(a, shape[1], 1)
                a = dft.inverse_fft(a, shape[0], 0)
                error1 = diff(a.real[1:, 1:], true[:-1, :-1])
                error2 = diff(a.imag, numarray.zeros(shape))
                self.failUnless(error1 < 1e-10 and error2 < 1e-10)

    def test_fourier_ellipsoid_real01(self):
        "ellipsoid fourier filter for real transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numarray.float32, numarray.float64]:
                a = numarray.zeros(shape, type)
                a[0, 0] = 1.0
                a = dft.real_fft(a, shape[0], 0)
                a = dft.fft(a, shape[1], 1)
                a = nd_image.fourier_ellipsoid(a, [5.0, 2.5],
                                                        shape[0], 0)
                a = dft.inverse_fft(a, shape[1], 1)
                a = dft.inverse_real_fft(a, shape[0], 0)
                self.failUnless(diff(nd_image.sum(a), 1.0) < eps)

    def test_fourier_ellipsoid_complex01(self):
        "ellipsoid fourier filter for complex transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numarray.complex64, numarray.complex128]:
                a = numarray.zeros(shape, type)
                a[0, 0] = 1.0
                a = dft.fft(a, shape[0], 0)
                a = dft.fft(a, shape[1], 1)
                a = nd_image.fourier_ellipsoid(a, [5.0, 2.5], -1,
                                                        0)
                a = dft.inverse_fft(a, shape[1], 1)
                a = dft.inverse_fft(a, shape[0], 0)
                error = diff(nd_image.sum(a.real), 1.0)
                self.failUnless(error < eps)

    def test_spline01(self):
        "spline filter 1"
        for type in self.types:
            data = numarray.ones([], type)
            for order in range(2, 6):
                out = nd_image.spline_filter(data, order = order)
                self.failUnless(diff(out, 1)< eps and
                                out.dtype.type == numarray.float64)

    def test_spline02(self):
        "spline filter 2"
        for type in self.types:
            data = numarray.array([1])
            for order in range(2, 6):
                out = nd_image.spline_filter(data, order = order)
                self.failUnless(diff(out, [1]) < eps and
                                out.dtype.type == numarray.float64)

    def test_spline03(self):
        "spline filter 3"
        for type in self.types:
            data = numarray.ones([], type)
            for order in range(2, 6):
                out = nd_image.spline_filter(data, order,
                                                      output = type)
                self.failUnless(diff(out, 1) < eps and
                                out.dtype.type == type)

    def test_spline04(self):
        "spline filter 4"
        for type in self.types:
            data = numarray.ones([4], type)
            for order in range(2, 6):
                out = nd_image.spline_filter(data, order)
                self.failUnless(diff(out, [1, 1, 1, 1]) < eps)

    def test_spline05(self):
        "spline filter 5"
        for type in self.types:
            data = numarray.ones([4, 4], type)
            for order in range(2, 6):
                out = nd_image.spline_filter(data, order = order)
                self.failUnless(diff(out, [[1, 1, 1, 1],
                                           [1, 1, 1, 1],
                                           [1, 1, 1, 1],
                                           [1, 1, 1, 1]]) < eps)

    def test_geometric_transform01(self):
        "geometric transform 1"
        data = numarray.array([1])
        def mapping(x):
            return x
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                        data.shape,
                                                        order=order)
            self.failUnless(diff(out, [1]) < eps)

    def test_geometric_transform02(self):
        "geometric transform 2"
        data = numarray.ones([4])
        def mapping(x):
            return x
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                  data.shape, order=order)
            self.failUnless(diff(out, [1, 1, 1, 1]) < eps)

    def test_geometric_transform03(self):
        "geometric transform 3"
        data = numarray.ones([4])
        def mapping(x):
            return (x[0] - 1,)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            self.failUnless(diff(out, [0, 1, 1, 1]) < eps)

    def test_geometric_transform04(self):
        "geometric transform 4"
        data = numarray.array([4, 1, 3, 2])
        def mapping(x):
            return (x[0] - 1,)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            self.failUnless(diff(out, [0, 4, 1, 3]) < eps)

    def test_geometric_transform05(self):
        "geometric transform 5"
        data = numarray.array([[1, 1, 1, 1],
                               [1, 1, 1, 1],
                               [1, 1, 1, 1]])
        def mapping(x):
            return (x[0], x[1] - 1)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            self.failUnless(diff(out, [[0, 1, 1, 1],
                                       [0, 1, 1, 1],
                                       [0, 1, 1, 1]]) < eps)

    def test_geometric_transform06(self):
        "geometric transform 6"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        def mapping(x):
            return (x[0], x[1] - 1)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            self.failUnless(diff(out, [[0, 4, 1, 3],
                                       [0, 7, 6, 8],
                                       [0, 3, 5, 3]]) < eps)

    def test_geometric_transform07(self):
        "geometric transform 7"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        def mapping(x):
            return (x[0] - 1, x[1])
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [4, 1, 3, 2],
                                       [7, 6, 8, 5]]) < eps)

    def test_geometric_transform08(self):
        "geometric transform 8"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        def mapping(x):
            return (x[0] - 1, x[1] - 1)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]]) < eps)

    def test_geometric_transform10(self):
        "geometric transform 10"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        def mapping(x):
            return (x[0] - 1, x[1] - 1)
        for order in range(0, 6):
            if (order > 1):
                filtered = nd_image.spline_filter(data,
                                                           order=order)
            else:
                filtered = data
            out = nd_image.geometric_transform(filtered, mapping,
                               data.shape, order=order, prefilter = False)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]]) < eps)

    def test_geometric_transform13(self):
        "geometric transform 13"
        data = numarray.ones([2], numarray.float64)
        def mapping(x):
            return (x[0] / 2,)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                        [4], order=order)
            self.failUnless(diff(out, [1, 1, 1, 1]) < eps)

    def test_geometric_transform14(self):
        "geometric transform 14"
        data = [1, 5, 2, 6, 3, 7, 4, 4]
        def mapping(x):
            return (2 * x[0],)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                        [4], order=order)
            self.failUnless(diff(out, [1, 2, 3, 4]) < eps)

    def test_geometric_transform15(self):
        "geometric transform 15"
        data = [1, 2, 3, 4]
        def mapping(x):
            return (x[0] / 2,)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                        [8], order=order)
            self.failUnless(diff(out[::2], [1, 2, 3, 4]) < eps)

    def test_geometric_transform16(self):
        "geometric transform 16"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9.0, 10, 11, 12]]
        def mapping(x):
            return (x[0], x[1] * 2)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                       (3, 2), order=order)
            self.failUnless(diff(out, [[1, 3], [5, 7], [9, 11]]) < eps)

    def test_geometric_transform17(self):
        "geometric transform 17"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0] * 2, x[1])
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                       (1, 4), order=order)
            self.failUnless(diff(out, [[1, 2, 3, 4]]) < eps)

    def test_geometric_transform18(self):
        "geometric transform 18"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0] * 2, x[1] * 2)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                       (1, 2), order=order)
            self.failUnless(diff(out, [[1, 3]]) < eps)

    def test_geometric_transform19(self):
        "geometric transform 19"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0], x[1] / 2)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                       (3, 8), order=order)
            self.failUnless(diff(out[..., ::2], data) < eps)

    def test_geometric_transform20(self):
        "geometric transform 20"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0] / 2, x[1])
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                       (6, 4), order=order)
            self.failUnless(diff(out[::2, ...], data) < eps)

    def test_geometric_transform21(self):
        "geometric transform 21"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0] / 2, x[1] / 2)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                      (6, 8), order=order)
            self.failUnless(diff(out[::2, ::2], data) < eps)


    def test_geometric_transform22(self):
        "geometric transform 22"
        data = numarray.array([[1, 2, 3, 4],
                               [5, 6, 7, 8],
                               [9, 10, 11, 12]], numarray.float64)
        def mapping1(x):
            return (x[0] / 2, x[1] / 2)
        def mapping2(x):
            return (x[0] * 2, x[1] * 2)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping1,
                                                      (6, 8),  order=order)
            out = nd_image.geometric_transform(out, mapping2,
                                                       (3, 4), order=order)
            error = diff(out, data)
            self.failUnless(diff(out, data) < eps)

    def test_geometric_transform23(self):
        "geometric transform 23"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (1, x[0] * 2)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                                        (2,), order=order)
            out = out.astype(numarray.int32)
            self.failUnless(diff(out, [5, 7]) < eps)

    def test_geometric_transform24(self):
        "geometric transform 24"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x, a, b):
            return (a, x[0] * b)
        for order in range(0, 6):
            out = nd_image.geometric_transform(data, mapping,
                                (2,), order=order, extra_arguments = (1,),
                                extra_keywords = {'b': 2})
            self.failUnless(diff(out, [5, 7]) < eps)

    def test_map_coordinates01(self):
        "map coordinates 1"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        idx = numarray.indices(data.shape)
        idx -= 1
        for order in range(0, 6):
            out = nd_image.map_coordinates(data, idx, order=order)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]]) < eps)

    def test_map_coordinates02(self):
        "map coordinates 2"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        idx = numarray.indices(data.shape, numarray.float64)
        idx -= 0.5
        for order in range(0, 6):
            out1 = nd_image.shift(data, 0.5, order=order)
            out2 = nd_image.map_coordinates(data, idx,
                                                     order=order)
            self.failUnless(diff(out1, out2) < eps)

    def test_affine_transform01(self):
        "affine_transform 1"
        data = numarray.array([1])
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1]],
                                                     order=order)
            self.failUnless(diff(out, [1]) < eps)

    def test_affine_transform02(self):
        "affine transform 2"
        data = numarray.ones([4])
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1]],
                                                     order=order)
            self.failUnless(diff(out, [1, 1, 1, 1]) < eps)

    def test_affine_transform03(self):
        "affine transform 3"
        data = numarray.ones([4])
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1]], -1,
                                                     order=order)
            self.failUnless(diff(out, [0, 1, 1, 1]) < eps)

    def test_affine_transform04(self):
        "affine transform 4"
        data = numarray.array([4, 1, 3, 2])
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1]], -1,
                                                     order=order)
            self.failUnless(diff(out, [0, 4, 1, 3]) < eps)

    def test_affine_transform05(self):
        "affine transform 5"
        data = numarray.array([[1, 1, 1, 1],
                               [1, 1, 1, 1],
                               [1, 1, 1, 1]])
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1, 0],
                                                            [0, 1]],
                                                     [0, -1], order=order)
            self.failUnless(diff(out, [[0, 1, 1, 1],
                                       [0, 1, 1, 1],
                                       [0, 1, 1, 1]]) < eps)

    def test_affine_transform06(self):
        "affine transform 6"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1, 0],
                                                            [0, 1]],
                                                     [0, -1], order=order)
            self.failUnless(diff(out, [[0, 4, 1, 3],
                                       [0, 7, 6, 8],
                                       [0, 3, 5, 3]]) < eps)

    def test_affine_transform07(self):
        "affine transform 7"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1, 0],
                                                            [0, 1]],
                                                     [-1, 0], order=order)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [4, 1, 3, 2],
                                       [7, 6, 8, 5]]) < eps)

    def test_affine_transform08(self):
        "affine transform 8"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1, 0],
                                                            [0, 1]],
                                                     [-1, -1], order=order)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]]) < eps)

    def test_affine_transform09(self):
        "affine transform 9"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            if (order > 1):
                filtered = nd_image.spline_filter(data,
                                                           order=order)
            else:
                filtered = data
            out = nd_image.affine_transform(filtered,[[1, 0],
                                                               [0, 1]],
                                  [-1, -1], order=order, prefilter = False)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]]) < eps)

    def test_affine_transform10(self):
        "affine transform 10"
        data = numarray.ones([2], numarray.float64)
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[0.5]],
                                          output_shape = (4,), order=order)
            self.failUnless(diff(out, [1, 1, 1, 1]) < eps)

    def test_affine_transform11(self):
        "affine transform 11"
        data = [1, 5, 2, 6, 3, 7, 4, 4]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[2]], 0, (4,),
                                                     order=order)
            self.failUnless(diff(out, [1, 2, 3, 4]) < eps)

    def test_affine_transform12(self):
        "affine transform 12"
        data = [1, 2, 3, 4]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[0.5]], 0,
                                                     (8,), order=order)
            self.failUnless(diff(out[::2], [1, 2, 3, 4]) < eps)

    def test_affine_transform13(self):
        "affine transform 13"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9.0, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1, 0],
                                                            [0, 2]], 0,
                                                     (3, 2), order=order)
            self.failUnless(diff(out, [[1, 3], [5, 7], [9, 11]]) < eps)

    def test_affine_transform14(self):
        "affine transform 14"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[2, 0],
                                                            [0, 1]], 0,
                                                     (1, 4), order=order)
            self.failUnless(diff(out, [[1, 2, 3, 4]]) < eps)

    def test_affine_transform15(self):
        "affine transform 15"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[2, 0],
                                                            [0, 2]], 0,
                                                     (1, 2), order=order)
            self.failUnless(diff(out, [[1, 3]]) < eps)

    def test_affine_transform16(self):
        "affine transform 16"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[1, 0.0],
                                                            [0, 0.5]], 0,
                                                     (3, 8), order=order)
            self.failUnless(diff(out[..., ::2], data) < eps)

    def test_affine_transform17(self):
        "affine transform 17"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[0.5, 0],
                                                            [0,   1]], 0,
                                                     (6, 4), order=order)
            self.failUnless(diff(out[::2, ...], data) < eps)

    def test_affine_transform18(self):
        "affine transform 18"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.affine_transform(data,
                                                     [[0.5, 0],
                                                      [0, 0.5]], 0,
                                                     (6, 8), order=order)
            self.failUnless(diff(out[::2, ::2], data) < eps)

    def test_affine_transform19(self):
        "affine transform 19"
        data = numarray.array([[1, 2, 3, 4],
                               [5, 6, 7, 8],
                               [9, 10, 11, 12]], numarray.float64)
        for order in range(0, 6):
            out = nd_image.affine_transform(data,
                                                     [[0.5, 0],
                                                      [0, 0.5]], 0,
                                                     (6, 8), order=order)
            out = nd_image.affine_transform(out,
                                                     [[2.0, 0],
                                                      [0, 2.0]], 0,
                                                     (3, 4), order=order)
            self.failUnless(diff(out, data) < eps)

    def test_affine_transform20(self):
        "affine transform 20"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[0], [2]], 0,
                                                     (2,), order=order)
            self.failUnless(diff(out, [1, 3]) < eps)

    def test_affine_transform21(self):
        "affine transform 21"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [[2], [0]], 0,
                                                     (2,), order=order)
            self.failUnless(diff(out, [1, 9]) < eps)

    def test_shift01(self):
        "shift 1"
        data = numarray.array([1])
        for order in range(0, 6):
            out = nd_image.shift(data, [1], order=order)
            self.failUnless(diff(out, [0]) < eps)

    def test_shift02(self):
        "shift 2"
        data = numarray.ones([4])
        for order in range(0, 6):
            out = nd_image.shift(data, [1], order=order)
            self.failUnless(diff(out, [0, 1, 1, 1]) < eps)

    def test_shift03(self):
        "shift 3"
        data = numarray.ones([4])
        for order in range(0, 6):
            out = nd_image.shift(data, -1, order=order)
            self.failUnless(diff(out, [1, 1, 1, 0]) < eps)

    def test_shift04(self):
        "shift 4"
        data = numarray.array([4, 1, 3, 2])
        for order in range(0, 6):
            out = nd_image.shift(data, 1, order=order)
            self.failUnless(diff(out, [0, 4, 1, 3]) < eps)

    def test_shift05(self):
        "shift 5"
        data = numarray.array([[1, 1, 1, 1],
                               [1, 1, 1, 1],
                               [1, 1, 1, 1]])
        for order in range(0, 6):
            out = nd_image.shift(data, [0, 1], order=order)
            self.failUnless(diff(out, [[0, 1, 1, 1],
                                       [0, 1, 1, 1],
                                       [0, 1, 1, 1]]) < eps)

    def test_shift06(self):
        "shift 6"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = nd_image.shift(data, [0, 1], order=order)
            self.failUnless(diff(out, [[0, 4, 1, 3],
                                       [0, 7, 6, 8],
                                       [0, 3, 5, 3]]) < eps)

    def test_shift07(self):
        "shift 7"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = nd_image.shift(data, [1, 0], order=order)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [4, 1, 3, 2],
                                       [7, 6, 8, 5]]) < eps)


    def test_shift08(self):
        "shift 8"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = nd_image.shift(data, [1, 1], order=order)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]]) < eps)

    def test_shift09(self):
        "shift 9"
        data = numarray.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            if (order > 1):
                filtered = nd_image.spline_filter(data,
                                                           order=order)
            else:
                filtered = data
            out = nd_image.shift(filtered, [1, 1], order=order,
                                          prefilter = False)
            self.failUnless(diff(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]]) < eps)

    def test_zoom01(self):
        "zoom 1"
        data = numarray.ones([2], numarray.float64)
        for order in range(0, 6):
            out = nd_image.zoom(data, 2.0, order=order)
            self.failUnless(diff(out, [1, 1, 1, 1]) < eps)

    def test_zoom02(self):
        "zoom 2"
        data = [1, 5, 2, 6, 3, 7, 4, 4]
        for order in range(0, 6):
            out = nd_image.zoom(data, 0.5, order=order)
            self.failUnless(diff(out, [1, 2, 3, 4]) < eps)

    def test_zoom03(self):
        "zoom 3"
        data = [1, 2, 3, 4]
        for order in range(0, 6):
            out = nd_image.zoom(data, 2, order=order)
            self.failUnless(diff(out[::2], [1, 2, 3, 4]) < eps)

    def test_zoom04(self):
        "zoom 4"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9.0, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.zoom(data, [1, 0.5], order=order)
            self.failUnless(diff(out, [[1, 3], [5, 7], [9, 11]]) < eps)

    def test_zoom05(self):
        "zoom 5"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.zoom(data, [0.5, 1], order=order)
            self.failUnless(diff(out, [[1, 2, 3, 4]]) < eps)

    def test_zoom06(self):
        "zoom 6"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.zoom(data, [0.5, 0.5], order=order)
            self.failUnless(diff(out, [[1, 3]]) < eps)

    def test_zoom07(self):
        "zoom 7"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.zoom(data, [1, 2], order=order)
            self.failUnless(diff(out[..., ::2], data) < eps)

    def test_zoom08(self):
        "zoom 8"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.zoom(data, [2, 1], order=order)
            self.failUnless(diff(out[::2, ...], data) < eps)

    def test_zoom09(self):
        "zoom 9"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.zoom(data, [2, 2], order=order)
            self.failUnless(diff(out[::2, ::2], data) < eps)

    def test_zoom10(self):
        "zoom 10"
        data = numarray.array([[1, 2, 3, 4],
                               [5, 6, 7, 8],
                               [9, 10, 11, 12]], numarray.float64)
        for order in range(0, 6):
            out = nd_image.zoom(data, [2, 2], order=order)
            out = nd_image.zoom(out, [0.5, 0.5], order=order)
            self.failUnless(diff(out, data) < eps)

    def test_zoom_affine01(self):
        "zoom by affine transformation 1"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = nd_image.affine_transform(data, [0.5, 0.5], 0,
                                                     (6, 8), order=order)
            self.failUnless(diff(out[::2, ::2], data) < eps)

    def test_rotate01(self):
        "rotate 1"
        data = numarray.array([[0, 0, 0, 0],
                               [0, 1, 1, 0],
                               [0, 0, 0, 0]], dtype = numarray.float64)
        for order in range(0, 6):
            out = nd_image.rotate(data, 0)
            self.failUnless(diff(out, data) < eps)

    def test_rotate02(self):
        "rotate 2"
        data = numarray.array([[0, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]], dtype = numarray.float64)
        true = numarray.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 1, 0],
                               [0, 0, 0]], dtype = numarray.float64)
        for order in range(0, 6):
            out = nd_image.rotate(data, 90)
            self.failUnless(diff(out, true) < eps)

    def test_rotate03(self):
        "rotate 3"
        data = numarray.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0]], dtype = numarray.float64)
        true = numarray.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 1, 0],
                               [0, 1, 0],
                               [0, 0, 0]], dtype = numarray.float64)
        for order in range(0, 6):
            out = nd_image.rotate(data, 90)
            self.failUnless(diff(out, true) < eps)

    def test_rotate04(self):
        "rotate 4"
        data = numarray.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0]], dtype = numarray.float64)
        true = numarray.array([[0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0]], dtype = numarray.float64)
        for order in range(0, 6):
            out = nd_image.rotate(data, 90, reshape = False)
            self.failUnless(diff(out, true) < eps)

    def test_rotate05(self):
        "rotate 5"
        data = numarray.array([[[0, 0, 0, 0, 0],
                                [0, 1, 1, 0, 0],
                                [0, 0, 0, 0, 0]]] * 3,
                              dtype = numarray.float64)
        true = numarray.array([[[0, 0, 0],
                                [0, 0, 0],
                                [0, 1, 0],
                                [0, 1, 0],
                                [0, 0, 0]]] * 3, dtype = numarray.float64)
        for order in range(0, 6):
            out = nd_image.rotate(data, 90)
            self.failUnless(diff(out, true) < eps)

    def test_rotate06(self):
        "rotate 6"
        data = numarray.array([[[0, 0, 0, 0, 0],
                                [0, 1, 1, 0, 0],
                                [0, 0, 0, 0, 0]]] * 3,
                              dtype = numarray.float64)
        true = numarray.array([[[0, 0, 0, 0, 0],
                                [0, 0, 1, 0, 0],
                                [0, 0, 1, 0, 0]]] * 3,
                              dtype = numarray.float64)
        for order in range(0, 6):
            out = nd_image.rotate(data, 90, reshape = False)
            self.failUnless(diff(out, true) < eps)

    def test_rotate07(self):
        "rotate 7"
        data = numarray.array([[[0, 0, 0, 0, 0],
                                [0, 1, 1, 0, 0],
                                [0, 0, 0, 0, 0]]] * 2,
                              dtype = numarray.float64)
        data = data.transpose()
        true = numarray.array([[[0, 0, 0],
                                [0, 1, 0],
                                [0, 1, 0],
                                [0, 0, 0],
                                [0, 0, 0]]] * 2, dtype = numarray.float64)
        true = true.transpose([2,1,0])

        for order in range(0, 6):
            out = nd_image.rotate(data, 90, axes = (0, 1))
            self.failUnless(diff(out, true) < eps)

    def test_rotate08(self):
        "rotate 8"
        data = numarray.array([[[0, 0, 0, 0, 0],
                                [0, 1, 1, 0, 0],
                                [0, 0, 0, 0, 0]]] * 2,
                              dtype = numarray.float64)
        data = data.transpose()
        true = numarray.array([[[0, 0, 1, 0, 0],
                                [0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 0]]] * 2,
                              dtype = numarray.float64)
        true = true.transpose()
        for order in range(0, 6):
            out = nd_image.rotate(data, 90, axes = (0, 1),
                                           reshape = False)
            self.failUnless(diff(out, true) < eps)

    def test_watershed_ift01(self):
        "watershed_ift 1"
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.uint8)
        markers = numarray.array([[ -1, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 1, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0]],
                                 numarray.int8)
        out = nd_image.watershed_ift(data, markers,
                                     structure = [[1,1,1],
                                                  [1,1,1],
                                                  [1,1,1]])
        error = diff([[-1, -1, -1, -1, -1, -1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1]], out)
        self.failUnless(error < eps)

    def test_watershed_ift02(self):
        "watershed_ift 2"
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.uint8)
        markers = numarray.array([[ -1, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 1, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0]],
                                 numarray.int8)
        out = nd_image.watershed_ift(data, markers)
        error = diff([[-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1,  1,  1,  1, -1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1, -1,  1,  1,  1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1]], out)
        self.failUnless(error < eps)

    def test_watershed_ift03(self):
        "watershed_ift 3"
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.uint8)
        markers = numarray.array([[ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 2, 0, 3, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, -1]],
                                 numarray.int8)
        out = nd_image.watershed_ift(data, markers)
        error = diff([[-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1,  2, -1,  3, -1, -1],
                      [-1,  2,  2,  3,  3,  3, -1],
                      [-1,  2,  2,  3,  3,  3, -1],
                      [-1,  2,  2,  3,  3,  3, -1],
                      [-1, -1,  2, -1,  3, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1]], out)
        self.failUnless(error < eps)

    def test_watershed_ift04(self):
        "watershed_ift 4"
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.uint8)
        markers = numarray.array([[ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 2, 0, 3, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, -1]],
                                 numarray.int8)
        out = nd_image.watershed_ift(data, markers,
                                              structure = [[1,1,1],
                                                           [1,1,1],
                                                           [1,1,1]])
        error = diff([[-1, -1, -1, -1, -1, -1, -1],
                      [-1,  2,  2,  3,  3,  3, -1],
                      [-1,  2,  2,  3,  3,  3, -1],
                      [-1,  2,  2,  3,  3,  3, -1],
                      [-1,  2,  2,  3,  3,  3, -1],
                      [-1,  2,  2,  3,  3,  3, -1],
                      [-1, -1, -1, -1, -1, -1, -1]], out)
        self.failUnless(error < eps)

    def test_watershed_ift05(self):
        "watershed_ift 5"
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.uint8)
        markers = numarray.array([[ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 3, 0, 2, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, -1]],
                                 numarray.int8)
        out = nd_image.watershed_ift(data, markers,
                                              structure = [[1,1,1],
                                                           [1,1,1],
                                                           [1,1,1]])
        error = diff([[-1, -1, -1, -1, -1, -1, -1],
                      [-1,  3,  3,  2,  2,  2, -1],
                      [-1,  3,  3,  2,  2,  2, -1],
                      [-1,  3,  3,  2,  2,  2, -1],
                      [-1,  3,  3,  2,  2,  2, -1],
                      [-1,  3,  3,  2,  2,  2, -1],
                      [-1, -1, -1, -1, -1, -1, -1]], out)
        self.failUnless(error < eps)

    def test_watershed_ift06(self):
        "watershed_ift 6"
        data = numarray.array([[0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.uint8)
        markers = numarray.array([[ -1, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 1, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0],
                                  [  0, 0, 0, 0, 0, 0, 0]],
                                 numarray.int8)
        out = nd_image.watershed_ift(data, markers,
                                              structure = [[1,1,1],
                                                           [1,1,1],
                                                           [1,1,1]])
        error = diff([[-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1]], out)
        self.failUnless(error < eps)

    def test_watershed_ift07(self):
        "watershed_ift 7"
        shape = (7, 6)
        data = numarray.zeros(shape, dtype = numarray.uint8)
        data = data.transpose()
        data[...] = numarray.array([[0, 1, 0, 0, 0, 1, 0],
                                    [0, 1, 0, 0, 0, 1, 0],
                                    [0, 1, 0, 0, 0, 1, 0],
                                    [0, 1, 1, 1, 1, 1, 0],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0]], numarray.uint8)
        markers = numarray.array([[-1, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 1, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0, 0, 0, 0, 0, 0, 0]],
                                 numarray.int8)
        out = numarray.zeros(shape, dtype = numarray.int16)
        out = out.transpose()
        nd_image.watershed_ift(data, markers,
                               structure = [[1,1,1],
                                            [1,1,1],
                                            [1,1,1]],
                               output = out)
        error = diff([[-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1,  1,  1,  1,  1,  1, -1],
                      [-1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1]], out)
        self.failUnless(error < eps)

    def test_label01(self):
        "label 1"
        data = numarray.ones([])
        out, n = nd_image.label(data)
        self.failUnless(diff(out, 1) < eps and n == 1)

    def test_label02(self):
        "label 2"
        data = numarray.zeros([])
        out, n = nd_image.label(data)
        self.failUnless(diff(out, 0) < eps and n == 0)

    def test_label03(self):
        "label 3"
        data = numarray.ones([1])
        out, n = nd_image.label(data)
        self.failUnless(diff(out, [1]) < eps and n == 1)

    def test_label04(self):
        "label 4"
        data = numarray.zeros([1])
        out, n = nd_image.label(data)
        self.failUnless(diff(out, [0]) < eps and n == 0)

    def test_label05(self):
        "label 5"
        data = numarray.ones([5])
        out, n = nd_image.label(data)
        self.failUnless(diff(out, [1, 1, 1, 1, 1]) < eps and n == 1)

    def test_label06(self):
        "label 6"
        data = numarray.array([1, 0, 1, 1, 0, 1])
        out, n = nd_image.label(data)
        self.failUnless(diff(out, [1, 0, 2, 2, 0, 3]) < eps and n == 3)

    def test_label07(self):
        "label 7"
        data = numarray.array([[0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0]])
        out, n = nd_image.label(data)
        self.failUnless(diff(out, [[0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0]]) < eps and n == 0)

    def test_label08(self):
        "label 8"
        data = numarray.array([[1, 0, 0, 0, 0, 0],
                               [0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0],
                               [1, 1, 0, 0, 0, 0],
                               [1, 1, 0, 0, 0, 0],
                               [0, 0, 0, 1, 1, 0]])
        out, n = nd_image.label(data)
        self.failUnless(diff(out, [[1, 0, 0, 0, 0, 0],
                                   [0, 0, 2, 2, 0, 0],
                                   [0, 0, 2, 2, 2, 0],
                                   [3, 3, 0, 0, 0, 0],
                                   [3, 3, 0, 0, 0, 0],
                                   [0, 0, 0, 4, 4, 0]]) < eps and n == 4)

    def test_label09(self):
        "label 9"
        data = numarray.array([[1, 0, 0, 0, 0, 0],
                               [0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0],
                               [1, 1, 0, 0, 0, 0],
                               [1, 1, 0, 0, 0, 0],
                               [0, 0, 0, 1, 1, 0]])
        struct = nd_image.generate_binary_structure(2, 2)
        out, n = nd_image.label(data, struct)
        self.failUnless(diff(out, [[1, 0, 0, 0, 0, 0],
                                   [0, 0, 2, 2, 0, 0],
                                   [0, 0, 2, 2, 2, 0],
                                   [2, 2, 0, 0, 0, 0],
                                   [2, 2, 0, 0, 0, 0],
                                   [0, 0, 0, 3, 3, 0]]) < eps and n == 3)

    def test_label10(self):
        "label 10"
        data = numarray.array([[0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 1, 0],
                               [0, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0]])
        struct = nd_image.generate_binary_structure(2, 2)
        out, n = nd_image.label(data, struct)
        self.failUnless(diff(out, [[0, 0, 0, 0, 0, 0],
                                   [0, 1, 1, 0, 1, 0],
                                   [0, 1, 1, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0]]) < eps and n == 1)

    def test_label11(self):
        "label 11"
        for type in self.types:
            data = numarray.array([[1, 0, 0, 0, 0, 0],
                                   [0, 0, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 0],
                                   [1, 1, 0, 0, 0, 0],
                                   [1, 1, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 0]], type)
            out, n = nd_image.label(data)
            error = diff(out, [[1, 0, 0, 0, 0, 0],
                               [0, 0, 2, 2, 0, 0],
                               [0, 0, 2, 2, 2, 0],
                               [3, 3, 0, 0, 0, 0],
                               [3, 3, 0, 0, 0, 0],
                               [0, 0, 0, 4, 4, 0]])
            self.failUnless(error < eps and n == 4)

    def test_label12(self):
        "label 12"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 1, 1],
                                   [0, 0, 0, 0, 0, 1],
                                   [0, 0, 1, 0, 1, 1],
                                   [0, 0, 1, 1, 1, 1],
                                   [0, 0, 0, 1, 1, 0]], type)
            out, n = nd_image.label(data)
            error = diff(out, [[0, 0, 0, 0, 1, 1],
                               [0, 0, 0, 0, 0, 1],
                               [0, 0, 1, 0, 1, 1],
                               [0, 0, 1, 1, 1, 1],
                               [0, 0, 0, 1, 1, 0]])
            self.failUnless(error < eps and n == 1)

    def test_label13(self):
        "label 13"
        for type in self.types:
            data = numarray.array([[1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                                   [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
                                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                                  type)
            out, n = nd_image.label(data)
            error = diff(out, [[1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                               [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
                               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
            self.failUnless(error < eps and n == 1)

    def test_find_objects01(self):
        "find_objects 1"
        data = numarray.ones([])
        out = nd_image.find_objects(data)
        self.failUnless(out == [()])

    def test_find_objects02(self):
        "find_objects 2"
        data = numarray.zeros([])
        out = nd_image.find_objects(data)
        self.failUnless(out == [])

    def test_find_objects03(self):
        "find_objects 3"
        data = numarray.ones([1])
        out = nd_image.find_objects(data)
        self.failUnless(out == [(slice(0, 1, None),)])

    def test_find_objects04(self):
        "find_objects 4"
        data = numarray.zeros([1])
        out = nd_image.find_objects(data)
        self.failUnless(out == [])

    def test_find_objects05(self):
        "find_objects 5"
        data = numarray.ones([5])
        out = nd_image.find_objects(data)
        self.failUnless(out == [(slice(0, 5, None),)])

    def test_find_objects06(self):
        "find_objects 6"
        data = numarray.array([1, 0, 2, 2, 0, 3])
        out = nd_image.find_objects(data)
        self.failUnless(out == [(slice(0, 1, None),),
                                (slice(2, 4, None),),
                                (slice(5, 6, None),)])

    def test_find_objects07(self):
        "find_objects 7"
        data = numarray.array([[0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0]])
        out = nd_image.find_objects(data)
        self.failUnless(out == []),

    def test_find_objects08(self):
        "find_objects 8"
        data = numarray.array([[1, 0, 0, 0, 0, 0],
                               [0, 0, 2, 2, 0, 0],
                               [0, 0, 2, 2, 2, 0],
                               [3, 3, 0, 0, 0, 0],
                               [3, 3, 0, 0, 0, 0],
                               [0, 0, 0, 4, 4, 0]])
        out = nd_image.find_objects(data)
        self.failUnless(out == [(slice(0, 1, None), slice(0, 1, None)),
                                (slice(1, 3, None), slice(2, 5, None)),
                                (slice(3, 5, None), slice(0, 2, None)),
                                (slice(5, 6, None), slice(3, 5, None))])

    def test_find_objects09(self):
        "find_objects 9"
        data = numarray.array([[1, 0, 0, 0, 0, 0],
                               [0, 0, 2, 2, 0, 0],
                               [0, 0, 2, 2, 2, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 4, 4, 0]])
        out = nd_image.find_objects(data)
        self.failUnless(out == [(slice(0, 1, None), slice(0, 1, None)),
                                (slice(1, 3, None), slice(2, 5, None)),
                                None,
                                (slice(5, 6, None), slice(3, 5, None))])

    def test_sum01(self):
        "sum 1"
        for type in self.types:
            input = numarray.array([], type)
            output = nd_image.sum(input)
            self.failUnless(output == 0.0)

    def test_sum02(self):
        "sum 2"
        for type in self.types:
            input = numarray.zeros([0, 4], type)
            output = nd_image.sum(input)
            self.failUnless(output == 0.0)

    def test_sum03(self):
        "sum 3"
        for type in self.types:
            input = numarray.ones([], type)
            output = nd_image.sum(input)
            self.failUnless(output == 1.0)

    def test_sum04(self):
        "sum 4"
        for type in self.types:
            input = numarray.array([1, 2], type)
            output = nd_image.sum(input)
            self.failUnless(output == 3.0)

    def test_sum05(self):
        "sum 5"
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.sum(input)
            self.failUnless(output == 10.0)

    def test_sum06(self):
        "sum 6"
        labels = numarray.array([], numarray.Bool)
        for type in self.types:
            input = numarray.array([], type)
            output = nd_image.sum(input, labels = labels)
            self.failUnless(output == 0.0)

    def test_sum07(self):
        "sum 7"
        labels = numarray.ones([0, 4], numarray.Bool)
        for type in self.types:
            input = numarray.zeros([0, 4], type)
            output = nd_image.sum(input, labels = labels)
            self.failUnless(output == 0.0)

    def test_sum08(self):
        "sum 8"
        labels = numarray.array([1, 0], numarray.Bool)
        for type in self.types:
            input = numarray.array([1, 2], type)
            output = nd_image.sum(input, labels = labels)
            self.failUnless(output == 1.0)

    def test_sum09(self):
        "sum 9"
        labels = numarray.array([1, 0], numarray.Bool)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.sum(input, labels = labels)
            self.failUnless(output == 4.0)

    def test_sum10(self):
        "sum 10"
        labels = numarray.array([1, 0], numarray.Bool)
        input = numarray.array([[1, 2], [3, 4]], numarray.Bool)
        output = nd_image.sum(input, labels = labels)
        self.failUnless(output == 2.0)

    def test_sum11(self):
        "sum 11"
        labels = numarray.array([1, 2], numarray.int8)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.sum(input, labels = labels,
                                           index = 2)
            self.failUnless(output == 6.0)

    def test_sum12(self):
        "sum 12"
        labels = numarray.array([[1, 2], [2, 4]], numarray.int8)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.sum(input, labels = labels,
                                            index = [4, 8, 2])
            self.failUnless(output == [4.0, 0.0, 5.0])

    def test_mean01(self):
        "mean 1"
        labels = numarray.array([1, 0], numarray.Bool)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.mean(input, labels = labels)
            self.failUnless(output == 2.0)

    def test_mean02(self):
        "mean 2"
        labels = numarray.array([1, 0], numarray.Bool)
        input = numarray.array([[1, 2], [3, 4]], numarray.Bool)
        output = nd_image.mean(input, labels = labels)
        self.failUnless(output == 1.0)

    def test_mean03(self):
        "mean 3"
        labels = numarray.array([1, 2])
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.mean(input, labels = labels,
                                            index = 2)
            self.failUnless(output == 3.0)

    def test_mean04(self):
        "mean 4"
        labels = numarray.array([[1, 2], [2, 4]], numarray.int8)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.mean(input, labels = labels,
                                            index = [4, 8, 2])
            self.failUnless(output == [4.0, 0.0, 2.5])

    def test_minimum01(self):
        "minimum 1"
        labels = numarray.array([1, 0], numarray.Bool)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.minimum(input, labels = labels)
            self.failUnless(output == 1.0)

    def test_minimum02(self):
        "minimum 2"
        labels = numarray.array([1, 0], numarray.Bool)
        input = numarray.array([[2, 2], [2, 4]], numarray.Bool)
        output = nd_image.minimum(input, labels = labels)
        self.failUnless(output == 1.0)

    def test_minimum03(self):
        "minimum 3"
        labels = numarray.array([1, 2])
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.minimum(input, labels = labels,
                                               index = 2)
            self.failUnless(output == 2.0)

    def test_minimum04(self):
        "minimum 4"
        labels = numarray.array([[1, 2], [2, 3]])
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.minimum(input, labels = labels,
                                               index = [2, 3, 8])
            self.failUnless(output == [2.0, 4.0, 0.0])

    def test_maximum01(self):
        "maximum 1"
        labels = numarray.array([1, 0], numarray.Bool)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.maximum(input, labels = labels)
            self.failUnless(output == 3.0)

    def test_maximum02(self):
        "maximum 2"
        labels = numarray.array([1, 0], numarray.Bool)
        input = numarray.array([[2, 2], [2, 4]], numarray.Bool)
        output = nd_image.maximum(input, labels = labels)
        self.failUnless(output == 1.0)

    def test_maximum03(self):
        "maximum 3"
        labels = numarray.array([1, 2])
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.maximum(input, labels = labels,
                                               index = 2)
            self.failUnless(output == 4.0)

    def test_maximum04(self):
        "maximum 4"
        labels = numarray.array([[1, 2], [2, 3]])
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.maximum(input, labels = labels,
                                               index = [2, 3, 8])
            self.failUnless(output == [3.0, 4.0, 0.0])

    def test_variance01(self):
        "variance 1"
        for type in self.types:
            input = numarray.array([], type)
            output = nd_image.variance(input)
            self.failUnless(float(output) == 0.0)

    def test_variance02(self):
        "variance 2"
        for type in self.types:
            input = numarray.array([1], type)
            output = nd_image.variance(input)
            self.failUnless(float(output) == 0.0)

    def test_variance03(self):
        "variance 3"
        for type in self.types:
            input = numarray.array([1, 3], type)
            output = nd_image.variance(input)
            self.failUnless(output == 2.0)

    def test_variance04(self):
        "variance 4"
        input = numarray.array([1, 0], numarray.Bool)
        output = nd_image.variance(input)
        self.failUnless(output == 0.5)

    def test_variance05(self):
        "variance 5"
        labels = [2, 2, 3]
        for type in self.types:
            input = numarray.array([1, 3, 8], type)
            output = nd_image.variance(input, labels, 2)
            self.failUnless(output == 2.0)

    def test_variance06(self):
        "variance 6"
        labels = [2, 2, 3, 3, 4]
        for type in self.types:
            input = numarray.array([1, 3, 8, 10, 8], type)
            output = nd_image.variance(input, labels, [2, 3, 4])
            self.failUnless(output == [2.0, 2.0, 0.0])

    def test_standard_deviation01(self):
        "standard deviation 1"
        for type in self.types:
            input = numarray.array([], type)
            output = nd_image.standard_deviation(input)
            self.failUnless(float(output) == 0.0)

    def test_standard_deviation02(self):
        "standard deviation 2"
        for type in self.types:
            input = numarray.array([1], type)
            output = nd_image.standard_deviation(input)
            self.failUnless(float(output) == 0.0)

    def test_standard_deviation03(self):
        "standard deviation 3"
        for type in self.types:
            input = numarray.array([1, 3], type)
            output = nd_image.standard_deviation(input)
            self.failUnless(output == math.sqrt(2.0))

    def test_standard_deviation04(self):
        "standard deviation 4"
        input = numarray.array([1, 0], numarray.Bool)
        output = nd_image.standard_deviation(input)
        self.failUnless(output == math.sqrt(0.5))

    def test_standard_deviation05(self):
        "standard deviation 5"
        labels = [2, 2, 3]
        for type in self.types:
            input = numarray.array([1, 3, 8], type)
            output = nd_image.standard_deviation(input, labels, 2)
            self.failUnless(output == math.sqrt(2.0))

    def test_standard_deviation06(self):
        "standard deviation 6"
        labels = [2, 2, 3, 3, 4]
        for type in self.types:
            input = numarray.array([1, 3, 8, 10, 8], type)
            output = nd_image.standard_deviation(input, labels,
                                                          [2, 3, 4])
            self.failUnless(output == [math.sqrt(2.0), math.sqrt(2.0),
                                       0.0])

    def test_minimum_position01(self):
        "minimum position 1"
        labels = numarray.array([1, 0], numarray.Bool)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.minimum_position(input,
                                                        labels = labels)
            self.failUnless(output == (0, 0))

    def test_minimum_position02(self):
        "minimum position 2"
        for type in self.types:
            input = numarray.array([[5, 4, 2, 5],
                                    [3, 7, 0, 2],
                                    [1, 5, 1, 1]], type)
            output = nd_image.minimum_position(input)
            self.failUnless(output == (1, 2))

    def test_minimum_position03(self):
        "minimum position 3"
        input = numarray.array([[5, 4, 2, 5],
                                [3, 7, 0, 2],
                                [1, 5, 1, 1]], numarray.Bool)
        output = nd_image.minimum_position(input)
        self.failUnless(output == (1, 2))

    def test_minimum_position04(self):
        "minimum position 4"
        input = numarray.array([[5, 4, 2, 5],
                                [3, 7, 1, 2],
                                [1, 5, 1, 1]], numarray.Bool)
        output = nd_image.minimum_position(input)
        self.failUnless(output == (0, 0))

    def test_minimum_position05(self):
        "minimum position 5"
        labels = [1, 2, 0, 4]
        for type in self.types:
            input = numarray.array([[5, 4, 2, 5],
                                    [3, 7, 0, 2],
                                    [1, 5, 2, 3]], type)
            output = nd_image.minimum_position(input, labels)
            self.failUnless(output == (2, 0))

    def test_minimum_position06(self):
        "minimum position 6"
        labels = [1, 2, 3, 4]
        for type in self.types:
            input = numarray.array([[5, 4, 2, 5],
                                    [3, 7, 0, 2],
                                    [1, 5, 1, 1]], type)
            output = nd_image.minimum_position(input, labels, 2)
            self.failUnless(output == (0, 1))

    def test_minimum_position07(self):
        "minimum position 7"
        labels = [1, 2, 3, 4]
        for type in self.types:
            input = numarray.array([[5, 4, 2, 5],
                                    [3, 7, 0, 2],
                                    [1, 5, 1, 1]], type)
            output = nd_image.minimum_position(input, labels,
                                                        [2, 3])
            self.failUnless(output == [(0, 1), (1, 2)])

    def test_maximum_position01(self):
        "maximum position 1"
        labels = numarray.array([1, 0], numarray.Bool)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output = nd_image.maximum_position(input,
                                                        labels = labels)
            self.failUnless(output == (1, 0))

    def test_maximum_position02(self):
        "maximum position 2"
        for type in self.types:
            input = numarray.array([[5, 4, 2, 5],
                                    [3, 7, 8, 2],
                                    [1, 5, 1, 1]], type)
            output = nd_image.maximum_position(input)
            self.failUnless(output == (1, 2))

    def test_maximum_position03(self):
        "maximum position 3"
        input = numarray.array([[5, 4, 2, 5],
                                [3, 7, 8, 2],
                                [1, 5, 1, 1]], numarray.Bool)
        output = nd_image.maximum_position(input)
        self.failUnless(output == (0, 0))

    def test_maximum_position04(self):
        "maximum position 4"
        labels = [1, 2, 0, 4]
        for type in self.types:
            input = numarray.array([[5, 4, 2, 5],
                                    [3, 7, 8, 2],
                                    [1, 5, 1, 1]], type)
            output = nd_image.maximum_position(input, labels)
            self.failUnless(output == (1, 1))

    def test_maximum_position05(self):
        "maximum position 5"
        labels = [1, 2, 0, 4]
        for type in self.types:
            input = numarray.array([[5, 4, 2, 5],
                                    [3, 7, 8, 2],
                                    [1, 5, 1, 1]], type)
            output = nd_image.maximum_position(input, labels, 1)
            self.failUnless(output == (0, 0))

    def test_maximum_position06(self):
        "maximum position 6"
        labels = [1, 2, 0, 4]
        for type in self.types:
            input = numarray.array([[5, 4, 2, 5],
                                    [3, 7, 8, 2],
                                    [1, 5, 1, 1]], type)
            output = nd_image.maximum_position(input, labels,
                                                        [1, 2])
            self.failUnless(output == [(0, 0), (1, 1)])

    def test_extrema01(self):
        "extrema 1"
        labels = numarray.array([1, 0], numarray.Bool)
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output1 = nd_image.extrema(input, labels = labels)
            output2 = nd_image.minimum(input, labels = labels)
            output3 = nd_image.maximum(input, labels = labels)
            output4 = nd_image.minimum_position(input,
                                                         labels = labels)
            output5 = nd_image.maximum_position(input,
                                                         labels = labels)
            self.failUnless(output1 == (output2, output3, output4,
                                        output5))

    def test_extrema02(self):
        "extrema 2"
        labels = numarray.array([1, 2])
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output1 = nd_image.extrema(input, labels = labels,
                                                index = 2)
            output2 = nd_image.minimum(input, labels = labels,
                                                index = 2)
            output3 = nd_image.maximum(input, labels = labels,
                                                index = 2)
            output4 = nd_image.minimum_position(input,
                                                labels = labels, index = 2)
            output5 = nd_image.maximum_position(input,
                                                labels = labels, index = 2)
            self.failUnless(output1 == (output2, output3, output4,
                                        output5))

    def test_extrema03(self):
        "extrema 3"
        labels = numarray.array([[1, 2], [2, 3]])
        for type in self.types:
            input = numarray.array([[1, 2], [3, 4]], type)
            output1 = nd_image.extrema(input, labels = labels,
                                                index = [2, 3, 8])
            output2 = nd_image.minimum(input, labels = labels,
                                                index = [2, 3, 8])
            output3 = nd_image.maximum(input, labels = labels,
                                                index = [2, 3, 8])
            output4 = nd_image.minimum_position(input,
                                        labels = labels, index = [2, 3, 8])
            output5 = nd_image.maximum_position(input,
                                        labels = labels, index = [2, 3, 8])
            self.failUnless(output1 == (output2, output3, output4,
                                        output5))

    def test_extrema04(self):
        "extrema 4"
        labels = [1, 2, 0, 4]
        for type in self.types:
            input = numarray.array([[5, 4, 2, 5],
                                    [3, 7, 8, 2],
                                    [1, 5, 1, 1]], type)
            output1 = nd_image.extrema(input, labels, [1, 2])
            output2 = nd_image.minimum(input, labels, [1, 2])
            output3 = nd_image.maximum(input, labels, [1, 2])
            output4 = nd_image.minimum_position(input, labels,
                                                         [1, 2])
            output5 = nd_image.maximum_position(input, labels,
                                                         [1, 2])
            self.failUnless(output1 == (output2, output3, output4,
                                        output5))

    def test_center_of_mass01(self):
        "center of mass 1"
        true = [0.0, 0.0]
        for type in self.types:
            input = numarray.array([[1, 0], [0, 0]], type)
            output = nd_image.center_of_mass(input)
            e = diff(true, output)
            self.failUnless(e < eps)

    def test_center_of_mass02(self):
        "center of mass 2"
        true = [1, 0]
        for type in self.types:
            input = numarray.array([[0, 0], [1, 0]], type)
            output = nd_image.center_of_mass(input)
            e = diff(true, output)
            self.failUnless(e < eps)

    def test_center_of_mass03(self):
        "center of mass 3"
        true = [0, 1]
        for type in self.types:
            input = numarray.array([[0, 1], [0, 0]], type)
            output = nd_image.center_of_mass(input)
            e = diff(true, output)
            self.failUnless(e < eps)

    def test_center_of_mass04(self):
        "center of mass 4"
        true = [1, 1]
        for type in self.types:
            input = numarray.array([[0, 0], [0, 1]], type)
            output = nd_image.center_of_mass(input)
            e = diff(true, output)
            self.failUnless(e < eps)

    def test_center_of_mass05(self):
        "center of mass 5"
        true = [0.5, 0.5]
        for type in self.types:
            input = numarray.array([[1, 1], [1, 1]], type)
            output = nd_image.center_of_mass(input)
            e = diff(true, output)
            self.failUnless(e < eps)

    def test_center_of_mass06(self):
        "center of mass 6"
        true = [0.5, 0.5]
        input = numarray.array([[1, 2], [3, 1]], numarray.Bool)
        output = nd_image.center_of_mass(input)
        e = diff(true, output)
        self.failUnless(e < eps)

    def test_center_of_mass07(self):
        "center of mass 7"
        labels = [1, 0]
        true = [0.5, 0.0]
        input = numarray.array([[1, 2], [3, 1]], numarray.Bool)
        output = nd_image.center_of_mass(input, labels)
        e = diff(true, output)
        self.failUnless(e < eps)

    def test_center_of_mass08(self):
        "center of mass 8"
        labels = [1, 2]
        true = [0.5, 1.0]
        input = numarray.array([[5, 2], [3, 1]], numarray.Bool)
        output = nd_image.center_of_mass(input, labels, 2)
        e = diff(true, output)
        self.failUnless(e < eps)


    def test_center_of_mass09(self):
        "center of mass 9"
        labels = [1, 2]
        true = [(0.5, 0.0), (0.5, 1.0)]
        input = numarray.array([[1, 2], [1, 1]], numarray.Bool)
        output = nd_image.center_of_mass(input, labels, [1, 2])
        e = diff(true, output)
        self.failUnless(e < eps)

    def test_histogram01(self):
        "histogram 1"
        true = numarray.ones(10)
        input = numarray.arange(10)
        output = nd_image.histogram(input, 0, 10, 10)
        e = diff(true, output)
        self.failUnless(e < eps)

    def test_histogram02(self):
        "histogram 2"
        labels = [1, 1, 1, 1, 2, 2, 2, 2]
        true = [0, 2, 0, 1, 0]
        input = numarray.array([1, 1, 3, 4, 3, 3, 3, 3])
        output = nd_image.histogram(input, 0, 4, 5, labels, 1)
        e = diff(true, output)
        self.failUnless(e < eps)

    def test_histogram03(self):
        "histogram 3"
        labels = [1, 0, 1, 1, 2, 2, 2, 2]
        true1 = [0, 1, 0, 1, 0]
        true2 = [0, 0, 0, 3, 0]
        input = numarray.array([1, 1, 3, 4, 3, 5, 3, 3])
        output = nd_image.histogram(input, 0, 4, 5, labels, (1,2))
        e1 = diff(true1, output[0])
        e2 = diff(true2, output[1])
        self.failUnless(e1 < eps and e2 < eps)

    def test_distance_transform_bf01(self):
        "brute force distance transform 1"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = nd_image.distance_transform_bf(data,
                                        'euclidean', return_indices = True)
        error1 = diff([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 1, 2, 4, 2, 1, 0, 0],
                       [0, 0, 1, 4, 8, 4, 1, 0, 0],
                       [0, 0, 1, 2, 4, 2, 1, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                    out * out)
        error2 = diff([[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [2, 2, 2, 2, 1, 2, 2, 2, 2],
                        [3, 3, 3, 2, 1, 2, 3, 3, 3],
                        [4, 4, 4, 4, 6, 4, 4, 4, 4],
                        [5, 5, 6, 6, 7, 6, 6, 5, 5],
                        [6, 6, 6, 7, 7, 7, 6, 6, 6],
                        [7, 7, 7, 7, 7, 7, 7, 7, 7],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                       [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 2, 4, 6, 6, 7, 8],
                        [0, 1, 1, 2, 4, 6, 7, 7, 8],
                        [0, 1, 1, 1, 6, 7, 7, 7, 8],
                        [0, 1, 2, 2, 4, 6, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8]]], ft)
        self.failUnless(error1 < eps and error2 < eps)

    def test_distance_transform_bf02(self):
        "brute force distance transform 2"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = nd_image.distance_transform_bf(data,
                                        'cityblock', return_indices = True)
        error1 = diff([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 1, 2, 2, 2, 1, 0, 0],
                       [0, 0, 1, 2, 3, 2, 1, 0, 0],
                       [0, 0, 1, 2, 2, 2, 1, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]], out)
        error2 = diff([[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [2, 2, 2, 2, 1, 2, 2, 2, 2],
                        [3, 3, 3, 3, 1, 3, 3, 3, 3],
                        [4, 4, 4, 4, 7, 4, 4, 4, 4],
                        [5, 5, 6, 7, 7, 7, 6, 5, 5],
                        [6, 6, 6, 7, 7, 7, 6, 6, 6],
                        [7, 7, 7, 7, 7, 7, 7, 7, 7],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                       [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 2, 4, 6, 6, 7, 8],
                        [0, 1, 1, 1, 4, 7, 7, 7, 8],
                        [0, 1, 1, 1, 4, 7, 7, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8]]], ft)
        self.failUnless(error1 < eps and error2 < eps)

    def test_distance_transform_bf03(self):
        "brute force distance transform 3"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = nd_image.distance_transform_bf(data,
                                    'chessboard', return_indices = True)
        error1 = diff([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 1, 1, 2, 1, 1, 0, 0],
                       [0, 0, 1, 2, 2, 2, 1, 0, 0],
                       [0, 0, 1, 1, 2, 1, 1, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]], out)
        error2 = diff([[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [2, 2, 2, 2, 1, 2, 2, 2, 2],
                        [3, 3, 4, 2, 2, 2, 4, 3, 3],
                        [4, 4, 5, 6, 6, 6, 5, 4, 4],
                        [5, 5, 6, 6, 7, 6, 6, 5, 5],
                        [6, 6, 6, 7, 7, 7, 6, 6, 6],
                        [7, 7, 7, 7, 7, 7, 7, 7, 7],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                       [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 2, 5, 6, 6, 7, 8],
                        [0, 1, 1, 2, 6, 6, 7, 7, 8],
                        [0, 1, 1, 2, 6, 7, 7, 7, 8],
                        [0, 1, 2, 2, 6, 6, 7, 7, 8],
                        [0, 1, 2, 4, 5, 6, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8]]], ft)
        self.failUnless(error1 < eps and error2 < eps)

    def test_distance_transform_bf04(self):
        "brute force distance transform 4"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        tdt, tft = nd_image.distance_transform_bf(data,
                                                    return_indices = 1)
        dts = []
        fts = []
        dt = numarray.zeros(data.shape, dtype = numarray.float64)
        nd_image.distance_transform_bf(data, distances = dt)
        dts.append(dt)
        ft = nd_image.distance_transform_bf(data,
                            return_distances = False, return_indices = 1)
        fts.append(ft)
        ft = numarray.indices(data.shape, dtype = numarray.int32)
        nd_image.distance_transform_bf(data,
             return_distances = False, return_indices = True, indices = ft)
        fts.append(ft)
        dt, ft = nd_image.distance_transform_bf(data,
                                                       return_indices = 1)
        dts.append(dt)
        fts.append(ft)
        dt = numarray.zeros(data.shape, dtype = numarray.float64)
        ft = nd_image.distance_transform_bf(data, distances = dt,
                                                     return_indices = True)
        dts.append(dt)
        fts.append(ft)
        ft = numarray.indices(data.shape, dtype = numarray.int32)
        dt = nd_image.distance_transform_bf(data,
                                       return_indices = True, indices = ft)
        dts.append(dt)
        fts.append(ft)
        dt = numarray.zeros(data.shape, dtype = numarray.float64)
        ft = numarray.indices(data.shape, dtype = numarray.int32)
        nd_image.distance_transform_bf(data, distances = dt,
                                       return_indices = True, indices = ft)
        dts.append(dt)
        fts.append(ft)
        for dt in dts:
            self.failUnless(diff(tdt, dt) < eps)
        for ft in fts:
            self.failUnless(diff(tft, ft) < eps)

    def test_distance_transform_bf05(self):
        "brute force distance transform 5"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = nd_image.distance_transform_bf(data,
                     'euclidean', return_indices = True, sampling = [2, 2])
        error1 = diff([[0, 0, 0,  0,  0,  0, 0, 0, 0],
                       [0, 0, 0,  0,  0,  0, 0, 0, 0],
                       [0, 0, 0,  4,  4,  4, 0, 0, 0],
                       [0, 0, 4,  8, 16,  8, 4, 0, 0],
                       [0, 0, 4, 16, 32, 16, 4, 0, 0],
                       [0, 0, 4,  8, 16,  8, 4, 0, 0],
                       [0, 0, 0,  4,  4,  4, 0, 0, 0],
                       [0, 0, 0,  0,  0,  0, 0, 0, 0],
                       [0, 0, 0,  0,  0,  0, 0, 0, 0]], out * out)
        error2 = diff([[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [2, 2, 2, 2, 1, 2, 2, 2, 2],
                        [3, 3, 3, 2, 1, 2, 3, 3, 3],
                        [4, 4, 4, 4, 6, 4, 4, 4, 4],
                        [5, 5, 6, 6, 7, 6, 6, 5, 5],
                        [6, 6, 6, 7, 7, 7, 6, 6, 6],
                        [7, 7, 7, 7, 7, 7, 7, 7, 7],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                       [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 2, 4, 6, 6, 7, 8],
                        [0, 1, 1, 2, 4, 6, 7, 7, 8],
                        [0, 1, 1, 1, 6, 7, 7, 7, 8],
                        [0, 1, 2, 2, 4, 6, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8]]], ft)
        self.failUnless(error1 < eps and error2 < eps)

    def test_distance_transform_bf06(self):
        "brute force distance transform 6"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = nd_image.distance_transform_bf(data,
                     'euclidean', return_indices = True, sampling = [2, 1])
        error1 = diff([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 4, 1, 0, 0, 0],
                       [0, 0, 1, 4, 8, 4, 1, 0, 0],
                       [0, 0, 1, 4, 9, 4, 1, 0, 0],
                       [0, 0, 1, 4, 8, 4, 1, 0, 0],
                       [0, 0, 0, 1, 4, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]], out * out)
        error2 = diff([[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [2, 2, 2, 2, 2, 2, 2, 2, 2],
                        [3, 3, 3, 3, 2, 3, 3, 3, 3],
                        [4, 4, 4, 4, 4, 4, 4, 4, 4],
                        [5, 5, 5, 5, 6, 5, 5, 5, 5],
                        [6, 6, 6, 6, 7, 6, 6, 6, 6],
                        [7, 7, 7, 7, 7, 7, 7, 7, 7],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                       [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 2, 6, 6, 6, 7, 8],
                        [0, 1, 1, 1, 6, 7, 7, 7, 8],
                        [0, 1, 1, 1, 7, 7, 7, 7, 8],
                        [0, 1, 1, 1, 6, 7, 7, 7, 8],
                        [0, 1, 2, 2, 4, 6, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8]]], ft)
        self.failUnless(error1 < eps and error2 < eps)
        self.failUnless(error1 < eps and error2 < eps)

    def test_distance_transform_cdt01(self):
        "chamfer type distance transform 1"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = nd_image.distance_transform_cdt(data,
                                        'cityblock', return_indices = True)
        bf = nd_image.distance_transform_bf(data, 'cityblock')
        error1 = diff(bf, out)
        error2 = diff([[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [2, 2, 2, 1, 1, 1, 2, 2, 2],
                        [3, 3, 2, 1, 1, 1, 2, 3, 3],
                        [4, 4, 4, 4, 1, 4, 4, 4, 4],
                        [5, 5, 5, 5, 7, 7, 6, 5, 5],
                        [6, 6, 6, 6, 7, 7, 6, 6, 6],
                        [7, 7, 7, 7, 7, 7, 7, 7, 7],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                       [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 1, 1, 4, 7, 7, 7, 8],
                        [0, 1, 1, 1, 4, 5, 6, 7, 8],
                        [0, 1, 2, 2, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],]], ft)
        self.failUnless(error1 < eps and error2 < eps)

    def test_distance_transform_cdt02(self):
        "chamfer type distance transform 2"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = nd_image.distance_transform_cdt(data,
                                       'chessboard', return_indices = True)
        bf = nd_image.distance_transform_bf(data, 'chessboard')
        error1 = diff(bf, out)
        error2 = diff([[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [2, 2, 2, 1, 1, 1, 2, 2, 2],
                        [3, 3, 2, 2, 1, 2, 2, 3, 3],
                        [4, 4, 3, 2, 2, 2, 3, 4, 4],
                        [5, 5, 4, 6, 7, 6, 4, 5, 5],
                        [6, 6, 6, 6, 7, 7, 6, 6, 6],
                        [7, 7, 7, 7, 7, 7, 7, 7, 7],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                       [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 2, 3, 4, 6, 7, 8],
                        [0, 1, 1, 2, 2, 6, 6, 7, 8],
                        [0, 1, 1, 1, 2, 6, 7, 7, 8],
                        [0, 1, 1, 2, 6, 6, 7, 7, 8],
                        [0, 1, 2, 2, 5, 6, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],
                        [0, 1, 2, 3, 4, 5, 6, 7, 8],]], ft)
        self.failUnless(error1 < eps and error2 < eps)

    def test_distance_transform_cdt03(self):
        "chamfer type distance transform 3"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        tdt, tft = nd_image.distance_transform_cdt(data,
                                                     return_indices = True)
        dts = []
        fts = []
        dt = numarray.zeros(data.shape, dtype = numarray.int32)
        nd_image.distance_transform_cdt(data, distances = dt)
        dts.append(dt)
        ft = nd_image.distance_transform_cdt(data,
                           return_distances = False, return_indices = True)
        fts.append(ft)
        ft = numarray.indices(data.shape, dtype = numarray.int32)
        nd_image.distance_transform_cdt(data,
             return_distances = False, return_indices = True, indices = ft)
        fts.append(ft)
        dt, ft = nd_image.distance_transform_cdt(data,
                                                     return_indices = True)
        dts.append(dt)
        fts.append(ft)
        dt = numarray.zeros(data.shape, dtype = numarray.int32)
        ft = nd_image.distance_transform_cdt(data, distances = dt,
                                                     return_indices = True)
        dts.append(dt)
        fts.append(ft)
        ft = numarray.indices(data.shape, dtype = numarray.int32)
        dt = nd_image.distance_transform_cdt(data,
                                       return_indices = True, indices = ft)
        dts.append(dt)
        fts.append(ft)
        dt = numarray.zeros(data.shape, dtype = numarray.int32)
        ft = numarray.indices(data.shape, dtype = numarray.int32)
        nd_image.distance_transform_cdt(data, distances = dt,
                                       return_indices = True, indices = ft)
        dts.append(dt)
        fts.append(ft)
        for dt in dts:
            self.failUnless(diff(tdt, dt) < eps)
        for ft in fts:
            self.failUnless(diff(tft, ft) < eps)

    def test_distance_transform_edt01(self):
        "euclidean distance transform 1"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = nd_image.distance_transform_edt(data,
                                                     return_indices = True)
        bf = nd_image.distance_transform_bf(data, 'euclidean')

        error1 = diff(bf, out)
        dt = ft - numarray.indices(ft.shape[1:], dtype = ft.dtype)
        dt = dt.astype(numarray.float64)
        numarray.multiply(dt, dt, dt)
        dt = numarray.add.reduce(dt, axis = 0)
        numarray.sqrt(dt, dt)
        error2 = diff(bf, dt)
        self.failUnless(error1 < eps and error2 < eps)

    def test_distance_transform_edt02(self):
        "euclidean distance transform 2"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        tdt, tft = nd_image.distance_transform_edt(data,
                                                     return_indices = True)
        dts = []
        fts = []
        dt = numarray.zeros(data.shape, dtype = numarray.float64)
        nd_image.distance_transform_edt(data, distances = dt)
        dts.append(dt)
        ft = nd_image.distance_transform_edt(data,
                               return_distances = 0, return_indices = True)
        fts.append(ft)
        ft = numarray.indices(data.shape, dtype = numarray.int32)
        nd_image.distance_transform_edt(data,
              return_distances = False,return_indices = True, indices = ft)
        fts.append(ft)
        dt, ft = nd_image.distance_transform_edt(data,
                                                     return_indices = True)
        dts.append(dt)
        fts.append(ft)
        dt = numarray.zeros(data.shape, dtype = numarray.float64)
        ft = nd_image.distance_transform_edt(data, distances = dt,
                                                     return_indices = True)
        dts.append(dt)
        fts.append(ft)
        ft = numarray.indices(data.shape, dtype = numarray.int32)
        dt = nd_image.distance_transform_edt(data,
                                       return_indices = True, indices = ft)
        dts.append(dt)
        fts.append(ft)
        dt = numarray.zeros(data.shape, dtype = numarray.float64)
        ft = numarray.indices(data.shape, dtype = numarray.int32)
        nd_image.distance_transform_edt(data, distances = dt,
                                       return_indices = True, indices = ft)
        dts.append(dt)
        fts.append(ft)
        for dt in dts:
            self.failUnless(diff(tdt, dt) < eps)
        for ft in fts:
            self.failUnless(diff(tft, ft) < eps)

    def test_distance_transform_edt03(self):
        "euclidean distance transform 3"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        ref = nd_image.distance_transform_bf(data, 'euclidean',
                                                      sampling = [2, 2])
        out = nd_image.distance_transform_edt(data,
                                                       sampling = [2, 2])
        self.failUnless(diff(ref, out) < eps)


    def test_distance_transform_edt4(self):
        "euclidean distance transform 4"
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        ref = nd_image.distance_transform_bf(data, 'euclidean',
                                                      sampling = [2, 1])
        out = nd_image.distance_transform_edt(data,
                                                       sampling = [2, 1])
        self.failUnless(diff(ref, out) < eps)

    def test_generate_structure01(self):
        "generation of a binary structure 1"
        struct = nd_image.generate_binary_structure(0, 1)
        self.failUnless(diff(struct, 1) < eps)

    def test_generate_structure02(self):
        "generation of a binary structure 2"
        struct = nd_image.generate_binary_structure(1, 1)
        self.failUnless(diff(struct, [1, 1, 1]) < eps)

    def test_generate_structure03(self):
        "generation of a binary structure 3"
        struct = nd_image.generate_binary_structure(2, 1)
        self.failUnless(diff(struct, [[0, 1, 0],
                                      [1, 1, 1],
                                      [0, 1, 0]]) < eps)

    def test_generate_structure04(self):
        "generation of a binary structure 4"
        struct = nd_image.generate_binary_structure(2, 2)
        self.failUnless(diff(struct, [[1, 1, 1],
                                      [1, 1, 1],
                                      [1, 1, 1]]) < eps)

    def test_iterate_structure01(self):
        "iterating a structure 1"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        out = nd_image.iterate_structure(struct, 2)
        self.failUnless(diff(out, [[0, 0, 1, 0, 0],
                                   [0, 1, 1, 1, 0],
                                   [1, 1, 1, 1, 1],
                                   [0, 1, 1, 1, 0],
                                   [0, 0, 1, 0, 0]]) < eps)

    def test_iterate_structure02(self):
        "iterating a structure 2"
        struct = [[0, 1],
                  [1, 1],
                  [0, 1]]
        out = nd_image.iterate_structure(struct, 2)
        self.failUnless(diff(out, [[0, 0, 1],
                                   [0, 1, 1],
                                   [1, 1, 1],
                                   [0, 1, 1],
                                   [0, 0, 1]]) < eps)

    def test_iterate_structure03(self):
        "iterating a structure 3"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        out = nd_image.iterate_structure(struct, 2, 1)
        error = diff(out[0], [[0, 0, 1, 0, 0],
                              [0, 1, 1, 1, 0],
                              [1, 1, 1, 1, 1],
                              [0, 1, 1, 1, 0],
                              [0, 0, 1, 0, 0]])
        self.failUnless(error < eps and out[1] == [2, 2])

    def test_binary_erosion01(self):
        "binary erosion 1"
        for type in self.types:
            data = numarray.ones([], type)
            out = nd_image.binary_erosion(data)
            self.failUnless(diff(out, 1) < eps)

    def test_binary_erosion02(self):
        "binary erosion 2"
        for type in self.types:
            data = numarray.ones([], type)
            out = nd_image.binary_erosion(data, border_value = 1)
            self.failUnless(diff(out, 1) < eps)

    def test_binary_erosion03(self):
        "binary erosion 3"
        for type in self.types:
            data = numarray.ones([1], type)
            out = nd_image.binary_erosion(data)
            self.failUnless(diff(out, [0]) < eps)

    def test_binary_erosion04(self):
        "binary erosion 4"
        for type in self.types:
            data = numarray.ones([1], type)
            out = nd_image.binary_erosion(data, border_value = 1)
            self.failUnless(diff(out, [1]) < eps)

    def test_binary_erosion05(self):
        "binary erosion 5"
        for type in self.types:
            data = numarray.ones([3], type)
            out = nd_image.binary_erosion(data)
            self.failUnless(diff(out, [0, 1, 0]) < eps)

    def test_binary_erosion06(self):
        "binary erosion 6"
        for type in self.types:
            data = numarray.ones([3], type)
            out = nd_image.binary_erosion(data, border_value = 1)
            self.failUnless(diff(out, [1, 1, 1]) < eps)

    def test_binary_erosion07(self):
        "binary erosion 7"
        for type in self.types:
            data = numarray.ones([5], type)
            out = nd_image.binary_erosion(data)
            self.failUnless(diff(out, [0, 1, 1, 1, 0]) < eps)

    def test_binary_erosion08(self):
        "binary erosion 8"
        for type in self.types:
            data = numarray.ones([5], type)
            out = nd_image.binary_erosion(data, border_value = 1)
            self.failUnless(diff(out, [1, 1, 1, 1, 1]) < eps)

    def test_binary_erosion09(self):
        "binary erosion 9"
        for type in self.types:
            data = numarray.ones([5], type)
            data[2] = 0
            out = nd_image.binary_erosion(data)
            self.failUnless(diff(out, [0, 0, 0, 0, 0]) < eps)

    def test_binary_erosion10(self):
        "binary erosion 10"
        for type in self.types:
            data = numarray.ones([5], type)
            data[2] = 0
            out = nd_image.binary_erosion(data, border_value = 1)
            self.failUnless(diff(out, [1, 0, 0, 0, 1]) < eps)

    def test_binary_erosion11(self):
        "binary erosion 11"
        for type in self.types:
            data = numarray.ones([5], type)
            data[2] = 0
            struct = [1, 0, 1]
            out = nd_image.binary_erosion(data, struct,
                                                   border_value = 1)
            self.failUnless(diff(out, [1, 0, 1, 0, 1]) < eps)

    def test_binary_erosion12(self):
        "binary erosion 12"
        for type in self.types:
            data = numarray.ones([5], type)
            data[2] = 0
            struct = [1, 0, 1]
            out = nd_image.binary_erosion(data, struct,
                                                   border_value = 1,
                                                   origin = -1)
            self.failUnless(diff(out, [0, 1, 0, 1, 1]) < eps)

    def test_binary_erosion13(self):
        "binary erosion 13"
        for type in self.types:
            data = numarray.ones([5], type)
            data[2] = 0
            struct = [1, 0, 1]
            out = nd_image.binary_erosion(data, struct,
                                                   border_value = 1,
                                                   origin = 1)
            self.failUnless(diff(out, [1, 1, 0, 1, 0]) < eps)

    def test_binary_erosion14(self):
        "binary erosion 14"
        for type in self.types:
            data = numarray.ones([5], type)
            data[2] = 0
            struct = [1, 1]
            out = nd_image.binary_erosion(data, struct,
                                                   border_value = 1)
            self.failUnless(diff(out, [1, 1, 0, 0, 1]) < eps)

    def test_binary_erosion15(self):
        "binary erosion 15"
        for type in self.types:
            data = numarray.ones([5], type)
            data[2] = 0
            struct = [1, 1]
            out = nd_image.binary_erosion(data, struct,
                                                   border_value = 1,
                                                   origin = -1)
            self.failUnless(diff(out, [1, 0, 0, 1, 1]) < eps)

    def test_binary_erosion16(self):
        "binary erosion 16"
        for type in self.types:
            data = numarray.ones([1, 1], type)
            out = nd_image.binary_erosion(data, border_value = 1)
            self.failUnless(diff(out, [[1]]) < eps)

    def test_binary_erosion17(self):
        "binary erosion 17"
        for type in self.types:
            data = numarray.ones([1, 1], type)
            out = nd_image.binary_erosion(data)
            self.failUnless(diff(out, [[0]]) < eps)

    def test_binary_erosion18(self):
        "binary erosion 18"
        for type in self.types:
            data = numarray.ones([1, 3], type)
            out = nd_image.binary_erosion(data)
            self.failUnless(diff(out, [[0, 0, 0]]) < eps)

    def test_binary_erosion19(self):
        "binary erosion 19"
        for type in self.types:
            data = numarray.ones([1, 3], type)
            out = nd_image.binary_erosion(data, border_value = 1)
            self.failUnless(diff(out, [[1, 1, 1]]) < eps)

    def test_binary_erosion20(self):
        "binary erosion 20"
        for type in self.types:
            data = numarray.ones([3, 3], type)
            out = nd_image.binary_erosion(data)
            self.failUnless(diff(out, [[0, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 0]]) < eps)

    def test_binary_erosion21(self):
        "binary erosion 21"
        for type in self.types:
            data = numarray.ones([3, 3], type)
            out = nd_image.binary_erosion(data, border_value = 1)
            self.failUnless(diff(out, [[1, 1, 1],
                                       [1, 1, 1],
                                       [1, 1, 1]]) < eps)

    def test_binary_erosion22(self):
        "binary erosion 22"
        true = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_erosion(data, border_value = 1)
            self.failUnless(diff(out, true) < eps)

    def test_binary_erosion23(self):
        "binary erosion 23"
        struct = nd_image.generate_binary_structure(2, 2)
        true = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_erosion(data, struct,
                                                   border_value = 1)
            self.failUnless(diff(out, true) < eps)

    def test_binary_erosion24(self):
        "binary erosion 24"
        struct = [[0, 1],
                  [1, 1]]
        true = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_erosion(data, struct,
                                                   border_value = 1)
            self.failUnless(diff(out, true) < eps)

    def test_binary_erosion25(self):
        "binary erosion 25"
        struct = [[0, 1, 0],
                  [1, 0, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 0, 1, 1],
                                   [0, 0, 1, 0, 1, 1, 0, 0],
                                   [0, 1, 0, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_erosion(data, struct,
                                                   border_value = 1)
            self.failUnless(diff(out, true) < eps)

    def test_binary_erosion26(self):
        "binary erosion 26"
        struct = [[0, 1, 0],
                  [1, 0, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1]]
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 0, 1, 1],
                                   [0, 0, 1, 0, 1, 1, 0, 0],
                                   [0, 1, 0, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_erosion(data, struct,
                                      border_value = 1, origin = (-1, -1))
            self.failUnless(diff(out, true) < eps)

    def test_binary_erosion27(self):
        "binary erosion 27"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_erosion(data, struct,
                                         border_value = 1, iterations = 2)
        self.failUnless(diff(out, true) < eps)

    def test_binary_erosion28(self):
        "binary erosion 28"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        out = numarray.zeros(data.shape, numarray.Bool)
        nd_image.binary_erosion(data, struct, border_value = 1,
                                         iterations = 2, output = out)
        self.failUnless(diff(out, true) < eps)

    def test_binary_erosion29(self):
        "binary erosion 29"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numarray.array([[0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [1, 1, 1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_erosion(data, struct,
                                         border_value = 1, iterations = 3)
        self.failUnless(diff(out, true) < eps)

    def test_binary_erosion30(self):
        "binary erosion 30"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numarray.array([[0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [1, 1, 1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0]], numarray.Bool)
        out = numarray.zeros(data.shape, numarray.Bool)
        nd_image.binary_erosion(data, struct, border_value = 1,
                                         iterations = 3, output = out)
        self.failUnless(diff(out, true) < eps)

    def test_binary_erosion31(self):
        "binary erosion 31"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 1],
                [0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 1]]
        data = numarray.array([[0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [1, 1, 1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0]], numarray.Bool)
        out = numarray.zeros(data.shape, numarray.Bool)
        nd_image.binary_erosion(data, struct, border_value = 1,
                          iterations = 1, output = out, origin = (-1, -1))
        self.failUnless(diff(out, true) < eps)

    def test_binary_erosion32(self):
        "binary erosion 32"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_erosion(data, struct,
                                         border_value = 1, iterations = 2)
        self.failUnless(diff(out, true) < eps)

    def test_binary_erosion33(self):
        "binary erosion 33"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        mask = [[1, 1, 1, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1]]
        data = numarray.array([[0, 0, 0, 0, 0, 1, 1],
                               [0, 0, 0, 1, 0, 0, 1],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_erosion(data, struct,
                            border_value = 1, mask = mask, iterations = -1)
        self.failUnless(diff(out, true) < eps)

    def test_binary_erosion34(self):
        "binary erosion 34"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        mask = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_erosion(data, struct,
                                            border_value = 1, mask = mask)
        self.failUnless(diff(out, true) < eps)

    def test_binary_erosion35(self):
        "binary erosion 35"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        mask = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numarray.array([[0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [1, 1, 1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0]], numarray.Bool)
        tmp = [[0, 0, 1, 0, 0, 0, 0],
               [0, 1, 1, 1, 0, 0, 0],
               [1, 1, 1, 1, 1, 0, 1],
               [0, 1, 1, 1, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 1]]
        true = numarray.logical_and(tmp, mask)
        tmp = numarray.logical_and(data, numarray.logical_not(mask))
        true = numarray.logical_or(true, tmp)
        out = numarray.zeros(data.shape, numarray.Bool)
        nd_image.binary_erosion(data, struct, border_value = 1,
                                         iterations = 1, output = out,
                                         origin = (-1, -1), mask = mask)
        self.failUnless(diff(out, true) < eps)

    def test_binary_erosion36(self):
        "binary erosion 36"
        struct = [[0, 1, 0],
                  [1, 0, 1],
                  [0, 1, 0]]
        mask = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        tmp = [[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 1, 0, 0, 1],
               [0, 0, 1, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1]]
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 1, 1],
                               [0, 0, 1, 1, 1, 0, 1, 1],
                               [0, 0, 1, 0, 1, 1, 0, 0],
                               [0, 1, 0, 1, 1, 1, 1, 0],
                               [0, 1, 1, 0, 0, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]])
        true = numarray.logical_and(tmp, mask)
        tmp = numarray.logical_and(data, numarray.logical_not(mask))
        true = numarray.logical_or(true, tmp)
        out = nd_image.binary_erosion(data, struct, mask = mask,
                                       border_value = 1, origin = (-1, -1))
        self.failUnless(diff(out, true) < eps)

    def test_binary_dilation01(self):
        "binary dilation 1"
        for type in self.types:
            data = numarray.ones([], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, 1) < eps)

    def test_binary_dilation02(self):
        "binary dilation 2"
        for type in self.types:
            data = numarray.zeros([], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, 0) < eps)

    def test_binary_dilation03(self):
        "binary dilation 3"
        for type in self.types:
            data = numarray.ones([1], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [1]) < eps)

    def test_binary_dilation04(self):
        "binary dilation 4"
        for type in self.types:
            data = numarray.zeros([1], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [0]) < eps)

    def test_binary_dilation05(self):
        "binary dilation 5"
        for type in self.types:
            data = numarray.ones([3], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [1, 1, 1]) < eps)

    def test_binary_dilation06(self):
        "binary dilation 6"
        for type in self.types:
            data = numarray.zeros([3], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [0, 0, 0]) < eps)

    def test_binary_dilation07(self):
        "binary dilation 7"
        struct = nd_image.generate_binary_structure(1, 1)
        for type in self.types:
            data = numarray.zeros([3], type)
            data[1] = 1
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [1, 1, 1]) < eps)

    def test_binary_dilation08(self):
        "binary dilation 8"
        for type in self.types:
            data = numarray.zeros([5], type)
            data[1] = 1
            data[3] = 1
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [1, 1, 1, 1, 1]) < eps)

    def test_binary_dilation09(self):
        "binary dilation 9"
        for type in self.types:
            data = numarray.zeros([5], type)
            data[1] = 1
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [1, 1, 1, 0, 0]) < eps)

    def test_binary_dilation10(self):
        "binary dilation 10"
        for type in self.types:
            data = numarray.zeros([5], type)
            data[1] = 1
            out = nd_image.binary_dilation(data, origin = -1)
            self.failUnless(diff(out, [0, 1, 1, 1, 0]) < eps)

    def test_binary_dilation11(self):
        "binary dilation 11"
        for type in self.types:
            data = numarray.zeros([5], type)
            data[1] = 1
            out = nd_image.binary_dilation(data, origin = 1)
            self.failUnless(diff(out, [1, 1, 0, 0, 0]) < eps)

    def test_binary_dilation12(self):
        "binary dilation 12"
        for type in self.types:
            data = numarray.zeros([5], type)
            data[1] = 1
            struct = [1, 0, 1]
            out = nd_image.binary_dilation(data, struct)
            self.failUnless(diff(out, [1, 0, 1, 0, 0]) < eps)

    def test_binary_dilation13(self):
        "binary dilation 13"
        for type in self.types:
            data = numarray.zeros([5], type)
            data[1] = 1
            struct = [1, 0, 1]
            out = nd_image.binary_dilation(data, struct,
                                                    border_value = 1)
            self.failUnless(diff(out, [1, 0, 1, 0, 1]) < eps)

    def test_binary_dilation14(self):
        "binary dilation 14"
        for type in self.types:
            data = numarray.zeros([5], type)
            data[1] = 1
            struct = [1, 0, 1]
            out = nd_image.binary_dilation(data, struct,
                                                    origin = -1)
            self.failUnless(diff(out, [0, 1, 0, 1, 0]) < eps)

    def test_binary_dilation15(self):
        "binary dilation 15"
        for type in self.types:
            data = numarray.zeros([5], type)
            data[1] = 1
            struct = [1, 0, 1]
            out = nd_image.binary_dilation(data, struct,
                                            origin = -1, border_value = 1)
            self.failUnless(diff(out, [1, 1, 0, 1, 0]) < eps)

    def test_binary_dilation16(self):
        "binary dilation 16"
        for type in self.types:
            data = numarray.ones([1, 1], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [[1]]) < eps)

    def test_binary_dilation17(self):
        "binary dilation 17"
        for type in self.types:
            data = numarray.zeros([1, 1], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [[0]]) < eps)

    def test_binary_dilation18(self):
        "binary dilation 18"
        for type in self.types:
            data = numarray.ones([1, 3], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [[1, 1, 1]]) < eps)

    def test_binary_dilation19(self):
        "binary dilation 19"
        for type in self.types:
            data = numarray.ones([3, 3], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [[1, 1, 1],
                               [1, 1, 1],
                               [1, 1, 1]]) < eps)

    def test_binary_dilation20(self):
        "binary dilation 20"
        for type in self.types:
            data = numarray.zeros([3, 3], type)
            data[1, 1] = 1
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, [[0, 1, 0],
                                       [1, 1, 1],
                                       [0, 1, 0]]) < eps)

    def test_binary_dilation21(self):
        "binary dilation 21"
        struct = nd_image.generate_binary_structure(2, 2)
        for type in self.types:
            data = numarray.zeros([3, 3], type)
            data[1, 1] = 1
            out = nd_image.binary_dilation(data, struct)
            self.failUnless(diff(out, [[1, 1, 1],
                                       [1, 1, 1],
                                       [1, 1, 1]]) < eps)

    def test_binary_dilation22(self):
        "binary dilation 22"
        true = [[0, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 1, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 1, 0, 0],
                                           [0, 0, 0, 1, 1, 0, 0, 0],
                                           [0, 0, 1, 0, 0, 1, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_dilation(data)
            self.failUnless(diff(out, true) < eps)

    def test_binary_dilation23(self):
        "binary dilation 23"
        true = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_dilation(data, border_value = 1)
            self.failUnless(diff(out, true) < eps)

    def test_binary_dilation24(self):
        "binary dilation 24"
        true = [[1, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_dilation(data, origin = (1, 1))
            self.failUnless(diff(out, true) < eps)

    def test_binary_dilation25(self):
        "binary dilation 25"
        true = [[1, 1, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 1, 0, 1, 1],
                [0, 0, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_dilation(data, origin = (1, 1),
                                                         border_value = 1)
            self.failUnless(diff(out, true) < eps)

    def test_binary_dilation26(self):
        "binary dilation 26"
        struct = nd_image.generate_binary_structure(2, 2)
        true = [[1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_dilation(data, struct)
            self.failUnless(diff(out, true) < eps)

    def test_binary_dilation27(self):
        "binary dilation 27"
        struct = [[0, 1],
                  [1, 1]]
        true = [[0, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_dilation(data, struct)
            self.failUnless(diff(out, true) < eps)

    def test_binary_dilation28(self):
        "binary dilation 28"
        true = [[1, 1, 1, 1],
                [1, 0, 0, 1],
                [1, 0, 0, 1],
                [1, 1, 1, 1]]

        for type in self.types:
            data = numarray.array([[0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0]], type)
            out = nd_image.binary_dilation(data, border_value = 1)
            self.failUnless(diff(out, true) < eps)

    def test_binary_dilation29(self):
        "binary dilation 29"
        struct = [[0, 1],
                  [1, 1]]
        true = [[0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]]

        data = numarray.array([[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_dilation(data, struct,
                                                iterations = 2)
        self.failUnless(diff(out, true) < eps)

    def test_binary_dilation30(self):
        "binary dilation 30"
        struct = [[0, 1],
                  [1, 1]]
        true = [[0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]]

        data = numarray.array([[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0]], numarray.Bool)
        out = numarray.zeros(data.shape, numarray.Bool)
        nd_image.binary_dilation(data, struct, iterations = 2,
                                          output = out)
        self.failUnless(diff(out, true) < eps)

    def test_binary_dilation31(self):
        "binary dilation 31"
        struct = [[0, 1],
                  [1, 1]]
        true = [[0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]]

        data = numarray.array([[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_dilation(data, struct,
                                                iterations = 3)
        self.failUnless(diff(out, true) < eps)

    def test_binary_dilation32(self):
        "binary dilation 32"
        struct = [[0, 1],
                  [1, 1]]
        true = [[0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]]

        data = numarray.array([[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0]], numarray.Bool)
        out = numarray.zeros(data.shape, numarray.Bool)
        nd_image.binary_dilation(data, struct, iterations = 3,
                                          output = out)
        self.failUnless(diff(out, true) < eps)

    def test_binary_dilation33(self):
        "binary dilation 33"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0],
                               [0, 1, 1, 0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        mask = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0],
                               [0, 1, 1, 0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        data = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)

        out = nd_image.binary_dilation(data, struct,
                           iterations = -1, mask = mask, border_value = 0)
        self.failUnless(diff(out, true) < eps)

    def test_binary_dilation34(self):
        "binary dilation 34"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        mask = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        data = numarray.zeros(mask.shape, numarray.Bool)
        out = nd_image.binary_dilation(data, struct,
                          iterations = -1, mask = mask, border_value = 1)
        self.failUnless(diff(out, true) < eps)

    def test_binary_dilation35(self):
        "binary dilation 35"
        tmp = [[1, 1, 0, 0, 0, 0, 1, 1],
               [1, 0, 0, 0, 1, 0, 1, 1],
               [0, 0, 1, 1, 1, 1, 1, 1],
               [0, 1, 1, 1, 1, 0, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [0, 1, 0, 0, 1, 0, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1]]
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]])
        mask = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        true = numarray.logical_and(tmp, mask)
        tmp = numarray.logical_and(data, numarray.logical_not(mask))
        true = numarray.logical_or(true, tmp)
        for type in self.types:
            data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_dilation(data, mask = mask,
                                        origin = (1, 1), border_value = 1)
            self.failUnless(diff(out, true) < eps)

    def test_binary_propagation01(self):
        "binary propagation 1"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0],
                               [0, 1, 1, 0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        mask = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0],
                               [0, 1, 1, 0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        data = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)

        out = nd_image.binary_propagation(data, struct,
                                            mask = mask, border_value = 0)
        self.failUnless(diff(out, true) < eps)

    def test_binary_propagation02(self):
        "binary propagation 2"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        mask = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        data = numarray.zeros(mask.shape, numarray.Bool)
        out = nd_image.binary_propagation(data, struct,
                                             mask = mask, border_value = 1)
        self.failUnless(diff(out, true) < eps)

    def test_binary_opening01(self):
        "binary opening 1"
        true = [[0, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 0, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_opening(data)
            self.failUnless(diff(out, true) < eps)

    def test_binary_opening02(self):
        "binary opening 2"
        struct = nd_image.generate_binary_structure(2, 2)
        true = [[1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[1, 1, 1, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 0, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_opening(data, struct)
            self.failUnless(diff(out, true) < eps)

    def test_binary_closing01(self):
        "binary closing 1"
        true = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[0, 1, 0, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 0, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_closing(data)
            self.failUnless(diff(out, true) < eps)

    def test_binary_closing02(self):
        "binary closing 2"
        struct = nd_image.generate_binary_structure(2, 2)
        true = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[1, 1, 1, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 0, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_closing(data, struct)
            self.failUnless(diff(out, true) < eps)

    def test_binary_fill_holes01(self):
        "binary fill holes 1"
        true = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_fill_holes(data)
        self.failUnless(diff(out, true) < eps)

    def test_binary_fill_holes02(self):
        "binary fill holes 2"
        true = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_fill_holes(data)
        self.failUnless(diff(out, true) < eps)

    def test_binary_fill_holes03(self):
        "binary fill holes 3"
        true = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 0, 1, 1, 1],
                               [0, 1, 1, 1, 0, 1, 1, 1],
                               [0, 1, 1, 1, 0, 1, 1, 1],
                               [0, 0, 1, 0, 0, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        data = numarray.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 1, 0, 1, 0, 1, 1, 1],
                               [0, 1, 0, 1, 0, 1, 0, 1],
                               [0, 1, 0, 1, 0, 1, 0, 1],
                               [0, 0, 1, 0, 0, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0, 0, 0]], numarray.Bool)
        out = nd_image.binary_fill_holes(data)
        self.failUnless(diff(out, true) < eps)

    def test_grey_erosion01(self):
        "grey erosion 1"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = nd_image.grey_erosion(array,
                                                footprint = footprint)
        self.failUnless(diff([[2, 2, 1, 1, 1],
                              [2, 3, 1, 3, 1],
                              [5, 5, 3, 3, 1]], output) < eps)

    def test_grey_erosion02(self):
        "grey erosion 2"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        output = nd_image.grey_erosion(array,
                              footprint = footprint, structure = structure)
        self.failUnless(diff([[2, 2, 1, 1, 1],
                              [2, 3, 1, 3, 1],
                              [5, 5, 3, 3, 1]], output) < eps)

    def test_grey_erosion03(self):
        "grey erosion 3"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[1, 1, 1], [1, 1, 1]]
        output = nd_image.grey_erosion(array,
                              footprint = footprint, structure = structure)
        self.failUnless(diff([[1, 1, 0, 0, 0],
                              [1, 2, 0, 2, 0],
                              [4, 4, 2, 2, 0]], output) < eps)

    def test_grey_dilation01(self):
        "grey dilation 1"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[0, 1, 1], [1, 0, 1]]
        output = nd_image.grey_dilation(array,
                                                 footprint = footprint)
        self.failUnless(diff([[7, 7, 9, 9, 5],
                              [7, 9, 8, 9, 7],
                              [8, 8, 8, 7, 7]], output) < eps)

    def test_grey_dilation02(self):
        "grey dilation 2"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[0, 1, 1], [1, 0, 1]]
        structure = [[0, 0, 0], [0, 0, 0]]
        output = nd_image.grey_dilation(array,
                             footprint = footprint, structure = structure)
        self.failUnless(diff([[7, 7, 9, 9, 5],
                              [7, 9, 8, 9, 7],
                              [8, 8, 8, 7, 7]], output) < eps)

    def test_grey_dilation03(self):
        "grey dilation 3"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[0, 1, 1], [1, 0, 1]]
        structure = [[1, 1, 1], [1, 1, 1]]
        output = nd_image.grey_dilation(array,
                             footprint = footprint, structure = structure)
        self.failUnless(diff([[8,  8, 10, 10, 6],
                              [8, 10,  9, 10, 8],
                              [9,  9,  9,  8, 8]], output) < eps)

    def test_grey_opening01(self):
        "grey opening 1"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        tmp = nd_image.grey_erosion(array, footprint = footprint)
        true = nd_image.grey_dilation(tmp, footprint = footprint)
        output = nd_image.grey_opening(array,
                                                footprint = footprint)
        self.failUnless(diff(true, output) < eps)


    def test_grey_opening02(self):
        "grey opening 2"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = nd_image.grey_erosion(array, footprint = footprint,
                                             structure = structure)
        true = nd_image.grey_dilation(tmp, footprint = footprint,
                                               structure = structure)
        output = nd_image.grey_opening(array,
                             footprint = footprint, structure = structure)
        self.failUnless(diff(true, output) < eps)

    def test_grey_closing01(self):
        "grey closing 1"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        tmp = nd_image.grey_dilation(array, footprint = footprint)
        true = nd_image.grey_erosion(tmp, footprint = footprint)
        output = nd_image.grey_closing(array,
                                                footprint = footprint)
        self.failUnless(diff(true, output) < eps)

    def test_grey_closing02(self):
        "grey closing 2"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = nd_image.grey_dilation(array, footprint = footprint,
                                              structure = structure)
        true = nd_image.grey_erosion(tmp, footprint = footprint,
                                              structure = structure)
        output = nd_image.grey_closing(array,
                              footprint = footprint, structure = structure)
        self.failUnless(diff(true, output) < eps)

    def test_morphological_gradient01(self):
        "morphological gradient 1"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp1 = nd_image.grey_dilation(array,
                             footprint = footprint, structure = structure)
        tmp2 = nd_image.grey_erosion(array, footprint = footprint,
                                              structure = structure)
        true = tmp1 - tmp2
        output = numarray.zeros(array.shape, array.dtype)
        nd_image.morphological_gradient(array,
                footprint=footprint, structure=structure, output = output)
        self.failUnless(diff(true, output) < eps)

    def test_morphological_gradient02(self):
        "morphological gradient 2"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp1 = nd_image.grey_dilation(array,
                             footprint = footprint, structure = structure)
        tmp2 = nd_image.grey_erosion(array, footprint = footprint,
                                              structure = structure)
        true = tmp1 - tmp2
        output =nd_image.morphological_gradient(array,
                                footprint=footprint, structure=structure)
        self.failUnless(diff(true, output) < eps)

    def test_morphological_laplace01(self):
        "morphological laplace 1"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp1 = nd_image.grey_dilation(array,
                              footprint = footprint, structure = structure)
        tmp2 = nd_image.grey_erosion(array, footprint = footprint,
                                              structure = structure)
        true = tmp1 + tmp2 - 2 * array
        output = numarray.zeros(array.shape, array.dtype)
        nd_image.morphological_laplace(array, footprint=footprint,
                                     structure=structure, output = output)
        self.failUnless(diff(true, output) < eps)

    def test_morphological_laplace02(self):
        "morphological laplace 2"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp1 = nd_image.grey_dilation(array,
                             footprint = footprint, structure = structure)
        tmp2 = nd_image.grey_erosion(array, footprint = footprint,
                                              structure = structure)
        true = tmp1 + tmp2 - 2 * array
        output = nd_image.morphological_laplace(array,
                                footprint=footprint, structure=structure)
        self.failUnless(diff(true, output) < eps)

    def test_white_tophat01(self):
        "white tophat 1"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = nd_image.grey_opening(array, footprint = footprint,
                                             structure = structure)
        true = array - tmp
        output = numarray.zeros(array.shape, array.dtype)
        nd_image.white_tophat(array, footprint=footprint,
                                      structure=structure, output = output)
        self.failUnless(diff(true, output) < eps)

    def test_white_tophat02(self):
        "white tophat 2"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = nd_image.grey_opening(array, footprint = footprint,
                                             structure = structure)
        true = array - tmp
        output = nd_image.white_tophat(array, footprint=footprint,
                                                structure=structure)
        self.failUnless(diff(true, output) < eps)

    def test_black_tophat01(self):
        "black tophat 1"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = nd_image.grey_closing(array, footprint = footprint,
                                             structure = structure)
        true = tmp - array
        output = numarray.zeros(array.shape, array.dtype)
        nd_image.black_tophat(array, footprint=footprint,
                                      structure=structure, output = output)
        self.failUnless(diff(true, output) < eps)

    def test_black_tophat02(self):
        "black tophat 2"
        array = numarray.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = nd_image.grey_closing(array, footprint = footprint,
                                             structure = structure)
        true = tmp - array
        output = nd_image.black_tophat(array, footprint=footprint,
                                                structure=structure)
        self.failUnless(diff(true, output) < eps)

    def test_hit_or_miss01(self):
        "binary hit-or-miss transform 1"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[0, 1, 0, 0, 0],
                                   [1, 1, 1, 0, 0],
                                   [0, 1, 0, 1, 1],
                                   [0, 0, 1, 1, 1],
                                   [0, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 1],
                                   [0, 1, 1, 1, 1],
                                   [0, 0, 0, 0, 0]], type)
            out = numarray.zeros(data.shape, numarray.Bool)
            nd_image.binary_hit_or_miss(data, struct,
                                                 output = out)
            self.failUnless(diff(true, out) < eps)

    def test_hit_or_miss02(self):
        "binary hit-or-miss transform 2"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        true = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[0, 1, 0, 0, 1, 1, 1, 0],
                                   [1, 1, 1, 0, 0, 1, 0, 0],
                                   [0, 1, 0, 1, 1, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_hit_or_miss(data, struct)
            self.failUnless(diff(true, out) < eps)

    def test_hit_or_miss03(self):
        "binary hit-or-miss transform 3"
        struct1 = [[0, 0, 0],
                   [1, 1, 1],
                   [0, 0, 0]]
        struct2 = [[1, 1, 1],
                   [0, 0, 0],
                   [1, 1, 1]]
        true = [[0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numarray.array([[0, 1, 0, 0, 1, 1, 1, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = nd_image.binary_hit_or_miss(data, struct1,
                                              struct2)
            self.failUnless(diff(true, out) < eps)


class NDImageTestResult(unittest.TestResult):
    separator1 = '=' * 70 + '\n'
    separator2 = '-' * 70 + '\n'

    def __init__(self, stream, verbose):
        unittest.TestResult.__init__(self)
        self.stream = stream
        self.verbose = verbose

    def getDescription(self, test):
        return test.shortDescription() or str(test)

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        if self.verbose:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        if self.verbose:
            self.stream.write("ok\n")

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        if self.verbose:
            self.stream.write("ERROR\n")

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        if self.verbose:
            self.stream.write("FAIL\n")

    def printErrors(self):
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.write(self.separator1)
            description = self.getDescription(test)
            self.stream.write("%s: %s\n" % (flavour, description))
            self.stream.write(self.separator2)
            self.stream.write(err)

def test():
    if '-v' in sys.argv[1:]:
        verbose = 1
    else:
        verbose = 0
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NDImageTest))
    result = NDImageTestResult(sys.stdout, verbose)
    suite(result)
    result.printErrors()
    return len(result.failures), result.testsRun

if __name__ == '__main__':
    unittest.main()
