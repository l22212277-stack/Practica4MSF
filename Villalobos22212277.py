"""
Práctica 5.4: Sistema cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Alberto Villalobos Valdez
Número de control: 22212277
Correo institucional: L22212277@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot


# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from scipy import signal
import pandas as pd

u = np.array(pd.read_excel('signal.xlsx', header = None))
X0,t0,tf,dt,w,h = 0,0,10,1E-3,10,5
N=round((tf-t0)/dt)+1
t = np.linspace(t0,tf,N)
u = np.reshape(signal.resample(u, len(t)),-1)

def cardio(Z,C,L,R):
    num=[L*R,R*Z]
    den=[C*L*R*Z,L*R+L*Z,R*Z]
    sys=ctrl.tf(num,den)
    return sys
#Funcion d transferencia: Normotenso
Z,C,R,L = 0.033,1.5,0.95,0.01
sysnormo=cardio(Z,C,L,R)
print(f'funcion de transferencia normotenso: {sysnormo}')
    
Z,C,R,L = 0.02,0.25,0.6,0.005
syshipo=cardio(Z,C,L,R)
print(f'funcion de transferencia normotenso: {syshipo}')

Z,C,R,L = 0.05,2.5,1.4,0.02
syshiper=cardio(Z,C,L,R)
print(f'funcion de transferencia normotenso: {syshiper}')
        
_,Pp0 = ctrl.forced_response(sysnormo,t,u,X0)
_,Pp1 = ctrl.forced_response(syshipo,t,u,X0)
_,Pp2 = ctrl.forced_response(syshiper,t,u,X0)

clr1= np.array([145,18,188])/255
clr2 = np.array([0,120,157])/255
clr6 = np.array([0,0,0])/255
clr3=np.array([120,157,188])/255
clr4=np.array([203,4,4])/255

fg1=plt.figure()
plt.plot(t,Pp0,'-',linewidth=1,color=clr1,label='Pp(t): Normotenso')
plt.plot(t,Pp1,'-',linewidth=1,color=clr2,label='Pp(t): Hipotenso')
plt.plot(t,Pp2,'-',linewidth=1,color=clr6,label='Pp(t): Hipertenso')
plt.xlabel('t [s]',fontsize = 11)
plt.ylabel('Pp(t) [V]',fontsize = 11)
plt.xlim(0,10);plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1);plt.yticks(np.arange(-0.6,1.6,0.2))
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol=3,fontsize = 9,frameon = True)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('SistemaCardioVascular.pdf',bbox_inches = 'tight',dpi=660)
fg1.savefig('SistemaCardioVascular.png',bbox_inches = 'tight',dpi=660)

def controlador(kP,kI,sys):
    Cr=1E-6
    Re=1/(kI*Cr)
    Rr=kP*Re
    numPI=[Rr*Cr,1]
    denPI=[Re*Cr,0]
    Pi=ctrl.tf(numPI,denPI)
    X=ctrl.series(Pi,sys)
    sysPI=ctrl.feedback(X,1,sign=-1)
    return sysPI
hipoPI=controlador(193.256201926113,13207.0629447757,syshipo)
hiperPI=controlador(2280.67262524598,728391.346123884,syshiper)

_,Pp3=ctrl.forced_response(hipoPI,t,Pp0,X0)
_,Pp4=ctrl.forced_response(hiperPI,t,Pp0,X0)

fg2=plt.figure()
plt.plot(t,Pp0,'-',linewidth=1,color=clr1,label='Pp(t): Normotenso')
plt.plot(t,Pp1,'-',linewidth=1,color=clr2,label='Pp(t): Hipotenso')
plt.plot(t,Pp3,':',linewidth=3,color=clr3,label='Pp(t): Hipotenso PI')
plt.xlabel('t [s]',fontsize = 11)
plt.ylabel('Pp(t) [V]',fontsize = 11)
plt.xlim(0,10);plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1);plt.yticks(np.arange(-0.6,1.6,0.2))
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol=3,fontsize = 9,frameon = True)
plt.show()
fg2.set_size_inches(w,h)
fg2.tight_layout()
fg2.savefig('SistemaCardioVascularPIHIPO.pdf',bbox_inches = 'tight',dpi=660)
fg2.savefig('SistemaCardioVascularPIHIPO.png',bbox_inches = 'tight',dpi=660)

fg3=plt.figure()
plt.plot(t,Pp0,'-',linewidth=1,color=clr1,label='Pp(t): Normotenso')
plt.plot(t,Pp2,'-',linewidth=1,color=clr2,label='Pp(t): Hipertenso')
plt.plot(t,Pp4,':',linewidth=3,color=clr4,label='Pp(t): Hipertenso PI')
plt.xlabel('t [s]',fontsize = 11)
plt.ylabel('Pp(t) [V]',fontsize = 11)
plt.xlim(0,10);plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1);plt.yticks(np.arange(-0.6,1.6,0.2))
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol=3,fontsize = 9,frameon = True)
plt.show()
fg3.set_size_inches(w,h)
fg3.tight_layout()
fg3.savefig('SistemaCardioVascularPIHIPER.pdf',bbox_inches = 'tight',dpi=660)
fg3.savefig('SistemaCardioVascularPIHIPER.png',bbox_inches = 'tight',dpi=660)



