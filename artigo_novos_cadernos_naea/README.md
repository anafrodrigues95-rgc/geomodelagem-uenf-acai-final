# Artigo: açaí no Baixo Tocantins (Novos Cadernos NAEA)

Código, dados processados e resultados do artigo submetido à revista *Novos Cadernos NAEA*.
Esta pasta reúne a versão final do trabalho; as pastas `parte1` a `parte3` do repositório
guardam a versão original da disciplina de Geomodelagem.

> As chaves de API **nunca** ficam no código. No Colab, guarde-as em *Segredos* (ícone de chave):
> `CDS_KEY` (Copernicus) e, se usar, `ROBOFLOW_API_KEY`.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `1_clima/` | Normal climatológica 1991–2020 e anomalias de 2024 do ERA5-Land (`era5land_climatologia.py`), mapas das Figuras 2–4 (`Mapas_artigo_acai_v2.ipynb`) e comparação com as normais do INMET (`comparacao_inmet/`, Figura S1 e Tabela S1) |
| `2_producao/` | Produção de açaí de Belém e do Pará, 2015–2025 (IBGE/SIDRA, PEVS tabela 289 e PAM tabela 1613) |
| `3_yolo/` | Treino e avaliação do YOLO11s-seg (`YOLO11_acai_triatomineos.ipynb` + `acai_yolo_pipeline.py`), download das imagens do iNaturalist, validação cruzada preliminar em CPU, divisão das imagens, anotações e resultados das 5 sementes |
| `figuras/` | Figuras 1–7 do artigo |

## Como reproduzir

1. **Clima:** rode `1_clima/Colab_normal_climatologica_e_imagens.ipynb` (ou `era5land_climatologia.py`) no Colab com `CDS_KEY` nos Segredos. Os mapas saem de `1_clima/Mapas_artigo_acai_v2.ipynb`.
2. **INMET:** em `1_clima/comparacao_inmet/`, rode `python comparar_era5_inmet.py` e depois `python figura_S1.py`. As planilhas das normais 1991–2020 do INMET estão em `inmet/`.
3. **YOLO:** baixe as imagens pelos links de `3_yolo/dados/lista_imagens_links_licencas.xlsx` (as do iNaturalist também podem ser baixadas com `baixar_imagens_inaturalist.py`), junte às anotações de `anotacoes_yolo_labels.zip` e rode `YOLO11_acai_triatomineos.ipynb` no Colab com GPU. A divisão usada no artigo está em `divisao_treino_validacao_teste.json` (semente 42).

Ambiente do treino final: Ultralytics 8.4.182, PyTorch 2.11, GPU Tesla T4 (`3_yolo/resultados/run_metadata.json`).

## Imagens

As imagens **não** estão no repositório, porque pertencem a terceiros. A planilha
`lista_imagens_links_licencas.xlsx` traz, para cada uma das 547 imagens, a origem, o link,
o autor e a licença (iNaturalist: CC0, CC BY ou CC BY-NC). Quem reutilizar as imagens deve
respeitar a licença de cada autor.

## Fontes de dados

- ERA5-Land (Copernicus Climate Data Store), Muñoz-Sabater et al. (2021).
- INMET, Normais Climatológicas do Brasil 1991–2020.
- IBGE, SIDRA: PEVS (tabela 289), PAM (tabela 1613) e malha municipal 2022.
- iNaturalist (observações com grau de pesquisa).
