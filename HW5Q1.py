#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 17:22:34 2020

@author: alansu
"""
from numpy import exp, linspace, abs
from matplotlib import pyplot as plt

def ODEfunc(r,y):
    """Defining dy/dx function"""
    return r*y*(1-y)

def solfunc(t):
    """Defining given ODE exact solution function"""
    return 1/(1+exp(-t))

def predict(r,y0,t0,t1,h=1e-5):
    """Utilizes RK4 calculation in finding t1"""
    un=y0
    segments=int(round(abs(t1-t0)/h))
    h=((t1-t0)/segments)
    print(segments)
    print(h)
    for i in range(segments):
        f1=ODEfunc(r,un)
        f2=ODEfunc(r,un+((h/2)*f1))
        f3=ODEfunc(r,un+((h/2)*f2))
        f4=ODEfunc(r,un+(h*f3))
        un+=(h/6)*(f1+(2*f2)+(2*f3)+f4)
    return un

def solver(r,y0,t0,t1,h=1e-5):
    """Uses RK4 to generate list of points with step size as optional input"""
    segments=round((t1-t0)/h)
    h=((t1-t0)/segments)
    t=linspace(t0,t1,num=segments+1)
    u=[0]*(segments+1)
    u[0]=y0
    for i in range(1,segments+1):
        f1=ODEfunc(r,u[i-1])
        f2=ODEfunc(r,u[i-1]+((h/2)*f1))
        f3=ODEfunc(r,u[i-1]+((h/2)*f2))
        f4=ODEfunc(r,u[i-1]+(h*f3))
        u[i]=u[i-1]+((h/6)*(f1+(2*f2)+(2*f3)+f4))
    return t,u

def test(h=0.2):
    """Test function calls solver with Q1(c) inputs and plots the output along
    with the exact solution. Computed solution is the solid red line, exact:
    solution is the dotted green line. Step size can be adjusted. 0.2 was
    determined to be the largest step size where the solution still looked accurate"""
    r=1
    y0=0.5
    t0=0
    t1=5
    t,u=solver(r,y0,t0,t1,h)
    plt.figure(1)
    plt.plot(t,u,'r',label='Computed Solution')
    plt.plot(t,solfunc(t), 'g--',label='Exact Solution')
    plt.xlabel('t')
    plt.ylabel('y(t)')
    plt.title('Computed and Exact Solutions to Logistic Population Growth ODE')
    plt.legend(frameon=True, loc='lower right')
    
def error(h=0.2):
    r=1
    y0=0.5
    t0=0
    t1=5
    t,u=solver(r,y0,t0,t1,h)
    y=[0]*(len(u))
    for i in range(len(u)):
        y[i]=solfunc(t[i])
        u[i]=abs(u[i]-y[i])
    return max(u)

def errlist():
    errors=[0]*10
    xnum=linspace(1,10,num=10)
    print(xnum)
    for k in range(1,11):
        errors[k-1]=error(h=(2**(-k)))
    print("errors is {}" .format(errors))
    plt.figure(2)
    plt.loglog(xnum,errors)
    plt.xlabel('k')
    plt.ylabel('Error')
    plt.title('Max Error Values of RK4 ODE Solver When h=2^-k')


        
    
    
    