import pandas as pd, numpy as np, requests, json

def query_hal(doi) :
    """
    requete HAL à partir du DOI
    retourne halId, submitType, linkExtId
    """

    req = requests.get( f"https://api.archives-ouvertes.fr/search/?q=doiId_s:{doi}&fl=halId_s,submitType_s,linkExtId_s")
    res = req.json()

    if res.get("error") or res['response']['numFound'] == 0 : 
        return {}

    else :
        """TODO many halId if len(res["response"]["docs"]) > 0 : 
            print("")"""

        res = res['response']['docs'][0]
        #print("data from 1st doc is \n", res)      
        return{
        "halId" : res["halId_s"],
        "submitType" : res['submitType_s'],
        "linkExtId" : res["linkExtId_s"] if res.get("linkExtId_s") else ""
        }

def print_progression(name, index, total) : 
    if total > 10 and index > 0 and index % (int(total/10)) == 0 : 
        print( f"{name} {round(index / total * 100)}% ")

def enrich_w_hal(df) : 
            
    print("nb DOI a verifier dans HAL", len(df))
    for row in df.itertuples():
        print_progression("hal", row.Index, len(df))
        hal_data = query_hal(row.doi)
        for field in hal_data : 
            df.at[row.Index, field] = hal_data[field]   
    print("hal 100%")
    return df


def query_upw(doi) : 
    req = requests.get( f"https://api.unpaywall.org/v2/{doi}?email=maxence.larrieu@u-paris.fr")
    res = req.json()

    # if not in upw
    if res.get("message") and "isn't in Unpaywall" in res.get("message") :
        return { "upw_state": "missing" }

    # if paper is closed
    if not res.get("oa_locations") : 
        return { 
        "upw_state" : "closed",
        "published_date" : res.get("published_date"),
        "has_issn" : True if res.get("journal_issns") else False
        }

    # if it is open     
    temp = {
    "upw_state" : "open",
    "published_date" : res.get("published_date"),
    "oa_publisher_license" : "",
    "oa_publisher_link" : "", 
    "oa_repo_link" : ""
    }
    #print(f"nb of location { len(res['oa_locations']) }")

    best_loc_is_publisher = False

    # get best oa_location
    if res.get("best_oa_location") : 
        if res["best_oa_location"]["host_type"] == "publisher" : 
            best_loc_is_publisher = True
            #on ne peut transmettre les données None car le df.at pose pb
            temp["oa_publisher_license"] = res["best_oa_location"]["license"] if res["best_oa_location"]["license"] else ""
            temp["oa_publisher_link"] = res["best_oa_location"]["url_for_pdf"] if res["best_oa_location"]["url_for_pdf"] else res["best_oa_location"]["url_for_landing_page"] 

        if res["best_oa_location"]["host_type"] == "repository" : 
            temp["oa_repo_link"] = str(res["best_oa_location"]["url_for_pdf"])
            # on passe en str car les urls peuvent contenir des espaces qui créent pb eg https://hal.archives-ouvertes.fr/hal-03189186/file/Pierre%20Uzan_Mind-Body%20Connection%20and%20Causation_HAL.pdf


    if best_loc_is_publisher : 
        for elem in res["oa_locations"] :
            if elem["host_type"] == "repository" : 
                temp["oa_repo_link"] = str(elem["url_for_pdf"])
                break #on prend la 1er oa_location de hostype repository
        
    return temp



def enrich_w_upw(df) : 

    """
    enrichie la df avec les données de upw
    pour une v2 ne plus faire iteration par champs
    voir new methode bso https://github.com/MinistereSupRecherche/bso/blob/master/notebooks/unpwaywall_utils.py#L100 
    """
    
    print(f"nb DOI a verifier dans upw \t{len(df)}")
    df.reset_index(drop=True, inplace = True)
    for row in df.itertuples() :

        print_progression("upw", row.Index, len(df))
        
        upw_data = query_upw(row.doi)
  
        for field in upw_data :
            try : 
                df.at[row.Index, field] = upw_data[field]
            except : 
                print("\n\npb ac doi upw\n", field , row.doi, '\n\n', upw_data)
                break
    print("upw 100%")
    return df



def add_permissions(row) : 
    """
    ajouter les possibilité de dépôt via l'API persmission

    """

    # si la publi est deja en repo ou bien en oa chez publisher 
    if row.oa_repo_link or row.oa_publisher_license : 
        #print(f"{row.doi}\t has repo or publisher licence")
        return ""

    try :
        req = requests.get(f"https://api.openaccessbutton.org/permissions/{row.doi}")
        res = req.json()
        res = res["best_permission"] # avancer dans l'arborescence
    except : 
        print("doi problem w permissions", row.doi)
        return "" 

    # s'assurer que repo est bien en location
    repository = False
    if res.get("locations") : 
        all_loc = " ".join(res["locations"])
        if "Repository" in all_loc : 
            repository = True

    # si published version autorisé récupérer licence & embargo
    if repository and res.get("version") : 
        if "publishedVersion" in res["version"] : 
            print(f"{row.doi} publishedVersion accepted ! ouraaaaah ")
            return f"publishedVersion ; {res.get('licence')} ; {res.get('embargo_months')}"

    
    ## si on peut deposer laccepted version dans un délai plus court que la loi
    if repository and res.get("version") and res.get("embargo_months") :
        if "acceptedVersion" in res["version"] :
            # fixer ici l'embargo en dessous duquel on récupère l'info
            if isinstance(res["embargo_months"], int): # verifier l'embargo est bien du int
                if res["embargo_months"] < 6 : 
                    print(f"{row.doi} acceptedVersion embargo of {res.get('embargo_months')} months")
                    return f"{res['version']} ; {res.get('licence')} ; {res.get('embargo_months')} months"


def deduce_todo(row) :
    """
    deduire les actions à réaliser ; les indiquer sous formes de texte
    """ 
    
    #1. si possible archiver la publishedVersion 
    if "publishedVersion" in str(row["deposit_condition"]) :
        return "recuperer PDF publisher et mailto auteur pour accord"

    #2. si publisher license AND NOT oa via reop
    if row["oa_publisher_license"] and not row["oa_repo_link"] :
        return "selon licence ajouter PDF publisher"

    #3. si LRN applicable envoyer email incitation
    if row["upw_state"] != "open" and row["has_issn"] : 
        return "mailto auteur pour appliquer LRN"

    #4. si c'est dans HAL, sans lien extérieur et pourtant dispo via upw
    if row["halId"] and row["linkExtId"] == "" and row["upw_state"] == "open" :
        return "verifier identifiants notice"

    #4. si ce n'est pas dans HAL
    if row["halId"] == "" :
        return "creer/retrouver notice"
    


def addCaclLinkFormula (pre_url, post_url, txt) : 
    """
    fonction pour rendre les liens cliquables avec formule de libreOffice 
    """

    if post_url : #permet de filtrer si la cellule est vide
        post_url, txt  = str(post_url) , str(txt)
        # pour les liens publisher et repo on coupe au 20 premiers caractères
        if txt.startswith("http") : 
            txt = txt[txt.index("/")+2 : ]
            txt = txt[4: 25] if txt.startswith("www") else txt[: 20]
        
        return '=LIEN.HYPERTEXTE("'+pre_url + post_url + '";"' + txt + '")' 



## ____________old________________

# def query_perm(doi) :
#     """
#     # retrieve data from permission API https://api.openaccessbutton.org/permissions
#     """ 
    
#     try :
#         req = requests.get(f"https://api.openaccessbutton.org/permissions/{doi}")
#         res = req.json()
#     except : 
#         print("doi problem w permissions", doi)
#         return {}
    

#     # avancer dans l'arborescence
#     res = res["best_permission"]

#     # s'assurer que le lieu de dépôt est bien un entrepot
#     repository = False
#     if "Repository" in res.get("locations") : 
#         repository = True


#     ## si published version , récupérer licence & embargo
#     if repository and res.get("version") == "publishedVersion" : 
#         print(f"{doi} publishedVersion accepted ! ouraaaaah ")
#         return {
#             "deposit_condition" : "publishedVersion" + " ; " + res.get("licence") + " ; " + res.get("embargo_months")
#         }

#     ## si les droits s'exercent sur l'acceptedVersion et que l'embarbo est moindre que la LRN
#     if repository and res.get("version") == "acceptedVersion" and res.get("embargo_months") < 12 : 
#         print(f"{doi} acceptedVersion embargo of {res['embargo_months']} months")
#         return {
#             "deposit_condition" : res["version"] + " ; " + res.get("licence") + " ; " + str(res["embargo_months"]) + " months"
#         }
