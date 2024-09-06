import numpy as np
from scipy.stats import norm

import streamlit as st


def calculatePrice(S,X,r,var,q,t,type='c'):
    d1=(np.log(S/X)+t*(r-q+(var**2)/2))/(var*np.sqrt(t))
    d2=d1-var*np.sqrt(t)
    # print(d1,' ',d2)
    # print('\n')

    if(type=='c'):
        optionPrice=S*(np.exp(-1*q*t))*norm.cdf(d1)-X*np.exp(-1*r*t)*norm.cdf(d2)
    else:
        optionPrice=X*np.exp(-1*r*t)*norm.cdf(-1*d2)-S*np.exp(-1*q*t)*norm.cdf(-1*d1)
    return optionPrice


def optionDelta(S,X,r,var,q,t,type='c'):
    d1=(np.log(S/X)+t*(r-q+(var**2)/2))/(var*np.sqrt(t))
    d2=d1-var*np.sqrt(t)

    if(type=='c'):
        optionD=np.exp(-1*q*t)*norm.cdf(d1)
    else:
        optionD=np.exp(-1*q*t)*(norm.cdf(-1*d1)-1)
    return optionD

def optionGamma(S,X,r,var,q,t):
    d1=(np.log(S/X)+t*(r-q+(var**2)/2))/(var*np.sqrt(t))
    gamma=np.exp(-1*q*t)*norm.pdf(d1)/(S*var*np.sqrt(t))
    return gamma

def optionTheta(S,X,r,var,q,t,type='c'):
    d1=(np.log(S/X)+t*(r-q+(var**2)/2))/(var*np.sqrt(t))
    d2=d1-var*np.sqrt(t)

    if(type=='c'):
        theta=(-1*(S*var*np.exp(-1*q*t)*norm.pdf(d1))/(2*np.sqrt(t))-r*X*np.exp(-1*r*t)*norm.cdf(d2)+q*S*np.exp(-1*q*t)*norm.cdf(d1))/t
    else:
        theta=(-1*(S*var*np.exp(-1*q*t*norm.pdf(d1))/(2*np.sqrt(t)))+r*X*np.exp(-1*r*t)*norm.cdf(-1*d2)-q*S*np.exp(-1*q*t)*norm.cdf(-1*d1))/t
    return theta

def optionVega(S,X,r,var,q,t):
    d1=(np.log(S/X)+t*(r-q+(var**2)/2))/(var*np.sqrt(t))
    d2=d1-var*np.sqrt(t)
    vega=S*np.exp(-1*q*t)*np.sqrt(t)*norm.pdf(d1)/100
    return vega

def optionRho(S,X,r,var,q,t,type='c'):
    d1=(np.log(S/X)+t*(r-q+(var**2)/2))/(var*np.sqrt(t))
    d2=d1-var*np.sqrt(t)

    if(type=='c'):
        rho=X*t*np.exp(-1*r*t)*norm.cdf(d2)/100
    else:
        rho=-1*(X*t*np.exp(-1*r*t)*norm.cdf(-1*d2))/100
    return rho


st.set_page_config(page_title="Black-Scholes Model")

sidebar_title = st.sidebar.header("Black-Scholes Parameters")
space = st.sidebar.header("")
r = st.sidebar.number_input("Risk-Free Rate", min_value=0.000, max_value=1.000, step=0.001, value=0.030)
S = st.sidebar.number_input("Underlying Asset Price", min_value=1.00, step=0.10, value=30.00)
X = st.sidebar.number_input("Strike Price", min_value=1.00, step=0.10, value=50.00)
days_to_expiry = st.sidebar.number_input("Time to Expiry Date (in days)", min_value=1, step=1, value=250)
var = st.sidebar.number_input("Volatility", min_value=0.000, max_value=1.000, step=0.01, value=0.30)
q= st.sidebar.number_input("Dividend Yield", min_value=0.00, max_value=1.000,step=0.10, value=0.00)
type_input = st.sidebar.selectbox("Option Type",["Call", "Put"])


type=""
if type_input=="Call":
    type = "c"
elif type_input=="Put":
    type = "p"

T = days_to_expiry/365

prices = calculatePrice(S,X,r,var,q,T, type)
deltas = optionDelta(S,X,r,var,q,T, type)
gammas = optionGamma(S,X,r,var,q,T)
thetas = optionTheta(S,X,r,var,q,T, type)
vegas = optionVega(S,X,r,var,q,T)
rhos = optionRho(S,X,r,var,q,T, type)


st.markdown("<h2 align='center'>Black-Scholes Option Price Calculator</h2>", unsafe_allow_html=True)
st.markdown("<h5 align='center'>Made by Samarth Bhutani</h5>", unsafe_allow_html=True)
st.header("")
st.markdown("<h3 align='center'>Option Prices and Greeks</h3>", unsafe_allow_html=True)
st.header("")
col1, col2, col3, col4, col5 = st.columns(5)
col2.metric("Call Price", str(round(calculatePrice(S,X,r,var,q,T, type="c"), 3)))
col4.metric("Put Price", str(round(calculatePrice(S,X,r,var,q,T, type="p"), 3)))

bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
bcol1.metric("Delta", str(round(calculatePrice(S,X,r,var,q,T, type), 3)))
bcol2.metric("Gamma", str(round(optionGamma(S,X,r,var,q,T), 3)))
bcol3.metric("Theta", str(round(optionTheta(S,X,r,var,q,T, type), 3)))
bcol4.metric("Vega", str(round(optionVega(S,X,r,var,q,T), 3)))
bcol5.metric("Rho", str(round(optionRho(S,X,r,var,q,T, type), 3)))
