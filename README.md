🧩 Core Base — Django + React Starter

Este repositorio contiene el núcleo común (core) utilizado como punto de partida para proyectos basados en Django + React.
Incluye componentes, contextos, utilidades y configuraciones que se repiten en la mayoría de los proyectos, tanto del backend como del frontend.

El objetivo es evitar reescribir lo mismo una y otra vez, mantener coherencia entre proyectos y permitir mejoras evolutivas compartidas.

🌱 Estructura general del repositorio
main              → rama neutra o de referencia (opcional)
core              → rama base compartida por todos los proyectos
carteles          → rama de proyecto A basada en core
feria_virtual     → rama de proyecto B basada en core


Cada rama de proyecto mantiene su independencia funcional, pero puede sincronizar los cambios comunes desde core.
