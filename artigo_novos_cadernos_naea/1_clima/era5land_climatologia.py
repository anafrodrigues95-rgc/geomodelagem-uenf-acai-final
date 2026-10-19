"""
ERA5-Land: normal climatológica 1991–2020 (padrão OMM), anomalias de 2024 e estações DJF corretas
(item 5 do parecer técnico).

Pré-requisitos (rodar no Colab ou no computador de vocês):
  pip install "cdsapi>=0.7" xarray netcdf4 pandas
  Criar conta em https://cds.climate.copernicus.eu, aceitar a licença do ERA5-Land
  e salvar a chave em ~/.cdsapirc  (url: https://cds.climate.copernicus.eu/api  key: <sua-chave>)

Saídas (pasta era5_out/):
  climatologia_mensal.csv   normal 1991–2020: média, DP entre anos, mínimo e máximo espacial por mês
  anomalias_2024.csv        2024 menos a climatologia, por mês e por estação
  estacoes.csv              DJF 2023–24, MAM, JJA, SON 2024 (e DJF 2024–25 se baixado 2025)

Notas metodológicas para o texto:
  * Precipitação: no produto mensal do ERA5-Land, 'tp' é a acumulação DIÁRIA MÉDIA do mês, em metros.
    Portanto mm/dia = tp * 1000. (Multiplicar pelo nº de dias do mês dá o total mensal em mm.)
  * Temperatura/umidade/vento são calculados de duas formas: média de todas as horas (caracterização
    climática geral) e média das 18 UTC = 15 h local (estresse térmico vespertino). Use as duas no artigo.
  * Umidade relativa (Magnus): UR = 100 * exp(17.625*Td/(243.04+Td)) / exp(17.625*T/(243.04+T)), T e Td em °C.
  * Comparar a normal ERA5-Land com as Normais Climatológicas 1991–2020 do INMET (estação Belém e outras da região).
  * Validar contra estações INMET (ex.: Belém A201, Cametá A209/ outras disponíveis no BDMEP):
    extrair a célula ERA5-Land mais próxima e calcular viés, RMSE e correlação mensais.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

AREA = [-1.4, -49.8, -2.6, -48.5]          # N, W, S, E  (domínio do artigo)
NORMAL = (1991, 2020)                         # normal climatológica padrão da OMM (30 anos)
YEARS = [str(y) for y in range(1990, 2025)]  # 1990 (dez/1990 p/ DJF 1990–91) até 2024; acrescente "2025" para DJF 2024–25
OUT = Path("era5_out"); OUT.mkdir(exist_ok=True)
VARS = ["2m_temperature", "2m_dewpoint_temperature", "10m_u_component_of_wind",
        "10m_v_component_of_wind", "total_precipitation"]


def download():
    import cdsapi
    c = cdsapi.Client()
    common = dict(variable=VARS, year=YEARS, month=[f"{m:02d}" for m in range(1, 13)],
                  area=AREA, data_format="netcdf", download_format="unarchived")
    if not (OUT / "monthly_allhours.nc").exists():
        c.retrieve("reanalysis-era5-land-monthly-means",
                   dict(product_type=["monthly_averaged_reanalysis"], time=["00:00"], **common),
                   str(OUT / "monthly_allhours.nc"))
    if not (OUT / "monthly_18utc.nc").exists():
        c.retrieve("reanalysis-era5-land-monthly-means",
                   dict(product_type=["monthly_averaged_reanalysis_by_hour_of_day"], time=["18:00"],
                        **{k: v for k, v in common.items() if k != "variable"},
                        variable=VARS[:4]),
                   str(OUT / "monthly_18utc.nc"))


def derive(ds):
    tdim = "valid_time" if "valid_time" in ds.dims else "time"
    ds = ds.rename({tdim: "time"})
    out = xr.Dataset()
    T = ds["t2m"] - 273.15
    Td = ds["d2m"] - 273.15
    out["temp_C"] = T
    out["rh_pct"] = 100 * np.exp(17.625 * Td / (243.04 + Td)) / np.exp(17.625 * T / (243.04 + T))
    out["wind_ms"] = np.hypot(ds["u10"], ds["v10"])
    if "tp" in ds:
        out["precip_mm_day"] = ds["tp"] * 1000.0
    return out.squeeze(drop=True)


def spatial_stats(da):
    dims = [d for d in da.dims if d != "time"]
    return pd.DataFrame({"mean": da.mean(dims).values, "sp_min": da.min(dims).values,
                         "sp_max": da.max(dims).values, "sp_sd": da.std(dims).values},
                        index=pd.to_datetime(da["time"].values))


def season_label(ts):
    m, y = ts.month, ts.year
    if m == 12:
        return f"DJF {y}-{str(y + 1)[-2:]}"
    if m in (1, 2):
        return f"DJF {y - 1}-{str(y)[-2:]}"
    return {3: "MAM", 4: "MAM", 5: "MAM", 6: "JJA", 7: "JJA", 8: "JJA"}.get(m, "SON") + f" {y}"


def main():
    download()
    allh = derive(xr.open_dataset(OUT / "monthly_allhours.nc"))
    h18 = derive(xr.open_dataset(OUT / "monthly_18utc.nc")).rename(
        {"temp_C": "temp_C_15h", "rh_pct": "rh_pct_15h", "wind_ms": "wind_ms_15h"})
    frames = []
    for ds in (allh, h18):
        for v in ds.data_vars:
            s = spatial_stats(ds[v]); s["var"] = v; frames.append(s)
    df = pd.concat(frames).rename_axis("time").reset_index()
    df["year"], df["month"] = df.time.dt.year, df.time.dt.month

    base = df[(df.year >= NORMAL[0]) & (df.year <= NORMAL[1])]
    clim = base.groupby(["var", "month"]).agg(clim_mean=("mean", "mean"), interannual_sd=("mean", "std"),
                                              sp_min=("sp_min", "min"), sp_max=("sp_max", "max")).reset_index()
    clim.to_csv(OUT / "climatologia_mensal.csv", index=False)

    y24 = df[df.year == 2024].merge(clim, on=["var", "month"])
    y24["anomaly"] = y24["mean"] - y24["clim_mean"]
    y24["z"] = y24["anomaly"] / y24["interannual_sd"]
    y24.to_csv(OUT / "anomalias_2024.csv", index=False)

    df["season"] = df.time.apply(season_label)
    keep = ["DJF 2023-24", "MAM 2024", "JJA 2024", "SON 2024", "DJF 2024-25"]
    seas = (df[df.season.isin(keep)].groupby(["season", "var"])
            .agg(n_months=("mean", "size"), mean=("mean", "mean"),
                 sp_min=("sp_min", "min"), sp_max=("sp_max", "max")).reset_index())
    seas = seas[seas.n_months == 3]   # descarta estação incompleta
    seas.to_csv(OUT / "estacoes.csv", index=False)
    print(seas.pivot(index="season", columns="var", values="mean").round(2))


if __name__ == "__main__":
    main()
