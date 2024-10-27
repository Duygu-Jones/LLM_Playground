import os
import pandas as pd
import seaborn as sns
import re

class UtilsAnalysis:
    def __init__(self):
        self.df = None  # Başlangıçta df'yi None olarak ayarla


    ######################## CATEGORICAL FEATURES SUMMARY #######################
    def object_summary(self):
        """
        Kategorik sütunlar için özetleme bilgilerini döndürür.
        """
        # Eğer self.df tanımlıysa, fonksiyona geçer
        if self.df is not None:
            obs = self.df.shape[0]
            duplicate_count = self.df.duplicated().sum()
            object_df = self.df.select_dtypes(include='object')

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
            print(f'1. Data shape (rows, columns): {self.df.shape}')
            print(f'2. Number of duplicate rows: {duplicate_count}')
            return summary_df
        else:
            print("Lütfen önce bir DataFrame yükleyin.")
            return None

    ######################## NUMERICAL FEATURES SUMMARY #########################
    def numeric_summary(self):
        """
        Numerik sütunlar için özetleme bilgilerini döndürür.
        """
        # Eğer self.df tanımlıysa, fonksiyona geçer
        if self.df is not None:
            obs = self.df.shape[0]
            duplicate_count = self.df.duplicated().sum()
            numeric_df = self.df.select_dtypes(include=['float64', 'int64'])

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
        else:
            print("Lütfen önce bir DataFrame yükleyin.")
            return None

        
   ######################## SELF COLUMN ##############################
    def set_column(self):
        """
        Kullanıcıya mevcut sütunları gösterir ve sütun adını seçmesini ister.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None

        # Mevcut sütunları listeleme
        print("Mevcut sütunlar:")
        print(" | ".join(self.df.columns))

        # Kullanıcıdan sütun adını alma
        print("\nLütfen analiz etmek istediğiniz sütun adını yazınız (örn: 'siparis_tarihi', 'siparisi_veren'):")
        column_name = input("Sütun adı: ")

        # Seçilen sütunun kontrolü
        if column_name not in self.df.columns:
            print(f"'{column_name}' sütunu mevcut değil. Lütfen geçerli bir sütun adı girin.")
            return None
        else:
            print(f"'{column_name}' sütunu başarıyla seçildi!")
            return column_name

    ######################## VALUE COUNTS ##############################
    def get_value_count(self):
        """
        Seçilen sütundaki değerlerin sayısını ve yüzde oranlarını döndürür.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None

        column_name = self.set_column()
        if column_name is None:
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
        DataFrame'deki tekrarlı değerleri kontrol eder ve varsa siler.
        """
        # DataFrame kontrolü
        if self.df is None:
            print("Lütfen önce bir DataFrame yükleyin.")
            return None

        # Tekrarlı değerlerin sayısını kontrol etme
        num_duplicates = self.df.duplicated().sum()
        if num_duplicates > 0:
            print(f"{num_duplicates} adet tekrarlı gözlem bulundu. Bunlar silinecek.")
            # Tekrarlı değerleri silme
            self.df.drop_duplicates(inplace=True)
            print(f"{num_duplicates} adet tekrarlı gözlem silindi.")
        else:
            print("Tekrarlı gözlem bulunamadı.")

        # Güncellenmiş DataFrame'i döndür
        return self.df
    

    ######################## MISSING VALUES ##############################
    def missing_values(self):
        """
        DataFrame'deki eksik değerlerin sayısını ve yüzdesini hesaplar.
        """
        if self.df is None:
            print("Önce bir DataFrame yüklemelisiniz.")
            return None

        missing_count = self.df.isnull().sum()
        value_count = self.df.shape[0]
        missing_percentage = (missing_count / value_count * 100).map("{:.2f}%".format)
        missing_df = pd.DataFrame({"Eksik Değer Sayısı": missing_count, "Yüzde": missing_percentage})
        
        print("Eksik değerlerin sütun bazında dökümü aşağıda verilmiştir:")
        return missing_df
    
######################## MISSING VALUE PLOT ##############################
    def na_ratio_plot(self):
        """
        Eksik değer oranlarını grafikler ve eksik değerlerin sayısını yazdırır.
        """
        # DataFrame kontrolü
        if self.df is None:
            print("Lütfen önce bir DataFrame yükleyin.")
            return None

        # Eksik değer oranlarını grafikte gösterme
        sns.displot(self.df.isna().melt(value_name='Missing_data', var_name='Features'), 
                    y='Features', hue='Missing_data', multiple='fill', aspect=9/8)
        print("Eksik değer sayısı (0'dan fazla olan sütunlar):")
        print(self.df.isna().sum()[self.df.isna().sum() > 0])

    ######################## ANOMALY DETECTION ##############################
    def detect_anomalies(self):
        """
        Sütunlarda alfasayısal olmayan karakterler içeren değerleri tespit eder.
        alfasayısal olmayan karakterler metinlerde kullanılan harf ve rakam dışındaki tüm sembolleri içerir.
        """
        # DataFrame kontrolü
        if self.df is None:
            print("Lütfen önce bir DataFrame yükleyin.")
            return None

        # Mevcut sütunları listeleme
        print("Mevcut sütunlar:")
        print(" | ".join(self.df.columns))

        # Kullanıcıdan sütun adını alma
        print("\nLütfen analiz etmek istediğiniz sütun adını yazınız:")
        column_name = input("Sütun adı: ")

        # Sütunun mevcut olup olmadığını kontrol etme
        if column_name not in self.df.columns:
            print(f"'{column_name}' sütunu mevcut değil. Lütfen geçerli bir sütun adı girin.")
            return None

        # Alfasayısal olmayan karakterlerin tespiti
        unique_values = self.df[column_name].unique()
        unusual_characters = [val for val in unique_values if isinstance(val, str) and not val.isalnum()]

        if unusual_characters:
            print(f"'{column_name}' sütununda alfasayısal olmayan karakterler tespit edildi:")
            return ', '.join(unusual_characters)
        else:
            print(f"'{column_name}' sütununda alfasayısal olmayan karakterler bulunamadı.")
            return None

######################## NON-NUMERIC CHARACTER DETECTION ####################
    def find_non_numeric_values(self):
        """
        Seçilen sütunda bulunan benzersiz sayısal olmayan değerleri tespit eder,
        NaN değerleri göz ardı eder.
        """
        # DataFrame kontrolü
        if self.df is None:
            print("Lütfen önce bir DataFrame yükleyin.")
            return None

        # Mevcut sütunları listeleme (yatay format)
        print("Mevcut sütunlar:")
        print(" | ".join(self.df.columns))

        # Kullanıcıdan sütun adını alma
        print("\nLütfen analiz etmek istediğiniz sütun adını yazınız (örn: 'siparis_no'):")
        column_name = input("Sütun adı: ")

        # Sütun kontrolü
        if column_name not in self.df.columns:
            print(f"'{column_name}' sütunu mevcut değil.")
            return None

        # Sayısal olmayan karakterlerin tespiti (NaN değerlerini göz ardı etme)
        column_data = self.df[column_name].dropna().astype(str)
        pattern = r'\D+'  # Sayısal olmayan karakterleri tespit etme
        non_numeric_values = set(re.findall(pattern, ' '.join(column_data)))

        if non_numeric_values:
            print(f"'{column_name}' sütununda bulunan benzersiz sayısal olmayan değerler:")
            return non_numeric_values
        else:
            print(f"'{column_name}' sütununda sayısal olmayan karakterler bulunamadı.")
            return None


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
        