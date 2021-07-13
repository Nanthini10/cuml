from cuml.explainer.sampling import kmeans_sampling
import cudf
import cupy as cp
from numba import cuda
import pytest


@pytest.mark.parametrize('input_type', ['df',
                                        'series',
                                        'cupy',
                                        'numba'])
def test_kmeans_input(input_type):
    X = cp.array([[0, 10],
                  [1, 24],
                  [0, 52],
                  [0, 48.0],
                  [0.2, 23],
                  [1, 24],
                  [1, 23]])
    if input_type == 'df':
        X = cudf.DataFrame(X)
    elif input_type == 'series':
        X = cudf.Series(X[:, 1])
    elif input_type == 'numba':
        X = cuda.as_cuda_array(X)

    summary = kmeans_sampling(X, k=2, detailed=True)

    if input_type == 'df':
        cp.testing.assert_array_equal(summary[0].values.tolist(),
                                      [[1., 23.],
                                       [0., 52.]])
        assert isinstance(summary[0], cudf.DataFrame)
    elif input_type == 'series':
        cp.testing.assert_array_equal(summary[0].values.tolist(),
                                      [23., 52.])
        assert isinstance(summary[0], cudf.core.series.Series)
    elif input_type == 'numba':
        cp.testing.assert_array_equal(cp.array(summary[0]).tolist(),
                                      [[1., 23.],
                                       [0., 52.]])
        assert isinstance(summary[0], cuda.devicearray.DeviceNDArray)
    else:
        cp.testing.assert_array_equal(summary[0].tolist(),
                                      [[1., 23.],
                                       [0., 52.]])
        assert isinstance(summary[0], cp.ndarray)
