from pyrfc import Connection
from pprint import PrettyPrinter
class SapConnection:
    def __init__(self, config):
        self.connector = None
        self.config = config
        self.StartConnection()
        self.pp = PrettyPrinter(indent=4)

    def StartConnection(self):

        try:
            self.connector = Connection(**self.config)  
        except Exception as e:
            print('Connection failed:', e)



    def GenericABAPI(self, BAPI=str, **kwargs):
        if self.connector is None:
            print('Sem conexao ativa')
            return
        


        try:
            print(BAPI)
            print(kwargs)

            
            data = self.connector.call(BAPI, **kwargs)
            # data = self.connector.call(BAPI,EMPLOYEE_ID="")

            if data:
                indexers = list(data.values()) 

                qt = len(indexers[1])
                data_json = {
                    'data': data,
                    'QtRegistro':qt
                }
                return data_json
            
        except Exception as e:
            return e



    def RFCgenericTable(self,QUERY_TABLE,DELIMITER=',',FIELDS=[],OPTIONS=[],ROWCOUNT=0,ROWSKIPS=0):
        if self.connector is None:
            print('Sem Conexoes ativas')
            return


        try:
            data = self.connector.call('RFC_READ_TABLE',QUERY_TABLE=QUERY_TABLE,DELIMITER=DELIMITER,FIELDS=FIELDS,OPTIONS=OPTIONS,ROWCOUNT=ROWCOUNT,ROWSKIPS=ROWSKIPS) 
            
            if data:
                itens_data = data['DATA']
                names_filds = data['FIELDS']
                
                data_json = {
                    'data': [],
                    'QtRegistro':len(itens_data)
                }
    
                # print(len(itens_data))
                # print(len(names_filds))
            
                for rowns in range(len(itens_data)):
                    # print(f'Line {rowns}:')

                    data_json['data'].append({})

                    for colls in range(len(names_filds)):
                        name_filds = str(names_filds[colls]['FIELDNAME']).strip()
                        item_data = str(itens_data[rowns]['WA'].split(",")[colls]).strip()

                        data_json['data'][rowns][name_filds] = item_data
                        
                       

            return data_json
        except Exception as e:
            return e
