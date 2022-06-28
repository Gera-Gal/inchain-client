import csv
import json
import os

class Crypto():
    """
        Allows to account for balances related to given crypto assets

        Attributes
        --------------------
        name : str
            Crypto asset common name
        symbol : str
            Stands for asset ticker
        balance : int
            Asset related balance
    """
    def __init__(self, name, symbol, balance):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError("'name' must be a string")
        if isinstance(symbol, str):
            self.symbol = symbol
        else:
            raise TypeError("'symbol' must be a string")
        if isinstance(balance, int) or isinstance(balance, float):
            self.balance = balance
        else:
            raise TypeError("'total_balance' must be a number")

    def __str__(self):
        """
            Crypto string representation overriding
            Exposes a crypto asset balance
            ** Funny fact: double leading and tralining underscores is called "mangling" **
            ** Intersting fact: mangling allows to override reserved methods, called "dunder methods" **
        """
        return "Asset:\t{}\n\tTicker: {}\n\tBalance: {}".format(
            self.name,
            self.symbol,
            self.balance
            )

    def get_symbol(self):
        """
            Accessory method for getting asset symbol
            Useful for further concatenating symbols in a listing and calling /cryptocurrency/info
        """
        return self.symbol

class User():
    """
        Allows to account for the user balances and total sum of them

        Attributes
        --------------------
        name : str
            user name
        total_balance : int | float
            total sum of crypto asset balances
        crypto_listing : Crypto[]
            list of Users' Crypto assets
    """
    def __init__(self, name, total_balance, crypto_listing):
        self.name = name
        if isinstance(total_balance, int) or isinstance(total_balance, float):
            self.total_balance = total_balance
        else:
            raise TypeError("'total_balance' must be a number")
        if isinstance(crypto_listing, list) and all(isinstance(crypto, Crypto) for crypto in crypto_listing):
            self.crypto_listing = crypto_listing
        else:
            raise TypeError("'crypto_listing' must be a list of Crypto")

    def listing_to_string(self):
        """
            Concatenating symbols in a listing
            Useful for passing result to /cryptocurrency/info
        """
        return ','.join([crypto.get_symbol() for crypto in self.crypto_listing])

    def balances_to_string(self):
        """
            Concatenation of Crypto string representations
        """
        return '\n'.join(["{}".format(crypto) for crypto in self.crypto_listing])

    def __str__(self):
        """
            User string representation overriding
            Exposes user's name, total balance and individual assets balance
        """
        return "Name: {}\n".format(self.name) + \
            "Total balance: {}\n".format(self.total_balance) + \
            "Balance per crypto asset:\n" + \
            self.balances_to_string()

def read_json_file(file_name):
    """
        Accessory function for reading a json file (utf-8)

        return : dict()
            Is inteded for cryptocurrencies data, /map and /info mainly
    """
    file_path = os.path.join(os.getcwd(),'static','files',file_name)
    asset_data_json = {}
    with open(file_path,'r',encoding='utf-8') as json_file:
        asset_data_json = json.load(json_file)
    return asset_data_json

def dump_crypto_to_csv(asset_data_listing, file_name, mode):
    """
        Writes data from a list of dictionaries into a csv file

        Two transformation algorithms were tested:
        1.  Using csv.DictWriter proved to be faster for this particular case.
            Dictionaries must come in format [{key_1: asset_1_value_1}, ..., {key_n: asset_n_value_n}]
            csv headers will be keys() from any dictionary in the list
        2 . Using dataframes from pandas which has greater scalabilty potential, however, performs unnecessary transformations.
            For the case of df's, reading a json file fit orient='split' straight fordward, if 'status' sub dictionary removed
            But providing a list of values() as data and keys() as columns is more flexible

            If {'data': [{key_1: asset_1_value_1}, ..., {key_n: asset_n_value_n}]}
            df = pd.read_json(json_file,orient='split')

            Actual response comes in format {'status':{...}, 'data':{...}}
            data_index_format = {}
            for index, crypto in enumerate(asset_data_dict):
                data_index_format[index]= list(crypto.values())
            df = pd.DataFrame.from_dict(
                data_index_format,
                orient='index',
                columns=list(asset_data_dict[0].keys()))
            df.to_csv(file_name,index=False)

        Speed was privileged over scalability for the actual task

        result : csv file
            Is intended for writing csv files with crypto assets details
    """
    if(mode == 'map' or mode == 'merged'):
        fieldnames = list(asset_data_listing[0].keys())
        with open(file_name, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(asset_data_listing)
    if(mode == 'info'):
        fieldnames = []
        for symbol in asset_data_listing:
            fieldnames = list(asset_data_listing.keys())
            break
        fieldnames.insert(1, 'symbol')
        asset_data_list = []
        for symbol in asset_data_listing:
            asset_data_list.append(dict(asset_data_listing, **{'symbol': symbol}))
        with open(file_name, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(asset_data_list)

def filter_data_listing(crypto_map, crypto_info, crypto_quotes, top_n, mode='', *filters):
    """
        Filters details from a crypto listing

        For 'full' and 'csv' modes, filters will be ignored, then it's faster to calculate top n listing first.
        For 'filter' mode, information will be first merged, then filtered.
    """
    filtered_listing = []
    if(mode == ''):
        raise Exception("'mode' is obligatory")
    if(mode == 'full'):
        """
            Filter the top n of crypto assets (based on rank position).

            Lambda function is used as filter for a pythonic comprehensive implementation
        """
        crypto_map = list(filter(lambda crypto: crypto['rank'] <= top_n, crypto_map))
        """
            Taking advantage of dictionary feature: dictionary unpacking
            "rank" key-value is extracted from
            /cryptocurrency/map response then inserted into
            /cryptocurrency/info response; both actions at once by means of a comprehension list
        """
        map_info_merged_data = {}
        for crypto in crypto_map:
            map_info_merged_data[crypto['symbol']] = dict(crypto_info[crypto['symbol']], **{'rank': crypto['rank']})
        crypto_merged_data = [
            dict(map_info_merged_data[crypto],
            **{
                'quote': crypto_quotes[crypto][0]['quote'],
                'max_supply': crypto_quotes[crypto][0]['max_supply'],
                'circulating_supply': crypto_quotes[crypto][0]['circulating_supply'],
                'total_supply': crypto_quotes[crypto][0]['total_supply']
            })
            for crypto in map_info_merged_data
        ]
        asset_data_filtered = {}
        for asset_data in crypto_merged_data:
            filtered_listing.append(
                {
                    'symbol': asset_data['symbol'],
                    'id': asset_data['id'],
                    'name': asset_data['name'],
                    'rank': asset_data['rank'],
                    'category': asset_data['category'],
                    'description': asset_data['description'],
                    'slug': asset_data['slug'],
                    'logo': asset_data['logo'],
                    'urls': asset_data['urls'],
                    'tags': asset_data['tags'],
                    'contract_address': asset_data['contract_address'],
                    'quote': asset_data['quote'],
                    'max_supply': asset_data['max_supply'],
                    'circulating_supply': asset_data['circulating_supply'],
                    'total_supply': asset_data['total_supply'],
                }
            )
    elif(mode == 'csv'):
        """
            Filter the top n of crypto assets (based on rank position).

            Lambda function is used as filter for a pythonic comprehensive implementation
        """
        crypto_map = list(filter(lambda crypto: crypto['rank'] <= top_n, crypto_map))
        """
            Taking advantage of dictionary feature: dictionary unpacking
            "rank" key-value is extracted from
            /cryptocurrency/map response then inserted into
            /cryptocurrency/info response both actions at once by means of a comprehension list
            As crypto map is shorter, is iterated in order to prune crypto info
        """
        map_info_merged_data = {}
        for crypto in crypto_map:
            map_info_merged_data[crypto['symbol']] = dict(crypto_info[crypto['symbol']], **{'rank': crypto['rank']})
        crypto_merged_data = [
            dict(map_info_merged_data[crypto],
            **{
                'quote': crypto_quotes[crypto][0]['quote'],
                'max_supply': crypto_quotes[crypto][0]['max_supply'],
                'circulating_supply': crypto_quotes[crypto][0]['circulating_supply'],
                'total_supply': crypto_quotes[crypto][0]['total_supply']
            })
            for crypto in map_info_merged_data
        ]
        for asset_data in crypto_merged_data:
            filtered_listing.append(
                {
                    'symbol': asset_data['symbol'],
                    'id': asset_data['id'],
                    'name': asset_data['name'],
                    'rank': asset_data['rank'],
                    'category': asset_data['category'],
                    'slug': asset_data['slug'],
                    'logo': asset_data['logo'],
                    'quote': asset_data['quote']['MXN']['market_cap_dominance'],
                    'max_supply': asset_data['max_supply'],
                    'circulating_supply': asset_data['circulating_supply'],
                    'total_supply': asset_data['total_supply'],
                    'tags': '|'.join(asset_data['tags'])
                }
            )
    elif(mode == 'customed'):
        crypto_merged_data = [dict(crypto_info[crypto['symbol']], **{'rank': crypto['rank']}) for crypto in crypto_map]
        crypto_merged_data = [dict(crypto_merged_data[crypto], **{'quote': crypto_quotes[crypto][0]['quote']}) for crypto in crypto_quotes]
        for asset_data in crypto_merged_data:
            asset_data_filtered = {}
            symbol = asset_data['symbol']
            for strainer in filters:
                crypto_merged_data[strainer] = asset_data[strainer]
            dict_listing_filtered = dict(dict_listing_filtered, **asset_data_filtered)
        dict_listing_filtered = dict(filter(lambda crypto: crypto_info[crypto]['rank'] <= top_n, dict_listing_filtered))
    else:
        raise ValueError("Only 'full', 'csv', 'customed' modes are valid")
    return filtered_listing

def main():
    """
    Reading json files. As read_json_file() is generic enough, two different files are provided.
    Each file contains a response from /cryptocurrency/map and /cryptocurrency/info, respectively.
    """
    json_map_data = read_json_file('cmc_crypto_map.json')['data']
    json_info_data = read_json_file('cmc_crypto_info.json')['data']
    json_quotes_data = read_json_file('cmc_crypto_quotes.json')['data']

    """
    Data transformation and data filtering for 'csv'
    """
    filtered_listing_data_csv = filter_data_listing(json_map_data, json_info_data, json_quotes_data, 5, 'csv')
    #print(filtered_listing_data)
    dump_crypto_to_csv(read_json_file('cmc_crypto_map.json')['data'],'cmc_crypto_map.csv', 'map')
    dump_crypto_to_csv(filtered_listing_data_csv, 'cmc_merged_crypto.csv', 'merged')

    """
    Filtering in 'customed' mode
    """
    filters = ['stablecoin', '']

    """
    Example of using classes and their methods
    """
    filtered_listing_data_full = filter_data_listing(json_map_data, json_info_data, json_quotes_data, 5, 'full')
    user = User("Gerardo",
            0,
            [Crypto(crypto['name'],crypto['symbol'],0) for crypto in filtered_listing_data_full]
            )
    print("Tickers of an asset listing concatenated in a comma separated string:\n{}".format(user.listing_to_string()))
    print("A user's balances:\n{}".format(user.balances_to_string()))
    print("A user's details with balances:\n{}".format(user))

    """
    Exception raised intentionally
    """
    #filtered_listing_data_csv = filter_data_listing(json_map_data, json_info_data, 5)
    #filtered_listing_data_csv = filter_data_listing(json_map_data, json_info_data, 5, 'invalid_mode')
    #exception_crypto = Crypto(0,"",0)
    #exception_crypto = Crypto("Bitcoin",0,0)
    #exception_crypto = Crypto("Bitcoin","BTC","")
    #exception_user = User("Rich Hacker","123",[Crypto("Bitcoin","BTC",1),Crypto("Ethereum","ETH",1)])
    #exception_user = User("Rich Hacker",786747+55272,{'BTC': Crypto("Bitcoin","BTC",1)})
    #exception_user = User("Rich Hacker",786747+55272,[Crypto("Bitcoin","BTC",1), {}])

if __name__ == '__main__':
    main()