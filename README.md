[![codecov](https://codecov.io/gh/Den-geografiska-oredan/eBike-controlsys-python/branch/master/graph/badge.svg?token=JPSD6XZ7GR)](https://codecov.io/gh/Den-geografiska-oredan/eBike-controlsys-python)

## Beskrivning

Detta program har till uppgift att simulera x antal cyklar i olika städer. Rutterna som cyklas är framslumpade bland ett antal för-definierade rutter för varje stad. Cyklarna i simlutionen rör sig med en fram-slumpad hastighet på mellan 5 - 20 km/h.

Alla cyklar som simuleras rapporterar sin position en gång per sekund.

### Installation

Programmet kan enkelt installeras och köras via docker. Med docker installerat kan du köra:

    docker pull robisr/e_bike_simulator:latest
    docker run -it robisr/e_bike_simulator 100

Detta för att köra igång en simulation med 100 st cyklar. Siffran efter docker run kommandot är ett commandline argument som anger det antal cyklar som ska köras.
