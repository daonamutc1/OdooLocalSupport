import os.path
from psycopg2 import sql
import io

from odoo import SUPERUSER_ID, api
from odoo.tools import misc, pycompat
from odoo import api, tools
from odoo.tools.misc import file_open

from . import models


def _import_sem_keyword_ads_historical_metrics_csv(env):
    fname = misc.file_path(os.path.join('viin_mkp_support', 'data',
                                        'sem.keyword.ads.historical.metrics.csv'))
    with file_open(fname, mode='rb') as fp:
        reader = pycompat.csv_reader(io.BytesIO(fp.read()), quotechar='"', delimiter=',')
        columns = next(reader)
        list_index_ref = []
        list_index_ref.append(columns.index('keyword_id'))
        list_index_ref.append(columns.index('country_id'))
        list_index_ref.append(columns.index('language_id'))
        list_index_ref.append(columns.index('currency_id'))
        datas = []
        for row in reader:
            for index in list_index_ref:
                row[index] = env.ref(row[index]).id
            datas.append(tuple(row))

        if datas:
            for small_batch in env['to.base'].splittor(datas, 10000):
                query = sql.SQL("INSERT INTO {} ({}) VALUES {}").format(
                    sql.Identifier('sem_keyword_ads_historical_metrics'),
                    sql.SQL(", ").join(sql.Identifier(name) for name in columns),
                    sql.SQL(", ".join([str(row).replace('None', 'Null') for row in small_batch])),
                )
            env.cr.execute(query)


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # active VietNam
    tools.convert_file(env.cr, 'viin_mkp_support', 'data/sem.keyword.csv', None,
                       mode='init', noupdate=True, kind='init')
    # _import_sem_keyword_ads_historical_metrics_csv(env)


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # active VietNam
    lang = env.ref('base.lang_vi_VN')
    env.ref('base.lang_vi_VN')._activate_lang(lang.code)
    mods = env['ir.module.module'].search([('state', '=', 'installed')])
    mods._update_translations(lang.code, True)
    env.cr.execute('ANALYZE ir_translation')
