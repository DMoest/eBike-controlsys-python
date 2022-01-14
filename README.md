[![Build](https://github.com/Den-geografiska-oredan/eBike-controlsys-python/actions/workflows/main.yml/badge.svg)](https://github.com/Den-geografiska-oredan/eBike-controlsys-python/actions/workflows/main.yml)

[![codecov](https://codecov.io/gh/Den-geografiska-oredan/eBike-controlsys-python/branch/master/graph/badge.svg?token=JPSD6XZ7GR)](https://codecov.io/gh/Den-geografiska-oredan/eBike-controlsys-python)

## Beskrivning

Detta program har till uppgift att simulera x antal cyklar i olika städer. Rutterna som cyklas är framslumpade bland ett antal för-definierade rutter för varje stad. Cyklarna i simlutionen rör sig med en fram-slumpad hastighet på mellan 5 - 20 km/h.

Alla cyklar som simuleras rapporterar sin position en gång var 30:e sekund.

### Installation

Bygg image:

    docker-compose build ebike_simulator

Kör igång:

    docker-compose run ebike_simulator <antal>

Detta för att köra igång en simulation med det angivna antalet cyklar (Max 1000 stycken). Siffran efter docker run kommandot är ett commandline argument som anger det antal cyklar som ska köras.


### Köra tester

Testerna för denna applikation kan köras med:

    pytest
