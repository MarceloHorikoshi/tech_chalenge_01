# tech_chalenge_01


## Exemplo de requisições

```py
import requests

url = "http://127.0.0.1:8000/producao/filtragem"
params = {
    'categoria': 'VINHO DE MESA',
    'nome_produto': 'Tinto',
    'ano_producao': [1977, 1978]
}

response = requests.get(url, params=params)

print(response.text)
```