try:
    import numpy as np
    import pandas as pd
    import PySimpleGUI as sg
    print('impor berhasil')
except:
    print('''Tidak dapat mengimport modul yang diperlukan, harap menginstall modul berikut 
             numpy : pip install numpy 
             pandas : pip install pandas 
             PySimpleGUI : pip install PySimpleGUI ''')
    raise ImportError 
class Objek:
    def __init__(self,Profit,Weight):
        '''Class untuk objek yang akan digunakan '''
        self.p = Profit
        self.w = Weight
        self.d = Profit / Weight
        self.x_bruteforce = 0
        self.x_greedy_profit = 0
        self.x_greedy_weight = 0
        self.x_greedy_density = 0

    def __str__(self) -> str:
        return f'(P = {self.p} , W = {self.w})'

class Knapsack:
    def __init__(self,kapasitas,**parameter):
        '''Constructor class knapsack , keterangan parameter :
        kapasitas : kapasitas dari knapsack
        N : jumlah objek ,jika diberikan paramater ini maka akan membuat objek secara otomatis dengan jumlah N
        set_objek : himpunnan semua objek berupa dictionary'''
        try:
            assert 'N' in parameter or 'set_objek' in parameter #parameter harus berisi N atau set_objek
            assert not ('N' in parameter and 'set_objek' in parameter) #parameter tidak boleh berisi N dan set_objek sekaligus
            self.K = kapasitas
            if 'N' not in parameter and 'set_objek' in parameter:
                self.N = len(parameter['set_objek'])
                self.__generate_objects_from(parameter['set_objek'])
            elif 'N' in parameter and 'set_objek' not in parameter:
                self.N = parameter['N']
                self.__generate_objects_random()
        except AssertionError:
            raise AssertionError('harap input salah satu parameter N atau set_objek, tetapi tidak keduanya sekaligus')
    
    def __str__(self) -> str:
        set = {key:str(val) for key,val in self.SET.items()}
        return str(set)

    @property
    def array_objek(self):
        arr = [f'{key} : (P = {val.p}, W = {val.w})' for key,val in self.SET.items()]
        splitter = list(range(2,self.N,2))
        arr = np.split(arr,splitter)
        return arr

    def __generate_objects_from(self,set_objek): #untuk membuat objek dari dictionary yang diberikan
        self.SET = {}
        for nama,objek in set_objek.items():
            self.SET[nama] = Objek(objek['p'],objek['w'])
        
    def __generate_objects_random(self): #untuk membuat objek otomatis
        self.SET = {}
        for i in range(self.N):
            Weight = np.random.randint(10,100)
            Profit = np.random.randint(10,100)
            self.SET[f'Objek{i+1}'] = Objek(Profit,Weight)

    def __subsetsUtil(self,A, subset, index, S): #method untuk mencari semua subset
        S.append(list(subset))                   #dari himpunan objek
        for i in range(index, len(A)):
            subset.append(list(A.items())[i])
            self.__subsetsUtil(A, subset, i + 1, S)
            subset.pop(-1)
        return

    def __subsets(self): #method untuk menyederhanakan parameter dari method __subsetUtil()
        self.subsets = []
        self.__subsetsUtil(self.SET, [], 0, self.subsets)

    @property
    def tabel_objects(self):
        '''Untuk menampilkan tabel semua objek beserta atribut-atributnya'''
        df = []
        for key,val in self.SET.items():
            df.append(
                {'Objek':key,'Weight':val.w,'Profit':val.p,'Density':val.d,
                'Brute Force':val.x_bruteforce,
                'Greedy by profit': val.x_greedy_profit,
                'Greedy by weight': val.x_greedy_weight,
                'Greedy by density': val.x_greedy_density})
       
        return pd.DataFrame(df)
    
    
    def show_subsets(self):
        '''Untuk menampilkan tabel semua himpunan bagian dari himpunan kandidat solusi
        beserta total profit dan total weight'''
        self.__subsets()
        df = []
        for subset in self.subsets:
            sub = []
            TW = 0
            TP = 0
            for key,val in subset:
                sub.append(key)
                TW += val.w
                TP += val.p
            df.append({'Subset':sub,'Total Weight':TW,'Total Profit':TP})
        return pd.DataFrame(df)

    
    def Bruteforce_Knapsack(self):
        '''Menjalankan algoritma Brute-force untuk instance knapsacck yang dibuat'''
        self.__subsets()
        SP = 0
        SW = 0
        for subset in self.subsets:
            sub = []
            TW = 0
            TP = 0
            for key,val in subset:
                sub.append(key)
                TW += val.w
                TP += val.p
            if TW <= self.K and TP > SP:
                SP = TP
                SW = TW
                solution = sub
                
        for objek in solution:
            self.SET[objek].x_bruteforce = 1

        return (solution,SP,SW)
    
    def GreedyByProfit_Knapsack(self):
        '''Menjalankan algoritma greedy by profit untuk instance knapsacck yang dibuat'''
        set = self.tabel_objects
        set = set.sort_values(by='Profit', ascending=False)
        TP = 0
        TW = 0
        Solusi = []
        Sisa = []
        for i in set.loc[:,'Objek']:
            objek = self.SET[i]
            if (TW + objek.w) <= self.K:
                TW += objek.w
                TP += objek.p
                Solusi.append(i)
            else:
                Sisa.append(i)
        Solusi,Sisa,TW,TP = self.__cek_ulang_knapsack(Solusi,Sisa,TW,TP)
        for objek in Solusi:
            self.SET[objek].x_greedy_profit = 1
        
        return (Solusi,TP,TW)
    
    def GreedyByWeight_Knapsack(self):
        '''Menjalankan algoritma greedy by weight untuk instance knapsacck yang dibuat'''
        set = self.tabel_objects
        set = set.sort_values(by='Weight', ascending=True)
        TP = 0
        TW = 0
        Solusi = []
        Sisa = []
        for i in set.loc[:,'Objek']:
            objek = self.SET[i]
            if (TW + objek.w) <= self.K:
                TW += objek.w
                TP += objek.p
                Solusi.append(i)
            else:
                Sisa.append(i)
        Solusi,Sisa,TW,TP = self.__cek_ulang_knapsack(Solusi,Sisa,TW,TP)
        for objek in Solusi:
            self.SET[objek].x_greedy_weight = 1
       
        return (Solusi,TP,TW)    
    
    def GreedyByDensity_Knapsack(self):
        '''Menjalankan algoritma greedy by density untuk instance knapsacck yang dibuat'''
        set = self.tabel_objects
        set = set.sort_values(by='Density', ascending=False)
        TP = 0
        TW = 0
        Solusi = []
        Sisa = []
        for i in set.loc[:,'Objek']:
            objek = self.SET[i]
            if (TW + objek.w) <= self.K:
                TW += objek.w
                TP += objek.p
                Solusi.append(i)
            else:
                Sisa.append(i)
        Solusi,Sisa,TW,TP = self.__cek_ulang_knapsack(Solusi,Sisa,TW,TP)
        for objek in Solusi:
            self.SET[objek].x_greedy_density = 1
        
        return (Solusi,TP,TW)

    def __cek_ulang_knapsack(self,Solusi,Sisa,TW,TP): #fungsi untuk mengecek ulang hasil knapsack dari algoritma greedy
        sk = self.K - TW #sisa kapasitas knapsack

        if len(Solusi) == self.N:
            return (Solusi,Sisa,TW,TP)

        for a,ori in enumerate(Solusi):
            for b,alt in enumerate(Sisa):
                sk_alt = self.K - (TW - self.SET[ori].w + self.SET[alt].w) #sisa kapasitas jika objek solusi ditukar dengan objek sisa
                if sk_alt < 0:
                    continue
                if sk >= sk_alt and self.SET[ori].p < self.SET[alt].p:
                    tmp = Solusi.pop(a)
                    Solusi.append(Sisa.pop(b))
                    Sisa.append(tmp)
                    TW = TW - self.SET[ori].w + self.SET[alt].w
                    TP = TP - self.SET[ori].p + self.SET[alt].p
        return (Solusi,Sisa,TW,TP)


def testing(N):
    print(f'''mengetest dengan perulangan sebanyak {N} kali
============================================================================''')
    beda = 0 #untuk menghitung berapa kali terjadi perbedaan antara hasil brute force dan greedy
    error = 0 #untuk menghitung breapa kali terjadi error
    for i in range(N):
        O = Knapsack(np.random.randint(50,250),N=np.random.randint(5,10)) #membuat instance knapsack acak
        try:
            S1,*K1 = O.Bruteforce_Knapsack() #menjalankan brute force
            S2,*K2 = O.GreedyByProfit_Knapsack() #menjalankan greedy by profit
            S3,*K3 = O.GreedyByWeight_Knapsack() #menjalankan greedy by weight
            S4,*K4 = O.GreedyByDensity_Knapsack() #menjalankan greedy by density
            greedy_jumlah = len(S2), len(S3), len(S4) #jumlah objek di himpunan solusi yang dihasilkan greedy
            greedy_TP = K2[0],K3[0],K4[0] #total profit yang dihasilkan greedy
            greedy_TW = K2[1],K3[1],K4[1] #total weight ------- || ----------
            if K1[0] not in greedy_TP: #membandingkan total profit brute force dengan greedy
                print(f'pada iterasi ke-{i},terdapat perbedaan')
                if len(S1) in greedy_jumlah:#membandingkan jumlah objek pada solusi
                    print(f'jumlah:BF = {len(S1)} , GP = {len(S2)}, GW = {len(S3)}, GD = {len(S4)}')
                    print(f'profit:BF = {K1[0]} , GP = {K2[0]}, GW = {K2[0]}, GD = {K4[0]}')
                    print(f'weight:BF = {K1[1]} , GP = {K2[1]}, GW = {K2[1]}, GD = {K4[1]}')
                    yield O.tabel_objects.sort_values(by='Density', ascending=False)
                print('============================================================================')
                beda += 1
        except Exception as e:
            print(f'pada iterasi ke-{i} terjadi error, pesan error : {e}')
            print('============================================================================')
            error+=1
    else:
        beda = round((beda/N)*100)
        error = round((error/N)*100)
        print(f'pengecekan selesai , persentase terjadi perbedaan = {beda}% , persentase error = {error}%')

def run_testing(N):
    arr = list(testing(N))

if __name__ == '__main__':
    #tulis code untuk mengetest modul di sini
    run_testing(10)