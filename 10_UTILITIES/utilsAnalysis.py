import os
import pandas as pd
import seaborn as sns
import re
from datetime import datetime
from datetime import timedelta
import dateparser


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

        
  
    ######################## VALUE COUNTS ##############################
    def get_value_count(self):
        """
        Seçilen sütundaki değerlerin sayısını ve yüzde oranlarını döndürür.
        """
        # DataFrame kontrolü
        if self.df is None:
            print("Lütfen önce bir DataFrame yükleyin.")
            return None

        # Mevcut sütunları listeleme (yatay format)
        print("Mevcut sütunlar:")
        print(" | ".join(self.df.columns))

        # Kullanıcıdan sütun adını alma
        print("\nLütfen değerlerini görmek istediğiniz sütun adını yazınız (örn: 'siparis_tarihi'):")
        column_name = input("Sütun adı: ").strip()

        # Sütun kontrolü
        if column_name not in self.df.columns:
            print(f"'{column_name}' sütunu mevcut değil.")
            return None

        # Değer sayımları ve yüzdeler
        vc = self.df[column_name].value_counts()
        vc_norm = self.df[column_name].value_counts(normalize=True)
        
        # DataFrame formatında birleştirme ve düzenleme
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

        
 #================================================================================       

    def groupby_get_values(self):
        """
        Kullanıcıdan bir index sütunu ve analiz edilecek sütunları alır,
        veriyi gruplandırır ve belirtilen sütunlardaki dolu değerlerin özetini DataFrame olarak döndürür.
        """
        # Mevcut sütunları gösterme
        print("Mevcut sütunlar:")
        print(" | ".join(self.df.columns))

        # Kullanıcıdan gruplandırma yapılacak index sütununu alma
        index_column = input("\nLütfen groupby yapılacak sütunu seçiniz (örneğin: kategori, teslim_tarihi vb.): ")
        if index_column not in self.df.columns:
            print(f"'{index_column}' sütunu mevcut değil. Lütfen geçerli bir sütun adı girin.")
            return

        # Kullanıcıdan analiz edilecek sütunları virgülle ayırarak alma
        columns_input = input("\nDeğerlerini görmek istediğiniz diğer sütunları virgülle ayırarak giriniz (örneğin: fiyat, adet, tarih): ")
        columns = [col.strip() for col in columns_input.split(',')]

        # Geçerli ve geçersiz sütunları ayırt etme
        valid_columns = [col for col in columns if col in self.df.columns]
        invalid_columns = [col for col in columns if col not in self.df.columns]

        # Geçersiz sütunlar varsa kullanıcıyı bilgilendirme
        if invalid_columns:
            print(f"\nGeçersiz sütunlar: {', '.join(invalid_columns)}")
            return

        # Kategorilere göre belirtilen sütunlardaki dolu değerlerin sayısını hesaplayan DataFrame
        grouped_df = self.df.groupby(index_column)[valid_columns].apply(lambda x: x.notnull().sum())

        # Sadece belirtilen sütunlar ve index sütununu içeren bir DataFrame oluşturma
        final_df = grouped_df.reset_index()

        # Sonuçları ekrana yazdırma
        print("\n# Gruplandırılmış DataFrame (Dolu Değerler):\n")
        return final_df


#===========================================================================================

    def groupby_get_null_values(self):
        """
        Kullanıcıdan bir index sütunu ve analiz edilecek sütunları alır,
        veriyi gruplandırır ve belirtilen sütunlardaki null değerlerin özetini DataFrame olarak döndürür.
        """
        # Mevcut sütunları gösterme
        print("Mevcut sütunlar:")
        print(" | ".join(self.df.columns))

        # Kullanıcıdan gruplandırma yapılacak index sütununu alma
        index_column = input("\nLütfen index olarak kullanılacak sütunu seçiniz (örneğin: kategori, teslim_tarihi vb.): ")
        if index_column not in self.df.columns:
            print(f"'{index_column}' sütunu mevcut değil. Lütfen geçerli bir sütun adı girin.")
            return

        # Kullanıcıdan analiz edilecek sütunları virgülle ayırarak alma
        columns_input = input("\nNull değerlerini görmek istediğiniz diğer sütunları virgülle ayırarak giriniz (örneğin: fiyat, adet, tarih): ")
        columns = [col.strip() for col in columns_input.split(',')]

        # Geçerli ve geçersiz sütunları ayırt etme
        valid_columns = [col for col in columns if col in self.df.columns]
        invalid_columns = [col for col in columns if col not in self.df.columns]

        # Geçersiz sütunlar varsa kullanıcıyı bilgilendirme
        if invalid_columns:
            print(f"\nGeçersiz sütunlar: {', '.join(invalid_columns)}")
            return

        # Kategorilere göre her sütundaki null değerlerin sayısını hesaplayan DataFrame
        grouped_df = self.df.groupby(index_column)[valid_columns].apply(lambda x: x.isnull().sum())

        # Sadece belirtilen sütunlar ve index sütununu içeren bir DataFrame oluşturma
        final_df = grouped_df.reset_index()

        # Sonuçları ekrana yazdırma
        print("\n# Gruplandırılmış DataFrame (Null Değerler):\n")
        return final_df


#=======================================================================

    def clean_and_standardize_date(self):
        """
        Seçilen sütundaki tarihleri temizleyip standart bir formata (YYYY-MM-DD) dönüştürür.
        """
        # DataFrame kontrolü
        if self.df is None:
            print("Lütfen önce bir DataFrame yükleyin.")
            return None

        # Mevcut sütunları listeleme (yatay format)
        print("Mevcut sütunlar:")
        print(" | ".join(self.df.columns))

        # Kullanıcıdan sütun adını alma
        print("\nLütfen tarihleri temizlemek istediğiniz sütun adını yazınız (örn: 'siparis_tarihi'):")
        column_name = input("Sütun adı: ").strip()

        # Sütun kontrolü
        if column_name not in self.df.columns:
            print(f"'{column_name}' sütunu mevcut değil.")
            return None

        # Tarih temizleme ve formatlama işlemi
        def standardize_date(date_string):
            if pd.isnull(date_string):  # Boş değer kontrolü
                return None

            # Kelime olarak girilen tarih ifadeleri de dahil olmak üzere tarih formatını analiz et
            parsed_date = dateparser.parse(date_string)
            if parsed_date:
                return parsed_date.strftime("%Y-%m-%d")
            else:
                return None

        # Seçilen sütundaki her bir tarihi temizleme ve formatlama
        self.df[column_name] = self.df[column_name].apply(standardize_date)
        print(f"'{column_name}' sütunundaki tarihler temizlenmiş ve standart hale getirilmiştir.")
        
        # İlk birkaç satırı göstermek için
        return self.df[[column_name]].head()

    
    
#===========================DATE CALCULATION =============================    
    def calculate_date_operation(self, index):
        """
        Belirli bir indeksli satırda, sipariş, teslim tarihi veya teslim süresi üzerinden eksik veriyi hesaplar.

        :param index: İşlem yapılacak satırın indeksi
        """
        # DataFrame kontrolü
        if self.df is None:
            print("Lütfen önce bir DataFrame yükleyin.")
            return None

        # Belirtilen indeksli satırın verilerini al
        row = self.df.loc[index]

        # Gerekli sütunların doluluğunu kontrol et
        siparis_tarihi = pd.to_datetime(row['siparis_tarihi'], errors='coerce')
        teslim_tarihi = pd.to_datetime(row['teslim_tarihi'], errors='coerce')
        teslim_suresi = row['teslim_suresi']

        # 1. Eğer siparis_tarihi ve teslim_tarihi varsa, teslim_suresi'ni gün farkı olarak hesapla
        if pd.notnull(siparis_tarihi) and pd.notnull(teslim_tarihi) and pd.isnull(teslim_suresi):
            day_difference = (teslim_tarihi - siparis_tarihi).days
            self.df.at[index, 'teslim_suresi'] = day_difference
            print(f"{index} indeksindeki 'teslim_suresi' sütunu gün farkı olarak ayarlandı: {day_difference} gün")

        # 2. Eğer siparis_tarihi ve teslim_suresi varsa, teslim_tarihi'ni hesapla
        elif pd.notnull(siparis_tarihi) and pd.notnull(teslim_suresi) and pd.isnull(teslim_tarihi):
            try:
                days_value = int(str(teslim_suresi).split()[0])  # Eğer teslim_suresi '10 gün' gibi bir formatta ise
                calculated_date = siparis_tarihi + timedelta(days=days_value)
                self.df.at[index, 'teslim_tarihi'] = calculated_date
                print(f"{index} indeksindeki 'teslim_tarihi' sütunu hesaplandı: {calculated_date}")
            except ValueError:
                print(f"{index} indeksinde 'teslim_suresi' sayısal bir değer içermiyor veya yanlış formatta.")

        # 3. Eğer teslim_tarihi ve teslim_suresi varsa, siparis_tarihi'ni hesapla
        elif pd.notnull(teslim_tarihi) and pd.notnull(teslim_suresi) and pd.isnull(siparis_tarihi):
            try:
                days_value = int(str(teslim_suresi).split()[0])  # Eğer teslim_suresi '10 gün' gibi bir formatta ise
                calculated_date = teslim_tarihi - timedelta(days=days_value)
                self.df.at[index, 'siparis_tarihi'] = calculated_date
                print(f"{index} indeksindeki 'siparis_tarihi' sütunu hesaplandı: {calculated_date}")
            except ValueError:
                print(f"{index} indeksinde 'teslim_suresi' sayısal bir değer içermiyor veya yanlış formatta.")

        # 4. Eğer yeterli bilgi yoksa, kullanıcıya bilgi ver
        else:
            print(f"{index} indeksinde yeterli veri yok veya tüm veriler mevcut. İşlem yapılamadı.")

