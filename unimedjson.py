import json
import urllib.request, urllib.parse, urllib.error
import ssl
import pandas as pd
from urllib.error import HTTPError

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
estados = ['Acre','Alagoas','Amapa','Amazonas','Bahia','Ceara','Distrito+Federal','Espirito+Santo','Goias','Maranhao','Mato+Grosso','Mato+Grosso+do+Sul','Minas+Gerais','Para','Paraiba','Parana','Pernambuco','Piaui','Rio+de+Janeiro','Rio+Grande+do+Norte','Rio+Grande+do+Sul','Rondonia','Roraima','Santa+Catarina','Sao+Paulo','Sergipe','Tocantins']

fileInit = open('unimedstarts.txt', 'r')
Line = fileInit.readlines()
continuaEstado = int(Line[0].strip())
for count,estado in enumerate(estados):
    df = None
    if count < continuaEstado:
        continue
    for page in range(1,69):
        try:    
            address = f'https://api.unimed.coop.br/guia-medico/v3/busca/busca-detalhada?bairro=&cidade=&estado={estado}&exclusaoSubst=false&filtro=&pagina={page}&qtdRegistros=399&qualificacao=&rede=&servico=&urgencia=false&ip=2804:2dc8:103:200:189e:2cb2:2db0:8'
            print(estado," +",page)
            url = urllib.request.urlopen(address, context=ctx)
            data = url.read()
            info = json.loads(data)
            if df is None:
                df = pd.json_normalize(info,record_path =['prestadores'])
            else:
                df = pd.concat([df,pd.json_normalize(info,record_path =['prestadores'])],ignore_index=True)
        except json.decoder.JSONDecodeError:
            print('jsondecodeerror')
            break
        except HTTPError as e:
            print(e) 
        df.to_csv(f'dataunimed/unimed{estado}.csv')
        file = open('unimedstarts.txt', 'w')
        file.writelines(str(count))
        file.close()