
### Kodda Kullanılan Tüm Parçaların Detaylı Açıklaması

#### **1. Kullanılan Kütüphaneler ve Modüller**
1. **`streamlit`**:  
   - **Nedir?** Python ile kullanıcı arayüzü oluşturmak için kullanılan bir kütüphane.  
   - **Hangi Durumlarda Kullanılır?** Web tabanlı veri görselleştirme ve kullanıcıdan veri almak için.  
   - **Bu Kodda Kullanımı:** API anahtarı girişini almak, soru sormak, yanıt göstermek ve Spinner ile işlem durumunu bildirmek için.

2. **`langchain_groq.ChatGroq`**:  
   - **Nedir?** Groq API üzerinden dil modeli oluşturmayı sağlayan bir sınıf.  
   - **Hangi Durumlarda Kullanılır?** Google Gemma 2 gibi dil modellerini çalıştırmak için.  
   - **Bu Kodda Kullanımı:** Groq API üzerinden soruları yanıtlamak için kullanılmış.

3. **`langchain.chains.LLMMathChain`**:  
   - **Nedir?** Matematik işlemlerini dil modeli yardımıyla çözen bir zincirleme fonksiyon.  
   - **Hangi Durumlarda Kullanılır?** Karmaşık matematik problemlerini çözmek için.  
   - **Bu Kodda Kullanımı:** Matematiksel ifadeleri çözmek ve yanıt döndürmek için kullanılmış.

4. **`langchain.prompts.PromptTemplate`**:  
   - **Nedir?** Dinamik istemler oluşturmak için kullanılan bir sınıf.  
   - **Hangi Durumlarda Kullanılır?** Kullanıcı girdisine uygun sorular oluşturmak ve bağlama göre yanıt üretmek için.  
   - **Bu Kodda Kullanımı:** Matematik sorularını mantıksal bir şekilde çözmek için bir istem şablonu tanımlanmış.

5. **`langchain.agents.Tool`**:  
   - **Nedir?** Belirli bir görevi gerçekleştiren işlevleri temsil eden bir yapı.  
   - **Hangi Durumlarda Kullanılır?** Wikipedia’dan veri alma, matematik çözümü veya mantık işlemleri gibi görevleri tanımlamak için.  
   - **Bu Kodda Kullanımı:** Matematik çözümü için bir **Calculator Tool** ve Wikipedia’dan veri almak için **Wikipedia Tool** tanımlanmış.

6. **`langchain.agents.initialize_agent`**:  
   - **Nedir?** Farklı araçları birleştirerek bir yapay zeka ajanı oluşturur.  
   - **Hangi Durumlarda Kullanılır?** Dil modeli ile birden fazla aracı entegre ederek sorulara yanıt oluşturmak için.  
   - **Bu Kodda Kullanımı:** Wikipedia, matematik ve mantık araçlarını birleştirerek bir asistan ajan oluşturmak için kullanılmış.

---

#### **2. Kodun Her Parçası ve Detaylı Açıklamaları**

##### **a) Uygulamanın Yapılandırılması**
```python
st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant", page_icon="🧮")
st.title("Text To Math Problem Solver Using Google Gemma 2")
```
- **Amaç:** Uygulamanın başlığını ve ikonunu ayarlayarak başlangıç yapılandırmasını oluşturur.
- **Parametreler:**
  - **`page_title`**: Sayfanın başlığı.
  - **`page_icon`**: Sayfa için bir emoji ikonu tanımlar.
- **Alternatifler:** **`layout='wide'`** parametresiyle daha geniş bir kullanıcı arayüzü sağlanabilir.

---

##### **b) Groq API Anahtarı Kontrolü**
```python
groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")
if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()
```
- **Amaç:** Kullanıcıdan API anahtarı almak ve eksikse uygulamayı durdurmak.
- **Fonksiyonlar:**
  - **`st.sidebar.text_input`**: Yan çubukta bir giriş alanı oluşturur.
  - **`st.stop`**: Anahtar eksikse uygulamayı durdurur.
- **Parametreler:**
  - **`type="password"`**: Giriş verisini gizler.

---

##### **c) Groq Modelinin Başlatılması**
```python
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
```
- **Amaç:** Google Gemma 2 modelini başlatır.
- **Parametreler:**
  - **`model`**: Kullanılacak modelin adı.  
  - **`groq_api_key`**: API erişimi için gerekli anahtar.

---

##### **d) Wikipedia Arama Aracı**
```python
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find the various information on the topics mentioned"
)
```
- **Amaç:** Wikipedia’dan veri almak için bir araç oluşturur.
- **Fonksiyonlar:**
  - **`Tool`**: Wikipedia verilerini işleyen işlevi bir araç olarak tanımlar.
- **Parametreler:**
  - **`name`**: Aracın adı.
  - **`func`**: Çalıştırılacak işlev.
  - **`description`**: Aracın ne yaptığını açıklar.

---

##### **e) Matematik Çözme Aracı (Calculator Tool)**
```python
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math related questions. Only input mathematical expression needs to be provided"
)
```
- **Amaç:** Matematiksel ifadeleri çözmek için bir araç oluşturur.
- **Fonksiyonlar ve Parametreleri ve Default Degerleri:**

- **`LLMMathChain.from_llm`**: LLM tabanlı bir matematik zinciri oluşturur.
    - **`llm`**: Matematik zincirini çalıştırmak için kullanılan dil modeli.

- **`Tool()`**: fonksiyonu, LangChain'de belirli işlevleri veya araçları tanımlamak için kullanılır. Bu araçlar, bir dil modeli ajanı tarafından kullanılabilir ve farklı görevleri yerine getirmek için işlevsellik sağlar.
    - **`name="Calculator"`**: Aracın adı, "Calculator".  
    - **`func=math_chain.run`**: Matematiksel işlemleri gerçekleştiren işlev.  
    - **`description`**: Aracın matematik sorularına yanıt vereceğini açıklar.  
    - **`return_direct=True`**: Aracın çıktısı, dil modeli tarafından daha fazla işlenmeden doğrudan kullanıcıya sunulur.

---

##### **f) Mantık Soruları ve İstem Zinciri**
```python
prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)
chain = LLMChain(llm=llm, prompt=prompt_template)
reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)
```
- **Amaç:** Kullanıcıdan gelen mantık sorularını çözmek için bir zincir oluşturur.
- **Fonksiyonlar:**
  - **`PromptTemplate`**: Kullanıcıdan gelen girdilere dayalı bir istem oluşturur.
  - **`LLMChain`**: Mantıksal soruları çözmek için istem şablonunu kullanır.

---

### Kod Parçası: **`initialize_agent`**

```python
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)
```

**Amaç:** Bir dil modeli ajanı oluşturur ve araçları kullanarak gelen sorulara yanıt verir. Wikipedia’dan veri alma, matematik işlemleri çözme ve mantıksal soruları yanıtlama gibi görevleri üstlenir.

**Parametreler:**
- **`tools`**: Ajanın kullanacağı araçların listesi. Burada `wikipedia_tool` (Wikipedia’dan bilgi alır), `calculator` (matematiksel işlemleri çözer), `reasoning_tool` (mantıksal soruları yanıtlar) tanımlanmıştır.
- **`llm`**: Ajanın kullandığı dil modeli. Burada `ChatGroq` ile yapılandırılmıştır.
- **`agent`**: Ajan tipi, `AgentType.ZERO_SHOT_REACT_DESCRIPTION` kullanılmıştır; bu, aracın açıklamalarına dayanarak sorguya yanıt verir.
- **`verbose`**: İşlem adımlarını ekranda gösterir mi? Varsayılan `False`.
- **`handle_parsing_errors`**: Hata durumlarını işler mi? Burada `True`, yani hata yönetimi etkinleştirilmiştir.

**Bu Kodda Kullanımı:** Tanımlanan araçları birleştirir ve bir ajan oluşturur. Ajan, gelen sorulara araçları kullanarak otomatik yanıt üretir. **Akış:** Soru, uygun araca yönlendirilir → İşlem yapılır → Yanıt kullanıcıya döndürülür.

---

#### **3. Kodun Genel Akışı**
1. **Başlangıç Yapılandırması:** Kullanıcıdan Groq API anahtarı alınır.  
2. **Araçların Tanımlanması:** Wikipedia, matematik ve mantık araçları oluşturulur.  
3. **Ajanın Başlatılması:** Tüm araçlar birleştirilerek asistan oluşturulur.  
4. **Kullanıcı Girdisi:** Kullanıcıdan bir soru alınır.  
5. **Yanıt Üretimi:** Girdi, ilgili araca yönlendirilir ve yanıt oluşturulur.  
6. **Sonuç Gösterimi:** Yanıt, Streamlit arayüzünde kullanıcıya sunulur.

---

# DETAYLI FONKSIYONLARIN ACIKALMALARI

### **`Tool()` Fonksiyonunun Parametreleri ve Açıklamaları**

`Tool()` fonksiyonu, LangChain'de belirli işlevleri veya araçları tanımlamak için kullanılır. Bu araçlar, bir dil modeli ajanı tarafından kullanılabilir ve farklı görevleri yerine getirmek için işlevsellik sağlar.

#### **`Tool()` Parametreleri**

1. **`name`** *(Zorunlu)*:
   - **Açıklama**: Aracın adını belirtir.
   - **Ne İşe Yarar?**: Araçlar birden fazla olduğunda, hangi aracın kullanılacağını belirlemek için kullanılır.
   - **Örnek**: `"Calculator"` → Bu araç matematiksel hesaplamalar yapmak için tanımlanır.

2. **`func`** *(Zorunlu)*:
   - **Açıklama**: Aracın çağıracağı işlev (fonksiyon).
   - **Ne İşe Yarar?**: Kullanıcı sorgusuna yanıt oluşturmak için bir işlev tanımlar.
   - **Örnek**: `math_chain.run` → Matematiksel hesaplamaları gerçekleştiren bir zincir işlevi.

3. **`description`** *(Zorunlu)*:
   - **Açıklama**: Aracın ne yaptığını açıklayan bir metin.
   - **Ne İşe Yarar?**: Ajanın hangi durumda bu aracı kullanması gerektiğini belirlemek için bir açıklama sağlar.
   - **Örnek**: `"A tool for answering math-related questions."`

4. **`return_direct`** *(Opsiyonel)*:
   - **Açıklama**: Aracın çıktısının direkt olarak kullanıcıya mı gösterileceğini belirler.
   - **Varsayılan Değer**: `False`
   - **Ne İşe Yarar?**: 
     - **`True`** → Aracın çıktısı işlenmeden direkt döndürülür.
     - **`False`** → Aracın çıktısı, başka işlemlere dahil edilebilir.
   - **Örnek**: 
     - `True` → Basit bir hesaplama sonucu direkt kullanıcıya gösterilir.
     - `False` → Yanıt daha fazla işlenebilir (ör. formatlama).

5. **`args`** *(Opsiyonel)*:
   - **Açıklama**: Aracın işlevine aktarılacak ek parametreler.
   - **Ne İşe Yarar?**: İşlevin dinamik bir şekilde çalışmasını sağlar.
   - **Örnek**: Bir Wikipedia araması sırasında filtreleme gibi ek bilgiler aktarılabilir.

---

#### **Parametrelerin Özet Tablosu**

| **Parametre**      | **Zorunlu mu?** | **Ne İşe Yarar?**                                               | **Varsayılan Değeri** |
|---------------------|-----------------|------------------------------------------------------------------|-----------------------|
| `name`             | Evet           | Aracın adını belirtir.                                          | Yok                   |
| `func`             | Evet           | Aracın çalıştıracağı işlevi tanımlar.                           | Yok                   |
| `description`      | Evet           | Aracın ne yaptığını ve hangi durumda kullanılacağını açıklar.   | Yok                   |
| `return_direct`    | Hayır          | Aracın çıktısının direkt döndürülüp döndürülmeyeceğini belirler. | `False`               |
| `args`             | Hayır          | İşleve aktarılacak ek parametreler.                             | Yok                   |

---

#### **Kodda Kullanımı**

Örnek:
```python
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math-related questions. Only input mathematical expression needs to be provided",
    return_direct=True
)
```

- **`name="Calculator"`**: Aracın adı, "Calculator".  
- **`func=math_chain.run`**: Matematiksel işlemleri gerçekleştiren işlev.  
- **`description`**: Aracın matematik sorularına yanıt vereceğini açıklar.  
- **`return_direct=True`**: Aracın çıktısı, dil modeli tarafından daha fazla işlenmeden doğrudan kullanıcıya sunulur.

---

#### **Alternatif Kullanım Senaryoları**
1. **Wikipedia Aracı**:
   ```python
   wikipedia_tool = Tool(
       name="Wikipedia",
       func=wikipedia_wrapper.run,
       description="Search Wikipedia for user-specified topics."
   )
   ```

2. **Dinamik Arama** (Ek Parametre Kullanımı):
   ```python
   search_tool = Tool(
       name="Dynamic Search",
       func=search_function,
       description="Performs a custom search with user-defined filters.",
       args={"filter": "recent"}
   )
   ```

---

Bu detaylarla, **`Tool()`** fonksiyonunun nasıl çalıştığını, parametrelerin ne işe yaradığını ve kodda nasıl kullanıldığını açıklamış olduk.


# Kod Parçası: **`initialize_agent`**

```python
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)
```

---

### **Amaç**
- Bu kod, bir **LangChain Ajanı** oluşturur. Ajan, tanımlanan araçları kullanarak gelen sorulara yanıt verebilir.
- Bu ajan, Wikipedia’dan veri almak, matematiksel işlemleri çözmek ve mantıksal soruları yanıtlamak için yapılandırılmıştır.

---

# **Fonksiyon: `initialize_agent`**

- **Nedir?**
  - `initialize_agent` fonksiyonu, bir veya birden fazla aracı (tools) birleştirerek bir yapay zeka ajanı oluşturur.
- **Hangi Durumlarda Kullanılır?**
  - Dil modellerinin belirli görevler için özelleştirilmiş araçlarla çalışmasını sağlamak için kullanılır. Örneğin:
    - Veri arama
    - Matematiksel hesaplama
    - Mantıksal çıkarımlar
- **Kullanım Alanı:** Araçların topluca kullanılacağı bir yapı oluşturur ve dil modelini bu araçlarla entegre eder.

---

### **Parametreler ve Varsayılan Değerler**

1. **`tools`** *(Zorunlu)*:  
   - **Açıklama**: Ajanın kullanacağı araçların bir listesi.  
   - **Bu Kodda Kullanımı**:  
     - **`wikipedia_tool`**: Wikipedia’dan bilgi alır.  
     - **`calculator`**: Matematiksel işlemleri gerçekleştirir.  
     - **`reasoning_tool`**: Mantıksal ve neden-sonuç ilişkisine dayalı soruları yanıtlar.

2. **`llm`** *(Zorunlu)*:  
   - **Açıklama**: Ajanın kullandığı dil modeli.  
   - **Bu Kodda Kullanımı**:  
     - **`llm=llm`**: `ChatGroq` modeliyle yapılandırılmıştır (Google Gemma 2 modeli).

3. **`agent`** *(Zorunlu)*:  
   - **Açıklama**: Kullanılacak ajan tipi.  
   - **Seçenekler**:  
     - **`ZERO_SHOT_REACT_DESCRIPTION`**: Aracın açıklamalarını kullanarak otomatik yanıt üretir.  
     - **`CONVERSATIONAL_REACT_DESCRIPTION`**: Daha diyalog odaklı bir ajan oluşturur.
   - **Bu Kodda Kullanımı**:  
     - **`ZERO_SHOT_REACT_DESCRIPTION`** → Kullanıcıdan gelen sorgular için tanımlanan araçlara dayanarak hemen yanıt üretir.

4. **`verbose`** *(Opsiyonel, Varsayılan: `False`)*:  
   - **Açıklama**: Ajanın çalışma sürecini ekranda ayrıntılı olarak gösterip göstermeyeceğini belirler.  
   - **Bu Kodda Kullanımı**: `False` olarak ayarlanmış, yani işlem adımları kullanıcıya gösterilmez.

5. **`handle_parsing_errors`** *(Opsiyonel, Varsayılan: `False`)*:  
   - **Açıklama**: Yanıt oluşturma sırasında meydana gelebilecek hata durumlarını yönetir.  
   - **Seçenekler**:  
     - **`True`**: Hatalar işlenir ve ajan yanıt üretmeye devam eder.  
     - **`False`**: Hata durumunda işlem kesilir.  
   - **Bu Kodda Kullanımı**: `True` olarak ayarlanmış, yani hata yönetimi etkinleştirilmiştir.

---

### **Bu Kodda Kullanımı**
1. **Araç Listesi (`tools`)**:
   - Wikipedia’dan veri almak, matematiksel işlemleri çözmek ve mantık tabanlı soruları yanıtlamak için üç araç tanımlanmıştır.
   
2. **Dil Modeli (`llm`)**:
   - Google Gemma 2 modeli kullanılmıştır. Bu model, araçlardan gelen girdileri işleyerek nihai yanıtları üretir.

3. **Ajan Tipi (`agent`)**:
   - **`ZERO_SHOT_REACT_DESCRIPTION`** → Herhangi bir ön bilgi olmadan araç açıklamalarını kullanarak sorulara yanıt verir.

4. **Hata Yönetimi (`handle_parsing_errors`)**:
   - Hatalar işlenir ve sistemin çalışmaya devam etmesi sağlanır.

---

### **Kodun Çalışma Akışı**
1. **Araçların Tanımlanması**:
   - **`wikipedia_tool`**: Wikipedia’dan bilgi almak için çalışır.
   - **`calculator`**: Matematiksel işlemleri çözmek için çalışır.
   - **`reasoning_tool`**: Mantık ve neden-sonuç ilişkisine dayalı soruları yanıtlar.

2. **Ajanın Başlatılması**:
   - Araçlar, dil modeliyle birleştirilir ve bir ajan oluşturulur.
   - Ajan, her sorguya uygun aracı seçerek yanıt oluşturur.

3. **Yanıt Oluşturma**:
   - Kullanıcıdan gelen sorgular, önce uygun araçlara yönlendirilir.
   - Araçlar, gerekli işlemleri yaparak sonucu ajan üzerinden döndürür. 

---

### **Alternatif Kullanım Senaryoları**
- **`agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION`** → Daha diyalog odaklı bir ajan oluşturulabilir.  
- **`verbose=True`** → İşlem adımları kullanıcıya gösterilebilir.  
- **Farklı Araçlar Eklemek**: Örneğin, bir `WebSearchTool` veya `FileReaderTool` aracı eklenerek yetenekler genişletilebilir.



# Session State

#### **Kod Parçası: Chat Oturumunun Başlatılması**

```python
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer all your math questions."}
    ]
```

**Amaç:** Streamlit uygulamasında oturum durumunu başlatır ve önceki mesajları saklar. Eğer oturumda daha önce bir mesaj yoksa, varsayılan bir karşılama mesajı ekler.

**Fonksiyonlar ve Parametreler:**
- **`st.session_state`**: Streamlit'in oturum durumlarını yönetmek için kullanılan yapısı.
- **`messages`**: Mesajları tutmak için kullanılan anahtar.  
- **`role`**: Mesajın kimden geldiğini belirler (`assistant` veya `user`).  
- **`content`**: Mesajın içeriği.

**Bu Kodda Kullanımı:** Kullanıcının ve asistanın mesaj geçmişini saklar. Bu sayede sohbet geçmişi korunur.

---

#### **Kod Parçası: Mesajların Gösterimi**

```python
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])
```

**Amaç:** Kullanıcının ve asistanın tüm mesajlarını sırayla ekrana yazdırır.

**Fonksiyonlar:**
- **`st.chat_message`**: Mesajın rolüne göre (`user` veya `assistant`) bir sohbet balonu oluşturur.
- **`write`**: Mesajın içeriğini ekrana yazar.

**Bu Kodda Kullanımı:** Mesaj geçmişini kullanıcıya göstermek için.

---

#### **Kod Parçası: Kullanıcı Sorusunun Alınması**

```python
question = st.text_area(
    "Enter your question:",
    "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. "
    "Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?"
)
```

**Amaç:** Kullanıcıdan bir soru almak için bir metin alanı oluşturur.

**Fonksiyonlar ve Parametreler:**
- **`st.text_area`**: Kullanıcıdan çok satırlı bir metin girdisi almak için kullanılır.
  - **`label`**: Metin alanının başlığı.
  - **`value`**: Metin alanına varsayılan olarak yazılan içerik.

**Bu Kodda Kullanımı:** Kullanıcı sorusunu alır ve işlemi başlatmak için hazırlar.

---

#### **Kod Parçası: Sorunun İşlenmesi ve Yanıt Üretilmesi**

```python
if st.button("Find my answer"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistant_agent.run(st.session_state.messages, callbacks=[st_cb])

            st.session_state.messages.append({'role': 'assistant', "content": response})
            st.write('### Response:')
            st.success(response)
    else:
        st.warning("Please enter the question.")
```

**Amaç:** Kullanıcıdan gelen soruyu alır, yanıtı üretir ve sonucu kullanıcıya gösterir.

**Fonksiyonlar ve Parametreler:**

1. **`st.button("Find my answer")`**:
   - Kullanıcı bir soruyu yanıtlamak istediğinde tıklayabileceği bir buton oluşturur.

2. **`st.spinner("Generating response...")`**:
   - Yanıt oluşturulurken bir yüklenme animasyonu gösterir.

3. **`st.session_state.messages.append({"role": "user", "content": question})`**:
   - Kullanıcının sorusunu mesaj geçmişine ekler.

4. **`st.chat_message("user").write(question)`**:
   - Kullanıcının mesajını ekrana yazar.

5. **`assistant_agent.run(st.session_state.messages, callbacks=[st_cb])`**:
   - **`assistant_agent`**: Daha önce tanımlanan yapay zeka ajanıdır.
   - **`run()`**: Mesaj geçmişine dayanarak uygun araçları kullanır ve yanıt üretir.
   - **`callbacks=[st_cb]`**: Yanıt üretim sürecini görselleştirmek için geri çağırma işlevi eklenir.

6. **`st.success(response)`**:
   - Üretilen yanıtı başarı mesajı olarak gösterir.

---

### **Kodun Genel Akışı**

1. **Oturum Başlatma:** Eğer mesaj geçmişi yoksa, asistanın varsayılan mesajı oluşturulur.
2. **Mesajların Gösterimi:** Kullanıcı ve asistanın önceki mesajları ekrana yazdırılır.
3. **Soru Alma:** Kullanıcı bir soru yazar ve butona tıklar.
4. **Yanıt Üretme:**
   - Kullanıcının sorusu oturum geçmişine eklenir.
   - Soru uygun araca yönlendirilir ve yanıt üretilir.
   - Yanıt oturum geçmişine eklenir ve kullanıcıya gösterilir.
5. **Hata Durumu:** Kullanıcı herhangi bir soru yazmazsa, uyarı mesajı görüntülenir.