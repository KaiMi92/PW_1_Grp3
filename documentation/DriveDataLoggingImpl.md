<h1>Implementierung des Loggings der Fahrdaten - Gruppe 3 / Gen 8</h1>

<h2>Eigene Anforderungen an das Logging der Fahrdaten</h2>

Ziel unserer DriveData-Logging-Implementierung war es, dass jede Klasse, die ein Fahrzeug repräsentiert, also
* BaseCar
* SonicCar
* SensorCar

selbst alle notwendigen Daten loggt. 

Dies hat folgende Vorteile:

* Abstraktion: Logging bleibt dem Benutzer (also den Fahrmodi) verborgen.
* Kapselung: Es werden garantiert alle notwendigen Daten geloggt, aber auch nur diese. 


<h2>Umsetzung in der Basisklasse BaseCar</h2>

In Python gibt es intern die Magic Methode "__setattr__(self, name, value)". Diese Methode wird aufgerufen, wenn der Wert eines Attributes der  Klasse gesetzt werden soll. Die Methode hat zwei Argument:
* name: der Name des Attributes, des Wert gesetzt werden soll
* value: der Wert, der diesem Attribut gegeben werden soll
Weitere Informationen finden sich hier: https://peps.python.org/pep-0726/

Es besteht die Möglichkeit diese Methode zu überschreiben. Damit werden dann jegliche Zuweisungen an ein Attribut an diese Methode übergeben. Unsere Implementierung in der Klasse BaseCar sieht wiefolgt aus:

Dies haben wir uns zu Nutze gemacht und schreiben bei Attributszuweisungen dies Werte in das Log-File, nachdem dieses in  "__init__" bereits angelegt wurde:

    def __setattr__(self, name, value):
        """
        - overwrite magic methode __setattr__:
        - logs all assignment to "public" attributes (without a leading underscore)
          into a CSV file together with timestamp.
        """

        # actual setting of the attribute
        object.__setattr__(self, name, value)

        # Check if we want logging
        # do not log if it is a "private" attribute (with a leading underscore)
        if not name.startswith("_"):
            t = round(time.time() - self._start_time, 2)

            current_values = []
            for prop in self.fieldnames_to_log:
                try:
                    v = getattr(self, str.lower(prop))

                    if isinstance(v, list):
                        for x in v:
                            current_values.append(x)
                    else:
                        current_values.append(v)
                except AttributeError:
                    # abort logging if not all values are set
                    return

            row = [t] + current_values

            # append to CSV file
            with open(self._log_filename, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(row)

Da nicht alle Attribute geloggt werden sollen, existieren zwei Listen als Klassenattribute mit selbsterklärenden Bezeichnungen:

    fieldnames_to_log = ['direction','speed','steering_angle']

Anhand dieser Listen werden die zu loggenden Attribute gefiltert. Da die Namen der Spalten der CSV-Logging-Datei zum Namen des Attributes unterschiedliche sein soll, existiert eine weitere Liste auf Klassenebene:

    csv_col_name_of_fieldnames = ['Direction','Speed','Steering']



<h2>Umsetzung in den abgeleiteten Klassen</h2>

Die von BaseCar abgeleiteten Klassen SonicCar und SensorCar eben die __setattr__ Implementierung aus BaseCar automatisch.
Somit sind in diesen Klassen nur die o.g. Listen der zu loggenden Attribute und deren CSV-Namen zu weitern, zum Beispiel in der Klasse SensorCar:

class SensorCar(SonicCar):
    fieldnames_to_log = BaseCar.fieldnames_to_log + ["analog_values"]
    csv_col_name_of_fieldnames = BaseCar.csv_col_name_of_fieldnames + ['IR-v1','IR-v2','IR-v3','IR-v4','IR-v5']

<h2>Besonderheiten beim Umgang mit Listen</h2>

Im gezeigten Beispiel der Klasse SensorCar wird das Attribut analog_values, das eine Liste repräsentiert, in der CSV auf die Spalten 'IR-v1' bis 'IR-v5' abgebildet. Dies geschieht, um für einzelnen Listenwerde eigene Spalten in der CSV-Datei zu haben.
Auch die passiert durch die Implementierung in BaseCar:

    if isinstance(v, list):
    for x in v:
        current_values.append(x)