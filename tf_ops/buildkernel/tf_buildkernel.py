import tensorflow as tf
from tensorflow.python.framework import ops
import sys, os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
buildkernel_module = tf.load_op_library(os.path.join(base_dir, 'tf_buildkernel_so.so'))


def spherical_kernel(database,
                     query,
                     nn_index,
                     nn_count,
                     nn_dist,
                     radius,
                     kernel=[8,2,3]):
    '''
    Input:
        database: (batch, npoint, 3+) float32 array, database points (x,y,z,...)
        query:    (batch, mpoint, 3+) float32 array, query points (x,y,z,...)
        nn_index: (batch, mpoint, nnsample) int32 array, neighbor indices
        nn_count: (batch, mpoint) int32 array, number of neighbors
        nn_dist: (batch, mpoint, nnsample) float32, sqrt distance array
        radius:  float32, range search radius
        kernel:   list of 3 int32, spherical kernel size
    Output:
        filt_index: (batch, mpoint, nnsample) int32 array, filter bin indices
    '''
    n, p, q = kernel

    database = database[:, :, 0:3]  #(x,y,z)
    query = query[:, :, 0:3] #(x,y,z)
    return buildkernel_module.spherical_kernel(database, query, nn_index, nn_count, nn_dist, radius, n, p, q)
ops.NoGradient('SphericalKernel')


def fuzzy_spherical_kernel(database,
                           query,
                           nn_index,
                           nn_count,
                           nn_dist,
                           radius,
                           kernel=[8,2,3]):
    '''
    Input:
        database: (batch, npoint, 3+) float32 array, database points (x,y,z,...)
        query:    (batch, mpoint, 3+) float32 array, query points (x,y,z,...)
        nn_index: (batch, mpoint, nnsample) int32 array, neighbor indices
        nn_count: (batch, mpoint) int32 array, number of neighbors
        nn_dist: (batch, mpoint, nnsample) float32, sqrt distance array
        radius:  float32, range search radius
        kernel:   list of 3 int32, spherical kernel size
    Output:
        filt_index: (batch, mpoint, nnsample, 8) int32 array, fuzzy filter indices,
                    (8=2*2*2, 2 for each splitting dimension)
        filt_coeff: (batch, mpoint, nnsample, 8) float32 array, fuzzy filter weights,
                    kernelsize=prod(kernel)+1
    '''
    n, p, q = kernel

    database = database[:, :, 0:3]  #(x,y,z)
    query = query[:, :, 0:3] #(x,y,z)
    return buildkernel_module.fuzzy_spherical_kernel(database, query, nn_index, nn_count, nn_dist, radius, n, p, q)
ops.NoGradient('FuzzySphericalKernel')


def kpconv_kernel(database,
                  query,
                  kernel_points,
                  nn_index,
                  nn_count,
                  radius):
    sigma = radius/2.5
    kernel_points = kernel_points*(1.5*sigma)
    database = database[:, :, 0:3]  #(x,y,z)
    query = query[:, :, 0:3] #(x,y,z)
    return buildkernel_module.kpconv_kernel(database, query, kernel_points, nn_index, nn_count, sigma)
ops.NoGradient('KpconvKernel')


def fuzzy_kpconv_kernel(database,
                        query,
                        kernel_points,
                        nn_index,
                        nn_count,
                        radius):
    sigma = radius/2.5
    kernel_points = kernel_points*(1.5*sigma)
    database = database[:, :, 0:3]  #(x,y,z)
    query = query[:, :, 0:3] #(x,y,z)
    return buildkernel_module.fuzzy_kpconv_kernel(database, query, kernel_points, nn_index, nn_count, sigma)
ops.NoGradient('FuzzyKpconvKernel')