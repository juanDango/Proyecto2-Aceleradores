from matplotlib.patches import Wedge
from matplotlib import animation
import matplotlib.pyplot as plt
from scipy import constants
from scipy import stats
import numpy as np
import datetime
import os

print()
print('------------------Simulación de un ciclotrón------------------')
print('---------Juan Daniel Castrellón y María Sofía Álvarez---------')
print()
# Parametros
#Diferencia de potencial para calcular posteriormente el campo electrico maximo de la region entre las dos D
dif_potencial = float(input('Escriba una diferencia de potencial en Volts para la región de campo eléctrico (e.g. 110):\n'))
#Radio del ciclotron
R = float(input('Escriba el radio del ciclotrón en metros (e.g. 1):\n'))
#Ancho de la region de campo electrico, ubicada entre las dos D
#Se divide entre 2 puesto que, para los calculos, nos es mas conveniente tomar unicamente la mitad 
regionE = float(input('Escriba el ancho de la región de campo eléctrico en metros (e.g. 0.05)\n'))/2
#Energia maxima que la particula puede alcanzar (en MeV)
Emax = float(input('Escriba la energía máxima, en MeV, que pueden alcanzar las partículas (e.g. 200)\n'))

#Calculo del campo electrico necesario para acelerar la particula a partir de la diferencia de potencial dada
factor_de_conversion = constants.e/(np.sqrt(1e6*constants.e*constants.m_p))
E0 = factor_de_conversion*dif_potencial/(2*regionE)
#Posicion inicial de la particula
posicion_inicial = np.array([[0.0, 0.0, 0.0]])
# Tiempo inicial para correr la simulacion
t_inicial = 0
#Carga del electron
e = 1#*constants.e
#Masa del proton
m_p = 1#*constants.m_p

delta_t = 1e-10


def fuerza_y_aceleracion(q, pos, v, B, m, E, regionE):
    # Fuerza magnetica
    Fmag = q*np.cross(v, B)

    # Fuerza Electrica
    Felec = 0
    if(abs(pos[:,1])<regionE):
        Felec = q*E
    F = Fmag + Felec
    a = F/m #raiz(MeV/m_p)/s
    a *= np.sqrt(1e6)
    a *= np.sqrt(constants.e)
    a *= np.sqrt(1/constants.m_p)
    return F, a

def mover_particula(dt, posicion_anterior, velocidad_anterior, aceleracion_anterior):
    posicion_actual = posicion_anterior + velocidad_anterior*dt + 0.5*aceleracion_anterior*(dt**2)
    velocidad_actual = velocidad_anterior + aceleracion_anterior*dt
    return posicion_actual, velocidad_actual

def evolucionar_verlet(e, m_p, delta_t, posicion_inicial, E0, regionE, R, Emax, archivo_E_v):
    archivo_E_v.write('E_entrar_region_D,E0-E_entrar_region_D,v\n')
    #Definicion de las trayectorias, velocidades y aceleraciones
    v_inicial = np.array([[0.0, 0.0, 0.0]])
    a_inicial = np.array([[0.0, 0.0, 0.0]])
    trayectoria = np.array(posicion_inicial)
    velocidad = np.array(v_inicial)
    aceleracion = np.array(a_inicial)

    #Encontramos el campo electrico querido
    p_max = np.sqrt(2*m_p*Emax) #raiz(mp*MeV)
    mag_B = p_max/(e*R) #raiz(mp*MeV)/qe*m
    B = np.array([[0.0, 0.0, mag_B]])

    #Calculamos las coondiciones iniciales
    r_xy = posicion_inicial[:,0]

    t = 0.0
    t_inicial = t
    esta_temporizando = True
    periodos = []
    tiempos = []
    omega = e*np.linalg.norm(B)/m_p
    omega = omega*10**3*np.sqrt(constants.e/constants.m_p)
    E = np.array([0, np.cos(omega*t)*E0, 0])
    F_1, a_1 = fuerza_y_aceleracion(e, posicion_inicial ,v_inicial, B, m_p, E, regionE)
    pos_1, v_1 = mover_particula(delta_t, posicion_inicial, v_inicial, a_1)
    r_xy_1 = np.sqrt(pos_1[:,0]**2 + pos_1[:,1]**2)
    trayectoria = np.append(trayectoria, pos_1, axis=0)
    velocidad = np.append(velocidad, v_1, axis=0)
    aceleracion = np.append(aceleracion, a_1, axis=0)
    primera_vez = True
    t+=delta_t
    r_obtenido_xy = [r_xy, r_xy_1]
    i = 1
    r_xy = r_xy_1
    energias = []
    formato = '{},{},{}\n'
    while r_xy < R:
        E = np.array([0, np.cos(omega*t)*E0, 0])
        F, a= fuerza_y_aceleracion(e, trayectoria[i].reshape(1,3) ,velocidad[i], B, m_p, E, regionE)
        pos, v = mover_particula(delta_t, trayectoria[i], velocidad[i], a)
        trayectoria = np.append(trayectoria, pos, axis=0)
        velocidad = np.append(velocidad, v, axis=0)
        aceleracion = np.append(aceleracion, a, axis=0)
        i += 1
        if esta_temporizando and pos[:,1] <= 0:
            esta_temporizando = False
            periodos.append(t - t_inicial)
            tiempos.append(t)
            energia_llegada = 0.5*constants.m_p*(np.linalg.norm(v)**2)
            energia_llegada /= (1e6*constants.e)
            energias.append(energia_llegada)
            archivo_E_v.write(formato.format(E[1], E0-np.abs(E[1]), v[:,1].item()))
        elif (not esta_temporizando and pos[:,1] >= 0):
            t_inicial = t
            esta_temporizando = True
        t += delta_t
        r_xy = np.sqrt(pos[:,0]**2+pos[:,1]**2)
        if(primera_vez and pos[:,1]<=0):
            radio = pos[:,0]/2
            trayectoria[:,0] -= radio
            primera_vez = False
        r_obtenido_xy.append(r_xy)
    periodos = np.array(periodos)
    tiempos = np.array(tiempos)
    return trayectoria, velocidad, aceleracion, periodos, tiempos, r_obtenido_xy, energias

def obtener_r_momento(radio, energia_J, masa_kg, carga_C, velocidad):
    magnitud_B = np.sqrt(2*masa_kg*energia_J)/(carga_C*radio)
    r_obtenido_momento = []
    for v in velocidad:
        momento = np.linalg.norm(v)*masa_kg
        r = momento/(magnitud_B*carga_C)
        r_obtenido_momento.append(r)
    return r_obtenido_momento

def graficar_trayectoria():
    plt.figure(figsize=(7,7))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    centro_sup = (0,regionE)
    centro_inf = (0,-regionE)
    w1 = Wedge(centro_sup, R, 0, 180, ec='dimgray', fc='white', linewidth=5)
    w2 = Wedge(centro_inf,R, 180, 360, ec='dimgray', fc='white', linewidth=5)
    ax.add_artist(w1)
    ax.add_artist(w2)

    plt.xlabel('Posición en x [m]')
    plt.ylabel('Posición en y [m]')
    plt.title('Posición de la partícula en x,y [m]')
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    plt.plot(trayectoria[:,0], trayectoria[:,1], '.', c='#69b6ff')
    plt.savefig(carpeta + '/trayectoria_ciclotron.png')
    plt.close()

def graficar_momento(trayectoria, velocidad, coordenada):
    plt.figure(figsize=(7,7))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    if coordenada == 'x':
        plt.xlabel('Posición en x [m]')
        plt.ylabel('Momento en x [m*kg/s]')
        plt.title('Momento de la partícula en función de la posición en x')
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.plot(trayectoria, velocidad*constants.m_p, '.', c='#d56bff')
        plt.savefig(carpeta + '/px_vs_x.png')
    else:
        plt.xlabel('Posición en y [m]')
        plt.ylabel('Momento en y [m*kg/s]')
        plt.title('Momento de la partícula en función de la posición en y')
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.plot(trayectoria, velocidad*constants.m_p,'.', c='#4debc1')
        plt.savefig(carpeta + '/py_vs_y.png')

def graficar_periodos(tiempos, periodos):
    plt.figure(figsize=(7,7))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('tiempo [s]')
    plt.ylabel('periodo [s]')
    plt.suptitle('Periodo de la partícula en el semicírculo superior en función del tiempo')
    plt.plot(tiempos, periodos,'.',c='#f590e9')
    plt.savefig(carpeta + '/periodo_vs_tiempo.png')

def graficar_r(r_xy, r_momento):
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.squeeze(r_momento), np.squeeze(r_xy))
    x = np.linspace(min(r_momento), max(r_xy), 1000)
    plt.figure(figsize=(7,7))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('Radio de la trayectoria a partir del momento')
    plt.ylabel('Radio de la trayectoria a partir de la posición')
    plt.title('Cálculo de los radios de la trayectoria por momento y posición')
    plt.plot(r_momento, r_xy,'.',c='#f5e990')
    plt.plot(x, intercept + slope*x, c='#f5c490', label=r'Ajuste lineal $r_p$ = {:3f}$r_x$ + {:.3f} con $R^2$={:.3f}'.format(slope, intercept, r_value**2))
    plt.legend(loc='best')
    plt.savefig(carpeta + '/r_xy_vs_r_momento.png')

def graficar_energia_tiempo(tiempo, energia):
    plt.figure(figsize=(7,7))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Energía [MeV]')
    plt.title('Energía de la partícula al salir de la "D" en función del tiempo')
    plt.plot(tiempo, energia,'.', c='#9f90f5')
    plt.savefig(carpeta + '/energia_tiempo.png')

def graficar_velocidades(velocidad):
    plt.figure(figsize=(7,7))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('Velocidad de la partícula en x [m/s]')
    plt.ylabel('Velocidad de la partícula en y [m/s]')
    plt.title('Velocidad de la partícula en y vs x')
    plt.plot(velocidad[:,0], velocidad[:,1],'.', c='#f59f90')
    plt.savefig(carpeta + '/vy_vx.png')

def update(j, data, ax):
    ax.clear()
    centro_sup = (0,regionE)
    centro_inf = (0,-regionE)
    w1 = Wedge(centro_sup, R, 0, 180, ec='dimgray',fc='white',linewidth=5,zorder=0)
    w2 = Wedge(centro_inf,R, 180, 360, ec='dimgray',fc='white', linewidth=5,zorder=0)
    ax.add_artist(w1)
    ax.add_artist(w2)
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.scatter(data[j,0], data[j,1], marker ='o', s = 500, color = '#69FF82',zorder=5)
    ax.plot(data[0:j+1,0], data[0:j+1,1], color = '#69FF82',zorder=5)

def crear_animacion(trayectoria):
    fig = plt.figure(figsize=(16,16), dpi=75)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax = fig.gca()
    centro_sup = (0,regionE)
    centro_inf = (0,-regionE)
    w1 = Wedge(centro_sup, R, 0, 180, ec='dimgray', fc='white', linewidth=5)
    w2 = Wedge(centro_inf,R, 180, 360, ec='dimgray', fc='white', linewidth=5)
    ax.add_artist(w1)
    ax.add_artist(w2)
    tomar_desde = int(len(trayectoria[:])*3/5)
    prueba = trayectoria[tomar_desde::5]
    N = prueba.shape[0]
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    #ax.plot(prueba[0:1,0], prueba[0:1,1], color = '#69FF82')
    #ax.scatter(prueba[0,0], prueba[0,1], marker='o', s = 500, color = '#69FF82')
    ani = animation.FuncAnimation(fig, update, N, fargs=(prueba, ax))
    ani.save(carpeta + '/ciclotron.mp4', fps=60)
    plt.close(fig)


path = './simulaciones/'
try:
    os.mkdir('simulaciones')
except:
    pass
fecha = str(datetime.datetime.now())
carpeta = ''
try:
    carpeta = os.path.join(path, fecha)
    os.mkdir(carpeta)
except:
    print('No se ha podido crear el directorio para almacenar los archivos')
    exit(-1)

archivo_E_v = open(carpeta + '/E_v.dat', 'w')
resultados_verlet =  evolucionar_verlet(e, m_p, delta_t, posicion_inicial, E0, regionE, R, Emax, archivo_E_v)
trayectoria = resultados_verlet[0]
velocidad = resultados_verlet[1]
periodos = resultados_verlet[3]
tiempos = resultados_verlet[4]
r_obtenido_xy = resultados_verlet[5]
energias = resultados_verlet[6]
r_obtenido_momento = obtener_r_momento(R, Emax*1e6*constants.e, constants.m_p, constants.e, velocidad)

print ('El numero de posiciones generadas fue de: {}'.format(len(trayectoria)))

p = constants.m_p*velocidad
Ecalc = np.linalg.norm(p[-1])**2/(2*constants.m_p) # J
Ecalc /= constants.e #EV
Ecalc /= 1e6

graficar_trayectoria()
graficar_momento(trayectoria[:,0], velocidad[:,0], 'x')
graficar_momento(trayectoria[:,1], velocidad[:,1], 'y')
graficar_periodos(tiempos, periodos)
graficar_r(r_obtenido_xy, r_obtenido_momento)
graficar_energia_tiempo(tiempos, energias)
graficar_velocidades(velocidad)
print('La energia calculada para la particula al final de la trayectoria es de: {:.2f}'.format(Ecalc))
crear_animacion(trayectoria)



