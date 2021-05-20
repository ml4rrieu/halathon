import pandas as pd, numpy as np, requests, json

def query_hal(doi) :

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
	req = requests.get( f"https://api.unpaywall.org/v2/{doi}?email=hal.dbm@listes.u-paris.fr")
	res = req.json()

	# if not in upw
	if res.get("message") and  "isn't in Unpaywall" in res.get("message") :
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
			#on ne peut transmettre les donnée None car le df.at pose pb
			temp["oa_publisher_license"] = res["best_oa_location"]["license"] if res["best_oa_location"]["license"] else ""
			temp["oa_publisher_link"] = res["best_oa_location"]["url_for_pdf"] if res["best_oa_location"]["url_for_pdf"] else res["best_oa_location"]["url_for_landing_page"] 

		if res["best_oa_location"]["host_type"] == "repository" : 
			temp["oa_repo_link"] = res["best_oa_location"]["url_for_pdf"]


	if best_loc_is_publisher : 
		for elem in res["oa_locations"] :
			if elem["host_type"] == "repository" : 
				temp["oa_repo_link"] = elem["url_for_pdf"]
				break #on prend la 1er oa_location de hostype repository
		
	return temp



def enrich_w_upw(df) : 
	
	print(f"nb DOI a verifier dans upw \t{len(df)}")
	df.reset_index(drop=True, inplace = True)
	for row in df.itertuples() :
		
		print_progression("upw", row.Index, len(df))	
		upw_data = query_upw(row.doi)
		for field in upw_data :
			try : 
				df.at[row.Index, field] = upw_data[field]
			except : 
				print("\n\npb ac doi upw\n", row.doi, '\n\n', upw_data)
				break
	print("upw 100%")
	return df


def query_perm(doi) : 
	
	try :
		req = requests.get(f"https://permissions.shareyourpaper.org/doi/{doi}")
		res = req.json()
	except : 
		print("doi problem w permissions", doi)
		return {}
	
	try : 
		res["authoritative_permission"]["application"].get("can_archive")
	except : 
		return {}

	if not res["authoritative_permission"]["application"].get("can_archive") : 
		return {} 

	res = res["authoritative_permission"]["application"]["can_archive_conditions"]	

	if res["permission_required"] or\
	res["author_affiliation_requirement"] or\
	res["author_affiliation_role_requirement"] or\
	res["author_affiliation_department_requirement"] or\
	res["author_funding_requirement"] or\
	res["author_funding_proportion_requirement"] : 
		return {}


	# continuer si accepterVersion ou publishedVersion
	only_submitted_version = True
	if "acceptedVersion" in res["versions_archivable_standard"] or "publishedVersion" in res["versions_archivable_standard"] : 
		only_submitted_version = False
	
	if only_submitted_version : 
		return {}

	try :
		res["versions_archivable_standard"].remove("submittedVersion")
	except : 
		pass

	# continuer seulement si on peut archiver dans un repository 
	if "repository" not in " ".join(res["archiving_locations_allowed"]) : 
		return {}
	
	license = ",".join(res["licenses_required"]) if res["licenses_required"] else ""
	embargo = str(res["postprint_embargo_end_calculated"]) if res["postprint_embargo_end_calculated"] else "" 

	return{
		"deposit_condition" : ",".join(res["versions_archivable_standard"]) + " ; " +license+ " ; " +embargo
	}
	

def enrich_w_permissions (df) : 

	df["deposit_condition"] = ""
	
	for row in df.itertuples():
		if row.oa_repo_link or row.oa_publisher_license : 
			continue

		#print(f"verif deposit policy for this \t {row.doi}")
		perm_data = query_perm(row.doi)

		for field in perm_data : 
			df.at[row.Index, field] = perm_data[field]
	print("permissions 100%")
	return df


def deduce_todo(row) : 
	
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
	"""fonction pour rendre les liens cliquables avec formule de libreOffice """
	if post_url :
		post_url, txt  = str(post_url) , str(txt)
		# pour les liens publisher et repo on coupe au 20 premiers caractères
		if txt.startswith("http") : 
			txt = txt[txt.index("/")+2 : ]
			txt = txt[4: 25] if txt.startswith("www") else txt[: 20]
		
		return '=LIEN.HYPERTEXTE("'+pre_url + post_url + '";"' + txt + '")' 