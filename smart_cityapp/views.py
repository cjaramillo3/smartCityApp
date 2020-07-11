from django.shortcuts import render
from django.http import HttpResponse
from SPARQLWrapper import SPARQLWrapper, JSON
from smart_cityapp.models import *
# Create your views here.{{observacion.sensor}}

def index(request):
    return render(request, 'smart_cityapp/index.html')

def economia(request):
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setQuery("""
      PREFIX sosa:<http://www.w3.org/ns/sosa/>
     PREFIX om:<http://www.ontology-of-units-of-measure.org/resource/om-2/>
     PREFIX time:<http://www.w3.org/2006/time#>
     PREFIX ssn:<http://www.w3.org/ns/ssn/>

     SELECT DISTINCT ?ObjetoInteres ?Propiedad ?Resultado ?Unidad ?UnidadMedida (concat(year(?FechaInicio), "-",month(?FechaInicio),"-", day(?FechaInicio))as ?FechaInicio)  (concat(year(?FechaFin), "-",month(?FechaFin),"-", day(?FechaFin))as ?FechaFin)  WHERE{
     ?observacion a sosa:Observation;
     rdfs:label "Venta Productos Industriales";
     sosa:hasFeatureOfInterest ?obint;
     ssn:hasProperty ?propiedad;
     time:hasBeginning ?FechaInicio;
     time:hasEnd ?FechaFin;
     sosa:hasResult ?resultado.
     ?resultado om:hasUnit ?um.
     ?um owl:sameAs ?UnidadMedida;
     rdfs:label ?Unidad.
     ?obint rdfs:label ?ObjetoInteres.
     ?propiedad rdfs:label ?Propiedad.
     ?resultado rdfs:label ?Resultado.
     ?unidad rdfs:label ?Unidad
     }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    productos = []
    for result in results["results"]["bindings"]:
        producto = Producto(result["ObjetoInteres"]["value"])
        producto.objeto = (result["ObjetoInteres"]["value"])
        producto.propiedad = result["Propiedad"]["value"]
        producto.resultado = result["Resultado"]["value"]
        producto.unidad = result["Unidad"]["value"]
        producto.unidaduri = result["UnidadMedida"]["value"]
        producto.inicio = result["FechaInicio"]["value"]
        producto.fin = result["FechaFin"]["value"]
        productos.append(producto)

    # CONSULTA actividades económicas
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setQuery("""
        PREFIX sosa:<http://www.w3.org/ns/sosa/>
        PREFIX time:<http://www.w3.org/2006/time#>
        PREFIX ssn:<http://www.w3.org/ns/ssn/>
        PREFIX sosa:<http://www.w3.org/ns/sosa/>
        SELECT DISTINCT ?ob ?ObjetoInteres ?Propiedad ?Resultado (concat(year(?FechaInicio), "-",month(?FechaInicio),"-", day(?FechaInicio))as ?FechaInicio)  (concat(year(?FechaFin), "-",month(?FechaFin),"-", day(?FechaFin))as ?FechaFin)  WHERE{
        ?observacion a sosa:Observation;
        rdfs:label ?ob;
        sosa:hasFeatureOfInterest ?obint;
        ssn:hasProperty ?propiedad;
        time:hasBeginning ?FechaInicio;
        time:hasEnd ?FechaFin;
        sosa:hasResult ?resultado.
        ?obint rdfs:label ?ObjetoInteres.
        ?propiedad rdfs:label ?Propiedad.
        ?resultado rdfs:label ?Resultado.
        ?unidad rdfs:label ?Unidad
        FILTER (?ob="Servicios" || ?ob="Agricultura, ganaderia y pesca" || ?ob="Industria y energia" || ?ob="Construccion")
        }
        ORDER BY (?ObjetoInteres)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    actividades = []
    for result in results["results"]["bindings"]:
        observacion = Actividades(result["ObjetoInteres"]["value"])
        observacion.obs = (result["ob"]["value"])
        observacion.objeto = (result["ObjetoInteres"]["value"])
        observacion.propiedad = result["Propiedad"]["value"]
        observacion.resultado = result["Resultado"]["value"]
        observacion.inicio = result["FechaInicio"]["value"]
        observacion.fin = result["FechaFin"]["value"]
        actividades.append(observacion)

    return render(request, 'smart_cityapp/economia.html', {'productos':productos, 'actividades':actividades})

def ambiente(request):
    # CONSULTA CLIMA
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setQuery("""
        PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX dul:<http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
        PREFIX sosa:<http://www.w3.org/ns/sosa/>
        PREFIX time:<http://www.w3.org/2006/time#>
        PREFIX ssn:<http://www.w3.org/ns/ssn/>
PREFIX om:<http://www.ontology-of-units-of-measure.org/resource/om-2/>

        SELECT DISTINCT ?ObjetoInteres ?uO ?Propiedad ?uP ?Sensor ?Latitud ?Longitud ?Resultado ?Unidad ?uM ?FechaInicio    WHERE{
        ?observacion a sosa:Observation;
        rdfs:label "Clima";
        sosa:hasFeatureOfInterest ?obint;
        ssn:hasProperty ?propiedad;
        sosa:resultTime ?FechaInicio;
        sosa:madeBySensor ?sensor;
        sosa:hasResult ?resultado.
        ?resultado om:hasUnit ?unidad.
        ?obint rdfs:label ?ObjetoInteres.
        ?propiedad rdfs:label ?Propiedad.
        ?resultado rdfs:label ?Resultado.
        ?unidad rdfs:label ?Unidad.
        ?sensor rdfs:label ?Sensor;
        dul:hasLocation ?punto.
        ?punto geo:lat ?Latitud;
        geo:long ?Longitud
        OPTIONAL{?obint owl:sameAs ?uO}
        OPTIONAL{?propiedad owl:sameAs ?uP}
        OPTIONAL{?unidad owl:sameAs ?uM}

        }ORDER BY ?ObjetoInteres ?FechaInicio
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    resultados = []
    for result in results["results"]["bindings"]:
        resultado = Clima(result["ObjetoInteres"]["value"])
        resultado.objeto = (result["ObjetoInteres"]["value"])
        resultado.objetoURI = (result["uO"]["value"])
        resultado.propiedad = result["Propiedad"]["value"]
        resultado.propiedadURI = result["uP"]["value"]
        resultado.sensor = result["Sensor"]["value"]
        resultado.latitud = result["Latitud"]["value"]
        resultado.longitud = result["Longitud"]["value"]
        resultado.resultado = result["Resultado"]["value"]
        resultado.unidad = result["Unidad"]["value"]
        resultado.unidadURI = result["uM"]["value"]
        resultado.inicio = result["FechaInicio"]["value"]
        resultados.append(resultado)

    # CONSULTA Incendios
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setQuery("""
        PREFIX sosa:<http://www.w3.org/ns/sosa/>
        PREFIX time:<http://www.w3.org/2006/time#>
        PREFIX ssn:<http://www.w3.org/ns/ssn/>
        PREFIX om:<http://www.ontology-of-units-of-measure.org/resource/om-2/>

        SELECT DISTINCT ?ObjetoInteres ?uO ?Propiedad ?Resultado ?Unidad ?uM (concat(year(?FechaInicio), "-",month(?FechaInicio),"-", day(?FechaInicio))as ?FechaInicio)  (concat(year(?FechaFin), "-",month(?FechaFin),"-", day(?FechaFin))as ?FechaFin)  WHERE{
        ?observacion a sosa:Observation;
        rdfs:label "Incendios";
        sosa:hasFeatureOfInterest ?obint;
        ssn:hasProperty ?propiedad;
        time:hasBeginning ?FechaInicio;
        time:hasEnd ?FechaFin;
        sosa:hasResult ?resultado.
        ?resultado om:hasUnit ?unidad.
        ?unidad rdfs:label ?Unidad.
        ?obint rdfs:label ?ObjetoInteres.
        ?propiedad rdfs:label ?Propiedad.
        ?resultado rdfs:label ?Resultado.
        ?unidad rdfs:label ?Unidad
        OPTIONAL{?obint owl:sameAs ?uO}
        OPTIONAL{?unidad owl:sameAs ?uM}
         }
         ORDER BY (?ObjetoInteres)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    incendios = []
    for result in results["results"]["bindings"]:
        observacion = Incendio(result["ObjetoInteres"]["value"])
        observacion.objeto = (result["ObjetoInteres"]["value"])
        observacion.objetoURI = (result["uO"]["value"])
        observacion.propiedad = result["Propiedad"]["value"]
        observacion.resultado = result["Resultado"]["value"]
        observacion.unidad = result["Unidad"]["value"]
        observacion.unidadURI = result["uM"]["value"]
        observacion.inicio = result["FechaInicio"]["value"]
        observacion.fin = result["FechaFin"]["value"]
        incendios.append(observacion)

    return render(request, 'smart_cityapp/ambiente.html', {'resultados':resultados, 'incendios':incendios})

def salud(request):
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setQuery("""
        PREFIX sosa:<http://www.w3.org/ns/sosa/>
        PREFIX om:<http://www.ontology-of-units-of-measure.org/resource/om-2/>
        PREFIX time:<http://www.w3.org/2006/time#>
        PREFIX ssn:<http://www.w3.org/ns/ssn/>

        SELECT DISTINCT ?Observacion ?uO ?ObjetoInteres ?Propiedad ?Resultado (concat(year(?FechaInicio), "-",month(?FechaInicio),"-", day(?FechaInicio))as ?Fecha)    WHERE{
        ?observacion a sosa:Observation;
        rdfs:label ?Observacion;
        owl:sameAs ?uO;
        sosa:hasFeatureOfInterest ?obint;
        ssn:hasProperty ?propiedad;
        sosa:resultTime ?FechaInicio;
        sosa:hasResult ?resultado.
        ?obint rdfs:label ?ObjetoInteres.
        ?propiedad rdfs:label ?Propiedad.
        ?resultado rdfs:label ?Resultado.
        FILTER(?Observacion = "Coronavirus")
        }
        ORDER BY DESC(?Fecha)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    coronavirus = []
    for result in results["results"]["bindings"]:
        corona = Casos(result["Observacion"]["value"])
        corona.observacion = (result["Observacion"]["value"])
        corona.observacionURI = (result["uO"]["value"])
        corona.objeto = (result["ObjetoInteres"]["value"])
        corona.propiedad = result["Propiedad"]["value"]
        corona.resultado = result["Resultado"]["value"]
        corona.inicio = result["Fecha"]["value"]
        coronavirus.append(corona)


    return render(request, 'smart_cityapp/salud.html', {'coronavirus':coronavirus})

def seguridad(request):
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setQuery("""
        PREFIX sosa:<http://www.w3.org/ns/sosa/>
        PREFIX om:<http://www.ontology-of-units-of-measure.org/resource/om-2/>
        PREFIX time:<http://www.w3.org/2006/time#>
        PREFIX ssn:<http://www.w3.org/ns/ssn/>

        SELECT DISTINCT ?ObjetoInteres ?uO ?Propiedad ?Resultado year(?FechaInicio)as ?Anio    WHERE{
        ?observacion a sosa:Observation;
        rdfs:label "Resultados Electorales";
        sosa:hasFeatureOfInterest ?obint;
        ssn:hasProperty ?propiedad;
        sosa:resultTime ?FechaInicio;
        sosa:hasResult ?resultado.
        ?obint rdfs:label ?ObjetoInteres.
        ?propiedad rdfs:label ?Propiedad.
        ?resultado rdfs:label ?Resultado.
        OPTIONAL {?obint owl:sameAs ?uO}
        }ORDER BY (?ObjetoInteres)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    resultados = []
    for result in results["results"]["bindings"]:
        resultado = Elecciones(result["ObjetoInteres"]["value"])
        resultado.objeto = (result["ObjetoInteres"]["value"])
        resultado.objetoURI = (result["uO"]["value"])
        resultado.propiedad = result["Propiedad"]["value"]
        resultado.resultado = result["Resultado"]["value"]
        resultado.inicio = result["Anio"]["value"]
        resultados.append(resultado)
    return render(request, 'smart_cityapp/seguridad.html', {'resultados':resultados})

def trafico(request):
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setQuery("""
        PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX dul:<http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
        PREFIX sosa:<http://www.w3.org/ns/sosa/>
        PREFIX time:<http://www.w3.org/2006/time#>
        PREFIX ssn:<http://www.w3.org/ns/ssn/>
        PREFIX om:<http://www.ontology-of-units-of-measure.org/resource/om-2/>

        SELECT DISTINCT ?ObjetoInteres ?Propiedad ?uP ?Sensor ?Latitud ?Longitud ?Resultado ?Unidad ?uM ?FechaInicio    WHERE{
        ?observacion a sosa:Observation;
        rdfs:label "Trafico";
        sosa:hasFeatureOfInterest ?obint;
        ssn:hasProperty ?propiedad;
        sosa:resultTime ?FechaInicio;
        sosa:madeBySensor ?sensor;
        sosa:hasResult ?resultado.
        ?resultado om:hasUnit ?unidad.
        ?unidad rdfs:label ?Unidad.
        ?obint rdfs:label ?ObjetoInteres.
        ?propiedad rdfs:label ?Propiedad.
        ?resultado rdfs:label ?Resultado.
        ?sensor rdfs:label ?Sensor;
        dul:hasLocation ?punto.
        ?punto geo:lat ?Latitud;
        geo:long ?Longitud
        OPTIONAL{?propiedad owl:sameAs ?uP}
        OPTIONAL{?unidad owl:sameAs ?uM}
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    resultados = []
    for result in results["results"]["bindings"]:
        resultado = Vehiculos(result["ObjetoInteres"]["value"])
        resultado.objeto = (result["ObjetoInteres"]["value"])
        resultado.propiedad = result["Propiedad"]["value"]
        resultado.propiedadURI = result["uP"]["value"]
        resultado.sensor = result["Sensor"]["value"]
        resultado.latitud = result["Latitud"]["value"]
        resultado.longitud = result["Longitud"]["value"]
        resultado.resultado = result["Resultado"]["value"]
        resultado.unidad= result["Unidad"]["value"]
        resultado.unidadURI = result["uM"]["value"]
        resultado.inicio = result["FechaInicio"]["value"]
        resultados.append(resultado)
    return render(request, 'smart_cityapp/trafico.html', {'resultados':resultados})

def turismo(request):
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setQuery("""
        PREFIX sosa:<http://www.w3.org/ns/sosa/>
        PREFIX om:<http://www.ontology-of-units-of-measure.org/resource/om-2/>
        PREFIX time:<http://www.w3.org/2006/time#>
        PREFIX ssn:<http://www.w3.org/ns/ssn/>

        SELECT DISTINCT ?Observacion ?ObjetoInteres ?uO ?Propiedad ?Resultado year(?FechaInicio)as ?Anio    WHERE{
        ?observacion a sosa:Observation;
        rdfs:label ?Observacion;
        sosa:hasFeatureOfInterest ?obint;
        ssn:hasProperty ?propiedad;
        sosa:resultTime ?FechaInicio;
        sosa:hasResult ?resultado.
        ?obint rdfs:label ?ObjetoInteres.
        ?propiedad rdfs:label ?Propiedad.
        ?resultado rdfs:label ?Resultado.
        OPTIONAL {?obint owl:sameAs ?uO}
        FILTER (?Observacion="Hotel 1 estrella" || ?Observacion="Hotel 2 estrellas" || ?Observacion="Hotel 3 estrellas" || ?Observacion="Hotel 4 estrellas" || ?ob="Hotel 5 estrellas" || ?Observacion="Hostal")
        }
        ORDER BY (?Observacion)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    hoteles = []
    for result in results["results"]["bindings"]:
        producto = Hoteles(result["Observacion"]["value"])
        producto.nombre = (result["Observacion"]["value"])
        producto.objeto = (result["ObjetoInteres"]["value"])
        producto.objetoURI = (result["uO"]["value"])
        producto.propiedad = result["Propiedad"]["value"]
        producto.resultado = result["Resultado"]["value"]
        producto.inicio = result["Anio"]["value"]
        hoteles.append(producto)
    return render(request, 'smart_cityapp/turismo.html', {'hoteles':hoteles})
