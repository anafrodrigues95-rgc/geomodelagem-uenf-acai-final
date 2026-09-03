# Trabalho de GeoModelagem e Visão Computacional - Açaí e Barbeiro

Este repositório reúne, de forma consolidada, o trabalho desenvolvido pelos três grupos da disciplina, combinando as melhores contribuições de cada equipe em um único material de análise integrada da produção de açaí no Estado do Pará: geoprocessamento, dados meteorológicos, modelagem espacial e visão computacional.

---

## 🎓 Informações Acadêmicas

* **Instituição:** Universidade Estadual do Norte Fluminense Darcy Ribeiro (UENF)
* **Laboratório:** LAMET – Laboratório de Meteorologia
* **Programa:** Mestrado em Clima e Energia
* **Disciplina:** GeoModelagem do Potencial Energético e do Microclima Urbano
* **Professora:** Dra. Raquel Jahara Lobosco

---

## 👥 Autores e Contribuições

| Autor(es) | Repositório original | Principal contribuição incorporada aqui |
| :--- | :--- | :--- |
| **Ana Flávia Rodrigues Barcelos Cordeiro & Rayane Pereira de Souza** | [`geomodelagem_uenf`](https://github.com/anafrodrigues95-rgc/geomodelagem_uenf) | Base das Partes 1 e 2 (mapas de contexto/uso do solo, dois experimentos YOLO com pasta de resultados), tabela quantitativa da Parte 3, relatório final em PDF e dados brutos Copernicus |
| **Letícia Raquel Trindade Gonçalves & Rafael de Oliveira Menezes** | [`geomodelagem`](https://github.com/LeticiaRaquel/geomodelagem) | Mapas sazonais individuais em alta resolução (Parte 1) e notebook complementar da Parte 3 |
| **Lucas Lopes Assad** | [`UENF_LucasAssad`](https://github.com/lucasassad/UENF_LucasAssad) | Discussão crítica sobre as limitações do caráter exploratório da análise integrada (Parte 3) |

---

## 🗺️ Parte 1 – Mapeamento Climático

* 🚀 [Clique aqui para abrir o Notebook principal da Parte 1 (Mapas_acai.ipynb)](./Mapas_acai.ipynb)
* 🚀 [Clique aqui para abrir a versão alternativa (Parte1GeoModelagem.ipynb)](./Parte1GeoModelagem.ipynb)

Nesta etapa, foram criados os mapas climáticos sazonais do Estado do Pará utilizando a biblioteca **Cartopy** em Python, destacando a principal região produtora de açaí (Igarapé-Miri, Cametá, Abaetetuba e entorno).

### 📍 Área de Estudo e Cobertura da Terra

Abaixo apresenta-se a delimitação da região produtora do Baixo Tocantins em foco e o respectivo mapeamento de uso e cobertura do solo:

<p align="center">
  <a href="Regiao_produtora.jpg">
    <img src="Regiao_produtora.jpg" width="45%" alt="Região Produtora"/>
  </a>
  <a href="Mapa_usoecobertura.jpg">
    <img src="Mapa_usoecobertura.jpg" width="45%" alt="Uso e Cobertura da Terra"/>
  </a>
</p>

* 📁 [Caminho do arquivo: Região Produtora (`Regiao_produtora.jpg`)](Regiao_produtora.jpg)
* 📁 [Caminho do arquivo: Uso e Cobertura do Solo (`Mapa_usoecobertura.jpg`)](Mapa_usoecobertura.jpg)

---

### 🖼️ Painéis Sazonais Consolidados (ERA5-Land 2024)

### 🌧️ Precipitação ou Índice Pluviométrico
<img width="100%" alt="Precipitação 4 Estações" src="https://github.com/user-attachments/assets/8b524ed6-4505-4eaf-992b-6c697917175f" />

### 🌡️ Temperatura do Ar (ºC)
<img width="100%" alt="Temperatura 4 Estações" src="https://github.com/user-attachments/assets/a9596f08-561b-4f80-b523-d4a8de806cff" />

### 💨 Intensidade do Vento (m/s)
<img width="100%" alt="Vento 4 Estações" src="https://github.com/user-attachments/assets/ef97590b-bfe5-4ae7-9c34-0e976b6e4d82" />

### 💧 Umidade (%)
<img width="100%" alt="Umidade 4 Estações" src="https://github.com/user-attachments/assets/c9c8124d-2007-4c37-813e-e7b3db4de977" />

---

### 🎨 Mapas Sazonais Individuais em Alta Resolução

Abaixo estão exibidos separadamente os mapas individuais em alta resolução desenvolvidos para a visualização detalhada de cada variável por estação do ano:

**🌧️ Precipitação**
<p align="center">
  <a href="prec_verao.png"><img src="prec_verao.png" width="45%" alt="Precipitação Verão"/></a>
  <a href="prec_outono.png"><img src="prec_outono.png" width="45%" alt="Precipitação Outono"/></a>
  <br/>
  <a href="prec_inverno.png"><img src="prec_inverno.png" width="45%" alt="Precipitação Inverno"/></a>
  <a href="prec_primavera.png"><img src="prec_primavera.png" width="45%" alt="Precipitação Primavera"/></a>
</p>

* 📁 [Precipitação Verão (`prec_verao.png`)](prec_verao.png)
* 📁 [Precipitação Outono (`prec_outono.png`)](prec_outono.png)
* 📁 [Precipitação Inverno (`prec_inverno.png`)](prec_inverno.png)
* 📁 [Precipitação Primavera (`prec_primavera.png`)](prec_primavera.png)

**🌡️ Temperatura do Ar**
<p align="center">
  <a href="temp_verao.png"><img src="temp_verao.png" width="45%" alt="Temperatura Verão"/></a>
  <a href="temp_outono.png"><img src="temp_outono.png" width="45%" alt="Temperatura Outono"/></a>
  <br/>
  <a href="temp_inverno.png"><img src="temp_inverno.png" width="45%" alt="Temperatura Inverno"/></a>
  <a href="temp_primavera.png"><img src="temp_primavera.png" width="45%" alt="Temperatura Primavera"/></a>
</p>

* 📁 [Temperatura Verão (`temp_verao.png`)](temp_verao.png)
* 📁 [Temperatura Outono (`temp_outono.png`)](temp_outono.png)
* 📁 [Temperatura Inverno (`temp_inverno.png`)](temp_inverno.png)
* 📁 [Temperatura Primavera (`temp_primavera.png`)](temp_primavera.png)

**💨 Vento**
<p align="center">
  <a href="vento_verao.png"><img src="vento_verao.png" width="45%" alt="Vento Verão"/></a>
  <a href="vento_outono.png"><img src="vento_outono.png" width="45%" alt="Vento Outono"/></a>
  <br/>
  <a href="vento_inverno.png"><img src="vento_inverno.png" width="45%" alt="Vento Inverno"/></a>
  <a href="vento_primavera.png"><img src="vento_primavera.png" width="45%" alt="Vento Primavera"/></a>
</p>

* 📁 [Vento Verão (`vento_verao.png`)](vento_verao.png)
* 📁 [Vento Outono (`vento_outono.png`)](vento_outono.png)
* 📁 [Vento Inverno (`vento_inverno.png`)](vento_inverno.png)
* 📁 [Vento Primavera (`vento_primavera.png`)](vento_primavera.png)

**💧 Umidade Relativa**
<p align="center">
  <a href="umidade_verao.png"><img src="umidade_verao.png" width="45%" alt="Umidade Verão"/></a>
  <a href="umidade_outono.png"><img src="umidade_outono.png" width="45%" alt="Umidade Outono"/></a>
  <br/>
  <a href="umidade_inverno.png"><img src="umidade_inverno.png" width="45%" alt="Umidade Inverno"/></a>
  <a href="umidade_primavera.png"><img src="umidade_primavera.png" width="45%" alt="Umidade Primavera"/></a>
</p>

* 📁 [Umidade Verão (`umidade_verao.png`)](umidade_verao.png)
* 📁 [Umidade Outono (`umidade_outono.png`)](umidade_outono.png)
* 📁 [Umidade Inverno (`umidade_inverno.png`)](umidade_inverno.png)
* 📁 [Umidade Primavera (`umidade_primavera.png`)](umidade_primavera.png)

---

## 👁️ Parte 2 – Visão Computacional com YOLO

Aplicação de visão computacional utilizando a biblioteca **YOLO/Ultralytics** para detectar elementos associados à produção de açaí e ao risco sanitário de transmissão oral da Doença de Chagas. O desenvolvimento foi dividido em dois experimentos complementares utilizando modelos de segmentação de instâncias:

### 🟣 Experimento 1: Segmentação de Classe Única (Açaí)
Focado no treinamento da rede para identificação precisa das estruturas do fruto e dos cachos de açaí em condições ideais e ambientes agrícolas.
* **Modelo Utilizado:** YOLO11l-seg (Large)
* 🚀 [Clique aqui para abrir o Notebook do Experimento 1](../parte2_visao_computacional_yolo/experimento1_segmentacao_acai.ipynb)
* 📦 [Dataset utilizado (acai.v1i.yolov11.zip)](../parte2_visao_computacional_yolo/acai.v1i.yolov11.zip)

### 🪲 Experimento 2: Detecção Multiclasse (Açaí + Barbeiro)
Extensão do modelo para um cenário real de triagem fitossanitária, treinado para realizar a detecção simultânea das estruturas do fruto e do inseto vetor (*triatomíneo/barbeiro*) em fundos complexos, aplicando penalização na função de perda para lidar com o desbalanceamento de classes.
* **Modelo Utilizado:** YOLO11m-seg (Medium)
* 🚀 [Clique aqui para abrir o Notebook do Experimento 2](../parte2_visao_computacional_yolo/experimento2_deteccao_acai_barbeiro.ipynb)
* 📦 [Dataset utilizado (acai.v2-barbeiro-e-acai.yolov11.zip)](../parte2_visao_computacional_yolo/acai.v2-barbeiro-e-acai.yolov11.zip)

---

### 🖼️ Resultados Visuais do YOLO

Os arquivos visuais gerados durante o treinamento, validação e as predições finais dos modelos YOLO estão organizados e salvos diretamente no repositório.

* 📁 [Clique aqui para acessar a pasta com os gráficos de treino, matriz de confusão e predições](../parte2_visao_computacional_yolo/resultados)

Nesta pasta você encontrará a evolução das curvas de perda (`results.png`), a matriz de confusão para análise de erros e acertos, e exemplos de imagens de teste com as máscaras de segmentação aplicadas no açaí e no barbeiro.

---

## 📊 Parte 3 – Análise Integrada entre Clima e Produção de Açaí

Abaixo apresenta-se a tabela comparativa correlacionando os dados meteorológicos do Copernicus com os aspectos ecológicos e biológicos observados na região produtora de Igarapé-Miri, Abaetetuba e Cametá.

### 📈 Tabela Comparativa Sazonal (Dados Reais ERA5-Land 2024)

| Estação | Precipitação (mm/dia) | Temperatura (°C) | Umidade (%) | Vento (m/s) | Índice de Produção |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Verão** | 4.48 | 30.06 | 68.22 | 2.03 | Baixo |
| **Outono** | 12.25 | 29.29 | 76.66 | 1.34 | Muito Baixo |
| **Inverno** | 1.31 | 32.54 | 50.11 | 2.00 | Médio |
| **Primavera** | 0.32 | 35.11 | 39.63 | 2.38 | **Alto** |

### 📉 Gráfico de Correlação Sazonal
<img width="100%" alt="Gráfico Clima x Produção" src="https://github.com/user-attachments/assets/36b4c580-171d-473e-9a1a-cc6be94983c0" />

---

### 📓 Notebooks Complementares
* 🚀 [Versão alternativa da análise integrada (parte3_repo.ipynb)](../parte3_analise_integrada/parte3_repo.ipynb)
* 🚀 [Discussão crítica sobre as limitações metodológicas (parte3_discussao_critica.ipynb)](../parte3_analise_integrada/parte3_discussao_critica.ipynb)

> 💡 **Nota sobre a discussão crítica:** Esta discussão aborda o caráter exploratório da análise: as médias climáticas utilizadas são estimativas de reanálise (modelo), não medições de campo, o que limita conclusões causais diretas entre clima e produtividade do açaí.

---

## 📄 Relatório Final

O relatório final detalhado com toda a fundamentação teórica, metodologia e análise aprofundada dos resultados foi gerado em formato PDF e pode ser consultado na documentação do projeto.

👉 [Clique aqui para acessar o Relatório Final Completo (PDF)](../relatorio_final/Ana_Flavia_Rodrigues_e_Rayane_Souza_Relatorio_de_Geomodelagem.pdf)

---

## 📊 Dados Brutos

Os arquivos `.nc` (NetCDF) originais, referentes às variáveis de superfície do ERA5-Land utilizadas no processamento da Parte 1, estão disponibilizados para fins de reprodutibilidade:

* 📁 [Clique aqui para acessar os dados brutos Copernicus](../dados_brutos_copernicus)

---

## 🚀 Como Reproduzir os Códigos

Todos os scripts foram desenvolvidos para serem executados no ambiente virtual do **Google Colab** com suporte a GPU (T4):

1. **Parte 1 (Mapas):** abra o arquivo `Mapas_acai.ipynb` no Colab. Certifique-se de instalar as dependências de geoprocessamento (`pip install cartopy xarray netcdf4 h5netcdf cdsapi`) e configurar o seu token da API do Copernicus no arquivo `.cdsapirc`.
2. **Parte 2 (YOLO):** os notebooks `experimento1_segmentacao_acai.ipynb` e `experimento2_deteccao_acai_barbeiro.ipynb` realizam a instalação automatizada da biblioteca `ultralytics` e o download das imagens via Roboflow. Basta executar as células sequencialmente.
3. **Parte 3 (Análise Integrada):** requer os resultados climáticos da Parte 1 já processados.

---

## 📊 Acesso ao Dataset

O banco de dados contendo as imagens anotadas e as máscaras de segmentação foi estruturado e hospedado publicamente na plataforma **Roboflow**.

Os notebooks da **Parte 2** já contêm a linha de código parametrizada com o ID do projeto para baixar e extrair o dataset automaticamente (`açai-2`) direto para o diretório de treino do modelo, garantindo a perfeita reprodução dos experimentos fitossanitários.

---

*Repositório consolidado a partir dos três trabalhos individuais da turma, reunindo as contribuições mais completas de cada grupo.*
