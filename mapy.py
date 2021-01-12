import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib as mpl
import datetime
import gc
import os
import psutil
import sys
import PIL

#parametry vytvářených map
steps = 6
shp = 'OBCE_P.shp'
map_color = 'YlGn'
map_color_diff = 'RdYlGn'

#proměnné pro zadávání parametrů
Huob = 0
Dsli = 0
Log = 0
Diff = 0

#dotazování se uživatele co chce zobrazit
ancount = 0
while ancount < 2:
    try:
        if ancount == 0:
            an = input("""\n \n 1/9  Tento script je vytvořen pro zobrazení počtu obyvatel a hustoty osídlení obcí v ČR.
            \n Data jsou dostupná pro roky 1971 až 2019. Pro správný chod je třeba mít ve stejném adresáři soubor 'data.csv' vytvořený pomocí 'data_create.py'
            \n Všechny vstupy prosím pište bez diakritiky.
            \n Přejete si pokračovat? (Ano / Ne): """)
            if an.upper() == ("NE"):
                sys.exit()
            elif an.upper() == ("ANO"):
                break
            else:
                an = input("""\n  Prosím napište "Ano" v případě že si přejete pokračovat nebo "Ne" v případě, že chcete script ukončit: """)
                ancount += 1
                continue
        else:
            if an.upper() == ("NE"):
                sys.exit()
            elif an.upper() == ("ANO"):
                break
            else:
                an = input("""\n  Prosím napište "Ano" v případě že si přejete pokračovat nebo "Ne" v případě, že chcete script ukončit: """)
                ancount += 1
                continue
    except:
        sys.exit()
else:
    print("\n Příliš mnoho špatných vstupů. Script se ukončuje.")
    sys.exit()

hocount = 0
while hocount < 2:
    try:
        if hocount == 0:
            ho = input("""\n \n 2/9  Přejete si zobrazit absolutní počet obyvatel nebo hustotu obyvatel v jednotlivých obcích?
            \n V případě, že počet obyvatel prosím napište "Obyvatele" a v případě hustoty napište "Hustota". """)
            if ho.upper() == ("OBYVATELE"):
                Huob = 1
                break
            elif ho.upper() == ("HUSTOTA"):
                break
            else:
                ho = input("""\n  Prosím napište "Obyvatele" v případě že si přejete vybrat mapu kde bude zobrazen počet obyvatel nebo "Hustota"
                \n v případě, že chcete zobrazit hustotu obyvatel v jednotlivých obcích: """)
                hocount += 1
                continue
        else:
            if ho.upper() == ("OBYVATELE"):
                Huob = 1
                break
            elif ho.upper() == ("HUSTOTA"):
                break
            else:
                ho = input("""\n  Prosím napište "Obyvatele" v případě že si přejete vybrat mapu kde bude zobrazen počet obyvatel nebo "Hustota"
                \n v případě, že chcete zobrazit hustotu obyvatel v jednotlivých obcích: """)
                hocount += 1
                continue
    except:
        sys.exit()
else:
    print("\n Příliš mnoho špatných vstupů. Script se ukončuje.")
    sys.exit()

dlcount = 0
while dlcount < 2:
    try:
        if dlcount == 0:
            dl = input("""\n \n 3/9  Přejete si zobrazit v lineárním nebo diskrétním rozdělení? V případě, že lineárním napište "Linearni",
            \n a v případě že diskrétním napište "Diskretni" (bez diakritiky). """)
            if dl.upper() == ("LINEARNI"):
                Dsli = 1
                break
            elif dl.upper() == ("DISKRETNI"):
                break
            else:
                dl = input("""\n  Prosím napište "Linearni" v případě že si přejete vybrat mapu kde bude zobrazen data lineárně nebo "Diskretni"
                \n v případě, že chcete zobrazit data v diskrétním rozdělení: """)
                hocount += 1
                continue
        else:
            if dl.upper() == ("LINEARNI"):
                Dsli = 1
                break
            elif dl.upper() == ("DISKRETNI"):
                break
            else:
                dl = input("""\n  Prosím napište "Linearni" v případě že si přejete vybrat mapu kde bude zobrazen data lineárně nebo "Diskretni"
                \n v případě, že chcete zobrazit data v diskrétním rozdělení: """)
                dlcount += 1
                continue
    except:
        sys.exit()
else:
    print("\n Příliš mnoho špatných vstupů. Script se ukončuje.")
    sys.exit()

lgcount = 0
while lgcount < 2:
    try:
        if lgcount == 0:
            lg = input("""\n \n 4/9  Chcete na zobrazovaná data aplikovat funkci dekadického logaritmu (log10)? (Ano / Ne): """)
            if lg.upper() == ("NE"):
                break
            elif lg.upper() == ("ANO"):
                Log = 1
                break
            else:
                lg = input("""\n  Prosím napište "Ano" v případě že si přejete aplikovat funkci dekadického logaritmu (log10) na date nebo "Ne" v případě, že nechcete. (Ano / Ne): """)
                lgcount += 1
                continue
        else:
            if lg.upper() == ("NE"):
                break
            elif lg.upper() == ("ANO"):
                Log = 1
                break
            else:
                lg = input("""\n  Prosím napište "Ano" v případě že si přejete aplikovat funkci dekadického logaritmu
                \n (log10) na date nebo "Ne" v případě, že nechcete. (Ano / Ne): """)
                lgcount += 1
                continue
    except:
        sys.exit()
else:
    print("\n Příliš mnoho špatných vstupů. Script se ukončuje.")
    sys.exit()

dfcount = 0
while dfcount < 2:
    try:
        if dfcount == 0:
            df = input("""\n \n 5/9  Chcete zobrazit data pro konkrétní rok nebo změnu v určitém období?
            \n Jestliže chcete zobrazit konkrétní rok napište prosím "Konkretni" (bez diakritiky).
            \n Jestliže chcete zobrazit změnu v určitém období napište prosím "Rozdil" (bez diakritiky): """)
            if df.upper() == ("KONKRETNI"):
                break
            elif df.upper() == ("ROZDIL"):
                Diff = 1
                break
            else:
                df = input("""\n  Prosím napište "Konkretni" v případě že si přejete zobrazit konkrétní rok nebo "Rozdil"
                \n v případě, že chcete szobrazit změnu v určitém období: """)
                dfcount += 1
                continue
        else:
            if df.upper() == ("KONKRETNI"):
                break
            elif df.upper() == ("ROZDIL"):
                Diff = 1
                break
            else:
                df = input("""\n  Prosím napište "Konkretni" v případě že si přejete zobrazit konkrétní rok nebo "Rozdil"
                \n v případě, že chcete szobrazit změnu v určitém období: """)
                dfcount += 1
                continue
    except:
        sys.exit()
else:
    print("\n Příliš mnoho špatných vstupů. Script se ukončuje.")
    sys.exit()

if Diff == 0:
    kncount = 0
    while kncount < 2:
        try:
            if kncount == 0:
                kn0 = input("""\n \n 6/9  Prosím napište, který rok si přejete zobrazit. Minimálně 1971 (včetně) a maximálně 2019 (včetně): """)
                try:
                    kn = int(kn0)
                    if kn in range(1971, 2020):
                        break
                    else:
                        print("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                        continue
                except ValueError:
                    kn0 = input("""\n Prosím napište, který rok si přejete zobrazit. Minimálně 1971 (včetně) a maximálně 2019 (včetně): """)
                    kncount += 1
                    continue
            else:
                try:
                    kn = int(kn0)
                    if kn in range(1971, 2020):
                        break
                    else:
                        print("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                        continue
                except ValueError:
                    kn0 = input("""\n Prosím napište, který rok si přejete zobrazit. Minimálně 1971 (včetně) a maximálně 2019 (včetně): """)
                    kncount += 1
                    continue
        except:
            sys.exit()
    else:
        print("\n Příliš mnoho špatných vstupů. Script se ukončuje.")
        sys.exit()

if Diff == 1:
    kn1count = 0
    while kn1count < 2:
        try:
            if kn1count == 0:
                kn01 = input("""\n \n 6.1/9  Prosím napište, PRVNÍ rok mezi kterým bude udělán rozdíl. Minimálně 1971 (včetně) a maximálně 2019 (včetně): """)
                try:
                    kn1 = int(kn01)
                    if kn1 in range(1971, 2020):
                        break
                    else:
                        print("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                        continue
                except ValueError:
                    kn01 = input("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                    kn1count += 1
                    continue
            else:
                try:
                    kn1 = int(kn01)
                    if kn1 in range(1971, 2020):
                        break
                    else:
                        print("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                        continue
                except ValueError:
                    kn01 = input("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                    kn1count += 1
                    continue
        except:
            sys.exit()
    else:
        print("\n Příliš mnoho špatných vstupů. Script se ukončuje.")
        sys.exit()

    kn2count = 0
    while kn2count < 2:
        try:
            if kn2count == 0:
                kn02 = input("""\n \n 6.2/9  Prosím napište, DRUHÝ rok mezi kterým bude udělán rozdíl. Minimálně 1971 (včetně) a maximálně 2019 (včetně): """)
                try:
                    kn2 = int(kn02)
                    if kn2 in range(1971, 2020):
                        break
                    else:
                        print("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                        continue
                except ValueError:
                    kn02 = input("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                    kn2count += 1
                    continue
            else:
                try:
                    kn2 = int(kn02)
                    if kn2 in range(1971, 2020):
                        break
                    else:
                        print("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                        continue
                except ValueError:
                    kn02 = input("""\n ! Zadané číslo není v rozmezí 1971 (včetně) až 2019 (včetně), nebo se nejedná o číslo. !""")
                    kn2count += 1
                    continue
        except:
            sys.exit()
    else:
        print("\n Příliš mnoho špatných vstupů. Script se ukončuje.")
        sys.exit()

#ošetření nesprávného pořadí roků nebo jejich shoda při Diff = 1
if Diff == 1:
    if kn01 > kn02:
        print("\n \n 6.3/9  PRVNÍ zadaný rok je větší než DRUHÝ - roky budou prohozeny aby byl výchozí rok nižší.")
        kn00 = kn02
        kn02 = kn01
        kn01 = kn00
    elif kn01 == kn02:
        print("\n \n 6.3/9  PRVNÍ a DRUHÝ zadaný rok jsou stejné. Nebude zobrazena mapa rozdílu dvou let, ale mapa konkrétního zadaného roku.")
        kn = kn01
        Diff = 0
    else:
        pass

# fce na přiřazení jména podle zadaných požadavků
def name_category (code):
    name = ""
    if code[0] == "0":
        pass
    else:
        name = name + "Log"
    if code[1] == "1":
        name = name + "Obyv"
    else:
        name = name + "Hust"
    if code[2] == "0":
        name = name + str(kn) + ".0"
    elif code[2] == "1":
        name = name + str(kn01) + ".0-" + str(kn02) + ".0"
    return(name)

#fce na tvorbu jména mapy
def map_name (colm_var):
    len_var = len(colm_var)
    if len_var == 10 or len_var == 13:
        if colm_var[0] == "O" or colm_var[3] == "O":
            name = "Počet obyvatel v jednotlivých obcích ČR v roce " + str(colm_var[-6:-2])
        else:
            name = "Hustota obyvatel v jednotlivých obcích ČR v roce " + str(colm_var[-6:-2])
    if len_var == 17 or len_var == 20:
        if colm_var[0] == "O" or colm_var[3] == "O":
            name = "Rozdíl počtu obyvatel v jednotlivých obcích ČR mezi lety " + str(colm_var[-13:-9]) + " (výchozí) a " + str(colm_var[-6:-2])
        else:
            name = "Rozdíl hustoty obyvatel v jednotlivých obcích ČR mezi lety " + str(colm_var[-13:-9]) + " (výchozí) a " + str(colm_var[-6:-2])
    return(name)

#fce na tvorbu "košů" diskrétního rozdělení u NErozdílových map
def bins_limits (colm_var, steps):
    set = data.loc[:, colm_var]
    list = set.tolist()

    sort_list = sorted(list, key = float)

    bins = []
    bin_values = int(len(sort_list) / (steps))
    counter = 0

    bins.append(0)
    while counter < (len(sort_list) - bin_values):
        counter += bin_values
        avrg = (sort_list[counter - 1] + sort_list[counter]) / 2
        bins.append(avrg)
    bins.append(max(sort_list))
    return(bins)

#fce na tvorbu "košů" diskrétního rozdělení u rozdílových map
def bin_boundries (colm_var, steps):
    set = data.loc[:, colm_var]
    list = set.tolist()

    sort_list = sorted(list, key = float)

    close_zero = 99999999
    position = 0
    for counter, value in enumerate(sort_list):
        if abs(value) < abs(close_zero):
            close_zero = value
            position = counter

    below_zero_kvantil = int(position / (((steps - 2) / 2) + 1))
    over_zero_kvantil = int((len(sort_list) - position) / (((steps - 2) / 2) + 1))
    below_zero_border = below_zero_kvantil
    over_zero_border = len(sort_list)

    count = 0
    bins = []
    end_count = (steps - 2) / 2

    bins.append(min(sort_list))

    while count < ((steps - 2) / 2):
        count += 1
        small = (sort_list[below_zero_border - 1])
        big = (sort_list[below_zero_border])
        avrg = (small + big) / 2
        below_zero_border += below_zero_kvantil
        bins.append(avrg)
    while count == ((steps / 2) - 1):
        count += 1
        bins.append(0)
    while count < steps - 1:
        count += 1
        over_zero_border_position = len(sort_list) - (over_zero_kvantil * end_count)
        small = (sort_list[int(over_zero_border_position - 1)])
        big = (sort_list[int(over_zero_border_position)])
        avrg = (small + big) / 2
        bins.append(avrg)
        end_count = end_count - 1

    bins.append(max(sort_list))
    return(bins)

#určení popis legendy
def label_name (code_name):
    labname = ""
    if code_name == "000" or code_name == "001":
        labname = "obyvatel / $km^{2}$"
    elif code_name == "010" or code_name == "011":
        labname = "obyvatel"
    elif code_name == "100" or code_name == "101":
        labname = "log10(obyvatel / $km^{2}$)"
    elif code_name == "111" or code_name == "110":
        labname = "log10(obyvatel)"
    return(labname)

#funkce na převod "velkých" čísel na čitelnější formát
def format_ticks(x, pos = None):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return(r'${} \times 10^{{{}}}$'.format(a, b))

def plot_map_dis (boundry, colm_var, shp, code_name, steps, map_df):
    #vytvoření seznamu hodnot pro gdfdict a nalezení min a max hodnoty proměnné
    name_val = []
    vmin = 9999999
    vmax = 0
    length = 0
    for row in range(lencodes):
        cell = str(data.iloc[row][colm_var])
        split_cell = cell.split(".")
        if len(split_cell[0]) > length:
            length = len(split_cell[0])
    for row in range(lencodes):
        cell = str(data.iloc[row][colm_var])
        split_cell = cell.split(".")
        if len(split_cell[0]) == length:
            name_val.append(str(split_cell[0]) + "." + str(split_cell[1]))
        elif len(split_cell[0]) < length:
            zeros = length - len(split_cell[0])
            numero = "0" * zeros + split_cell[0]
            name_val.append(str(numero) + "." + str(split_cell[1]))
        if float(cell) > vmax:
            vmax = int(float(cell))
        elif float(cell) < vmin:
            vmin = int(float(cell))
    gdfdict[colm_var] = name_val
    #načtení dat
    df = pd.DataFrame(gdfdict)
    #odstranění již nepotřebných dat ze slovníku
    del gdfdict[colm_var]
    #spojení tabulek dat a tvarů
    merge = map_df.merge(df, left_on = 'KOD', right_on = 'Kod')
    #tvorba prázdné "mapy" a stupnice (prázdné)
    fig, ax = plt.subplots(1, figsize = (40, 20))
    #barevné schéma mapy
    cmap = plt.cm.get_cmap(map_color, steps)
    #nastavení velikosti "košů" diskrétního nastavení
    norm = mpl.colors.BoundaryNorm(boundry, cmap.N)
    #vytvoření stupnice s popiskem
    cb = plt.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap = plt.cm.get_cmap(map_color, steps)), orientation = "vertical", format = mpl.ticker.FuncFormatter(format_ticks))
    cb.set_label(label = label_name(code_name), size = 20)
    #vytvoření mapy
    #0.08 MB increase
    merge.plot(column = colm_var, cmap = plt.cm.get_cmap(map_color, steps), linewidth = 0.2, ax = ax, edgecolor = '0.7')
    #popis mapy
    ax.set_title(map_name(colm_var), fontdict = {'fontsize': '35', 'fontweight' : '10'})
    ax.axis('off')
    #uložení do png
    name_of_map = "Discret" + colm_var + ".jpeg"
    #8 MB increase
    plt.savefig(path_script + "/Mapy/" + name_of_map, dpi = 100)

def plot_map_lin (boundry, colm_var, shp, code_name, map_df):
    #vytvoření seznamu hodnot pro gdfdict a nalezení min a max hodnoty proměnné
    name_val = []
    vmin = 9999999
    vmax = 0
    for row in range(lencodes):
        cell = data.iloc[row][colm_var]
        name_val.append(float(cell) + abs(boundry[0]))
        if float(cell) > vmax:
            vmax = int(cell)
        elif float(cell) < vmin:
            vmin = int(cell)
    gdfdict[colm_var] = name_val
    #načtení dat
    df = pd.DataFrame(gdfdict)
    #odstranění již nepotřebných dat ze slovníku
    del gdfdict[colm_var]
    #spojení tabulek dat a tvarů
    merge = map_df.merge(df, left_on = 'KOD', right_on = 'Kod')
    #tvorba prázdné "mapy" a stupnice (prázdné)
    fig, ax = plt.subplots(1, figsize = (40, 20))
    #barevné schéma mapy
    cmap = mpl.cm.YlGn
    #nastavení hranic stupnice
    norm = mpl.colors.Normalize(vmin = vmin, vmax = vmax)
    #vytvoření stupnice s popiskem
    cb = plt.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap = cmap), orientation = 'vertical', format = mpl.ticker.FuncFormatter(format_ticks))
    cb.set_label(label = label_name(code_name), size = 20)
    #vytvoření mapy
    #0.08 MB increase
    merge.plot(column = colm_var, cmap = map_color, linewidth = 0.2, ax = ax, edgecolor = '0.5')
    #popis mapy
    ax.set_title(map_name(colm_var), fontdict = {'fontsize': '35', 'fontweight' : '10'})
    ax.axis('off')
    #uložení do png
    name_of_map = "Linear" + colm_var + ".jpeg"
    #8 MB increase
    plt.savefig(path_script + "/Mapy/" + name_of_map, dpi = 100)

def plot_map_diff_lin (boundry, colm_var, shp, code_name, map_df):
    #vytvoření seznamu hodnot pro gdfdict a nalezení min a max hodnoty proměnné
    name_val = []
    vmin = 9999999
    vmax = 0
    length = 0
    for row in range(lencodes):
        cell = str(data.iloc[row][colm_var])
        split_cell = cell.split(".")
        if len(split_cell[0]) > length:
            length = len(split_cell[0])
    for row in range(lencodes):
        cell = str(data.iloc[row][colm_var])
        new_cell = str(float(cell) + abs(boundry[0]))
        split_cell = new_cell.split(".")
        if len(split_cell[0]) == length:
            name_val.append(str(split_cell[0]) + "." + str(split_cell[1]))
        elif len(split_cell[0]) < length:
            zeros = length - len(split_cell[0])
            numero = "0" * zeros + split_cell[0]
            name_val.append(str(numero) + "." + str(split_cell[1]))
        if float(cell) > vmax:
            vmax = float(cell)
        elif float(cell) < vmin:
            vmin = float(cell)
    gdfdict[colm_var] = name_val
    #načtení dat
    df = pd.DataFrame(gdfdict)
    #odstranění již nepotřebných dat ze slovníku
    del gdfdict[colm_var]
    #spojení tabulek dat a tvarů
    merge = map_df.merge(df, left_on = 'KOD', right_on = 'Kod')
    #tvorba prázdné "mapy" a stupnice (prázdné)
    fig, ax = plt.subplots(1, figsize = (40, 20))
    #barevné schéma mapy
    cmap = mpl.cm.RdYlGn
    #nastavení hranic stupnice
    norm = mpl.colors.TwoSlopeNorm(vmin = vmin, vcenter = 0, vmax = vmax)
    #vytvoření stupnice s popiskem
    cb = plt.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap = cmap), orientation = 'vertical')
    cb.set_label(label = label_name(code_name), size = 20)
    #vytvoření mapy
    merge.plot(column = colm_var, cmap = map_color_diff, linewidth = 0.2, ax = ax, edgecolor = '0.5')
    #popis mapy
    ax.set_title(map_name(colm_var), fontdict = {'fontsize': '35', 'fontweight' : '10'})
    ax.axis('off')
    #uložení do png
    name_of_map = "Linear" + colm_var + ".jpeg"
    plt.savefig(path_script + "/Mapy/" + name_of_map, dpi = 100)

def plot_map_diff_dis (boundry, colm_var, shp, code_name, steps, map_df):
    #vytvoření seznamu hodnot pro gdfdict a nalezení min a max hodnoty proměnné
    name_val = []
    max_plot = boundry[-2]
    vmin = 9999999
    vmax = 0
    for row in range(lencodes):
        cell = data.iloc[row][colm_var]
        if cell > max_plot and float(cell) > vmax:
            vmax = float(cell)
            name_val.append(str(cell + abs(boundry[0])))
        elif cell > max_plot:
            name_val.append(str(cell + abs(boundry[0])))
        elif cell < max_plot and float(cell) < vmin:
            vmin = float(cell)
            name_val.append(str(cell + abs(boundry[0])))
        else:
            name_val.append(str(cell + abs(boundry[0])))
    gdfdict[colm_var] = name_val
    #načtení dat
    df = pd.DataFrame(gdfdict)
    #odstranění již nepotřebných dat ze slovníku
    del gdfdict[colm_var]
    #spojení tabulek dat a tvarů
    merge = map_df.merge(df, left_on = 'KOD', right_on = 'Kod')
    #tvorba prázdné "mapy" a stupnice (prázdné)
    fig, ax = plt.subplots(1, figsize = (40, 20))
    #barevné schéma mapy
    cmap = plt.cm.get_cmap(map_color_diff, steps)
    #nastavení velikosti "košů" diskrétního nastavení
    norm = mpl.colors.BoundaryNorm(boundry, cmap.N)
    #vytvoření stupnice s popiskem
    cb = plt.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap = plt.cm.get_cmap(map_color_diff, steps)), orientation = "vertical")
    cb.set_label(label = label_name(code_name), size = 20)
    #vytvoření mapy
    merge.plot(column = colm_var, cmap = plt.cm.get_cmap(map_color_diff, steps), linewidth = 0.2, ax = ax, edgecolor = '0.7')
    #popis mapy
    ax.set_title(map_name(colm_var), fontdict = {'fontsize': '35', 'fontweight' : '10'})
    ax.axis('off')
    #uložení do png
    name_of_map = "Discret" + colm_var + ".jpeg"
    plt.savefig(path_script + "/Mapy/" + name_of_map, dpi = 100)

############################################################################

print("\n \n 7/9  Načítám data potřebná k vytvoření mapy. Čas: ", datetime.datetime.now())

#vytvoření kódu ze zadaných parametrů
code = (str(Log) + str(Huob) + str(Diff))

#cesta a obsah složky kde je spouštěn skript
path_script = os.path.abspath('')
files = os.listdir(path_script)

#jestli není složka "Mapy" přítomna tak se vytvoří
if 'Mapy' not in files:
    path_mapy = path_script + "/Mapy"
    os.mkdir(path_mapy)

#načtení dat
data = pd.read_csv("data.csv")
gdfdict = {}

codes = data["Kod"]
lencodes = len(codes)

#načtení kodu obcí pro gdfdict
name_kod = []
for row in range(lencodes):
    cell_val = data.iloc[row]['Kod']
    name_kod.append(cell_val)
gdfdict['Kod'] = name_kod

#načtení tvarů obcí
map_df = gpd.read_file(shp)
map_df['KOD'] = map_df['KOD'].astype(int)

colm_var = name_category(code)

print("\n \n 8/9  Začínám tvořit mapu. Čas začátku: ", datetime.datetime.now())

if code == "000":
    #000 "HustXXXX.0"
    #hranice diskrétního rozdělení
    boundry = bins_limits (colm_var, steps)
    if Dsli == 0:
        #Diskrétní mapa
        plot_map_dis (boundry, colm_var, shp, code, steps, map_df)
    else:
        #Lineární mapa
        plot_map_lin (boundry, colm_var, shp, code, map_df)

elif code == "010":
    #010 "ObyvXXXX.0"
    #hranice diskrétního rozdělení
    boundry = bins_limits (colm_var, steps)
    if Dsli == 0:
        #Diskrétní mapa
        plot_map_dis (boundry, colm_var, shp, code, steps, map_df)
    else:
        #Lineární mapa
        plot_map_lin (boundry, colm_var, shp, code, map_df)

elif code == "100":
    #100 "LogHustXXXX.0"
    #hranice diskrétního rozdělení
    boundry = bins_limits (colm_var, steps)
    if Dsli == 0:
        #Diskrétní mapa
        plot_map_dis (boundry, colm_var, shp, code, steps, map_df)
    else:
        #Lineární mapa
        plot_map_lin (boundry, colm_var, shp, code, map_df)

elif code == "110":
    #110 "LogObyvXXXX.0"
    #hranice diskrétního rozdělení
    boundry = bins_limits (colm_var, steps)
    if Dsli == 0:
        #Diskrétní mapa
        plot_map_dis (boundry, colm_var, shp, code, steps, map_df)
    else:
        #Lineární mapa
        plot_map_lin (boundry, colm_var, shp, code, map_df)

elif code == "001":
    #001 "HustXXXX.0-XXXX.0"
    #hranice diskrétního rozdělení
    boundry = bin_boundries (colm_var, steps)
    if Dsli == 0:
        #Diskrétní mapa
        plot_map_diff_dis (boundry, colm_var, shp, code, steps, map_df)
    else:
        #Lineární mapa
        plot_map_diff_lin (boundry, colm_var, shp, code, map_df)

elif code == "011":
    #011 "ObyvXXXX.0-XXXX.0"
    #hranice diskrétního rozdělení
    boundry = bin_boundries (colm_var, steps)
    if Dsli == 0:
        #Diskrétní mapa
        plot_map_diff_dis (boundry, colm_var, shp, code, steps, map_df)
    else:
        #Lineární mapa
        plot_map_diff_lin (boundry, colm_var, shp, code, map_df)

elif code == "101":
    #101 "LogHustXXXX.0-XXXX.0"

    #hranice diskrétního rozdělení
    boundry = bin_boundries (colm_var, steps)
    if Dsli == 0:
        #Diskrétní mapa
        plot_map_diff_dis (boundry, colm_var, shp, code, steps, map_df)
    else:
        #Lineární mapa
        plot_map_diff_lin (boundry, colm_var, shp, code, map_df)

elif code == "111":
    #111 "LogObyvXXXX.0-XXXX.0"
    #hranice diskrétního rozdělení
    boundry = bin_boundries (colm_var, steps)
    if Dsli == 0:
        #Diskrétní mapa
        plot_map_diff_dis (boundry, colm_var, shp, code, steps, map_df)
    else:
        #Lineární mapa
        plot_map_diff_lin (boundry, colm_var, shp, code, map_df)

print("\n \n 9/9  Čas ukončení: ", datetime.datetime.now(), """\n \n Mapa je uložena ve složce "/Mapy", která byla vytvořena v adresáři, kde byl tento scrip spuštěn. \n """)

#načtení cesty k mapě
if Dsli == 1:
    path = path_script + "/Mapy/Linear" + str(colm_var) + ".jpeg"
else:
    path = path_script + "/Mapy/Discret" + str(colm_var) + ".jpeg"

#zobrazení mapy
img = PIL.Image.open(path)
img.show()
