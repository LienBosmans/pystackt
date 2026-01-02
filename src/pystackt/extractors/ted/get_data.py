import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
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

    retry_strategy = Retry(
        total=5,                                    # Total number of retries
        status_forcelist=[429, 500, 502, 503, 504], # Only retry on 503 (add 502, 504 if needed)
        backoff_factor=1,                           # Wait 1s, 2s, 4s, 8s... between retries
        allowed_methods=["GET", "POST"]             # Methods to retry on
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(base_url, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed after retries: {e}")

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
    formatted_names = ", ".join([f'{name}' for name in legal_names])

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
        (GROUP_CONCAT(DISTINCT CONCAT('"', lang(?procedureTitle), '":"', ?procedureTitle, '"') ; separator=",") AS ?procedureTitles)
		(GROUP_CONCAT(DISTINCT CONCAT('"', lang(?procedureDescription), '":"', ?procedureDescription, '"') ; separator=",") AS ?procedureDescriptions)
        ?procedureTypeUri
        ?procedureType

    WHERE {{
        FILTER (?legalName IN ( {formatted_names} ) )
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
      
        ?procedureUri ns3:identifier ?procedureIdentifier .
      	?procedureIdentifier skos:notation ?procedureId .
    
        OPTIONAL {{ ?procedureUri dcterms:title ?procedureTitle . }}
        OPTIONAL {{ ?procedureUri dcterms:description ?procedureDescription . }}
        OPTIONAL {{ 
            ?procedureUri epo:hasInternalIdentifier ?procedureInternalIdentifier . 
            ?procedureInternalIdentifier skos:notation ?procedureInternalId .
        }}
        OPTIONAL {{ ?procedureUri epo:isAccelerated ?isAccelerated . }}

        OPTIONAL {{ 
            ?procedureUri epo:hasPurpose ?procedurePurposeUri .
            ?procedurePurposeUri epo:hasMainClassification ?purposeClassification .
            ?purposeClassification skos:prefLabel ?mainPurpose .
            FILTER(lang(?mainPurpose) = "en")
        }}
        
        OPTIONAL {{
            ?procedureUri epo:hasLegalBasis ?legalBasisUri .
            ?legalBasisUri skos:scopeNote ?legalBasis .
            FILTER(lang(?legalBasis) = "en")
        }}
        
        OPTIONAL {{
            ?procedureUri epo:hasProcedureType ?procedureTypeUri .
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
        ?procedureTypeUri
        ?procedureType
    ORDER BY 
        ?procedureInternalId
    """

    return _get_query_result(query)


def _get_notices(procedure_ids:list):
    '''Returns dataframe with all notices linked to procedure in `procedure_ids`.'''

    formatted_ids = ", ".join([f'"{id}"' for id in procedure_ids])

    query = f"""
    PREFIX epo: <http://data.europa.eu/a4g/ontology#>  
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX ns3: <http://www.w3.org/ns/adms#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>

    SELECT 
        ?procedureId
        ?noticeUri
        ?ojsIssueNumber
        ?noticePublicationNumber
        ?noticeType
        ?noticeTypeDescription
        ?noticeFormType
        ?noticePublicationDate
        ?noticeESenderDispatchDate
        (GROUP_CONCAT(DISTINCT CONCAT('"', ?announcesLotId, '"') ; separator=",") AS ?announcesLotIds)
    	(GROUP_CONCAT(DISTINCT CONCAT('"', ?refersLotId, '"') ; separator=",") AS ?refersLotIds)
        (GROUP_CONCAT(DISTINCT CONCAT('"', ?announcesProcedureId, '"') ; separator=",") AS ?announcesProcedureIds)
    	(GROUP_CONCAT(DISTINCT CONCAT('"', ?refersProcedureId, '"') ; separator=",") AS ?refersProcedureIds)

    WHERE {{
        ?procedureUri a epo:Procedure ;
            ns3:identifier ?procedureIdentifier .

        ?procedureIdentifier skos:notation ?procedureId .
        FILTER(?procedureId in ( {formatted_ids} ) )
    
        ?noticeUri a epo:Notice ;
            epo:refersToProcedure ?procedureUri ;
            epo:hasOJSIssueNumber ?ojsIssueNumber ;
            epo:hasNoticePublicationNumber ?noticePublicationNumber ;
            epo:hasNoticeType ?noticeTypeUri ;
            epo:hasFormType ?noticeFormTypeUri ;
            epo:hasPublicationDate ?noticePublicationDate ;
            epo:hasESenderDispatchDate ?noticeESenderDispatchDate .
    
        ?noticeTypeUri dc:identifier ?noticeType .
             
        ?noticeTypeUri skos:prefLabel ?noticeTypeDescription .
  	    FILTER(lang(?noticeTypeDescription) = "en")    

        ?noticeFormTypeUri skos:prefLabel ?noticeFormType .
        FILTER(lang(?noticeFormType) = "en")

        OPTIONAL {{ ?noticeUri epo:announcesLot/ns3:identifier/skos:notation ?announcesLotId .  }}
      	OPTIONAL {{ ?noticeUri epo:refersToLot/ns3:identifier/skos:notation ?refersLotId . }}
          
        OPTIONAL {{ ?noticeUri epo:announcesProcedure/ns3:identifier/skos:notation ?announcesProcedureId .  }}
      	OPTIONAL {{ ?noticeUri epo:refersToProcedure/ns3:identifier/skos:notation ?refersProcedureId . }}
    }}

    GROUP BY 
		?procedureId
        ?noticeUri
        ?ojsIssueNumber
        ?noticePublicationNumber
        ?noticeType
        ?noticeTypeDescription
        ?noticeFormType
        ?noticePublicationDate
        ?noticeESenderDispatchDate

    ORDER BY ?procedureId ?noticePublicationDate
    """
    return _get_query_result(query)


def _get_lots(procedure_ids:list):
    '''Returns dataframe with all lots linked to procedure in `procedure_ids`.'''

    formatted_ids = ", ".join([f'"{id}"' for id in procedure_ids])

    query = f"""
    PREFIX epo: <http://data.europa.eu/a4g/ontology#>  
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX ns3: <http://www.w3.org/ns/adms#>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT 
      ?procedureId
      ?lotId
      ?internalId
      (GROUP_CONCAT(DISTINCT CONCAT('"', lang(?lotTitle), '":"', ?lotTitle, '"') ; separator=",") AS ?lotTitles)
      (GROUP_CONCAT(DISTINCT CONCAT('"', lang(?lotDescription), '":"', ?lotDescription, '"') ; separator=",") AS ?lotDescriptions)
      ?mainPurpose
      (MAX(?participationDeadline) AS ?participationDeadline)

    WHERE {{
      ?procedureUri a epo:Procedure ;
                      ns3:identifier ?procedureIdentifier .

      ?procedureIdentifier skos:notation ?procedureId .
      FILTER(?procedureId in ( {formatted_ids} ) )

      OPTIONAl {{
          ?procedureUri epo:hasProcurementScopeDividedIntoLot ?lotUri .

          ?lotUri a epo:Lot;
              ns3:identifier/skos:notation ?lotId ;
              epo:hasInternalIdentifier/skos:notation ?internalId ;
              epo:hasPurpose/epo:hasMainClassification/skos:prefLabel ?mainPurpose ;
              dcterms:title ?lotTitle ;
              dcterms:description ?lotDescription .
          FILTER(lang(?mainPurpose) = "en")

        OPTIONAL {{ 
          ?lotUri epo:isSubjectToLotSpecificTerm ?lotTermUri .
          ?lotTermUri a epo:SubmissionTerm .
          ?lotTermUri epo:hasReceiptParticipationRequestDeadline | epo:hasReceiptTenderDeadline ?participationDeadline . 
        }}

      }}


    }}

    GROUP BY ?procedureId ?lotId ?internalId ?mainPurpose
    ORDER BY ?procedureId
    """

    return _get_query_result(query)
