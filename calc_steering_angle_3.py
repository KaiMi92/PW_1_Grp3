import time

"""
    !!! Generelle Information !!!
    Diese Funktion berechnet den Lenkwinkel des Autos.
    Dazu wird die Steigung der gesamten Linien berechnet, die durch die Hough-Transformation gefunden wurden.
    Der Durchschnitt der Steigungen wird dann in einen Lenkwinkel umgerechnet.
    Der Lenkwinkel wird dann zurückgegeben.
"""

def calculate_steering_angle(image, lines):
    sum = 0
    runs = 0
    average = 0
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            """ 
            Berechnung der Steigung 
            """
            if (x2 - x1) != 0:
                slope = (y2 - y1) / (x2 - x1)
            else:
                continue

            """
            Berechnung des Durchschnitts der Steigungen
            """

            runs += 1
            sum += slope
            average = sum/runs

    """""
    Umrechnung der Steigung in einen Lenkwinkel
    Der Lenkwinkel wird auf einen Wert zwischen 45 und 135 begrenzt"
    """

    x = 90
    if average > 0 and average <3:
        x = x - (average * 70)
        if x < 45:
            x = 45

    elif average < 0 and average > -3:
        x = x + (abs(average) * 70)
        if x > 135:
            x = 135

    steering_angle = x

    return steering_angle

#calculate_steering_angle()