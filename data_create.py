import csv
import pathlib
import os
import pandas
import math
import datetime

folder = pathlib.Path(os.path.abspath('') + "/Obce_obyvatele/")
files = os.listdir(folder)

#fce na vytvoření seznamů *.csv souborů ve složce
def csv_in_folder(files):
    csv_files = []
    for file in files:
        sf = file.split('.')
        if sf[1] == 'csv':
            csv_files.append(file)
    return(csv_files)

#funkce na vrácení prvních dvou znaků
def first2(word):
    return(word[:2])

#funkce na vytvoření kombinací roků
def nonrepcom2 (lst):
    result = []
    length = len(lst)
    max = len(lst)
    count = 0
    while count < max:
        year = count
        n = 1
        while n < length:
            com = count + n
            result.append((lst[year], lst[com]))
            n += 1
        count += 1
        length = length - 1
    return(result)

#seznam všech csv ve složce "Obce_obyvatele"
csvs = (csv_in_folder(files))

#seznam roků pro které jsou počítána data
years = []
for year in range(1971, 2020):
    years.append(str(year) + '.0')

#projetí všech csv souborů s daty - jejich převod na požadovaný formát a do
#jednoho souboru data.csv, dopočítání chbějících dat/údajů a úrvara stávajících
#dat podle dopočítaných dat
for flnum in range(len(csvs)):
    print("Start of", flnum + 1, "/", len(csvs), "-", csvs[flnum])
    print(datetime.datetime.now())
    settl = []
    settl_years_lst = {}
    settl_years_dct = {}
    settl_years_miss = {}
    ins_out = {}
    settl_movement = {}
    #otevření csv
    with open(folder/csvs[flnum], encoding='latin-1') as file:
        read = csv.reader(file)
        reader = list(read)
        #postupné čtení csv
        for row in reader:
            if row == []:
                pass
            else:
                #postupné načtení ködů všech obcí
                cd = str(row[1]).split('.')
                try:
                    code = int(cd[0])
                    if str(code) not in settl:
                        settl.append(str(code))
                except:
                    pass
        for row in reader:
            if row == []:
                pass
            else:
                #postupné vytvoření klíčů pro daný kód ve všech slovnících
                code = str(row[1]).split('.')
                if code[0] in settl:
                    settl_years_lst[code[0]] = []
                    settl_years_miss[code[0]] = []
                    settl_years_dct[code[0]] = []
        for row in reader:
            if row == []:
                pass
            else:
                #načtení počtu obyvatel z csv souboru
                code = str(row[1]).split('.')
                for key in settl_years_lst.keys():
                    if code[0] == key:
                        settl_years_lst.get(code[0]).append(row[0])
                        settl_years_dct.get(code[0]).append({row[0] : row[4]})
        #vytvoření seznamu roků kde chybí údaje v csv
        for key in settl_years_miss.keys():
            sydata = settl_years_lst.get(key)
            diff = list(set(years) - set(sydata))
            diff.sort()
            settl_years_miss[key] = diff
        for key in settl_years_miss:
            if (settl_years_miss[key]) == []:
                pass
            elif max(settl_years_miss[key]) == '2019.0':
                pass
            else:
                minimal = min(settl_years_miss[key])
                min_year = str(minimal).split('.')
                maximal = max(settl_years_miss[key])
                max_year = str(maximal).split('.')
                for row in reader:
                    if row == []:
                        pass
                    else:
                        if (str(key) + '.0') == row[1]:
                            if minimal == '1971.0':
                                min_habitat = row[4].split('.')
                                min_habit = min_habitat[0]
                            elif (str(int(min_year[0]) - 1) + '.0') == row[0]:
                                min_habitat = row[4].split('.')
                                min_habit = min_habitat[0]
                for row in reader:
                    if row == []:
                        pass
                    else:
                        if (str(key) + '.0') == row[1] and (str(int(max_year[0]) + 1) + '.0') == row[0]:
                            if row[4] == '-':
                                max_habitat = row[12].split('.')
                                max_habit = max_habitat[0]
                            else:
                                max_habitat = row[4].split('.')
                                max_habit = max_habitat[0]
                #vypočtení průměrné změny počtu obyvatel v chybějících letech
                dif_habit = -(int(min_habit) - int(max_habit))
                num_years_miss = len(range(int(min_year[0]), int(max_year[0]) + 1)) - 1
                avrg_change = dif_habit / (num_years_miss + 2)
                actual_habit = int(min_habit)
                for year in range(int(min_year[0]), int(max_year[0]) + 1):
                    actual_habit += avrg_change
                    settl_years_dct[key].append({(str(year) + '.0')  : str(actual_habit)})
        #vytvoření slovníku s roky kdy se každá obec oddělila a/nebo spojila
        #s jinou obcí pokud nebyla samostatná nepřetržitě od 1971 do 2019
        for key in settl_years_dct:
                for row in reader:
                    if row == []:
                        pass
                    else:
                        #spojení s jinou obcí
                        if (str(key) + '.0') == row[1] and row[17] != '' and len(row[17]) > 2 and ((row[12] != '-' and float(row[12]) < 0) or (row[14] != '-' and float(row[14]) < 0) and float(row[14]) == -float(row[13])):
                            if key not in ins_out.keys():
                                set_cd = row[17].split('.')
                                try:
                                    ins_out[key] = {'ins' : [set_cd[0], row[0]]}
                                except:
                                    ins_out[key] = {'ins' : [set_cd[0], row[0]]}
                for row in reader:
                    if row == []:
                        pass
                    else:
                        #osamostatnění obce
                        if (str(key) + '.0') == row[1] and row[15] != '' and len(row[15]) > 2 and ((row[3] != '-' and float(row[3]) > 0) or (row[14] != '-' and float(row[14]) > 0)):
                            if key not in ins_out.keys():
                                try:
                                    set_cd = row[15].split('.')
                                    ins_out[key] = {'out' : [set_cd[0], row[0]]}
                                except:
                                    ins_out[key] = {'out' : [set_cd[0], row[0]]}
                            else:
                                try:
                                    set_cd = row[15].split('.')
                                    ins_out[key].update({'out' : [set_cd[0], row[0]]})
                                except:
                                    ins_out[key].update({'out' : [set_cd[0], row[0]]})
    #načtení kódu obce a počtu obyvatel s kterou se daná obec spojila A
    #rozpojila
    for key, val in ins_out.items():
        if len(val.items()) == 2:
            ins = val.get('ins')
            out = val.get('out')
            ins_settl = (key, ins[0], ins[1])
            out_settl = (key, out[0], out[1])
            for key2 in settl_years_dct:
                if key2 == ins_settl[1]:
                    for settl in settl_years_dct.get(ins_settl[0]):
                        for data in settl:
                            if data == (ins_settl[2]):
                                first = (ins_settl[0], data, settl[data])
                    for settl in settl_years_dct.get(ins_settl[1]):
                        for data in settl:
                            if data == (ins_settl[2]):
                                settl_movement[key] = [['INS', first[0], first[1], first[2], ins_settl[1], data, settl[data]]]
            for key2 in settl_years_dct:
                if key2 == out_settl[1]:
                    for settl in settl_years_dct.get(out_settl[0]):
                        for data in settl:
                            if data == (out_settl[2]):
                                first = (out_settl[0], data, settl[data])
                    for settl in settl_years_dct.get(out_settl[1]):
                        for data in settl:
                            if data == (out_settl[2]):
                                settl_movement[key].append(['OUT', first[0], first[1], first[2], out_settl[1], data, settl[data]])
        #načtení kódu obce a počtu obyvatel s kterou se daná obec spojila NEBO
        #rozpojila
        elif len(val.items()) == 1:
            try:
                ins = val.get('ins')
                ins_settl = (key, ins[0], ins[1])
                for key2 in settl_years_dct:
                    if key2 == ins_settl[1]:
                        for settl in settl_years_dct.get(ins_settl[0]):
                            for data in settl:
                                if data == (ins_settl[2]):
                                    first = (ins_settl[0], data, settl[data])
                        for settl in settl_years_dct.get(ins_settl[1]):
                            for data in settl:
                                if data == (ins_settl[2]):
                                    settl_movement[key] = [['INS', first[0], first[1], first[2], ins_settl[1], data, settl[data]]]
            except:
                out = val.get('out')
                out_settl = (key, out[0], out[1])
                for key2 in settl_years_dct:
                    if key2 == out_settl[1]:
                        for settl in settl_years_dct.get(out_settl[0]):
                            for data in settl:
                                if data == (out_settl[2]):
                                    first = (out_settl[0], data, settl[data])
                        for settl in settl_years_dct.get(out_settl[1]):
                            for data in settl:
                                if data == (out_settl[2]):
                                    settl_movement[key] = [['OUT', first[0], first[1], first[2], out_settl[1], data, settl[data]]]
    #výpočet "nového" počtu obyvatel podle toho jak a kdy se jednotlivé obce
    #spojovaly (např. jestli se obec odpojila v roce 2000 tak z "mateřské""
    #obce se odečte počet obyvatel pro roky 1971-1999, protože by neodpovídala
    #data na mapě vzhledem k rozloze a rozpoložení obyvatel - bez této korekce
    #vy se obyvatelé na mapě zobrazovali v určitých případech (často) 2x)
    for settl in settl_movement:
        #korekce pro případy kdy se obec odpojila/spojila a následně
        #spojila/odpojila
        if len(settl_movement[settl]) == 2:
            for i in range(int(float(settl_movement[settl][0][5])) + 1, int(float(settl_movement[settl][1][5]))):
                year = (str(i) + '.0')
                for j in settl_years_dct[settl_movement[settl][0][4]]:
                    for yr in j:
                        if yr == year:
                            orig = j.get(year)
                for j in settl_years_dct[settl]:
                    for yr in j:
                        if yr == year:
                            new = j.get(year)
                            for i in settl_years_dct[settl_movement[settl][0][4]]:
                                for j in i:
                                    if j == year:
                                            if float(new) > float(orig):
                                                pass
                                            else:
                                                i[j] = float(orig) - float(new)
        #korekce pro případy kdy se obec jen spojila
        else:
            if settl_movement[settl][0][0] == 'INS':
                for i in range(1971, int(float(settl_movement[settl][0][5]))):
                    year = (str(i) + '.0')
                    for j in settl_years_dct[settl_movement[settl][0][4]]:
                        for yr in j:
                            if yr == year:
                                orig = j.get(year)
                    for j in settl_years_dct[settl]:
                        for yr in j:
                            if yr == year:
                                new = j.get(year)
                                for i in settl_years_dct[settl_movement[settl][0][4]]:
                                    for j in i:
                                        if j == year:
                                            if float(new) > float(orig):
                                                pass
                                            else:
                                                i[j] = float(orig) - float(new)
            #korekce pro případy kdy se obec jen odpojila
            else:
                for i in range(1971, int(float(settl_movement[settl][0][5]))):
                    year = (str(i) + '.0')
                    for j in settl_years_dct[settl_movement[settl][0][4]]:
                        for yr in j:
                            if yr == year:
                                orig = j.get(year)
                    for j in settl_years_dct[settl]:
                        for yr in j:
                            if yr == year:
                                new = j.get(year)
                                for i in settl_years_dct[settl_movement[settl][0][4]]:
                                    for j in i:
                                        if j == year:
                                            if float(new) > float(orig):
                                                pass
                                            else:
                                                i[j] = float(orig) - float(new)

    #seznam roků
    yearlist = []
    for year in range(1971,2020):
        yearlist.append(year)

    tuplist = nonrepcom2(yearlist)

    #začátek hlavičky tabulky data.csv
    header = ['Kod', 'Plochakm']

    #hlavička pro jednotlivé roky
    for rok in range(1971, 2020):
        header.append('Obyv' + str(rok) + ".0")
        header.append('Hust' + str(rok) + ".0")
        header.append('LogObyv' + str(rok) + ".0")
        header.append('LogHust' + str(rok) + ".0")

    #hlavička pro kombinace (rozdíl) let
    for comb in tuplist:
        header.append('Obyv' + str(comb[0]) + ".0" + "-" + str(comb[1]) + ".0")
        header.append('Hust' + str(comb[0]) + ".0" + "-" + str(comb[1]) + ".0")
        header.append('LogObyv' + str(comb[0]) + ".0" + "-" + str(comb[1]) + ".0")
        header.append('LogHust' + str(comb[0]) + ".0" + "-" + str(comb[1]) + ".0")

    #načtení kódů a plochy obcí
    cod_areakm = []
    with open('obyvatele_plocha.csv') as data:
        reader = csv.reader(data)
        for row in reader:
            for part in row:
                record = part.split(';')
                for word in record:
                    if first2(word) == 'CZ':
                        cod = record[3]
                        areaha = int(record[8].replace(' ', ''))
                        areakm = float(areaha / 100)
                        cod_areakm.append([cod, areakm])

    #kontrola zda data.csv existují
    folder2 = pathlib.Path("/home/ondrej/Python/CZE_density_map/")
    files2 = os.listdir(folder2)
    if "data.csv" in files2:
        pass
    else:
    #vytvoření hlavičky a doplnění kódu obcí a plochy do data.csv
        with open('data.csv', 'w', encoding = 'utf8') as data:
            writer = csv.writer(data)
            writer.writerow(header)
            for settl in cod_areakm:
                writer.writerow([settl[0], settl[1]])

    #vytvoření slovníku s názvy sloupců a hodnotou "float64" pro přiřazení typu po otevření pomocí pandas
    dtypes = {}
    for col in header:
        dtypes[col] = 'float64'

    #načtení data.csv pomocí pandas
    data = pandas.read_csv('data.csv')
    data = data.astype(dtypes)
    dk = data.set_index("Kod", drop = False)

    #nahrání dat do data.csv
    kod = dk["Kod"]
    for kd in kod.values:
        for cd in settl_years_dct:
            if int(kd) == int(cd):
                for dct in settl_years_dct[cd]:
                    for year in dct:
                        #nahrání počtu obyvatel v jednotlivých letech
                        obyv = "Obyv" + year
                        dk.at[[int(cd)],[str(obyv)]] = dct[year]
                        #nahrání hustoty obyvatel v jednotlivých letech
                        hustnum = float(dct[year]) / float(dk["Plochakm"][int(cd)])
                        hust = "Hust" + year
                        dk.at[[int(cd)],[str(hust)]] = hustnum
                        #nahrání počtu obyvatel v jednotlivých letech (logaritmické měřítko)
                        logobyv = "LogObyv" + year
                        if float(dct[year]) == 0:
                            dk.at[[int(cd)],[str(logobyv)]] = 0
                        else:
                            dk.at[[int(cd)],[str(logobyv)]] = math.log10(1 + float(dct[year]))
                        #nahrání hustoty obyvatel v jednotlivých letech (logaritmické měřítko)
                        hustnum = float(dct[year]) / float(dk["Plochakm"][int(cd)])
                        loghust = "LogHust" + year
                        if hustnum == 0:
                            dk.at[[int(cd)],[str(loghust)]] = 0
                        else:
                            dk.at[[int(cd)],[str(loghust)]] = math.log10(1 + hustnum)
                for comb in tuplist:
                    #nahrání rozdílů počtu obyvatel mezi jednotlivými roky
                    obyvdiff = ("Obyv" + str(comb[0]) + ".0" + "-" + str(comb[1]) + ".0")
                    obyvyear1 = "Obyv" + str(comb[0]) + ".0"
                    obyvyear2 = "Obyv" + str(comb[1]) + ".0"
                    obyvyear1val = dk[obyvyear1][int(cd)]
                    obyvyear2val = dk[obyvyear2][int(cd)]
                    val = float(obyvyear2val) - float(obyvyear1val)
                    if val < 0:
                        dk.at[[int(cd)],[str(obyvdiff)]] = str(val)
                    else:
                        dk.at[[int(cd)],[str(obyvdiff)]] = val
                    #nahrání rozdílů hustoty obyvatel mezi jednotlivými roky
                    hustdiff = ("Hust" + str(comb[0]) + ".0" + "-" + str(comb[1]) + ".0")
                    hustyear1 = "Hust" + str(comb[0]) + ".0"
                    hustyear2 = "Hust" + str(comb[1]) + ".0"
                    hustyear1val = dk[hustyear1][int(cd)]
                    hustyear2val = dk[hustyear2][int(cd)]
                    val = float(hustyear2val) - float(hustyear1val)
                    if val < 0:
                        dk.at[[int(cd)],[str(hustdiff)]] = str(val)
                    else:
                        dk.at[[int(cd)],[str(hustdiff)]] = val
                    #nahrání rozdílů počtu obyvatel mezi jednotlivými roky (logaritmické měřítko)
                    logobyvdiff = ("LogObyv" + str(comb[0]) + ".0" + "-" + str(comb[1]) + ".0")
                    if float(obyvyear2val) - float(obyvyear1val) < 0:
                        dk.at[[int(cd)],[str(logobyvdiff)]] = "-" + str(math.log10(1 - (float(obyvyear2val) - float(obyvyear1val))))
                    elif float(obyvyear2val) - float(obyvyear1val) == 0:
                        dk.at[[int(cd)],[str(logobyvdiff)]] = 0
                    else:
                        dk.at[[int(cd)],[str(logobyvdiff)]] = math.log10(1 + (float(obyvyear2val) - float(obyvyear1val)))
                    #nahrání rozdílů hustoty obyvatel mezi jednotlivými roky (logaritmické měřítko)
                    loghustdiff = ("LogHust" + str(comb[0]) + ".0" + "-" + str(comb[1]) + ".0")
                    if float(hustyear2val) - float(hustyear1val) < 0:
                        dk.at[[int(cd)],[str(loghustdiff)]] = "-" + str(math.log10(1 - (float(hustyear2val) - float(hustyear1val))))
                    elif float(hustyear2val) - float(hustyear1val) == 0:
                        dk.at[[int(cd)],[str(loghustdiff)]] = 0
                    else:
                        dk.at[[int(cd)],[str(loghustdiff)]] = math.log10(1 + (float(hustyear2val) - float(hustyear1val)))
    #mazání duplikujích se sloupců "Kod"
    if "Kod.1" in dk.columns:
        del dk["Kod.1"]
    #uložení data.csv
    dk.to_csv("data.csv")
    print("----------------------------------------------------")

print("Hotovo")
print(datetime.datetime.now())
