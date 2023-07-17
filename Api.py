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

            if data:
                indexers = list(data.values()) # converte dict para lista 

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

                    data_json['data'].append({})

                    for colls in range(len(names_filds)):
                        name_filds = str(names_filds[colls]['FIELDNAME']).strip()
                        item_data = str(itens_data[rowns]['WA'].split(",")[colls]).strip()

                        data_json['data'][rowns][name_filds] = item_data
                        
                       

            return data_json
        except Exception as e:
            return e



    def FuncionariosPayroll(self, LIST_PAYROLL=[]):
        if self.connector is None:
            print('Sem Conexoes ativas')
            return

        try:
            print(LIST_PAYROLL)
            data_json = {
                'data': [],
                'QtRegistro':0
            }

            for payroll in LIST_PAYROLL:
                print(payroll)
                data = self.connector.call(
                    'BAPI_OUTEMPLOYEE_GETLIST', IABKRS=payroll)
                if data:
                    indexers = list(data.values())
                    qt = len(indexers[1])


                    OUTEMPLOYEE_LIST = data['OUTEMPLOYEE_LIST']
                    counter = 0
                    
                    ################## OUTEMPLOYEE_LIST ##################
                    for dict_employee in OUTEMPLOYEE_LIST:
                        json_mount = {}
                        
                        for itens_dict in dict_employee:
                            
                            employee_id = dict_employee['EMPLOYEENUMBER']
                            key_employee = itens_dict
                            value_employee = dict_employee[itens_dict]
                            json_mount[key_employee] = value_employee

                        data_json['data'].append(json_mount)

                    ################## BAPI_EMPLOYEE_GETDATA ##################
                        counter += 1

                    if counter > 0:
                        for employee in data_json['data']:
                            employee_id = employee['EMPLOYEENUMBER']
                            employee_docs = self.connector.call('BAPI_EMPLOYEE_GETDATA', EMPLOYEE_ID=employee_id)

                            # adiciona os dados de documentos do funcionario 

                            employee['PERSONAL_DATA'] = [{}]
                            employee['ORG_ASSIGNMENT'] = [{}]
                            employee['PA0000TABLE'] =[{}]
                            employee['PA0465-RG'] = [{}]
                            employee['PA0465-CTPS'] = [{}]
                            employee['PA0465-CPF'] = [{}]
                            employee['PA0465-PIS'] = [{}]
                            employee['BAPI_ADDRESSEMPGETDETAILEDLIST'] = [{}]
                            employee['PA0398-CAT-ESC-APO'] = [{}]

                            ############## PERSONAL_DATA ##############

                            for i in range(len(employee_docs['PERSONAL_DATA'])):
                                employee['PERSONAL_DATA'][i]['INDICE'] = i
                                employee['PERSONAL_DATA'][i]['MAR_STATUS'] = employee_docs['PERSONAL_DATA'][i]['MAR_STATUS']    #EST_CIVIL
                                employee['PERSONAL_DATA'][i]['BIRTHDATE']  = employee_docs['PERSONAL_DATA'][i]['BIRTHDATE']     #DT_NASC
                                employee['PERSONAL_DATA'][i]['GENDER']     = employee_docs['PERSONAL_DATA'][i]['GENDER']        #SEXO


                            for i in range(len(employee_docs['ORG_ASSIGNMENT'])):
                                employee['ORG_ASSIGNMENT'][i]['INDICE'] = i
                                employee['ORG_ASSIGNMENT'][i]['ORG_UNIT']  = employee_docs['ORG_ASSIGNMENT'][i]['ORG_UNIT']     #SETOR
                                employee['ORG_ASSIGNMENT'][i]['POSITION']  = employee_docs['ORG_ASSIGNMENT'][i]['POSITION']     #CARGO
                                employee['ORG_ASSIGNMENT'][i]['COMP_CODE'] = employee_docs['ORG_ASSIGNMENT'][i]['COMP_CODE']    #EMPRESA
                                employee['ORG_ASSIGNMENT'][i]['P_SUBAREA'] = employee_docs['ORG_ASSIGNMENT'][i]['P_SUBAREA']    #POSICAO 
                                employee['ORG_ASSIGNMENT'][i]['PERS_AREA'] = employee_docs['ORG_ASSIGNMENT'][i]['PERS_AREA']    #UNIDADE




                            ############## PA0000 ADMISSAO ##############
                            #Params RFC
                            FIELDS = ['BEGDA','PERNR']

                            employee_ad = self.RFCgenericTable(QUERY_TABLE='PA0000',FIELDS=FIELDS,OPTIONS=[{"TEXT":"PERNR = '"+employee_id+"' AND MASSN ='01'"}],ROWCOUNT=0)

                            for i in range(len(employee_ad['data'])):

                                employee['PA0000TABLE'].append({}) ## adiona mais um item a cada range
                                employee['PA0000TABLE'][i]['INDICE'] = i
                                employee['PA0000TABLE'][i]['BEGDA-AD'] = employee_ad['data'][i]['BEGDA']

                            ############## PA0000 DEMISSAO ##############
                            #Params RFC
                            FIELDS_DEMI = ['BEGDA']
                            employee_dem = self.RFCgenericTable(QUERY_TABLE='PA0000',FIELDS=FIELDS_DEMI,OPTIONS=[{"TEXT":"PERNR = '"+employee_id+"' AND MASSN ='10'"}],ROWCOUNT=0)


                            for i in range(len(employee_dem['data'])):

                                employee['PA0000TABLE'].append({}) ## adiona mais um item a cada range                              
                                employee['PA0000TABLE'][i]['INDICE'] = i
                                employee['PA0000TABLE'][i]['BEGDA-DEMI'] = employee_dem['data'][i]['BEGDA']


                            ############## PA0465 SUBTYPE = 0002 ############## rg docs
                            #Params RFC 
                            FILEDS_RG = ['SUBTY','IDENT_NR','ES_EMIS','DT_EMIS','IDENT_ORG']
                            employee_sub = self.RFCgenericTable(QUERY_TABLE='PA0465',FIELDS=FILEDS_RG,OPTIONS=[{"TEXT": "PERNR  = '"+employee_id+"' AND SUBTY = '0002'"}],ROWCOUNT=0)
                            

                            employee['PA0465-RG'] = []

                            for i in range(len(employee_sub['data'])):
                                if employee_sub['data'][i]:
                                    employee['PA0465-RG'].append({})
                                    employee['PA0465-RG'][i]['SUBTY']  = employee_sub['data'][i]['SUBTY']
                                    employee['PA0465-RG'][i]['INDICE'] = i
                                    employee['PA0465-RG'][i]['IDENT_NR'] = employee_sub['data'][i]['IDENT_NR']
                                    employee['PA0465-RG'][i]['ES_EMIS']  = employee_sub['data'][i]['ES_EMIS']
                                    employee['PA0465-RG'][i]['DT_EMIS'] = employee_sub['data'][i]['DT_EMIS']
                                    employee['PA0465-RG'][i]['IDENT_ORG']= employee_sub['data'][i]['IDENT_ORG']
                                else:
                                    pass

                            ############## PA0465 SUBTYPE = 0003 ############## ctps docs

                            FIELDS_CTPS = ['PERNR','SUBTY','CTPS_NR','CTPS_SERIE','DT_EMIS','ES_EMIS']
                            employee_ctps = self.RFCgenericTable(QUERY_TABLE='PA0465',FIELDS=FIELDS_CTPS,OPTIONS=[{"TEXT": "PERNR  = '"+employee_id+"' AND SUBTY = '0003'"}],ROWCOUNT=0)

                            employee['PA0465-CTPS'] = []
                            # print(employee_ctps)
                            for i in range(len(employee_ctps['data'])):
                                if employee_ctps['data'][i]:
                                    employee['PA0465-CTPS'].append({})
                                    employee['PA0465-CTPS'][i]['INDICE'] = i
                                    employee['PA0465-CTPS'][i]['CTPS_NR'] = employee_ctps['data'][i]['CTPS_NR']
                                    employee['PA0465-CTPS'][i]['CTPS_SERIE']  = employee_ctps['data'][i]['CTPS_SERIE']
                                    employee['PA0465-CTPS'][i]['DT_EMIS'] = employee_ctps['data'][i]['DT_EMIS']
                                    employee['PA0465-CTPS'][i]['ES_EMIS']= employee_ctps['data'][i]['ES_EMIS']
                                else:
                                    pass
                            
                            ############# PA0465 NON SUBTYPE ############## CPF
                            FIELDS_CPF = ['PERNR','SUBTY','CPF_NR']
                            employee_cpf = self.RFCgenericTable(QUERY_TABLE='PA0465',FIELDS=FIELDS_CPF,OPTIONS=[{"TEXT": "PERNR  = '"+employee_id+"'"}],ROWCOUNT=0)

                            employee['PA0465-CPF'] = []
           
                            COUNTER_CPF = 0
                            for i in range(len(employee_cpf['data'])):
                                if employee_cpf['data'][i]:
                                    if  len(employee_cpf['data'][i]['CPF_NR']) > 0:
                                        employee['PA0465-CPF'].append({})
                                        employee['PA0465-CPF'][COUNTER_CPF]['INDICE'] = i
                                        employee['PA0465-CPF'][COUNTER_CPF]['CPF_NR'] = employee_cpf['data'][i]['CPF_NR']
                                        COUNTER_CPF=+1
                                else:
                                    pass
                            ############# PA0465 NON SUBTYPE ############## PIS/PASEP
                            FIELDS_PIS = ['PERNR','SUBTY','PIS_NR']
                            employee_pis = self.RFCgenericTable(QUERY_TABLE='PA0465',FIELDS=FIELDS_PIS,OPTIONS=[{"TEXT": "PERNR  = '"+employee_id+"'"}],ROWCOUNT=0)

                            # print(employee_pis)
                            employee['PA0465-PIS'] = []

                            COUNTER_PIS = 0
                            for i in range(len(employee_pis['data'])):
                                if employee_pis['data'][i]:
                                    
                                    if len(employee_pis['data'][i]['PIS_NR']) > 0:
                                        employee['PA0465-PIS'].append({})
                                        employee['PA0465-PIS'][COUNTER_PIS]['INDICE'] = i
                                        employee['PA0465-PIS'][COUNTER_PIS]['PIS_NR'] = employee_pis['data'][i]['PIS_NR']
                                        COUNTER_PIS=+1
                                else:
                                    pass


                            ############# BAPI_ADDRESSEMPGETDETAILEDLIST ############## ENDERECO
                            data_adrrs = self.connector.call('BAPI_ADDRESSEMPGETDETAILEDLIST',EMPLOYEENUMBER=employee_id)
                            # print(data_adrrs)
                            employee['BAPI_ADDRESSEMPGETDETAILEDLIST'] = []
                            for i in range(len(data_adrrs['ADDRESS'])):

                                employee['BAPI_ADDRESSEMPGETDETAILEDLIST'].append({})
                                employee['BAPI_ADDRESSEMPGETDETAILEDLIST'][i]['INDICE'] = i
                                employee['BAPI_ADDRESSEMPGETDETAILEDLIST'][i]['STREETANDHOUSENO'] = data_adrrs['ADDRESS'][i]['STREETANDHOUSENO']
                                employee['BAPI_ADDRESSEMPGETDETAILEDLIST'][i]['CITY'] = data_adrrs['ADDRESS'][i]['CITY']
                                employee['BAPI_ADDRESSEMPGETDETAILEDLIST'][i]['STATE'] = data_adrrs['ADDRESS'][i]['STATE']
                                employee['BAPI_ADDRESSEMPGETDETAILEDLIST'][i]['DISTRICT'] = data_adrrs['ADDRESS'][i]['DISTRICT']
                                employee['BAPI_ADDRESSEMPGETDETAILEDLIST'][i]['POSTALCODECITY'] = data_adrrs['ADDRESS'][i]['POSTALCODECITY']
                                employee['BAPI_ADDRESSEMPGETDETAILEDLIST'][i]['COUNTRY'] = data_adrrs['ADDRESS'][i]['COUNTRY']

                            ############# PA0398 ############## CATEGORIA E ESCOLARIDADE APOSETADO
                            FILDS_CATEGORIA_ES_APO = ['RETFL','ESCOL','CATTR']
                            employee_CEA = self.RFCgenericTable(QUERY_TABLE='PA0398',FIELDS=FILDS_CATEGORIA_ES_APO,OPTIONS=[{"TEXT": "PERNR  = '"+employee_id+"'"}],ROWCOUNT=0)

                            employee['PA0398-CAT-ESC-APO'] = []
                            for i in range(len(employee_CEA['data'])):
                                if employee_CEA['data'][i]:
                                    employee['PA0398-CAT-ESC-APO'].append({})
                                    employee['PA0398-CAT-ESC-APO'][i]['INDICE'] = i
                                    employee['PA0398-CAT-ESC-APO'][i]['RETFL'] = employee_CEA['data'][i]['RETFL']
                                    employee['PA0398-CAT-ESC-APO'][i]['ESCOL'] = employee_CEA['data'][i]['ESCOL']
                                    employee['PA0398-CAT-ESC-APO'][i]['CATTR'] = employee_CEA['data'][i]['CATTR']
                                else:
                                    pass
                                



                    data_json['QtRegistro'] += counter



            return data_json
                

        except Exception as e:
            print(e)
            return e

    def CustomCargoSetor(self, employe_id):
        data_custom_CargosSetor = {
            "PERNR": employe_id,
            "DADOS_CARGO": [],
            "DADOS_SETOR": []
        }

        pega_ids = self.RFCgenericTable(QUERY_TABLE='PA0001', FIELDS=['ORGEH','PLANS','ENDDA','BEGDA'], OPTIONS=[{"TEXT": "PERNR  = '"+employe_id+"'"}], ROWCOUNT=0)

        counter_cargo = 0
        if len(pega_ids['data']) > 0:
            for campos in pega_ids['data']:
                ID_SETOR = campos['ORGEH']
                ID_CARGO = campos['PLANS']
                DT_FIM = campos['ENDDA']
                DT_INICO = campos['BEGDA']

                data_custom_CargosSetor['DADOS_CARGO'].append({
                    'ID_CARGO': ID_CARGO,
                    'DT_INICO': DT_INICO,
                    'DT_FIM': DT_FIM
                })

                pega_cargo = self.RFCgenericTable(QUERY_TABLE='HRP1000', FIELDS=['SHORT','STEXT','MC_SEARK'], OPTIONS=[{"TEXT": "OTYPE = 'S' AND OBJID = '"+ID_CARGO+"'"}], ROWCOUNT=0)
                if len(pega_cargo['data']) > 0:
                    for campos_cargo in pega_cargo['data']:
                        data_custom_CargosSetor['DADOS_CARGO'][counter_cargo]['INDICE'] = counter_cargo
                        data_custom_CargosSetor['DADOS_CARGO'][counter_cargo]['CARGO_SHORT'] = campos_cargo['SHORT']
                        data_custom_CargosSetor['DADOS_CARGO'][counter_cargo]['CARGO_STEXT'] = campos_cargo['STEXT']
                        data_custom_CargosSetor['DADOS_CARGO'][counter_cargo]['CARGO_MC_SEARK'] = campos_cargo['MC_SEARK']

                pega_setor = self.connector.call('BAPI_ORGUNITEXT_DATA_GET', OBJID=ID_SETOR, OTYPE='O')

                counter_setor = 0
                for i, pega_setor_data in enumerate(pega_setor['OBJECTSDATA']):
                    if pega_setor_data['OBJECT_ID'] == str(ID_SETOR):
                        print(pega_setor_data['LONG_TEXT'])
                        data_custom_CargosSetor['DADOS_SETOR'].append({
                            'INDICE': counter_setor,
                            'ID_SETOR': ID_SETOR,
                            'SETOR_LONG_TEXT': pega_setor_data['LONG_TEXT'],
                            'SETOR_SHORT_TEXT': pega_setor_data['SHORT_TEXT']
                        })
        return data_custom_CargosSetor


    def FuncionariosPayroll_Modelo2(self, LIST_PAYROLL=[], page=0, limit=50):
        if self.connector is None:
            print('Sem conexões ativas')
            return

        try:
            

            data_json = {
                'data': [],
                'QtRegistro': 0
            }

            offset = limit * (page - 1)
            skipped_employees = offset  # Número de funcionários para pular

            counter = 0
            for payroll in LIST_PAYROLL:
                if counter >= limit:
                    print('Limite máximo por PAYROLL atingido')
                    break

                data = self.connector.call('BAPI_OUTEMPLOYEE_GETLIST', IABKRS=payroll)
                if data:
                    OUTEMPLOYEE_LIST = data['OUTEMPLOYEE_LIST']

                    for dict_employee in OUTEMPLOYEE_LIST:
                        if skipped_employees > 0:
                            skipped_employees -= 1
                            continue

                        if counter >= limit:
                            break

                        employee_id = dict_employee['EMPLOYEENUMBER']
                        json_mount = {
                            'EMPLOYEENUMBER': employee_id,
                            'PERSONAL_DATA': [],
                            'ORG_ASSIGNMENT': [],
                            'PA0000TABLE-AD': [],
                            'PA0000TABLE-DEMI': [],
                            'PA0465-RG': [],
                            'PA0465-CTPS': [],
                            'PA0465-CPF': [],
                            'PA0465-PIS': [],
                            'BAPI_ADDRESSEMPGETDETAILEDLIST': [],
                            'PA0398-CAT-ESC-APO': [],
                            # 'CUSTOM_CARGOS_SETOR': [] 
                            
                        }

                        #self.CustomCargoSetor(employee_id)
                        json_mount['CUSTOM_CARGOS_SETOR'] = self.CustomCargoSetor(employee_id)

                        employee_docs = self.connector.call('BAPI_EMPLOYEE_GETDATA', EMPLOYEE_ID=employee_id)
                        employee_ad = self.RFCgenericTable(QUERY_TABLE='PA0000', FIELDS=['BEGDA', 'PERNR'],
                                                           OPTIONS=[{"TEXT": "PERNR = '" + employee_id + "' AND MASSN ='01'"}], ROWCOUNT=0)
                        employee_dem = self.RFCgenericTable(QUERY_TABLE='PA0000', FIELDS=['BEGDA'],
                                                            OPTIONS=[{"TEXT": "PERNR = '" + employee_id + "' AND MASSN ='10'"}], ROWCOUNT=0)
                        employee_sub = self.RFCgenericTable(QUERY_TABLE='PA0465',
                                                            FIELDS=['SUBTY', 'IDENT_NR', 'ES_EMIS', 'DT_EMIS', 'IDENT_ORG'],
                                                            OPTIONS=[{"TEXT": "PERNR  = '" + employee_id + "' AND SUBTY = '0002'"}], ROWCOUNT=0)
                        employee_ctps = self.RFCgenericTable(QUERY_TABLE='PA0465',
                                                             FIELDS=['PERNR', 'SUBTY', 'CTPS_NR', 'CTPS_SERIE', 'DT_EMIS', 'ES_EMIS'],
                                                             OPTIONS=[{"TEXT": "PERNR  = '" + employee_id + "' AND SUBTY = '0003'"}], ROWCOUNT=0)
                        employee_cpf = self.RFCgenericTable(QUERY_TABLE='PA0465',
                                                            FIELDS=['PERNR', 'SUBTY', 'CPF_NR'],
                                                            OPTIONS=[{"TEXT": "PERNR  = '" + employee_id + "'"}], ROWCOUNT=0)
                        employee_pis = self.RFCgenericTable(QUERY_TABLE='PA0465',
                                                            FIELDS=['PERNR', 'SUBTY', 'PIS_NR'],
                                                            OPTIONS=[{"TEXT": "PERNR  = '" + employee_id + "'"}], ROWCOUNT=0)
                        data_adrrs = self.connector.call('BAPI_ADDRESSEMPGETDETAILEDLIST', EMPLOYEENUMBER=employee_id)
                        employee_CEA = self.RFCgenericTable(QUERY_TABLE='PA0398',
                                                            FIELDS=['RETFL', 'ESCOL', 'CATTR'],
                                                            OPTIONS=[{"TEXT": "PERNR  = '" + employee_id + "'"}], ROWCOUNT=0)

                        for i, personal_data in enumerate(employee_docs['PERSONAL_DATA']):
                            personal_data['INDICE'] = i
                            json_mount['PERSONAL_DATA'].append(personal_data)

                        for i, org_assignment in enumerate(employee_docs['ORG_ASSIGNMENT']):
                            org_assignment['INDICE'] = i
                            json_mount['ORG_ASSIGNMENT'].append(org_assignment)

                        if len(employee_ad['data']) > 0:
                            for i, ad in enumerate(employee_ad['data']):
                                ad['INDICE'] = i
                                json_mount['PA0000TABLE-AD'].append(ad)
                        else:
                            #adiciona um registro vazio
                            json_mount['PA0000TABLE-AD'].append({'BEGDA': '', 'INDICE': 0})

                        if len(employee_dem['data']) > 0:
                            for i, dem in enumerate(employee_dem['data']):

                                dem['INDICE'] = i
                                json_mount['PA0000TABLE-DEMI'].append(dem)
                        else:
                            #adiciona um registro vazio
                            json_mount['PA0000TABLE-DEMI'].append({'BEGDA': '', 'INDICE': 0})
                            
                        if len(employee_sub['data']) > 0:
                            for i, sub in enumerate(employee_sub['data']):
                                if sub:
                                    sub['INDICE'] = i
                                    json_mount['PA0465-RG'].append(sub)
                        else:
                            #adiciona um registro vazio
                            json_mount['PA0465-RG'].append({'SUBTY': '', 'IDENT_NR': '', 'ES_EMIS': '', 'DT_EMIS': '', 'IDENT_ORG': '', 'INDICE': 0})

                        if len(employee_ctps['data']) > 0:
                            for i, ctps in enumerate(employee_ctps['data']):
                                if ctps:
                                    ctps['INDICE'] = i
                                    json_mount['PA0465-CTPS'].append(ctps)
                        else:
                            #adiciona um registro vazio
                            json_mount['PA0465-CTPS'].append({'SUBTY': '', 'CTPS_NR': '', 'CTPS_SERIE': '', 'DT_EMIS': '', 'ES_EMIS': '', 'INDICE': 0})

                        counter_cpf = 0
                        if len(employee_cpf['data']) > 0:
                            for i, cpf in enumerate(employee_cpf['data']):
                                if cpf and len(cpf['CPF_NR']) > 0:
                                    cpf['INDICE'] = counter_cpf
                                    json_mount['PA0465-CPF'].append(cpf)
                                    counter_cpf += 1
                        else:
                            #adiciona um registro vazio
                            json_mount['PA0465-CPF'].append({'SUBTY': '', 'CPF_NR': '', 'INDICE': 0})

                        counter_pis = 0
                        if len(employee_pis['data']) > 0:
                            for i, pis in enumerate(employee_pis['data']):
                                if pis and len(pis['PIS_NR']) > 0:
                                    pis['INDICE'] = counter_pis
                                    json_mount['PA0465-PIS'].append(pis)
                                    
                                else:
                                    #adiciona um registro vazio
                                    json_mount['PA0465-PIS'].append({'SUBTY': '', 'PIS_NR': '', 'INDICE': counter_pis})
                                counter_pis += 1
                        else:
                            #adiciona um registro vazio
                            json_mount['PA0465-PIS'].append({'SUBTY': '', 'PIS_NR': '', 'INDICE': 0})

                        for i, address in enumerate(data_adrrs['ADDRESS']):
                            address['INDICE'] = i
                            json_mount['BAPI_ADDRESSEMPGETDETAILEDLIST'].append(address)

                        for i, cea in enumerate(employee_CEA['data']):
                            if cea:
                                cea['INDICE'] = i
                                json_mount['PA0398-CAT-ESC-APO'].append(cea)

                        data_json['data'].append(json_mount)
                        counter += 1

            data_json['QtRegistro'] += counter

            return data_json
        except Exception as e:
            print(e)
            return e




