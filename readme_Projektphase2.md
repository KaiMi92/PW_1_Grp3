<details close>

<summary>

# Beschreibung wie die Lenkwinkel errechnet wurden (Frank)
---
</summary>

<br>

__1.Berechnungen der Lenkwinkel aus den drei Methoden__

- Median von Frank stark abhängig von der erkannten Anzahl der Linien rechts und links bei einer Fahrbahn besser

```python
{
  def calculate_steering_angle(image, lines):
    winkel_liste = []
    steering_angle = 90
    fahrwinkel_median = 0
    print(lines)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
        
#         # Berechnung der Steigung
            if (x2 - x1) != 0:
                slope = (y2 - y1) / (x2 - x1)
                angle_rad = np.arctan(slope)
                angle_deg = np.degrees(angle_rad) 
                winkel_liste.append(angle_deg)
            else:
                slope = float('inf') 

            #print(f"Linie von ({x1},{y1}) nach ({x2},{y2}) hat eine Steigung von {slope}, Winkel {angle_deg}")
              
        
        if winkel_liste :
            winkel_liste.sort()

            fahrwinkel_median = np.median(winkel_liste)

            if 0 <= fahrwinkel_median <= 15:
                steering_angle = 45
                print("Max-Links genommen")

            elif -15<= fahrwinkel_median < 0:
                steering_angle = 135
                print("Max-Rechts")
            else:
                steering_angle = (90-(fahrwinkel_median/2))
        

            
            print(f"Lenkwinkel= {steering_angle}")
            print(f"MedianWinkel= {fahrwinkel_median}")
            print(f"Winkel-Liste {winkel_liste}")
        
    return steering_angle
}
```
- Abstand von Punkt und Geraden von Sebastian mit Rückwärtsgang wenn es doch zu eng wird :)

[geringster Abstand zur Navigation](https://www.gutefrage.net/frage/wie-berechne-ich-abstand-von-punkt-und-gerade-allgemein2d)

- 3. Methode mit dem mittleren Steigungswert aller Linien von Kai

__Generelle Information__ 
_Diese Funktion berechnet den Lenkwinkel des Autos.Dazu wird die Steigung der gesamten Linien berechnet, die durch die Hough-Transformation gefunden wurden.Der Durchschnitt der Steigungen wird dann in einen Lenkwinkel umgerechnet.Der Lenkwinkel wird dann zurückgegeben._

---

</details>

<details close>

<summary>

# Welche Probleme gab es bei den Umsetzungen (Frank)

---

</summary>

<br>

## Weißes Pixel 

_am Rand scheinbar ein Bug aus einer früheren OPENCV-Version_


![Weißer Pixel-Rand](hhttps://i.ibb.co/pjs472xb/Wei-er-Pixel.png)

## Lichtverhältnisse

_die Lichtverhältnisse haben die Kantenerkennung stark beeinflusst und daher mussten die Filter bei unterschiedlichen Lichtverhältnissen angepasst werden._

__Lösungsmöglichkeiten__
- Einlesen der Linien bei unterschiedlichen Lichtverhältnissen mit einem Konfig-Programm
- Schieberegler bei denen die Filter vom Anwender gesetzt werden können, um eine optimalere Kantenerkennung zu ermöglichen

![Einfluss von Lichtervhätlnissen](https://fotografische.de/wp-content/uploads/lichtverhaeltnisse.jpg)

## unterschiedliche Böden

_Jeder Boden hat seine Besonderheit, die das Licht unterschiedlich stark reflektieren, Kanten, Spalten, Muster haben und viele weitere Aspekte die eine Bilderkennung beeinflussen._

![Einfluss von Böden variieren](https://www.holzland.de/media/i/MP_Bodengestaltung_1200x350-10429-0.jpg)



### zu wenig blaues Klebeband (wünsche)

### zweites paar Akkus (wünsche)

## Bild richtig übergeben OpenCV (mit Linien gelernt aber ohne) 

## Verständnis zu den Modellen viel kopiert aber nicht vollständig durchdrungen (wunsch ggf. 2Tage )

## Git Fetch Git Pull, das gleichzeitige Arbeiten an Dateien diesmal besser weil stärker auf die Reiehnfolge geachtet und mehr zusammen programmiert

## Schrumpfende Gruppe externe Einflüsse 

## Erkenntnis ggf. im Front-End manuelle Fahrt mit Bildspeicherung und dem dazugehörigen Lenkwinkel

---

</details>

<details close>

<summary>

# Wie sind die NN umgestezt worden (Frank)

---

</summary>

<br>

## Bild-Vervielfachungen
## Weißes Pixel
## wie sich ggf. Frames unterscheiden
## MAE val_loss haben

---

</details>

<details close>

<summary>

# Beschreibung des HTML-Frontends (Tonspur, Life-Umschalten) (Frank-Screenshoot)

---

</summary>

<br>
---

</details>

<details close>

<summary>

# Ggf. Video von Fahrten (Frank ggf. Sebastian mit entschärfter Todeskurve)

---

</summary>

<br>

---

</details>

<details close>

<summary>

# Ggf. MLFlow (Tonspuel, Life-vorstellung) (Sebastian)

---

</summary>

<br>

## Installationsbedingungen mit Virtueller Umgebung
## Was kann man da durch die Lernprogramme alles sehen/ erkennen

---

</details>