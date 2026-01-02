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

        OPTIONAL {{
        	?noticeUri epo:announcesLot ?announcesLotUri .
          	?announcesLotUri ns3:identifier ?announcesLotIdUri .
          	?announcesLotIdUri skos:notation ?announcesLotId .
        }}
      
      	OPTIONAL {{
            ?noticeUri epo:refersToLot ?refersLotUri .
          	?refersLotUri ns3:identifier ?refersLotIdUri .
          	?refersLotIdUri skos:notation ?refersLotId .
        }}
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

    WHERE {{
    ?procedureUri a epo:Procedure ;
                    ns3:identifier ?procedureIdentifier .
                        
    ?procedureIdentifier skos:notation ?procedureId .
    FILTER(?procedureId in ( {formatted_ids}) )
    
    OPTIONAl {{
        ?procedureUri epo:hasProcurementScopeDividedIntoLot ?lotUri .
        
        ?lotUri a epo:Lot;
            ns3:identifier ?lotIdUri ;
            epo:hasInternalIdentifier ?internalIdUri ;
            epo:hasPurpose ?lotPurposeUri ;
            dcterms:title ?lotTitle ;
            dcterms:description ?lotDescription .        
        
        ?lotIdUri skos:notation ?lotId .
        
        ?internalIdUri skos:notation ?internalId.
        
        ?lotPurposeUri epo:hasMainClassification ?purposeClassification .
        ?purposeClassification skos:prefLabel ?mainPurpose .
        FILTER(lang(?mainPurpose) = "en")
    }}


    }}

    GROUP BY ?procedureId ?lotId ?internalId ?mainPurpose
    ORDER BY ?procedureId
    """

    return _get_query_result(query)
