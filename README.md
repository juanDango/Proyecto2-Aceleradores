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
El objetivo de este proyecto fue el de simular la trayectoria de un protón acelerado en un ciclotrón a una energía de 200MeV. De esta forma, se quería verificar propiedades importantes para el funcionamiento del dispositivo, como el que se mantenga el periodo constante a lo largo del tiempo, además, de visualizar la trayectoria que sigue la partícula, el espacio de fase y su radio calculado de dos formas distintas. De esta manera, se creó un programa en python el cual simula un protón que entra en un ciclotrón y que se acelera a una cierta energía $E_max$
</p>
<p align="justify">
El ciclotrón es una máquina propuesta por Ernest Lawrence, la cual tiene como objetivo el acelerar iones a altas energías haciendo uso de voltajes pequeños. En si, el diseño está compuesto por dos semicírculos en los cuales hay un campo magnético constante perpendicular al plano de los semicírculos. Asimismo, el espacio entre las dos regiones con forma de D se encuentra un campo eléctrico conectado a una fuente AC, el cual se encarga de aumentar la energía de las partículas.
</p>
<p align="center">
<img src="Ciclotron.png" />
</p>
<p align="justify">
 En el segundo programa se simulan partículas que entran con un ángulo de incidencia theta_0 medido respecto al eje y. Para este caso se estudiaron dos escenarios. El primero consistía en variar la velocidad de salida mientras se mantenía constante theta_0  y el segundo que variaba theta_0, manteniendo constante la magnitud de la velocidad. Para cada partícula que salía con un ángulo theta_0 se simulaba una segunda que incidía en un ángulo -theta_0. El campo magnético se aplicó nuevamente con una magnitud B=8T en la dirección k con una carga de magnitud q = 5C. En teoría, el punto donde finalizan ambas trayectorias debe coincidir, lo cual genera un efecto de enfoque. El montaje se puede ver en la figura mostrada a continuación. El archivo que contiene el código está en el repositorio que se encuentra al final del documento en el archivo <code>parte2/parte2.py</code>.

