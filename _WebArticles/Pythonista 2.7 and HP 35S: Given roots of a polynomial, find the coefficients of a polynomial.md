# Pythonista 2.7 and HP 35S: Given roots of a polynomial, find the coefficients of a polynomial

_Captured: 2015-09-30 at 17:44 from [edspi31415.blogspot.de](http://edspi31415.blogspot.de/2014/08/pythonista-27-and-hp-35s-given-roots-of.html)_

**General**

Variables:  
Number of Roots: N   
Roots: R, S, T, U  
Coefficients: A, B, C, D, E

N = 2, roots R and S:  
(x - R) * (x - S) -> A * x^2 + B * x + C

Formulas:   
A = 1  
B = -(R + S)  
C = R * S

N = 3, roots R, S, and T:  
(x - R) * (x - S) * (x - T) -> A * x^3 + B * x^2 + C * x + D

Formulas:  
A = 1  
B = -(R + S + T)  
C = R * S + R * T + S * T

N = 4, roots R, S, T, and U:  
(x - R) * (x - S) * (x - T) * (x - U) -> A * x^4 + B * x^3 + C * x^2 + D * x + E

Formulas:  
A = 1  
B = -(R + S + T + U)  
C = R * S + R * T + R * U + S * T + S * U + T * U  
D = -(R * S * T + R * S * U + R * T * U + S * T * U)  
E = R * S * T * U

**HP-35S: Coefficients To Roots**

Program:   
C001 LBL C  
C002 SF 10 // SF, decimal point, 0  
C003 NO OF ROOTS // enter message as an equation  
C004 CF 10 // CF, decimal point, 0  
C005 INPUT N  
C006 4 // error checking  
C007 xC008 GTO C113  
C009 R-down  
C010 2  
C011 x>y?   
C012 GTO C113  
C013 1 // main routine  
C014 STO A  
C015 INPUT R  
C016 INPUT S  
C017 RCL N   
C018 3  
C019 x=y?  
C020 GTO C033  
C021 R-down  
C022 4  
C023 x=y?  
C024 GTO C054  
C025 RCL R // two roots  
C026 RCL+ S  
C027 +/-  
C028 STO B  
C029 RCL R  
C030 RCLx S  
C031 STO C  
C032 GTO C101  
C033 INPUT T // three roots  
C034 RCL R  
C035 RCL+ S  
C036 RCL+ T  
C037 +/-  
C038 STO B  
C039 RCL R  
C040 RCLx S  
C041 RCL R  
C042 RCLx T  
C043 +  
C044 RCL S  
C045 RCLx T  
C046 +  
C047 STO C  
C048 RCL R  
C049 RCLx S  
C050 RCLx T  
C051 +/-  
C052 STO D  
C053 GTO C101  
C054 INPUT T // four roots  
C055 INPUT U  
C056 +  
C057 RCL+ S  
C058 RCL+ R  
C059 +/-  
C060 STO B  
C061 RCL R  
C062 RCLx S  
C063 RCL R  
C064 RCLx T  
C065 +  
C066 RCL R  
C067 RCLx U  
C068 +  
C069 RCL S  
C070 RCLx T  
C071 +  
C072 RCL S  
C073 RCLx U  
C074 +  
C075 RCL T  
C076 RCLx U  
C077 +  
C078 STO C  
C079 RCL R  
C080 RCLx S  
C081 RCLx T  
C082 RCL R  
C083 RCLx S  
C084 RCLx U  
C085 +  
C086 RCL R  
C087 RCLx T  
C088 RCLx U  
C089 +  
C090 RCL S  
C091 RCLx T  
C092 RCLx U  
C093 +  
C094 +/-  
C095 STO D  
C096 RCL R  
C097 RCLx S  
C098 RCLx T  
C099 RCLx U  
C100 STO E  
C101 VIEW A // results  
C102 VIEW B  
C103 VIEW C  
C104 RCL N  
C105 3  
C106 x≤y?  
C107 VIEW D  
C108 RCL N  
C109 4  
C110 x=y?  
C111 VIEW E  
C112 RTN  
C113 0 // invoking the error condition  
C114 1/x

**Pythonista**

Input: Enter a vector of coefficients, up to 4 roots  
Output: A list of coefficients, in descending order

Note: the triple periods indicate a tab (...)

# let roots be the list of roots, up to 4  
# EWS 2014-08-20  
import math  
roots=input('List of Roots (up to 4):')  
n=len(roots)  
poly=[1]  
# check for order  
if n==2:  
...# quadratic  
...poly.append(-(roots[0]+roots[1]))  
...poly.append(roots[0]*roots[1])  
...print('List of coefficients: ',poly)  
elif n==3:  
...# cubic  
...temp=-(roots[0]+roots[1]+roots[2])  
...poly.append(temp)  
...temp=roots[0]*roots[1]+roots[0]*roots[2]+roots[1]*roots[2]  
...poly.append(temp)  
...temp=-roots[0]*roots[1]*roots[2]  
...poly.append(temp)  
...print('List of coefficients: ',poly)  
elif n==4:  
...# quartic  
...temp=-(roots[0]+roots[1]+roots[2]+roots[3])  
...poly.append(temp)  
...temp=roots[0]*roots[1]+roots[0]*roots[2]+roots[0]*roots[3]+roots[1]*roots[2]+roots[1]*roots[3]+roots[2]*roots[3]  
...poly.append(temp)  
...temp=-(roots[0]*roots[1]*roots[2]+roots[0]*roots[1]*roots[3]+roots[0]*roots[2]*roots[3]+roots[1]*roots[2]*roots[3])  
...poly.append(temp)  
...temp=roots[0]*roots[1]*roots[2]*roots[3]  
...poly.append(temp)  
...print('List of Coefficients: ',poly)  
else:  
...print('Error: not a valid list')

**Examples:**

Quadratic:  
R = 2, S = -4  
A = 1, B = 2, C = -8

Cubic:  
R = 3, S = -1, T = -3  
A = 1, B = 1, C = -9, D = -9

Quartic:  
R = 3, S = -1, T = -3, U = 4  
A = 1, B = -3, C = -13, D = 27, E = 36

Eddie

This blog is property of Edward Shore. 2014

![](https://lh4.googleusercontent.com/-kwqQ5Ih4irY/U_a99ydO2UI/AAAAAAAAChM/QSlZYlK10pY/76612CD4-D819-4426-A2F2-48ACA1D0AD16.jpg)
