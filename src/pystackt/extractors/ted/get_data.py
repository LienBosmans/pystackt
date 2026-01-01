import requests
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
        print("Error in _get_query_result:\n", response.status_code, response.text)
        return None


def _get_procedures(legal_names:list):
    '''Returns dataframe with all procedures linked to organization
    that appears in `legal_names`.'''
    formatted_names = ", ".join([f'"{name}"@en' for name in legal_names])


    query = f"""
    PREFIX epo: <http://data.europa.eu/a4g/ontology#>  
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX ns3: <http://www.w3.org/ns/adms#>

    SELECT 
        (MIN(?eSenderDispatchDate) AS ?earliestNoticeTimestamp)
        ?mainPurpose
        ?legalBasis
        ?isAccelerated
        ?procedureId
        ?procedureInternalId 
        ?procedureTitle
        ?procedureDescription
        ?procedureTypeUri
        ?procedureType

    WHERE {{
        FILTER (?legalName IN ({formatted_names}) )
        ?noticeUri a epo:Notice ;
            epo:refersToProcedure ?procedureUri ;
            epo:hasESenderDispatchDate ?eSenderDispatchDate ;
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
                epo:hasPurpose ?procedurePurposeUri ;
                epo:hasLegalBasis ?legalBasisUri ;
                epo:hasProcedureType ?procedureTypeUri .
            FILTER(lang(?procedureTitle) = "en")
            FILTER(lang(?procedureDescription) = "en")

            OPTIONAL {{ ?procedureUri epo:isAccelerated ?isAccelerated . }}

            ?procedureIdentifier skos:notation ?procedureId .

            ?procedureInternalIdentifier skos:notation ?procedureInternalId .

            ?procedurePurposeUri epo:hasMainClassification ?purposeClassification .
          	?purposeClassification skos:prefLabel ?mainPurpose .
          	FILTER(lang(?mainPurpose) = "en")
              
            ?legalBasisUri skos:scopeNote ?legalBasis .
          	FILTER(lang(?legalBasis) = "en")

            ?procedureTypeUri skos:prefLabel ?procedureType .
            FILTER(lang(?procedureType) = "en")
        }}
    }}

    GROUP BY 
        ?mainPurpose
        ?legalBasis
        ?isAccelerated
        ?procedureId
        ?procedureInternalId
        ?procedureTitle
        ?procedureDescription
        ?procedureTypeUri
        ?procedureType
    ORDER BY 
        ?procedureInternalId
    """

    return _get_query_result(query)


def _get_notices(procedure_uris:list):
    '''Returns dataframe with all notices linked to procedure in `procedure_uris`.'''

    formatted_uris = ", ".join([f'"{uri}"' for uri in procedure_uris])

    query = f"""
    PREFIX epo: <http://data.europa.eu/a4g/ontology#>  
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX ns3: <http://www.w3.org/ns/adms#>

    SELECT 
        ?procedureId
        ?noticeUri
        ?noticePublicationNumber
        ?noticeType
        ?noticeFormType
        ?noticePublicationDate
        ?noticeESenderDispatchDate

    WHERE {{
        ?procedureUri a epo:Procedure ;
            ns3:identifier ?procedureIdentifier .

        ?procedureIdentifier skos:notation ?procedureId .
        FILTER(?procedureId in ( {formatted_uris} ) )
    
        ?noticeUri a epo:Notice ;
            epo:refersToProcedure ?procedureUri ;
            epo:hasNoticePublicationNumber ?noticePublicationNumber ;
            epo:hasNoticeType ?noticeTypeUri ;
            epo:hasFormType ?noticeFormTypeUri ;
            epo:hasPublicationDate ?noticePublicationDate ;
            epo:hasESenderDispatchDate ?noticeESenderDispatchDate .
    
        ?noticeTypeUri skos:prefLabel ?noticeType .
  	    FILTER(lang(?noticeType) = "en")    

        ?noticeFormTypeUri skos:prefLabel ?noticeFormType .
        FILTER(lang(?noticeFormType) = "en")
    }}

    ORDER BY ?procedureId ?noticePublicationDate
    """

    return _get_query_result(query)
