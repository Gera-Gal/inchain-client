from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from gql import gql

from .crypto_utilities import *
from .graphql import client

def get_listing(request):
    reference_currency = request.GET.get('reference-currency')
    reference_currency = '' if reference_currency == 'usd' else '&convert=' + reference_currency
    n = int(request.GET.get('n'))
    #json_map_data = read_json_file('cmc_crypto_map.json')['data']
    #json_info_data = read_json_file('cmc_crypto_info.json')['data']
    #json_quotes_data = read_json_file('cmc_crypto_quotes.json')['data']
    import http.client
    import json
    conn = http.client.HTTPSConnection("pro-api.coinmarketcap.com")
    payload = ''
    headers = {
        'X-CMC_PRO_API_KEY': '334b1a1b-d34a-4329-9f79-713dd27e2173'
    }
    conn.request("GET", "/v1/cryptocurrency/map", payload, headers)
    res = conn.getresponse()
    json_map_data = res.read()
    json_map_data = json.loads(json_map_data.decode("utf-8"))['data']
    coins_top_n = [crypto['symbol'] for crypto in json_map_data if crypto['rank'] <= n]
    coins_for_query = ','.join(coins_top_n)
    conn.request("GET", "/v1/cryptocurrency/info?symbol={}".format(coins_for_query), payload, headers)
    res = conn.getresponse()
    json_info_data = res.read()
    json_info_data = json.loads(json_info_data.decode("utf-8"))['data']
    print("/v2/cryptocurrency/quotes/latest?symbol={0}{1}".format(coins_for_query, reference_currency))
    conn.request("GET", "/v2/cryptocurrency/quotes/latest?symbol={0}{1}".format(coins_for_query, reference_currency), payload, headers)
    res = conn.getresponse()
    json_quotes_data = res.read()
    json_quotes_data = json.loads(json_quotes_data.decode("utf-8"))['data']
    return JsonResponse(filter_data_listing(json_map_data, json_info_data, json_quotes_data, n, 'full'), safe=False)

@login_required
def crypto_charts(request):
    return render(request, 'cryptos/crypto_charts.html')

@login_required
def crypto_browser(request):
    if request.method == 'POST':
        context = {}
        category = request.POST.get('category')
        ecosystem = request.POST.get('ecosystem')
        query_string = '''
{{
    allCryptos(category: "{0}", tags_Icontains: "{1}") {{
        edges {{
            node {{
                id
                name
                symbol
                rank
                category
                slug
                logo
                quote
                tags
            }}
        }}
    }}
}}
            '''.format(category, ecosystem)
        query = gql(
            query_string
        )
        response = client.execute(query)['allCryptos']['edges']
        query = []
        for  node in response:
            node['node']['tags'] = node['node']['tags'].split('|')
            query.append(node['node'])
        context['query'] = query
        return render(request, 'cryptos/crypto_browser.html', context=context)
    return render(request, 'cryptos/crypto_browser.html')