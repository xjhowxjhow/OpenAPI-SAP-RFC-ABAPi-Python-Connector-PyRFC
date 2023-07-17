from Api import SapConnection
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

app = FastAPI()



class RfcRequest(BaseModel):
    ROWSKIPS: int = 0
    ROWCOUNT: int = 1000
    FIELDS: List[str] = []
    WHERE: List[Dict[str, str]] = []
    CONFIG :Dict[str,str] = []
    TABELA: str


class BapiRequest(BaseModel):
    BAPI: str
    CONFIG :Dict[str,str] = [] 
    KWARGS : Dict[str,str] = {}
    

class CustomFuncionarios(BaseModel):
    LIST_PAYROLL: List[str] 
    CONFIG :Dict[str,str] 

class FuncionarioModel2(BaseModel):
    LIST_PAYROLL: List[str] 
    CONFIG :Dict[str,str] 
    PAGE: int


@app.get("/")
async def root():
    return {"message": "Conexao SAPRFC-PYRFC- Para Swagger: http://seuip:3000/docs "}


@app.post("/bapi")
async def Bapi(request: BapiRequest, parametro: str = Query('')):

    try:
        call = SapConnection(request.CONFIG)
        result = call.GenericABAPI(
            BAPI = request.BAPI,
            **request.KWARGS

        )
        return {"result": result, "parametro": parametro}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@app.post("/rfc")
async def Rfc(request: RfcRequest, parametro: str = Query('')):


    try:
        call = SapConnection(request.CONFIG)
        result = call.RFCgenericTable(
            QUERY_TABLE = request.TABELA,
            ROWSKIPS=request.ROWSKIPS,
            ROWCOUNT=request.ROWCOUNT,
            FIELDS=request.FIELDS,
            OPTIONS=request.WHERE,
        )
        return {"result": result, "parametro": parametro}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/funcionarios")
async def Funcionarios(request: CustomFuncionarios, parametro: str = Query('')):
    try:

        call = SapConnection(request.CONFIG)
        result = call.FuncionariosPayroll(
            LIST_PAYROLL=request.LIST_PAYROLL,
        )
        return {"result": result, "parametro": parametro}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/funcionarios2") 
async def Funcionarios(request: FuncionarioModel2, parametro: str = Query('')):
    try:

        call = SapConnection(request.CONFIG)
        result = call.FuncionariosPayroll_Modelo2(
            LIST_PAYROLL=request.LIST_PAYROLL,
            page=request.PAGE,
            limit=50

        )
        return {"result": result, "parametro": parametro}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run("MainBaseModel:app", port=3000, host='0.0.0.0', reload=True)

