import numpy as np
import pandas as pd

def tukar_nilai(A,B):
    A,B = B,A

class Objek:
    def __init__(self,Profit,Weight):
        self.p = Profit
        self.w = Weight
        self.d = Profit / Weight
        self.x_bruteforce = 0
        self.x_greedy_profit = 0
        self.x_greedy_weight = 0
        self.x_greedy_density = 0


class Knapsack:
    def __init__(self,kapasitas,**parameter):
        
        assert 'N' in parameter or 'set_objek' in parameter #parameter harus berisi N atau set_objek
        assert not ('N' in parameter and 'set_objek' in parameter) #parameter tidak boleh berisi N dan set_objek sekaligus

        self.K = kapasitas
        if 'N' not in parameter and 'set_objek' in parameter:
            self.N = len(parameter['set_objek'])
            self.__generate_objects_from(parameter['set_objek'])
        elif 'N' in parameter and 'set_objek' not in parameter:
            self.N = parameter['N']
            self.__generate_objects_random()
            
    def __generate_objects_from(self,set_objek):
        self.SET = {}
        for nama,objek in set_objek.items():
            self.SET[nama] = Objek(objek['p'],objek['w'])
        
    def __generate_objects_random(self):
        self.SET = {}
        for i in range(self.N):
            Weight = np.random.randint(10,100)
            Profit = np.random.randint(10,100)
            self.SET[f'Objek{i+1}'] = Objek(Profit,Weight)

    def __subsetsUtil(self,A, subset, index, S):
        S.append(list(subset))
        for i in range(index, len(A)):
            subset.append(list(A.items())[i])
            self.__subsetsUtil(A, subset, i + 1, S)
            subset.pop(-1)
        return

    def __subsets(self):
        self.subsets = []
        self.__subsetsUtil(self.SET, [], 0, self.subsets)

    @property
    def tabel_objects(self):
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

        # print(f'''
        # Hasil dari algoritma brute-force:
        # Total Profit = {SP}
        # Total Weight = {SW}
        # Objek yang diambil = {solution}
        # ''')
        return (solution,SP,SW)
    
    
    def GreedyByProfit_Knapsack(self):
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
        # print(f'''
        # Hasil dari algoritma greedy by profit:
        # Total Profit = {TP}
        # Total Weight = {TW}
        # Objek yang diambil = {Solusi}
        # ''')
        return (Solusi,TP,TW)
    
    def GreedyByWeight_Knapsack(self):
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
        # print(f'''
        # Hasil dari algoritma greedy by weight:
        # Total Profit = {TP}
        # Total Weight = {TW}
        # Objek yang diambil = {Solusi}
        # ''')
        return (Solusi,TP,TW)    
    
    def GreedyByDensity_Knapsack(self):
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
        # print(f'''
        # Hasil dari algoritma greedy by density:
        # Total Profit = {TP}
        # Total Weight = {TW}
        # Objek yang diambil = {Solusi}
        # ''')
        return (Solusi,TP,TW)

    def __cek_ulang_knapsack(self,Solusi,Sisa,TW,TP):
        sk = self.K - TW #sisa kapasitas knapsack
        # Solusi_alt = Solusi.copy()

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
                            

if __name__ == '__main__':
    N = 1000
    
