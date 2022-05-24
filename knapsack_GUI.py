from knapsack import *
from pathlib import Path

nama_aplikasi = 'Aplikasi 0-1 Knapsack Problem'
N = 0
kapasitas = 0
set_objek = {}
methods = ['Brute force','Greedy by profit','Greedy by weight', 'Greedy by density']
cara_input = ''
running = True
file_input = False
path = ''
err_msg = ''

while running:
    layout = [
        [sg.Image("Knapsack_logo.png")],
        [sg.Text('Input file data-data barang (.txt):')],
        [sg.Input(sg.user_settings_get_entry('-filename-', ''),key='path'), sg.FileBrowse(file_types=("CSV .csv","*.csv .csv"))],
        [sg.Text("Kapasitas knapsack (K) = "),sg.Input(size=(10),key='k')],
        [sg.Text(err_msg,text_color='red')],
        [sg.B('Save',button_color='green'), sg.B('Input langsung di aplikasi', key='in_app')]
    ]
    window = sg.Window(nama_aplikasi, layout)
    event, value = window.read()
    if event == sg.WINDOW_CLOSED:
        running = False
        break
    elif event == 'Save':
        file_input = True
        sg.user_settings_set_entry('-filename-', value['Browse'])
    elif event == 'in_app':
        file_input = False
        break
    try:
        kapasitas = int(value['k'])
        path = str(Path(value['path']))
        window.close()
        break 
    except:
        err_msg = 'harap masukkan bilangan bulat pada kapasitas'
        window.close()
if file_input:
    KP = Knapsack(kapasitas,file_path=path)
elif not file_input:
    err_msg = ''
    while running:
        layout = [
            [sg.Text('')],
            [sg.Text("Input jumlah barang (N) = "),sg.Input()],
            [sg.Text("Kapasitas knapsack (K) = "),sg.Input()],
            [sg.Text('Pilih cara yang anda inginkan untuk menginput data barang')],
            [sg.Button('Input satu-per-satu',button_color='green'),sg.Button('Buatkan otomatis',button_color='green'),],
            [sg.Text(err_msg,text_color='red')],
            [sg.Text('')],
        ]
        window = sg.Window(nama_aplikasi,layout)
        event, value = window.read()
        if event == sg.WIN_CLOSED:
            running = False
            break
        try:
            N = int(value[0]) 
            kapasitas = int(value[1])
            cara_input = event
            window.close()
            break 
        except:
            err_msg = 'harap masukkan bilangan bulat'
            window.close()
    if cara_input == 'Input satu-per-satu' and running:
        i = 1
        err_msg = ''
        while True:
            if i > N:
                break
            layout = [
                [sg.Text(f'Input data barang ke-{i} ,sudah diinput {i-1}/{N}')],
                [sg.Text("Nama = "),sg.Input()],
                [sg.Text("Profit ="),sg.Input()],
                [sg.Text("Weight ="),sg.Input()],
                [sg.Text(err_msg,text_color='red')],
                [sg.Button('next')] 
            ]
            window = sg.Window(nama_aplikasi,layout)
            event, value = window.read()
            if event == sg.WIN_CLOSED:
                running = False
                break
            try:
                Barang = value[0]
                P = int(value[1])
                W = int(value[2])
                set_objek[Barang] = {'w':W,'p':P}
                if event == 'next':
                    i += 1
                    window.close()
                    continue
            except:
                err_msg = 'harap masukkan bilangan bulat'
                window.close()
        KP = Knapsack(kapasitas,set_objek=set_objek)
    elif cara_input == 'Buatkan otomatis' and running:
        KP = Knapsack(kapasitas,N=N)

metode = ''
solusi = ''
TW = ''
TP = ''
err_msg = ''

while running:
    layout = [
            [sg.Text('Instance knapsack yang dibuat :')],
            [[sg.Text(str(O))] for O in KP.array_objek],
            [sg.Text(f'kapasitas knapsack = {kapasitas}'),],
            [sg.Text('Pilih metode untuk menyelesaikan')],
            [sg.DropDown(methods),sg.Button('ok')], 
            [sg.Text(f'== hasil {metode} ==')],
            [sg.Text('Himpunan solusi :'),sg.Text(solusi)],
            [sg.Text('Total profit :'),sg.Text(TP)],
            [sg.Text('Total weight :'),sg.Text(TW)],
            [sg.Text(err_msg,text_color='red')], 
        ]
    window = sg.Window(nama_aplikasi,layout)
    event, value = window.read()
    metode = value[0]
    if event == sg.WIN_CLOSED:
        window.close()
        break
    window.close()
    if metode == 'Brute force':
        S,TP,TW = KP.Bruteforce_Knapsack()
        solusi = f'{S}'
        TP = str(TP)
        TW = str(TW)
        err_msg = ''
    elif metode == 'Greedy by profit':
        S,TP,TW = KP.GreedyByProfit_Knapsack()
        solusi = f'{S}'
        TP = str(TP)
        TW = str(TW)
        err_msg = ''
    elif metode == 'Greedy by weight':
        S,TP,TW = KP.GreedyByWeight_Knapsack()
        solusi = f'{S}'
        TP = str(TP)
        TW = str(TW)
        err_msg = ''
    elif metode == 'Greedy by density':
        S,TP,TW = KP.GreedyByDensity_Knapsack()
        solusi = f'{S}'
        TP = str(TP)
        TW = str(TW)
        err_msg = ''
    else:
        err_msg = 'harap pilih metode'