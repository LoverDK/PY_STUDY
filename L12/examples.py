"""L12: in-memory NumPy indexing and axis examples; no file I/O."""
import warnings
import numpy as np
from numpy.testing import assert_array_equal, assert_allclose

def main():
    A = np.arange(12).reshape(3,4)
    before = A.copy()
    assert_array_equal(A[[0,2],[1,3]],[1,11])
    block = A[np.ix_([0,2],[1,3])]
    assert_array_equal(block,[[1,3],[9,11]])
    assert block.shape == (2,2) and not np.shares_memory(A,block)
    assert_array_equal(A[[2,0,2],0],[8,0,8])
    assert_array_equal(A.sum(axis=0),[12,15,18,21])
    assert_array_equal(A.sum(axis=1),[6,22,38])
    assert A.sum() == 66
    row_mean = A.mean(axis=1,keepdims=True)
    assert row_mean.shape == (3,1)
    centered = A-row_mean
    assert_allclose(centered,np.tile([-1.5,-0.5,0.5,1.5],(3,1)))
    square = np.array([[1.,3.],[10.,20.]])
    correct = square-square.mean(axis=1,keepdims=True)
    wrong = square-square.mean(axis=1)
    assert_allclose(correct,[[-1,1],[-5,5]])
    assert not np.allclose(wrong,correct)
    B = np.array([[60.,80.],[90.,70.],[50.,100.]])
    chosen = B[B[:,0]>=60]
    assert chosen.shape == (2,2)
    assert_allclose(chosen.mean(axis=0),[75.,75.])
    assert_array_equal(B[B>=80],[80,90,100])
    empty = A[np.ix_(np.array([],dtype=np.intp),np.array([1,3],dtype=np.intp))]
    assert empty.shape == (0,2)
    with warnings.catch_warnings():
        warnings.simplefilter("error",RuntimeWarning)
        selected = B[B[:,0]>101]
        means = selected.mean(axis=0) if len(selected) else np.full(B.shape[1],np.nan,dtype=np.float64)
        assert_allclose(means,[np.nan,np.nan],equal_nan=True)
    base = np.arange(6).reshape(2,3)
    view = base[:,1:]
    assert np.shares_memory(base,view)
    view[0,0] = -1
    assert base[0,1] == -1
    copy = base[[0,1]]
    copy[0,0] = 999
    assert base[0,0] == 0
    y = np.zeros(3,dtype=int)
    np.add.at(y,[0,0],1)
    assert_array_equal(y,[2,0,0])
    assert_array_equal(A,before)
    print("Paired:",A[[0,2],[1,3]])
    print("Cartesian block:",block,sep="\n")
    print("Row means:",row_mean,sep="\n")
    print("L12 example assertions passed")

if __name__ == "__main__":
    main()
