import plotly 

py = plotly.plotly(username='**username**', key='**put your api key here**')


y=0
t=0
dt=0.01
g=9.8
v=4
yp=[]
tp=[]

while y>=0:
    v=v-g*dt
    y=y+v*dt
    t=t+dt
    yp=yp+[y]
    tp=tp+[t]



response=py.plot(tp,yp)
url=response['url']
filename=response['filename']
print(url)
print(filename)
