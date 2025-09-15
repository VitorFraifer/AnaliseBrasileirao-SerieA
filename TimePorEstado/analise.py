import pandas as pd
import os

caminho_base = os.path.dirname(__file__)

df_partidas = pd.read_csv(os.path.join(caminho_base, 'campeonato-brasileiro-full.csv'))

df_partidas['data'] = pd.to_datetime(df_partidas['data'], dayfirst=True)
df_partidas['temporada'] = df_partidas['data'].dt.year

df_mandante = df_partidas[['temporada', 'mandante', 'mandante_Estado', 'mandante_Placar', 'visitante_Placar']].copy()
df_mandante.rename(columns={'mandante':'time', 'mandante_Estado':'estado', 'mandante_Placar':'placar_time', 'visitante_Placar':'placar_adversario'}, inplace=True)

df_visitante = df_partidas[['temporada', 'visitante', 'visitante_Estado', 'visitante_Placar', 'mandante_Placar']].copy()
df_visitante.rename(columns={'visitante':'time', 'visitante_Estado':'estado', 'visitante_Placar':'placar_time', 'mandante_Placar':'placar_adversario'}, inplace=True)

df_times = pd.concat([df_mandante, df_visitante], ignore_index=True)

def calcular_pontos(row):
    if row['placar_time'] > row['placar_adversario']:
        return 3
    elif row['placar_time'] == row['placar_adversario']:
        return 1
    else:
        return 0

df_times['pontos'] = df_times.apply(calcular_pontos, axis=1)

df_pontos_totais = df_times.groupby(['temporada', 'time', 'estado'], as_index=False)['pontos'].sum()

df_result = df_pontos_totais.groupby(['temporada', 'estado'], as_index=False).agg(
    numero_de_times=('time', 'nunique'),
    times=('time', lambda x: ", ".join(sorted(x))),
    media_pontos=('pontos', 'mean')
)

df_result['media_pontos'] = df_result['media_pontos'].round(2)


df_result.to_csv(os.path.join(caminho_base, 'analise_times_por_estado.csv'), index=False)

print("Arquivo 'analise_times_por_estado.csv' gerado com sucesso!")
print(df_result.head())
