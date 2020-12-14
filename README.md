## Aceleradores de Partículas y sus Aplicaciones
### Proyecto 2: Ciclotron
> Elaborado por: Juan Daniel Castrellón Botero (201729285) y María Sofía Álvarez López (201729031)}

<div align="center"><a name="menu"></a>
  <h4>
    <a href="#intro">
      Introducción al proyecto
    </a>
    <span> | </span>
    <a href=#correr>
      Correr el proyecto
    </a>
  </h4>
</div>

<h2 name="intro">Introducción al proyecto</h2>
<p align="justify"> 
El objetivo de este proyecto fue el de simular la trayectoria de un protón acelerado en un ciclotrón a una energía de 200MeV. De esta forma, se quería verificar propiedades importantes para el funcionamiento del dispositivo, como el que se mantenga el periodo constante a lo largo del tiempo, además, de visualizar la trayectoria que sigue la partícula, el espacio de fase y su radio calculado de dos formas distintas. De esta manera, se creó un programa en python el cual simula un protón que entra en un ciclotrón y que se acelera a una cierta energía $E_{max}$
</p>
<p align="justify">
  Con el fin de lograr el objetivo propuesto, se crearon dos programas en el lenguaje de programación Python. El primero simula una partícula que incide perpendicularmente a la base del espectrómetro, es decir, tiene una velocidad en la dirección <i>j</i>. Por su lado, el campo magnético tenía una magnitud B=8T en dirección <i>k</i>. El objetivo de este programa era verificar que el momento de la partícula al entrar al espectrómetro, calculado como |p| = m|v|, es el mismo al salir, calculado según la ecuación |p| = q|B|R, donde <i>B</i> es el campo magnético, <i>R</i> el radio de la trayectoria semicircular que sigue la partícula y q = 5 C la carga de la partícula. El radio de la partícula se calculó con la distancia x_final a la que sale la partícula del espectrómetro, medida desde su punto de entrada, teniendo en cuenta que x_final = 2R. El código implementado para llevar a cabo este objetivo se encuentra en el archivo <code>parte1/parte1.py</code>.
</p>
<p align="justify">
 En el segundo programa se simulan partículas que entran con un ángulo de incidencia theta_0 medido respecto al eje y. Para este caso se estudiaron dos escenarios. El primero consistía en variar la velocidad de salida mientras se mantenía constante theta_0  y el segundo que variaba theta_0, manteniendo constante la magnitud de la velocidad. Para cada partícula que salía con un ángulo theta_0 se simulaba una segunda que incidía en un ángulo -theta_0. El campo magnético se aplicó nuevamente con una magnitud B=8T en la dirección k con una carga de magnitud q = 5C. En teoría, el punto donde finalizan ambas trayectorias debe coincidir, lo cual genera un efecto de enfoque. El montaje se puede ver en la figura mostrada a continuación. El archivo que contiene el código está en el repositorio que se encuentra al final del documento en el archivo <code>parte2/parte2.py</code>.
 <p align="center">
<img src="imagenes/Feynman_theta.png" />
</p>
