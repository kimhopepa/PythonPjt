import numpy as np

tmp_arr1 = np.array([1,2,3])
print("1차원 배열", tmp_arr1)

tmp_arr2 = np.array([[1,2], [3,4]])
print("2차원 배열", tmp_arr2)

#1. 2차원 배열로 출력 가능
tmp_arr3= np.array([[1,2,3], [1,2,3]])
print("0, 2 좌표를 출력" , tmp_arr3[0,2])


# arrar 매소드 확인
#2-1. 차원 확인
print(tmp_arr1.ndim, tmp_arr3.ndim)

#2-2. 각 차원의 길이
print("차원의 길이", tmp_arr1.shape, tmp_arr2.shape, tmp_arr3.shape, type(tmp_arr3.shape))

#2-3. 
print("배열의 총합", tmp_arr1.sum(), tmp_arr2.sum(), tmp_arr3.sum(), type(tmp_arr3.sum()))