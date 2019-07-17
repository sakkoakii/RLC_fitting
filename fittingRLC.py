# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

PI = np.pi

## csvファイル名を定義
file_path = './'
file_id = input()

file_name = file_path + file_id
data = np.loadtxt(file_name, comments='#' ,delimiter=',')

#x,yデータを読み込む
x_csv = data[:,0]
y_csv = data[:,1]


def main():
    #rlcパラメータ推定のための初期値[c,l,r]
    parameter0 = [1e-9,1e-9,1e-3]

    #leastsq() -> 最小二乗法, fit_funcが最小になるような値を返す
    result = optimize.leastsq(fit_func,parameter0,args=(x_csv,y_csv))
    print(result)
    c_fit = result[0][0]
    l_fit = result[0][1]
    r_fit = result[0][2]
    
    plt.figure(figsize=(9,6))
    plt.loglog(x_csv,y_csv,linewidth=3)
    plt.loglog(x_csv, np.sqrt( r_fit**2 + (( 2 * PI * x_csv * l_fit ) - ( 1 / (2 * PI * x_csv * c_fit ) ))**2 ),linestyle="dashed",color="black",linewidth=4)
    plt.legend(['AC analysis','Fitting'])
    plt.xlabel("Frequency [Hz]") 
    plt.ylabel("Impedance [Ω]") 
    
    print('R = ',r_fit, '[Ohm]')
    print('L = ',l_fit, '[H]')
    print('C = ',c_fit, '[F]')
    plt.grid()
    plt.show()


## フィッティングする関数式
def fit_func(parameter,x,y):
    c = parameter[0]
    l = parameter[1]
    r = parameter[2]
    residual = y - np.sqrt( r**2 + (( 2 * PI * x_csv * l ) - ( 1 / (2 * PI * x_csv * c ) ))**2 )
    return residual


if __name__ == "__main__":
    main()