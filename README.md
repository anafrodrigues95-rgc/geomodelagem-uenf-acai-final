# GeoModelagem do Potencial Energético e do Microclima Urbano
## Análise Integrada: Clima × Produção de Açaí × Visão Computacional (Estado do Pará)

Este repositório reúne, de forma consolidada, os trabalhos desenvolvidos por três grupos da disciplina, combinando as melhores contribuições de cada equipe em um único material para submissão.

## 🎓 Informações Acadêmicas

- **Instituição:** Universidade Estadual do Norte Fluminense Darcy Ribeiro (UENF)
- **Laboratório:** LAMET – Laboratório de Meteorologia
- **Programa:** Mestrado em Clima e Energia
- **Disciplina:** GeoModelagem do Potencial Energético e do Microclima Urbano
- **Professora:** Dra. Raquel Jahara Lobosco

## 👥 Autores e Contribuições

| Autor(es) | Repositório original | Principal contribuição incorporada aqui |
|---|---|---|
| Ana Flávia Rodrigues Barcelos Cordeiro | [geomodelagem_uenf](https://github.com/anafrodrigues95-rgc/geomodelagem_uenf) | Base das Partes 1 e 2 (mapas de contexto/uso do solo, dois experimentos YOLO com pasta de resultados), tabela quantitativa da Parte 3, relatório final em PDF e dados brutos Copernicus |
| Letícia Raquel Trindade Gonçalves| [geomodelagem](https://github.com/leticiagoncalves-ship-it/geomodelagem) | Mapas sazonais individuais em alta resolução (Parte 1) e notebook complementar da Parte 3 |
| Lucas Lopes Assad | [UENF_LucasAssad](https://github.com/lucaslopesassad-bit/UENF_LucasAssad) | Discussão crítica sobre as limitações do caráter exploratório da análise integrada (Parte 3) |

## 📁 Estrutura do Repositório

```
├── parte1_mapeamento_climatico/
│   ├── Mapas_acai.ipynb                          # notebook principal (mapas + contexto da área)
│   ├── Regiao_produtora.jpeg / Mapa_usoecobertura.jpeg
│   ├── Precipitacao_4_estacoes.jpeg, Temperatura_..., Vento_..., Umidade_...
│   ├── Parte1GeoModelagem_repo_leticia_rafael.ipynb   # versão alternativa
│   └── imagens_individuais_alta_res/              # 16 mapas sazonais separados, alta resolução
│
├── parte2_visao_computacional_yolo/
│   ├── experimento1_segmentacao_acai.ipynb        # YOLO11l-seg, classe única
│   ├── experimento2_deteccao_acai_barbeiro.ipynb  # YOLO11m-seg, multiclasse
│   ├── acai.v1i.yolov11.zip / acai.v2-barbeiro-e-acai.yolov11.zip  # datasets
│   └── resultados/                                # curvas de treino, matriz de confusão, predições
│
├── parte3_analise_integrada/
│   ├── grafico_clima_x_indice_de_producao.png     # gráfico com dados reais ERA5-Land 2024
│   ├── parte3_repo_leticia_rafael.ipynb           # versão alternativa da análise
│   └── parte3_discussao_critica_lucas.ipynb       # discussão sobre limitações metodológicas
│
├── relatorio_final/
│   └── Ana Flávia Rodrigues e Rayane Souza - Relatório de Geomodelagem.pdf
│
└── dados_brutos_copernicus/
    └── arquivos .nc (ERA5-Land, variáveis de superfície)
```

## 🗺️ Parte 1 – Mapeamento Climático

Mapas climáticos sazonais do Estado do Pará, com foco na principal região produtora de açaí (Igarapé-Miri, Cametá, Abaetetuba), gerados com `Cartopy` a partir de dados **Copernicus ERA5/ERA5-Land** (2024, 15h).

## 👁️ Parte 2 – Visão Computacional com YOLO

Dois experimentos complementares de segmentação de instâncias:
- **Experimento 1:** segmentação de classe única (estruturas do açaí) — YOLO11l-seg
- **Experimento 2:** detecção multiclasse (açaí + barbeiro/triatomíneo, vetor da Doença de Chagas) — YOLO11m-seg, com penalização para desbalanceamento de classes

## 📊 Parte 3 – Análise Integrada Clima × Produção de Açaí

Tabela comparativa sazonal com dados reais ERA5-Land 2024 (precipitação, temperatura, umidade, vento) correlacionados com o índice de produção de açaí, acompanhada de discussão crítica sobre o caráter exploratório da análise (as médias climáticas são estimativas de reanálise, não medições de campo).

## 🚀 Como Reproduzir

Todos os notebooks foram desenvolvidos para rodar no **Google Colab** com suporte a GPU (T4):

1. **Parte 1:** abrir `Mapas_acai.ipynb`; instalar dependências de geoprocessamento (`pip install cartopy xarray netcdf4 h5netcdf cdsapi`) e configurar o token da API Copernicus (`.cdsapirc`).
2. **Parte 2:** os notebooks já contêm a instalação automatizada de `ultralytics` e download dos datasets via Roboflow.
3. **Parte 3:** requer os resultados da Parte 1 (dados climáticos) já processados.

---

*Repositório consolidado a partir dos três trabalhos individuais da turma, reunindo as contribuições mais completas de cada grupo.*

