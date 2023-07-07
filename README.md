
# OPEN API - SAP RFC/ABAPi Python Connector-  PyRFC

This project consists of creating a RestAPI for ABAP/RFC'S Read Tables SAP calls, in order to be consumed in other services with dynamic parameters.



## Install

Dependencies:

```bash
  pip install Cython
  pip install uvicorn
  pip install fastapi
  pip install pydantic
  pip install c:\folder\resources\pyrfc-lib\PyRFC-1.9.93.tar.gz
```

```bash
Install Build Tools 2019 C in resources\vss\setup.exe
```
-  Download [NW RFC SDK](https://support.sap.com/en/product/connectors/nwrfcsdk.html)
   
environment variables :

```bash
  Create a folder called 'sap' with the files extracted from the RFC NEW SDK and Move in C:\'
  ADD to PATCH: 'C:\sap\nwrfcsdk\lib'
  CREATE environment variables  NAME:'SAPNWRFC_HOME' VALUE:'C:\sap\nwrfcsdk'
```



## Server Change:
MainBaseModel.py
```python
if __name__ == '__main__':
    uvicorn.run("MainBaseModel:app", port=8080, host='0.0.0.0', reload=True)

```


## API documentation

#### Return swagger

```http
  GET /docs
```

| Description                           |
| :---------------------------------- |
 | **swagger FastAPI**. |

#### ABAPI Call'S Request 

```http
  POST /bapi
```

Send JSon in Body:raw/Json for parameters and connection
```json
{
    "CONFIG": {
        "ashost":"XX.XX.XX.XX",
        "sysnr": "XX",
        "client":"XXX",
        "user":  "XXXXXXX",
        "passwd":"XXXXXX",
        "lang":  "pt"
    },
    "BAPI": "BAPI_EXAMPLE_GETDETAIL", ex: //BAPI_COMPANY_GETLIST //
    "KWARGS": {
        "EXPORTPARAMS1":"Value", // Args to  ABAPI
        "EXPORTPARAMS2":"Value"
    }
}
```




#### RFCs Read Tables Call'S Request 

```http
  POST /rfc
```

Send JSon in Body:raw/Json for parameters and connection
```json
{
    "ROWSKIPS": 0,
    "ROWCOUNT": 20,
    "FIELDS": [
        "NAME_FIELD1",
        "NAME_FIELD2",
        "NAME_FIELD3",
        "NAME_FIELD4",
        "NAME_FIELD5"
    ],
    "WHERE": [
        {
            "TEXT": "NAME_FIELD1  = 'S'",
            "TEXT": "NAME_FIELD2  LIKE '%VALUE%'",
            "TEXT": "NAME_FIELD3  <> 'VALUE'"

        }
    ],
    "CONFIG": {
        "ashost":"XX.XX.XX.XX",
        "sysnr": "XX",
        "client":"XXX",
        "user":  "XXXXXXX",
        "passwd":"XXXXXX",
        "lang":  "pt"
    },
    "TABELA": "PA0001" // TABLES SAP 
}
```


