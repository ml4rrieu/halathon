Code réalisé dans le cadre du [CasuHalathon 2021](https://casuhal2021.sciencesconf.org/resource/page/id/8) permettant de repérer les publications d'un établissement pouvant être déposées en texte intégral dans HAL.

**Idée**
Effectuer le maximum de dépôt en autonomie, solliciter les auteurs en dernier recours.

**Fonctionnement**
Récupérer les DOIs via ScanR, les enrichir avec HAL, Unpaywall et Permissions. Selon les données récoltées déduire 5 actions à réaliser manuellement : 

1. "Récupérer le PDF publisher et mailto auteur pour accord" 
la politique du publisher autorise le partage en archive ouverte de la version éditée. Reste à contacter l'auteur pour avoir son accord.

2.  "Selon licence ajouter PDF editeur"
la publication est en accès ouvert sur le site du publisher avec présence d'une licence. Si celle-ci le permet (CC-BY ...) ajouter le PDF dans HAL. Nota : le code cible les publications qui ne sont pas déjà dans une archive ouverte (logique de pérennisation)

3. "Mailto auteur pour appliquer LRN"
Solliciter l'auteur afin qu'il applique la LRN.

4. "verifier identifiants notice"
La publication est dans HAL et Unpaywall l'a trouvée en accès ouvert sur le web mais HAL n'a pas fait le lien (métadonnée *linkExtId*). Vérifier les identifiants (DOI, Arxiv) de la notice HAL .

5. "creer/retrouver notice"
le DOI n'a pas été trouvé dans HAL. Vérifier par le titre si une notice correspondante n'est pas déjà présente sinon l'a créer.

**Reproduire pour son établissement**
- Assurez vous de pouvoir lire, modifier, exécuter des notebook Jupyter
- Télécharger le .zip du projet
- Renseigner votre email pour les requêtes Unpaywall `casuhal_utils.py` lignes 40
- Ouvrer le notebook  _2021_halathon.ipynb_ 
- Réaliser toutes les étapes
- Ouvrir le tableau produit _dois_a_traiter_formula.csv_ avec libreOffice
- Réaliser toutes les actions mentionnées dans la colonne _todo_

**Schéma de données**

| métadonnée           |     explication                                                              |     remarque                                 |
|----------------------|------------------------------------------------------------------------------|----------------------------------------------|
| halId                |                                                                              |                                              |
| halId                |                                                                              |                                              |
| linkExtId            |                                                                              |                                              |
| upw_state            | statut d'accès ouvert dans Unpaywall                                         | open, closed, missing            |
| published_date       |                                                                              |                                              |
| oa_publisher_license | licence présente sur le site de l'éditeur                                    | CC-BY   |
| oa_publisher_link    | lien vers le PDF sur le site de l'éditeur                                    |  |
| oa_repo_link         | lien vers le PDF disponible en archive                                       |                                              |
| deposit_condition    | les conditions pour le dépôt en archive  _version_ ; _licence_ ; _fin d'embargo_ | acceptedVersion ; cc-by-nc-nd ; 2021-01-01   |
| todo                 | action à réaliser manuellement                                               |                 |

**Statistiques**

**Outil**
- [Récupérer les DOI de son établissements](https://github.com/MinistereSupRecherche/bso/blob/master/notebooks/scanr_utils.py)
- [Unpaywall](https://www.unpaywall.org/)
- [Persmissions](https://shareyourpaper.org/permissions)


**Disclaimer**


**Limites**
les DOI sont ceux de ScanR


**Disclaimer**

> [the information provided] make no legal representations as to the accuracy, completeness, suitability or validity of any data or information on this site and will not be liable for any errors or omissions in this data and information or for any losses, injuries or damages arising from its display or use

[Permissions](https://shareyourpaper.org/permissions/about#disclaimer)