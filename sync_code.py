# zatím nebyly nalezeny žádné zádrhele

x = 0
new_file = []
with open(r"C:\Users\tseif\OneDrive\Dokumenty\b\python\year's project\kody_se_z\DeGen(ruzovy_text_lepsiuztonejde)_sez.gcode", mode="r") as file_o:  # otevíraný soubor
    for line in file_o:
        if "Z" in line:
            new_file.append("M0")
        else:
            if line != "\n":  # zbaví se pouze "\n"
                if "\n" in line:
                    line = line.replace("\n", "")  # odstraní "\n"
                new_file.append(line)
# nové odstranění začátečního a koncového G0 X0.0 Y0.0 (kdyby byl steh na G0 x0 Y0, tak ho nechá)
for g in range(0, len(new_file)-1):
    if new_file[g] == "G0 X0.0 Y0.0":
        del new_file[g]
        break
for q in range(len(new_file)-1, 0, -1):
    if new_file[q] == "G0 X0.0 Y0.0":
        del new_file[q]
        break
z = 0
jumps = ["Jump stitches:"]
while z < len(new_file):
    if "G0" in new_file[z]:
        for i in range(z-1, 0, -1):  # bere i od z-1 do 0
            if "G0" in new_file[i]:
                souradnice_i = new_file[i].split(" ")
                souradnice_z = new_file[z].split(" ")
        # oddělí z Xkové souřadnice stringové části a převede ji na float
                x_i = float(souradnice_i[1].replace("X", ""))
                x_z = float(souradnice_z[1].replace("X", ""))
                y_i = float(souradnice_i[2].replace("Y", ""))
                y_z = float(souradnice_z[2].replace("Y", ""))
        # absolutní hodnota vzdáleností souřadnic x1 a x0 a y1 a y0
                if abs(x_z-x_i) > 1 or abs(y_z-y_i) > 1:
                    # 6 stehů před jump stitchem se spustí buzzer
                    new_file.insert(i-14, "M8")
                    # a těsně před jump stitchem se vypne
                    new_file.insert(i+1, "M9")
                    z += 2 # za přidané M8 a M9
                    i += 2
                    # nechat-uloží souřadnice jump stitchů
                    jump_stitch = (f"X: {x_i}, Y: {y_i}\tX: {x_z}, Y: {y_z}\t z (index): {z}")
                    jumps.append(jump_stitch)
                    # range je prostor mezi M8 a M9 stávajícího new_code[i], kde se nesmí vyskytovat jiné M9
                break
    z += 1
m_nines = []
for n in range(0, len(new_file)-1):
    if new_file[n] == "M9":
        m_nines.append(n)  # založí seznam s new_fileovými indexy M9tek
r = 1  # aby se mohlo pracovat s r-1
if len(m_nines)>1:
    while True:  # r= index v m_nines
        if ((m_nines[r])-(m_nines[r-1])) <= 14:  # m_nines[r]=index "M9" v new_file
            new_file.pop(m_nines[r-1])  # odstraní dřívější "M9" z new_file
            m_nines.pop(r-1)  # odstraní new_fileový index odstraněné "M9" z m_nines
            for k in range(0, len(m_nines)-1):
                if k >= (r-1):
                    # upraví new_file indexy v m_nines po odebrání jednoho "M9"
                    m_nines[k] -= 1
            r -= 1
        r += 1
        if r >= len(m_nines):
            break

# před 20. stehem (asi 15 s do konce) se spustí buzzer
new_file.insert(-41, "M8")
# jako předposlední příkaz se buzzer vypne (po M0 a před M30)
new_file.insert(-1, "M9")
# test buzzeru
new_file.insert(0, "M8")
new_file.insert(12, "M9")
for i in jumps:
    print(i)
with open(r"C:\Users\tseif\OneDrive\Dokumenty\b\python\year's project\kody_s_jumpstitches\DeGen_lepsi\DeGen(ruzovy_text_lepsiuztonejde)_jump.gcode", mode="w", encoding="utf-8") as output_file:  # cílový soubor
    for i in new_file:  # nahraje new_file do output_file
        print(i, file=output_file)
