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
    
    ################################################################################



class UtilsAnalysis:
    def __init__(self, df=None):
        self.df = df  # Class instance içinde df'yi saklama
    
    def set_df(self, df):
        """df'yi dışarıdan alma fonksiyonu."""
        self.df = df


   ######################## COLUMN RENAMING ######################## 
    def rename_columns_by_position(self, new_column_names):
        """
        DataFrame'deki sütun adlarını pozisyona göre yeniden adlandırır.
        """
        if self.df is None:
            raise ValueError("Geçerli bir DataFrame sağlamalısınız.")
        
        # Sütun sayısının uyumlu olup olmadığını kontrol et
        if len(new_column_names) != len(self.df.columns):
            raise ValueError("Sütun sayısı ile yeni adların sayısı eşleşmiyor.")

        # Yeni sütun adlarını atama
        self.df.columns = new_column_names
        return self.df

    
    ######################## CATEGORICAL FEATURES SUMMARY #######################
    def object_summary(self, df):
        """
        Kategorik sütunlar için özetleme bilgilerini döndürür.
        """
        if df is None:
            print("Geçerli bir DataFrame sağlamalısınız.")
            return None

        obs = df.shape[0]
        duplicate_count = df.duplicated().sum()
        object_df = df.select_dtypes(include='object')

        summary_df = pd.DataFrame(index=object_df.columns)
        summary_df['Dtype'] = object_df.dtypes
        summary_df['Counts'] = object_df.count()
        summary_df['Nulls'] = object_df.isnull().sum()
        summary_df['NullPercent'] = (object_df.isnull().sum() / obs) * 100
        summary_df['Top'] = object_df.apply(lambda x: x.mode().iloc[0] if not x.mode().empty else '-')
        summary_df['Frequency'] = object_df.apply(lambda x: x.value_counts().max() if not x.value_counts().empty else '-')
        summary_df['Uniques'] = object_df.nunique()
        summary_df['UniqueValues'] = object_df.apply(
            lambda x: ', '.join(map(str, x.unique()[:10])) + '...' if x.nunique() > 10 else ', '.join(map(str, x.unique()))
        )
        print(f'1. Data shape (rows, columns): {df.shape}')
        print(f'2. Number of duplicate rows: {duplicate_count}')
        return summary_df

    ######################## NUMERICAL FEATURES SUMMARY #########################
    def numeric_summary(self, df):
        """
        Numerik sütunlar için özetleme bilgilerini döndürür.
        """
        if df is None:
            print("Geçerli bir DataFrame sağlamalısınız.")
            return None

        obs = df.shape[0]
        duplicate_count = df.duplicated().sum()
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        summary_df = pd.DataFrame(index=numeric_df.columns)

        summary_df['Dtype'] = numeric_df.dtypes
        summary_df['Counts'] = numeric_df.count()
        summary_df['Nulls'] = numeric_df.isnull().sum()
        summary_df['NullPercent'] = (numeric_df.isnull().sum() / obs) * 100
        summary_df['Mean'] = numeric_df.mean()
        summary_df['Std'] = numeric_df.std()
        summary_df['Min'] = numeric_df.min()
        summary_df['25%'] = numeric_df.quantile(0.25)
        summary_df['50% (Median)'] = numeric_df.median()
        summary_df['75%'] = numeric_df.quantile(0.75)
        summary_df['Max'] = numeric_df.max()
        print(f'1. Data shape (rows, columns): {df.shape}')
        print(f'2. Number of duplicate rows: {duplicate_count}')
        return summary_df

    ######################## VALUE COUNTS ##############################
    def get_value_count(self, df, column_name):
        """
        Belirtilen bir sütundaki değerlerin sayısını ve yüzdelerini döndürür.
        """
        if df is None:
            print("Geçerli bir DataFrame sağlamalısınız.")
            return None

        vc = df[column_name].value_counts()
        vc_norm = df[column_name].value_counts(normalize=True)
        vc = vc.rename_axis(column_name).reset_index(name='counts')
        vc_norm = vc_norm.rename_axis(column_name).reset_index(name='percent')
        vc_norm['percent'] = (vc_norm['percent'] * 100).map('{:.2f}%'.format)
        df_result = pd.concat([vc[column_name], vc['counts'], vc_norm['percent']], axis=1)
        return df_result

    ######################## DUPLICATE CHECK AND DROP ############################
    def duplicate_values(self, df):
        """
        Tekrarlı değerleri kontrol eder ve varsa siler.
        """
        if df is None:
            print("Geçerli bir DataFrame sağlamalısınız.")
            return None

        num_duplicates = df.duplicated().sum()
        if num_duplicates > 0:
            print("There are", num_duplicates, "duplicated observations in the dataset.")
            df.drop_duplicates(inplace=True)
            print(num_duplicates, "duplicates were dropped!")
        else:
            print("No duplicated observations found.")
        return df

    ######################## MISSING VALUES ##############################
    def missing_values(self, df):
        """
        Eksik değerlerin sayısını ve yüzdesini hesaplar.
        """
        if df is None:
            print("Geçerli bir DataFrame sağlamalısınız.")
            return None

        missing_count = df.isnull().sum()
        value_count = df.isnull().count()
        missing_percentage = round(missing_count / value_count * 100, 2)
        missing_percentage_formatted = missing_percentage.map("{:.2f}%".format)
        missing_df = pd.DataFrame({"count": missing_count, "percentage": missing_percentage_formatted})
        return missing_df

    ######################## MISSING VALUE PLOT ##############################
    def na_ratio_plot(self, df):
        """
        Eksik değer oranlarını grafikler ve eksik değerlerin sayısını yazdırır.
        """
        if df is None:
            print("Geçerli bir DataFrame sağlamalısınız.")
            return None

        sns.displot(df.isna().melt(value_name='Missing_data', var_name='Features'), 
                    y='Features', hue='Missing_data', multiple='fill', aspect=9/8)
        print(df.isna().sum()[df.isna().sum() > 0])

    ######################## ANOMALY DETECTION ##############################
    def detect_anomalies(self, df, column_name):
        """
        Alfasayısal olmayan karakterler içeren değerleri tespit eder.
        """
        if df is None:
            print("Geçerli bir DataFrame sağlamalısınız.")
            return None

        unique_values = df[column_name].unique()
        unusual_characters = [val for val in unique_values if isinstance(val, str) and not val.isalnum()]
        return ', '.join(unusual_characters)

    ######################## NON-NUMERIC CHARACTER DETECTION ####################
    def find_non_numeric_values(self, df, column_name):
        """
        Bir sütunda bulunan benzersiz sayısal olmayan değerleri tespit eder.
        """
        if df is None:
            print("Geçerli bir DataFrame sağlamalısınız.")
            return None

        pattern = r'\D+'
        return set(re.findall(pattern, ' '.join(df[column_name].astype(str))))

    ######################## COLUMN RENAMING ####################################
    def rename_columns_by_position(self, new_column_names):
        """
        DataFrame'deki sütun adlarını pozisyona göre yeniden adlandırır.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None
        
        # Sütun sayısının uyumlu olup olmadığını kontrol et
        if len(new_column_names) != len(self.df.columns):
            raise ValueError("Sütun sayısı ile yeni adların sayısı eşleşmiyor.")
        
        # Yeni sütun adlarını atama
        self.df.columns = new_column_names   
        return self.df  # DataFrame'i geri döndürme

    ######################## CATEGORICAL FEATURES SUMMARY #######################
    def object_summary(self):
        """
        Kategorik sütunlar için özetleme bilgilerini döndürür.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None
        
        obs = self.df.shape[0]
        duplicate_count = self.df.duplicated().sum()

        # Kategorik sütunlar için özetleme
        object_df = self.df.select_dtypes(include='object')
        
        # Yeni bir boş DataFrame oluşturma
        summary_df = pd.DataFrame(index=object_df.columns)

        summary_df['Dtype'] = object_df.dtypes
        summary_df['Counts'] = object_df.count()
        summary_df['Nulls'] = object_df.isnull().sum()
        summary_df['NullPercent'] = (object_df.isnull().sum() / obs) * 100
        summary_df['Top'] = object_df.apply(lambda x: x.mode().iloc[0] if not x.mode().empty else '-')
        summary_df['Frequency'] = object_df.apply(lambda x: x.value_counts().max() if not x.value_counts().empty else '-')
        summary_df['Uniques'] = object_df.nunique()

        # UniqueValues sütununu kontrol ederek ekleme (dize olarak)
        summary_df['UniqueValues'] = object_df.apply(
            lambda x: ', '.join(map(str, x.unique()[:10])) + '...' if x.nunique() > 10 else ', '.join(map(str, x.unique()))
        )

        print(f'1. Data shape (rows, columns): {self.df.shape}')
        print(f'2. Number of duplicate rows: {duplicate_count}')
        return summary_df

    ######################## NUMERICAL FEATURES SUMMARY #########################
    def numeric_summary(self):
        """
        Numerik sütunlar için özetleme bilgilerini döndürür.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None
        
        obs = self.df.shape[0]
        duplicate_count = self.df.duplicated().sum()

        # Numerik sütunlar için özetleme
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])

        # Yeni bir boş DataFrame oluşturma
        summary_df = pd.DataFrame(index=numeric_df.columns)

        summary_df['Dtype'] = numeric_df.dtypes
        summary_df['Counts'] = numeric_df.count()
        summary_df['Nulls'] = numeric_df.isnull().sum()
        summary_df['NullPercent'] = (numeric_df.isnull().sum() / obs) * 100
        summary_df['Mean'] = numeric_df.mean()
        summary_df['Std'] = numeric_df.std()
        summary_df['Min'] = numeric_df.min()
        summary_df['25%'] = numeric_df.quantile(0.25)
        summary_df['50% (Median)'] = numeric_df.median()
        summary_df['75%'] = numeric_df.quantile(0.75)
        summary_df['Max'] = numeric_df.max()

        print(f'1. Data shape (rows, columns): {self.df.shape}')
        print(f'2. Number of duplicate rows: {duplicate_count}')
        return summary_df

    ######################## VALUE COUNTS ##############################
    def get_value_count(self, column_name):
        """
        Bu fonksiyon, belirtilen bir sütundaki değerlerin sayısını ve yüzde oranlarını döndürür.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None
        
        vc = self.df[column_name].value_counts()
        vc_norm = self.df[column_name].value_counts(normalize=True)
        
        vc = vc.rename_axis(column_name).reset_index(name='counts')
        vc_norm = vc_norm.rename_axis(column_name).reset_index(name='percent')
        vc_norm['percent'] = (vc_norm['percent'] * 100).map('{:.2f}%'.format)
        
        df_result = pd.concat([vc[column_name], vc['counts'], vc_norm['percent']], axis=1)
        return df_result

    ######################## DUPLICATE CHECK AND DROP ############################
    def duplicate_values(self):
        """
        Tekrarlı değerleri kontrol eder ve varsa siler.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None
        
        print("Duplicate check...")
        num_duplicates = self.df.duplicated(subset=None, keep='first').sum()
        if num_duplicates > 0:
            print("There are", num_duplicates, "duplicated observations in the dataset.")
            self.df.drop_duplicates(keep='first', inplace=True)
            print(num_duplicates, "duplicates were dropped!")
            print("No more duplicate rows!")
        else:
            print("There are no duplicated observations in the dataset.")
        return self.df

    ######################## MISSING VALUES ##############################
    def missing_values(self):
        """
        Eksik değerlerin sayısını ve yüzdesini hesaplar.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None
        
        missing_count = self.df.isnull().sum()
        value_count = self.df.isnull().count()
        missing_percentage = round(missing_count / value_count * 100, 2)
        
        # Yüzdeleri '0.00%' formatında görüntüleme
        missing_percentage_formatted = missing_percentage.map("{:.2f}%".format)
        # Sonuçları depolamak için bir DataFrame oluşturma
        missing_df = pd.DataFrame({"count": missing_count, "percentage": missing_percentage_formatted}) 
        return missing_df

    ######################## MISSING VALUE PLOT ##############################
    def na_ratio_plot(self):
        """
        Her özellik için eksik değer oranlarını grafikler ve eksik değerlerin sayısını yazdırır.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None
        
        sns.displot(self.df.isna().melt(value_name='Missing_data', var_name='Features'), 
                    y='Features', hue='Missing_data', multiple='fill', aspect=9/8)

        print(self.df.isna().sum()[self.df.isna().sum() > 0])

    ######################## ANOMALY DETECTION ##############################
    def detect_anomalies(self, column_name):
        """
        Alfasayısal olmayan karakterler içeren değerleri tespit eder.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None
        
        unique_values = self.df[column_name].unique()    
        unusual_characters = [val for val in unique_values if isinstance(val, str) and not val.isalnum()]
        
        # Bulunan değerleri birleştirip döndürme
        return ', '.join(unusual_characters)

    ######################## NON-NUMERIC CHARACTER DETECTION ####################
    def find_non_numeric_values(self, column_name):
        """
        Bir sütunda bulunan benzersiz sayısal olmayan değerleri tespit eder.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None
        
        pattern = r'\D+'  # Sayısal olmayan karakterleri bulmak için desen
        # Sayısal olmayan karakterleri bul ve listeyi set ile benzersiz hale getir
        return set(re.findall(pattern, ' '.join(self.df[column_name].astype(str))))
