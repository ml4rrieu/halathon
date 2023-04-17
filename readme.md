HALathon : identifier automatiquement les publications pouvant être déposées dans HAL! Les données sur les publications sont récupérées (HAL, [Unpaywall](https://unpaywall.org) et [Permissions](https://shareyourpaper.org/permissions) ) et des actions, à réaliser manuellement, sont déduites.


## Fonctionnement

1. Récupérer les DOIs de son établissement. A effectuer depuis un fichier local ou depuis l'API de ScanR
2. Enrichir les données en utilisant HAL, Unpaywall et Permissions
3. Déduire à partir des données reccueillies des actions à réaliser

## Actions déduites à réaliser manuellement

* **Récuperer le PDF éditeur et écrire a l'auteur pour accord** :green_book: :pencil: 

La publication n'est pas en accès ouvert mais la politique du publisher autorise le partage en archive de la version éditée (eg. la revue [Physical Review B](https://aurehal.archives-ouvertes.fr/journal/read/id/153339)). Reste alors à contacter l'auteur pour avoir son accord.

*  **Selon la licence ajouter le PDF éditeur** :green_book:

La publication est en accès ouvert sur le site du publisher avec la mention d'une licence. Si celle-ci le permet (Creative Commons) ajouter le PDF dans HAL. Nota : le code cible les publications qui ne sont pas déjà dans une archive ouverte (logique de pérennisation).

* **Ecrire à l'auteur pour appliquer la LRN** :pencil:

La publication n'est pas en accès ouvert, solliciter l'auteur afin qu'il applique la Loi pour une République Numérique.

* **Vérifier les identifiants de la notice** :link:

La publication est référencée dans HAL, elle est bien marquée _open access_ dans Unpaywall mais HAL n'a pas fait le lien (métadonnée *linkExtId*). Il faut alors vérifier les identifiants (DOI, Arxiv) de la notice.

* **Créer ou retrouver la notice** :mag_right:

Le DOI n'a pas été trouvé dans HAL. Faites une recherche par titre dans HAL afin de rectifier un éventuel oubli du DOI, créer la notice si nécessaire.

<br />

## Reproduire pour son établissement

- Télécharger le .zip du projet
- Personnaliser _casuhal_utils.py_ : renseigner l'embargo maximal à considérer (l'enjeu est de savoir si la politique du publisher est plus permissive que la LRN), renseigner un email pour les requêtes unpaywall
- Ouvrir le notebook  _2022_halathon.ipynb_ 
- Exécuter toutes les cellules
- Ouvrir le tableau produit _data\dois_a_traiter_formula.csv_ avec libreOffice
- Déposez massivement :boom::boom::boom:

**Tester en ligne**

[![Binder](https://mybinder.org/badge_logo.svg)](https://hub.gke2.mybinder.org/user/ml4rrieu-halathon-j1jiw4ew/notebooks/2022_halathon.ipynb)


<br />

## Schéma de données

| métadonnée           |     explication                                                              |     exemple                                  |
|----------------------|------------------------------------------------------------------------------|----------------------------------------------|
| halId                |                                                                              |                                              |
| linkExtId            | disponibilité de la publication à l'extérieur de HAL                         | openaccess, arxiv, pubmedcentral, itsex      |
| upw_state            | statut d'accès ouvert dans Unpaywall                                         | open, closed, missing                        |
| published_date       |                                                                              |                                              |
| oa_publisher_license | licence présente sur le site de l'éditeur                                    | CC-BY                                        |
| oa_publisher_link    | lien vers le PDF sur le site de l'éditeur                                    |                                              |
| oa_repo_link         | lien vers le PDF disponible en archive                                       |                                              |
| deposit_condition    | les conditions pour le dépôt en archive                                      | publishedVersion ; cc-by ; 2 months   |
| todo                 | action à réaliser manuellement                                               | selon licence ajouter PDF publisher          |

<br />

### Outils et API utilisés

- [Unpaywall](https://www.unpaywall.org/)
- [Permissions](https://shareyourpaper.org/permissions)
- [HAL](https://api.archives-ouvertes.fr/docs)
- Script ScanR [récupérer les DOI de son établissement](https://github.com/MinistereSupRecherche/bso/blob/master/notebooks/OA_perimetre_specifique.ipynb)



<br />


### Statistiques


Halathon 2023-05 Université Paris Cité (FacultéSanté ). Scopus
```
nb de DOI a traiter                                          905
ecrire a l auteur pour appliquer la LRN                      428
selon la licence ajouter le PDF editeur                      308
creer ou retrouver la notice                                 135
recuperer le PDF editeur et ecrire a l auteur pour accord     24
verifier les identifiants de la notice                         5
```

Halathon 2022-05 Université Paris Cité (Faculté Sciences + IPGP). Scopus. 500 récentes publications. 
```
nb de DOI a traiter                                          329

creer ou retrouver la notice                                 123
ecrire a l auteur pour appliquer la LRN                      119
selon la licence ajouter le PDF editeur                       66
recuperer le PDF editeur et ecrire a l auteur pour accord     15
verifier les identifiants de la notice                         2
```


CasuHalathon 2021-06 Université Paris Cité. Scopus. Publications de l'année
```
nb de DOI a traiter                                     1062
mailto auteur pour appliquer LRN                        564
creer/retrouver notice                                  273
selon licence ajouter PDF publisher                     204
verifier identifiants notice                              5
recuperer PDF publisher et mailto auteur pour accord      5
```



Partagez les votres en issue dans github 

<br />
<br />

-------

Mémo Université Paris Cité

* req Scopus Santé

`
AF-ID(60123803) OR AF-ID(60106282) OR AF-ID(60210102) OR AF-ID(60210145) OR AF-ID(60210142) OR AF-ID(60026040) OR AF-ID(60123678) OR AF-ID(60123713) OR AF-ID(60210107) OR AF-ID(60123665) OR AF-ID(60031594) OR AF-ID(60123804) OR AF-ID(60123784) OR AF-ID(60123816) OR AF-ID(60210101) OR AF-ID(60123697) OR AF-ID(60210185) OR AF-ID(60123774) OR AF-ID(60210109) OR AF-ID(60136279) OR AF-ID(60210100) OR AF-ID(60210108) OR AF-ID(60210169) OR AF-ID(60105728) OR AF-ID(60210154)
`

* req scopus faculté S&H

`(AF-ID(60120303) OR AF-ID(60123643) OR AF-ID(60210180) OR AF-ID(60123161) OR AF-ID(60136261) OR AF-ID(60117541) OR AF-ID(60106086) OR AF-ID(60119214) OR AF-ID(60123637) OR AF-ID(60123696) OR AF-ID(60210118) OR AF-ID(60123629) OR AF-ID(60123670) OR AF-ID(60126107) OR AF-ID(60123675) OR AF-ID(60210117) OR AF-ID(60210182) OR AF-ID(60123642) OR AF-ID(60210166) OR AF-ID(60210148) OR AF-ID(60210170) OR AF-ID(60123662) OR AF-ID(60210181) OR AF-ID(60123653) OR AF-ID(60210168) OR AF-ID(60210171) OR AF-ID(60210144) OR AF-ID(60110966) OR AF-ID(60198731) OR AF-ID(60110705) OR AF-ID(60210157)`

* req Scopus faculté Sciences + IPGP

` AF-ID(60106184) OR AF-ID(60105477) OR AF-ID(60123679) OR AF-ID(60123680) OR AF-ID(60109179) OR AF-ID(60180341) OR AF-ID(60123773) OR AF-ID(60210112) OR AF-ID(60210114) OR AF-ID(60123709) OR AF-ID(60123712) OR AF-ID(60123710) OR AF-ID(60112048) OR AF-ID(60180347) OR AF-ID(60005370) OR AF-ID(60105746) OR AF-ID(60004833) OR AF-ID(60210214) OR AF-ID(60106138) OR AF-ID(60123660) OR AF-ID(60123640) OR AF-ID(60210110) OR AF-ID(60210113) OR AF-ID(60123672) OR AF-ID(60123663) OR AF-ID(60123666) OR AF-ID(60028894) OR AF-ID(60123652) OR AF-ID(60122451) OR AF-ID(60072945) OR AF-ID(60210266) OR AF-ID(60157983) OR AF-ID(60111003) OR AF-ID(60003174) OR AF-ID(60210111) OR AF-ID(60123671) OR AF-ID(60123695) OR AF-ID(60123705) OR AF-ID(60072969) OR AF-ID(60106185) OR AF-ID(60210186) OR AF-ID(60210184) OR AF-ID(60031186) OR AF-ID(60001970)`