
x = 0
new_file = []
with open(r"", mode="r") as file_o:  # in inverted commas - opened file
    for line in file_o:
        if "Z" in line:
            new_file.append("M0")
        else:
            if line != "\n":  # tests for "\n" in line
                if "\n" in line:
                    line = line.replace("\n", "")  # removes the "\n"
                new_file.append(line)
# removal of starting and final G0 X0.0 Y0.0 (if that coordinate would be in the middle of the G-Code file, it would not be removed)
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
        for i in range(z-1, 0, -1):  # takes i from z-1 to 0
            if "G0" in new_file[i]:
                coordinates_i = new_file[i].split(" ")
                coordinates_z = new_file[z].split(" ")
        # extracts the X and Y coordinates from the line and converts them into float type
                x_i = float(souradnice_i[1].replace("X", ""))
                x_z = float(souradnice_z[1].replace("X", ""))
                y_i = float(souradnice_i[2].replace("Y", ""))
                y_z = float(souradnice_z[2].replace("Y", ""))
        # absolute value of distance between x1 and x0; the same goes for y1 and y0
                if abs(x_z-x_i) > 1 or abs(y_z-y_i) > 1:
                    # the buzzer is turned on 6 stitches before the jump stitch
                    new_file.insert(i-14, "M8")
                    # and turns itself off right before the jump stitch
                    new_file.insert(i+1, "M9")
                    z += 2 # for added M8 and M9
                    i += 2
                    # stores the jump stitch coordinates
                    jump_stitch = (f"X: {x_i}, Y: {y_i}\tX: {x_z}, Y: {y_z}\t z (index): {z}")
                    jumps.append(jump_stitch)
                break
    z += 1
m_nines = []
for n in range(0, len(new_file)-1):
    if new_file[n] == "M9":
        m_nines.append(n)  # creates a list with the new_file indexes of all "M9"'s
r = 1  # for working with r-1
if len(m_nines)>1:
    while True:  # r= index in m_nines
        if ((m_nines[r])-(m_nines[r-1])) <= 14:  # m_nines[r]=index "M9" in new_file
            new_file.pop(m_nines[r-1])  # removes previous "M9" from new_file
            m_nines.pop(r-1)  # removes the index of the removed "M9" from m_nines
            for k in range(0, len(m_nines)-1):
                # changes new_file indexes in m_nines after a "M9" removal
                if k >= (r-1):
                    m_nines[k] -= 1
            r -= 1
        r += 1
        if r >= len(m_nines):
            break

# before a 20. stitch (about 15 s) until the end, the buzzer is turned on
new_file.insert(-41, "M8")
# sets switching off of the buzzer as the next-to-last command
new_file.insert(-1, "M9")
# test of the buzzer at the beginning of embroidery
new_file.insert(0, "M8")
new_file.insert(12, "M9")
for i in jumps:
    print(i)
with open(r"", mode="w", encoding="utf-8") as output_file:  # creates a destination file (supposed to be in inverted commas)
    for i in new_file:  # uploads new_file into destination file
        print(i, file=output_file)

