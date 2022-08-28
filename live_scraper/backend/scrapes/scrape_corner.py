import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sqlalchemy
import pandas as pd
import numpy as np
from time import sleep
import datetime
from typing import List, Dict
import requests
import pytz
import json
from httplib2 import Http
from simplejson import JSONDecodeError
from apscheduler.schedulers.blocking import BlockingScheduler

category_id_and_name = [
    ['C_538', 'Frutas e verduras'],  # desbloq
    # ['C_520', 'Mercearia'],
    # ['C_512', 'Laticínios e ovos'],
    # ['C_526', 'Lar'],
    # ['C_518', 'Doces, petiscos e biscoitos'],
    # ['C_514', 'Bebidas não alcoólicas'],
    # ['C_527', 'Perfumaria e beleza'],
    # ['C_530', 'Congelados'],  # desbloq
    # ['C_46', 'Pães e massas'],
    # ['C_519', 'Massas'],
    # ['C_521', 'Enlatados e conservas'],
    # ['C_16', 'Aves'],  # desbloq
    # ['C_20', 'Linguiça, salsichas e bacon'],  # desbloq
    # ['C_515', 'Bebidas alcoólicas'],
    # ['C_17', 'Carnes vermelhas'],  # desbloq
    # ['C_517', 'Bebês'],
    # ['C_523', 'Café da manhã'],
    # ['C_636', 'Cozinha'],
    # ['C_1618', 'Frios'],  # desbloq
    # ['C_15', 'Peixes e mariscos'],  # desbloq
    # ['C_126', 'Cães'],
    # ['C_606', 'Mesa'],
    # ['C_124', 'Gatos'],
    # ['C_580', 'Saúde'],
    # ['C_509', 'Pratos prontos'],
    # ['C_537', 'Alimentação saudável'],
    # ['C_1636', 'Substitutos de carne'],
    # ['C_806', 'Natal'],
    ['C_535', 'A granel'],
]

# Ja existem: [33787, 14824, 15725] / geo_id[5, 4, 1]
market_pack = {'data': {
    'market_id': [33787, 33789, ],  # 33792, 33560, 14824, 37691, 17938, 14822, 15725, 14823],
    'market': ['corner_assai_sp_os', 'corner_assai_spsp_zo_barra_funda', ],
    # 'corner_assai_spsp_zo_carapicuiba', 'corner_atacadao_spsp_zo_carapicuiba',
    # 'corner_atacadao_sp_os', 'corner_atacadao_sp_os_2',
    # 'corner_atacadao_spsp_zl_aricanduva', 'corner_atacadao_spsp_zl_itaquera',
    # 'corner_atacadao_spsp_zl_sm', 'corner_atacadao_spsp_zl_vjacui'],
    'geo_id': [5, 11, ],  # 12, 13, 4, 14, 15, 16, 1, 17]
}
}


# df_x = pd.DataFrame(market_pack['data'])
# print(df_x[df_x['market'].str.split('_').str[1]=='atacadao'])


def request_api(ids_list: List[int], market: List[str], geo_id: List[int]):  # , marketss, markets
    corner_list = []
    for ids in category_id_and_name:  # range [0:2] list, cada num inteiro adicionado corresponde a uma categoria extra
        # time.sleep(0.1)
        for values in range(0, len(market_pack['data']['market_id'][0:])):  # qtd de mercados ['market_id'][0:2]
            url = f'https://cornershopapp.com/api/v2/branches/{ids_list[values]}/aisles/{ids[0]}/products'
            # markets = markets[values]
            # essa poderia ser uma segunda func q retornava "requests.get(url).json()"
            try:
                for prod in requests.get(url).json():
                    time.sleep(0.02)

                    # marketss = marketss[values]
                    # dict[values] qd entra aqui abre em valores, qd o valor está acima ou itera duas vezes "market = m"
                    # ou quebra a lista antes de iterar sobre ela
                    try:
                        product_id = prod['id']
                    except (AttributeError, TypeError):
                        product_id = 'None'

                    try:
                        brand = prod['brand']['name']
                    except (AttributeError, TypeError):
                        brand = 'None'

                    try:
                        description = prod['description'].replace('NaN', '')
                    except (AttributeError, TypeError):
                        description = 'None'

                    try:
                        price = prod['original_price'].replace('NaN', '')
                    except (AttributeError, TypeError):
                        price = None

                    try:
                        batch_sections = prod['description_sections'][0]['title']  # [0].replace('NaN', '')
                        # print(batch_sections)
                    except (AttributeError, TypeError, IndexError):
                        batch_sections = None

                    try:
                        batch_type = prod['description_sections'][0]['type']
                        # print(batch_type)
                    except (AttributeError, TypeError, IndexError):
                        batch_type = 'None'

                    try:
                        discount = prod['label'].replace('NaN', '').upper().strip()
                    except (AttributeError, TypeError):
                        discount = None

                    batch_title = ''
                    batch_text = ''
                    try:
                        if 'DELIVERY' in batch_type.upper() or 'DISCOUNT' in batch_type.upper() \
                                and 'VER PROMO' in discount:

                            try:
                                batch_title = prod['description_sections'][0]['title']
                            except (AttributeError, TypeError, IndexError):
                                batch_title = None

                            try:
                                batch_text = prod['description_sections'][0]['text']
                            except (AttributeError, TypeError, IndexError):
                                batch_text = None
                    except:
                        continue

                    products = {
                        'section': ids[1],
                        'product_id': product_id,
                        'product_name': prod['name'],
                        'product_brand': brand,
                        'unit': prod['buy_unit'],
                        'default_buy_unit': prod['default_buy_unit'],
                        'price': price,
                        'price_offer': prod['price'],
                        'discount': discount,
                        'product_price_per_unit': prod['price_per_unit'],
                        'product_desc': description,
                        'availability': prod['purchasable'],
                        'package': prod['package'],
                        'img_url': prod['img_url'],
                        'batch_sections': batch_sections,
                        'batch_title': batch_title,
                        'batch_text': batch_text,
                        'batch_type': batch_type,
                        'market': market[values],
                        'geo_id': geo_id[values]

                    }

                    corner_list.append(products)
            # JSONDecodeError
            except JSONDecodeError:
                continue
    return corner_list


# """""
def create_df() -> pd.DataFrame:
    # defining the function
    corner_data = request_api(ids_list=market_pack['data']['market_id'], market=market_pack['data']['market'],
                              geo_id=market_pack['data']['geo_id'])

    df = pd.DataFrame(corner_data)
    df = df.drop_duplicates(subset=['product_id', 'geo_id'])
    try:
        df['price_'] = df['price']
    except:
        df['price_'] = '0'

    df['price'] = np.where(df['price_offer'].fillna(0).astype('float') > df['price'].fillna(0).astype('float'),
                           df['price_offer'], df['price'])

    df['price_offer'] = np.where(
        df['price_offer'].fillna(0).astype('float') < df['price_'].fillna(0).astype('float'),
        df['price_offer'].astype('float'), 0)

    var_prod = r' PRODUTOS | PRODUTO '
    var_unit = r' UNIDADE | UNIDADES '

    # Essa funcao pega o texto da coluna 'batch_text' e "explode" separando para o lado esquerdo a "batch_buying"
    # e na direita a "batch_offer" se str[index] == 1, tbm remove texto e espaco, mantem apenas float

    # ex: 10,99 -> explode -> lista[0] = 10 e lista[1] = 99 -> 10.99
    def f_batch_format(col: str, index: int) -> np.ndarray:
        # verificar se quebra assim
        # df[col].astype('string').str.upper().str.split(var_prod).astype('string').str[index].str.replace(', ', '')
        # old -> df[col].str.upper().str.split(var_prod).str[index].str.replace(', ', '')
        try:
            formats = df[col].str.upper().str.split(var_prod).str[index].str.replace(', ', ''). \
                str.replace('.', '', regex=True).str.replace(',', '.').str.replace('[^0-9.]', '', regex=True)
        except:
            formats = None
        try:
            setter = np.where(formats.str.strip().str.len() > 0, formats, '0').astype('float')
        except AttributeError:
            setter = 0
        return setter

    # A func acha valores unidades/produtos e converte para UN/REAIS para saber o retorno da coluna "batch_unit"
    # Se der algum erro de NA preencher o "fillna('')" com novas infos
    def f_batch_unit(col: str, index: int, col2: str) -> pd.Series:
        setter = np.where(
            df[col].astype('string').str.upper().str.findall(var_unit).str[index].astype(
                'string').str.strip().fillna('')
            == ('UNIDADES' or 'UNIDADE' and df[col2] == 'DISCOUNT'),
            df[col].astype('string').str.upper().astype('string').str.findall(var_unit).str[index].astype(
                'string').str.strip().fillna(''),

            np.where(
                df[col2] == 'DISCOUNT',
                df[col].astype('string').str.upper().str.findall(var_prod).str[
                    index].astype('string').str.strip().fillna('')
                , ''
            )
        )
        df[col] = setter  # Metodologia pra evitar problemas de numpy array
        df[col] = df[col].str.replace('UNIDADES', 'UN').str.replace('PRODUTOS', 'REAIS')
        return df[col]

    df['batch_buying'] = f_batch_format(col='batch_text', index=0)
    df['batch_offer'] = f_batch_format(col='batch_text', index=1)
    df['batch_unit'] = f_batch_unit(col='batch_text', index=0, col2='batch_type')

    for cols in ['price', 'price_offer']:
        df[cols] = df[cols].astype('float')

    df['batch_info'] = df['batch_title']
    df = df.drop(['price_', 'batch_sections', 'batch_title', 'batch_text'], axis=1)

    # func pode ser substituida por for c/ df[var] = df[var].str[:49], onde var=col
    def f_limit(var):
        limiter = np.where(df[var].str.strip().str.len() <= 49, df[var], df[var].str[:49])
        return limiter

    for cols in ['batch_info']:
        df[cols] = f_limit(var=cols)

    sql_format = '%Y-%m-%d %H:%M:%S'
    add_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).strftime(sql_format)
    df['scrape_date'] = add_date

    #  df['mkt_pid'] = df['market'] + df['product_id'].astype('string')

    df = df.sort_values(['product_id'], ascending=[True])

    df = df.replace(np.nan, 'None').astype('string')
    return df


ScrapeCorner = create_df().to_dict('records')

# data1 = data_t3.scraper_t3()

# data1 = dict('{' + 'request' + ':'f'{data_t3.scraper_t3()}' + '}')
# print(data1)

# dictss = {'request': [{'id': 1191407, 'availability_status': 'AVAILABLE', 'price': None, 'brand': 'Intimus'}, {'id': 1265903, 'availability_status': 'AVAILABLE', 'price': None, 'brand': 'Intimus'}]}
#
# for x in dictss['request']:
#     print(x)

# dicts = {'abc': 123, 'axl': 'pi'}
#
# print(dicts['axl'])

# <!--<p style='margin-bottom:2px;'>campo: <b>{{ items }} {{ items }}</b></p>-->
