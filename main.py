from pdfreader import SimplePDFViewer
from gtts import gTTS
import re
import glob
from itertools import cycle
# from playsound import playsound

def digito_verificador(rut):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    return (-s) % 11

print("Hola")
print(glob.glob('*'))
files = glob.glob('pdfs/*[!_backup].pdf')
print(files)

# Read each pdf file and parse it to get some values and store it as a string
# Numero de informe
# Folio externo
# Nombre
# Edad
# Rut
# Fecha de recepcion
# Fecha de entrega
# Procedencia
# Doctor

to_read = []
for f in files:
    fd = open(f, "rb")
    viewer = SimplePDFViewer(fd)
    viewer.render()

    plain_text = "".join(viewer.canvas.strings)

    values = re.split(("(?:Informe No : ([0-9]+-[0-9]+))\s+?"
                            "(?:Fol\.Externo:([0-9]+))\s+?"
                            "(?:NOMBRE : ((\w+\s?)+)Edad)"
                            "(?: :([0-9]+))\s+?"
                            "(?:Rut :([0-9]+-[0-9kK]))\s+?"
                            "(?:F.Recep.:([0-9]+-[0-9]+-[0-9]+))\s+?"
                            "(?:F.Entrega.:([0-9]+-[0-9]+-[0-9]+))\s+?"
                            "(?:Procedencia :\s+?((\w+\s?)+)DR. \(A\) )"
                            "(?:: ((\w+\s?)+)Muestra)"), plain_text)
    texto = (f[5:] + 
            ", Informe número " + values[1] + 
            ", Folio externo " + values[2] + 
            ", Nombre " + values[3] + 
            ", edad " + values[5] + 
            ", rut " + values[6] + 
            ", fecha de recepción " + values[7] + 
            ", fecha de entrega " + values[8] + 
            ", procedencia " + values[9] + 
            ", doctor " + values[11])
    to_read.append([f[5:], texto])

    # Check for the last digit to confirm if it is correct
    dv = str(digito_verificador(values[6][:-2]))
    if dv == "10":
        dv = "K"

    # Capitalize the letter k
    values[6] = values[6].upper()

    if dv == values[6][-1]:
        print("RUT " + values[6] + " OK")
    else:
        print("RUT " + values[6] + " OJO CON ESTE RUT, debería ser -" + dv)

print(to_read)

# Read each string and write an MP3 file with the reading
for read in to_read:
    filename = read[0][:-4]
    tts = gTTS(read[1], lang='es')
    with open("audio/"+filename+".mp3", "wb") as archivo:
        tts.write_to_fp(archivo)

    # playsound("audio/"+filename+".mp3")