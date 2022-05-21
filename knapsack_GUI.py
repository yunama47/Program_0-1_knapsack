from knapsack import *

nama_aplikasi = 'Aplikasi 0-1 Knapsack Problem'
N = 0
kapasitas = 0
err_msg = ''
set_objek = {}

while True:
    layout = [
        [sg.Text('')],
        [sg.Text("Input jumlah barang (N) = "),sg.Input()],
        [sg.Text("Kapasitas knapsack (K) = "),sg.Input()],
        [sg.Text(err_msg,text_color='red')],
        [sg.Button('next'),] 
    ]
    window = sg.Window(nama_aplikasi,layout)
    event, value = window.read()
    if event == sg.WIN_CLOSED:
        next = False
        break
    try:
        N = int(value[0]) 
        kapasitas = int(value[1])
        next = True
        break
    except:
        err_msg = 'harap masukkan bilangan bulat'
window.close()
err_msg = ''
i = 1
while next:
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
methods = ['Brute force','Greedy by profit','Greedy by weight', 'Greedy by density']
solusi = ''
TW = ''
TP = ''
metode = ''

while next:
    layout = [
            [sg.Text('Pilih metode')],
            [sg.DropDown(methods),sg.Button('ok')], 
            [sg.Text(f'hasil {metode}')],
            [sg.Text('Himpunan solusi :'),sg.Text(solusi)],
            [sg.Text('Total profit :'),sg.Text(TP)],
            [sg.Text('Total weight :'),sg.Text(TW)],
            [sg.Button('selesai')], 
        ]
    window = sg.Window(nama_aplikasi,layout)
    event, value = window.read()
    metode = value[0]
    if event == sg.WIN_CLOSED or event == 'selesai':
        break
    if metode == 'Brute force':
        S,TP,TW = KP.Bruteforce_Knapsack()
        solusi = f'{S}'
        TP = str(TP)
        TW = str(TW)
    elif metode == 'Greedy by profit':
        S,TP,TW = KP.GreedyByProfit_Knapsack()
        solusi = f'{S}'
        TP = str(TP)
        TW = str(TW)
    elif metode == 'Greedy by weight':
        S,TP,TW = KP.GreedyByWeight_Knapsack()
        solusi = f'{S}'
        TP = str(TP)
        TW = str(TW)
    elif metode == 'Greedy by density':
        S,TP,TW = KP.GreedyByDensity_Knapsack()
        solusi = f'{S}'
        TP = str(TP)
        TW = str(TW)
window.close()
    
