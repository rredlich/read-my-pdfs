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

def check_regex(match):
    if match:
            return match.group(1)
    else:
            return "No"


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

    values = []

    values.append(check_regex(re.search("Informe No\s*:\s*([0-9]+-[0-9]+)", plain_text, re.IGNORECASE)))
    values.append(check_regex(re.search("Fol\.Externo\s*:\s*([0-9]+)", plain_text, re.IGNORECASE)))
    values.append(check_regex(re.search("NOMBRE\s*:\s*(.*)Edad :", plain_text, re.IGNORECASE)))
    values.append(check_regex(re.search("Edad\s*:\s*([0-9]+)", plain_text, re.IGNORECASE)))
    values.append(check_regex(re.search("Rut\s*:\s*([0-9]+-[0-9kK])", plain_text, re.IGNORECASE)))
    values.append(check_regex(re.search("F.Recep.\s*:\s*([0-9]+-[0-9]+-[0-9]+)", plain_text, re.IGNORECASE)))
    values.append(check_regex(re.search("F.Entrega.\s*:\s*([0-9]+-[0-9]+-[0-9]+)", plain_text, re.IGNORECASE)))
    values.append(check_regex(re.search("Procedencia\s*:\s*(.*)DR\. \(A\)", plain_text, re.IGNORECASE)))
    values.append(check_regex(re.search("DR\. \(A\)\s*:\s*(.*)Muestra ", plain_text, re.IGNORECASE)))
    
    texto = (f[5:] + 
            ", Informe número " + values[0] + 
            ", Folio externo " + values[1] + 
            ", Nombre " + values[2] + 
            ", edad " + values[3] + 
            ", rut " + values[4] + 
            ", fecha de recepción " + values[5] + 
            ", fecha de entrega " + values[6] + 
            ", procedencia " + values[7] + 
            ", doctor " + values[8])
    to_read.append([f[5:], texto])

    # Check for the last digit to confirm if it is correct
    dv = str(digito_verificador(values[4][:-2]))
    if dv == "10":
        dv = "K"

    # Capitalize the letter k
    values[6] = values[4].upper()

    if dv == values[4][-1]:
        print("RUT " + values[4] + " OK")
    else:
        print("RUT " + values[4] + " OJO CON ESTE RUT, debería ser -" + dv)

print(to_read)

# Read each string and write an MP3 file with the reading
for read in to_read:
    filename = read[0][:-4]
    tts = gTTS(read[1], lang='es')
    with open("audio/"+filename+".mp3", "wb") as archivo:
        tts.write_to_fp(archivo)

    # playsound("audio/"+filename+".mp3")