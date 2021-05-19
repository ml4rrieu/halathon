
Code réalisé dans le cadre du [CasuHalathon 2021](https://casuhal2021.sciencesconf.org/resource/page/id/8) permettant de repérer les publications d'un établissement pouvant être déposées en texte intégral dans HAL. Le code récupère des données sur les publications et déduit des actions à réaliser. Les actions sont à réaliser manuellement.


![bandeau Casuhalathon](https://casuhal2021.sciencesconf.org/data/pages/Bandeau_Casuhalaton.jpg)


## Fonctionnement

Étapes du code : 1. récupérer les DOIs de son établissement. Cela peut être effectué à l'aide d'un fichier local et/ou en utilisant l'API de ScanR. 2. enrichir les DOIs en utilisant HAL, Unpaywall et Permissions. 3. déduire à partir des données reccueillies des actions à réaliser. 
Cinq actions, à réaliser manuellement, sont différenciées : 

* **Récupérer le PDF publisher et mailto auteur pour accord** :green_book: :pencil: 

La politique du publisher autorise le partage en archive ouverte de la version éditée (eg. la revue [Physical Review B](https://aurehal.archives-ouvertes.fr/journal/read/id/153339)). Reste alors à contacter l'auteur pour avoir son accord.

*  **Selon licence ajouter PDF publisher** :green_book:

La publication est en accès ouvert sur le site du publisher avec la mention d'une licence ouverte. Si celle-ci le permet (eg. les Creative Commons) ajouter le PDF dans HAL. Nota : le code cible les publications qui ne sont pas déjà dans une archive ouverte (logique de pérennisation).

* **Mailto auteur pour appliquer LRN** :pencil:

Solliciter l'auteur afin qu'il applique la Loi pour une République Numérique.

* **Vérifier identifiants notice** :link:

La publication est référencée dans HAL, elle est bien marquée _open access_ dans Unpaywall mais HAL n'a pas fait le lien (métadonnée *linkExtId*). Il faut alors vérifier les identifiants (DOI, Arxiv) de la notice.

* **Créer/retrouver notice** :mag_right:

Le DOI n'a pas été trouvé dans HAL. Faites une recherche par titre dans HAL afin de rectifier un éventuel oubli du DOI, sinon créer la notice.

<br />

## Reproduire pour son établissement

- Assurez-vous de pouvoir modifier et exécuter des notebooks Jupyter
- Télécharger le .zip du projet
- Renseigner votre email pour les requêtes Unpaywall dans le fichier _casuhal_utils.py_ ligne 40
- Ouvrir le notebook  _2021_halathon.ipynb_ 
- Réaliser toutes les étapes du notebook
- Ouvrir le tableau produit _data\dois_a_traiter_formula.csv_ avec libreOffice
- Déposez massivement :boom::boom::boom:

**Tester en ligne**

[![Binder](https://mybinder.org/badge_logo.svg)](https://hub.gke2.mybinder.org/user/ml4rrieu-halathon-j1jiw4ew/notebooks/2021_halathon.ipynb)


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
| deposit_condition    | les conditions pour le dépôt en archive                                      | acceptedVersion ; cc-by-nc-nd ; 2021-01-01   |
| todo                 | action à réaliser manuellement                                               | selon licence ajouter PDF publisher          |

<br />

### Outils

- Script ScanR [récupérer les DOI de son établissement](https://github.com/MinistereSupRecherche/bso/blob/master/notebooks/OA_perimetre_specifique.ipynb)
- [Unpaywall](https://www.unpaywall.org/)
- [Permissions](https://shareyourpaper.org/permissions)

<br />


### Statistiques

pour l'université de Paris avec des DOIs de 2021 venant de Scopus
```
nb de DOI a traiter                                     1062
mailto auteur pour appliquer LRN                        564
creer/retrouver notice                                  273
selon licence ajouter PDF publisher                     204
verifier identifiants notice                              5
recuperer PDF publisher et mailto auteur pour accord      5
```
Partagez les votres en issue dans github 
