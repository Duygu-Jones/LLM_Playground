import os
import pandas as pd
import seaborn as sns
import re


class Utils:
    def __init__(self):
        self.df = None  # DataFrame başlangıçta boş olacak


        
# BU MODULDE EN COK KULLANDIGIMIZ FONKSIYONLARI DERLEYECEGIZ. 
# BU MODUL ORTAK BIR ALANDA BULUNACAK VE J-NOTEBOOK ICERISINDE KULLANACAGINIZ ZAMAN BU MODULE AIT DOSYA YOLUNU VEREREK IMPORT ETDINIZ       
               
        
    ######################### READ EXCEL PAGE ###################################
    def read_excel_page(self):
        """
        Excel dosyasındaki bir sayfayı seçip okuyan fonksiyon.
        """
        # 1. Kullanıcıdan çalışma dizinini alma (Datasetinizin bulunduğu dizin)
        base_dir = input(r"Lütfen Dataset dosya yolunu girin (örnek: C:\Users\ASUS\Desktop\INT_1_PROJECT\00_Data\01_Satis_Uretim): ")
        os.chdir(base_dir)  # Çalışma dizinini ayarla

        # 2. Kullanıcıdan dosya adını alma (xlsx dosyası)
        file_name = input("Lütfen Excel dosyasının adını girin (örnek: 2018-Uretim_Takip.xlsx): ")

        try:
            # 3. Dosyadaki tüm sayfa adlarını listeleme (alt sayfa isimlerini listeler)
            xls = pd.ExcelFile(file_name)
            sheet_names = xls.sheet_names
            print(f"Dosyadaki sayfa adları: {sheet_names}")

            # 4. Kullanıcıdan sayfa adını seçmesini isteme
            selected_page = input("Lütfen okumak istediğiniz sayfanın adını girin: ")

            # 5. Seçilen sayfayı DataFrame olarak alma
            if selected_page in sheet_names:
                self.df = pd.read_excel(file_name, sheet_name=selected_page)

                # 6. Boş sütunları kaldırma
                self.df = self.df.loc[:, ~self.df.columns.str.contains('^Unnamed')]

                # 7. Dinamik DataFrame adı oluşturma
                df_name = f"df_otoklav_{file_name.split('-')[0]}"

                # 8. DataFrame'i döndürme ve adıyla birlikte yazdırma
                globals()[df_name] = self.df  # Global değişken olarak atama
                print(f"'{df_name}' olarak kaydedildi.")
                return self.df

            else:
                print("Geçersiz sayfa adı. Lütfen doğru sayfa adını girin.")

        except FileNotFoundError:
            print("Dosya bulunamadı. Lütfen dosya adını doğru girdiğinizden emin olun.")
        except Exception as e:
            print(f"Hata: {e}")

            
            
    ######################## SAVE AND LOAD AS CSV ####################################
    def save_and_load_csv(self, filename, dir_path):
        """
        DataFrame'i belirtilen dizine CSV olarak kaydeder ve tekrar yükler.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return

        # 1. Tam dosya yolunu oluşturma
        csv_file_path = os.path.join(dir_path, filename)

        # 2. DataFrame'i CSV dosyası olarak kaydetme
        self.df.to_csv(csv_file_path, index=False)
        print(f"DataFrame başarıyla '{csv_file_path}' olarak kaydedildi.")

        # 3. Kaydedilen CSV dosyasını okuma
        loaded_df = pd.read_csv(csv_file_path)
        print(f"DataFrame başarıyla '{csv_file_path}' dosyasından okundu.")

        return loaded_df
    

 ######################## DATAFRAME'LERIN SUTUN ISIMLERINI KARSILASTIRIR ####################

    def create_columns_table(self, *dfs):
        """
        Verilen DataFrame'lerin sütun isimlerini tablo halinde gösterir.
        DataFrame'lere sırasıyla otomatik isim verir.
        
        :param dfs: Sırasız olarak verilen DataFrame'ler (örneğin, df1, df2, ...)
        :return: Sütun isimlerini gösteren bir DataFrame
        """
        # Sütun isimlerini bir listede topla
        column_lists = [df.columns.tolist() for df in dfs]
        
        # En uzun sütun listesine göre eksik sütunları doldurmak için her listeyi aynı uzunlukta yap
        max_len = max(len(cols) for cols in column_lists)
        column_lists = [cols + [None] * (max_len - len(cols)) for cols in column_lists]
        
        # DataFrame'lere otomatik isimler ver (örneğin, df1, df2, ...)
        col_table = pd.DataFrame({f'df{i+1}': cols for i, cols in enumerate(column_lists)})
        return col_table       
        

