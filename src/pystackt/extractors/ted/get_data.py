import requests
import json
import duckdb
import polars as pl

def _get_query_result(query:str):
    '''Sends query to EU ted web api and returns data in response as polars dataframe.'''

    base_url = "https://publications.europa.eu/webapi/rdf/sparql"
    params = {
        "default-graph-uri": "",
        "query": query,
        "format": "application/sparql-results+json",
        "timeout": 30000
    }

    response = requests.get(base_url, params)

    if response.status_code == 200:
        raw_data = response.json().get("results").get("bindings")
        df = pl.DataFrame(raw_data)
        df = df.with_columns([
            pl.col(name).struct.field("value").name.keep()
            for name in df.columns
        ])
        return df
    else:
        print("Error in _get_url_response:\n", response.status_code, response.text)
        return None


def _query_procedures_linked_to_org(legal_names:list):
    '''Returns query for obtaining list of all procedures linked to organization
    that appears in `legal_names`.'''
    formatted_names = ", ".join([f'"{name}"@en' for name in legal_names])


    query = f"""
    PREFIX epo: <http://data.europa.eu/a4g/ontology#>  
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX ns3: <http://www.w3.org/ns/adms#>

    SELECT ?procedureId ?procedureInternalId  ?procedureTitle ?procedureDescription ?procedureTypeUri ?procedureType

    WHERE {{
        FILTER (?legalName IN ({formatted_names}) )
        ?noticeUri a epo:Notice ;
            epo:refersToProcedure ?procedureUri ;
            epo:announcesRole [  
                a ?role ; 
                    epo:playedBy [
                        a org:Organization;
                        epo:hasLegalName ?legalName ;
                    ] 
            ] .
    
        OPTIONAL {{
            ?procedureUri a epo:Procedure ;
                ns3:identifier ?procedureIdentifier ;
                epo:hasInternalIdentifier ?procedureInternalIdentifier ;
                dcterms:title ?procedureTitle ;
                dcterms:description ?procedureDescription ;
                epo:hasProcedureType ?procedureTypeUri .
            FILTER(lang(?procedureTitle) = "en")
            FILTER(lang(?procedureDescription) = "en")

            ?procedureIdentifier skos:notation ?procedureId .

            ?procedureInternalIdentifier skos:notation ?procedureInternalId .

            ?procedureTypeUri skos:prefLabel ?procedureType .
            FILTER(lang(?procedureType) = "en")
        }}
    }}

    GROUP BY ?procedureId ?procedureInternalId ?procedureTitle ?procedureDescription ?procedureTypeUri ?procedureType
    ORDER BY ?procedureInternalId
    """

    return query


# legal_names = ["Imec EU Pilot line NV", "IMEC VZW"]
# query = _query_procedures_linked_to_org(legal_names)
# data = _get_query_result(query)
# print(data)
