Code réalisé dans le cadre du [CasuHalathon 2021](https://casuhal2021.sciencesconf.org/resource/page/id/8) permettant de repérer les publications d'un établissement pouvant être déposées en texte intégral dans HAL.


## Fonctionnement

Récupérer les DOIs (scanR et autres bases), les enrichir avec HAL, Unpaywall et Permissions. Selon les données récoltées déduire 5 actions à réaliser manuellement : 

1. **Récupérer le PDF publisher et mailto auteur pour accord** 

la politique du publisher autorise le partage en archive ouverte de la version éditée. Reste à contacter l'auteur pour avoir son accord.

2.  **Selon licence ajouter PDF editeur**

la publication est en accès ouvert sur le site du publisher avec présence d'une licence. Si celle-ci le permet (CC-BY ...) ajouter le PDF dans HAL. Nota : le code cible les publications qui ne sont pas déjà dans une archive ouverte (logique de pérennisation)

3. **Mailto auteur pour appliquer LRN**

Solliciter l'auteur afin qu'il applique la LRN.

4. **Verifier identifiants notice**

La publication est dans HAL et Unpaywall l'a trouvée en accès ouvert sur le web mais HAL n'a pas fait le lien (métadonnée *linkExtId*). Vérifier les identifiants (DOI, Arxiv) de la notice HAL .

5. **Creer/retrouver notice**

le DOI n'a pas été trouvé dans HAL. Vérifier par le titre si une notice correspondante n'est pas déjà présente sinon l'a créer.

<br />

## Reproduire pour son établissement

- Assurez vous de pouvoir lire, modifier, exécuter des notebook Jupyter
- Télécharger le .zip du projet
- Renseigner votre email pour les requêtes Unpaywall dans le fichier _casuhal_utils.py_ ligne 40
- Ouvrer le notebook  _2021_halathon.ipynb_ 
- Réaliser toutes les étapes du notebook
- Ouvrir le tableau produit _data\dois_a_traiter_formula.csv_ avec libreOffice

**Tester en ligne**

[![Binder](https://mybinder.org/badge_logo.svg)](https://hub.gke2.mybinder.org/user/ml4rrieu-halathon-j1jiw4ew/notebooks/2021_halathon.ipynb)


<br />

## Schéma de données

| métadonnée           |     explication                                                              |     exemple                                  |
|----------------------|------------------------------------------------------------------------------|----------------------------------------------|
| halId                |                                                                              |                                              |
| linkExtId            | disponibilité de la publication à l'extérieur de HAL                         | openaccess, arxiv, pubmedcentral, itsex       |
| upw_state            | statut d'accès ouvert dans Unpaywall                                         | open, closed, missing                        |
| published_date       |                                                                              |                                              |
| oa_publisher_license | licence présente sur le site de l'éditeur                                    | CC-BY                                        |
| oa_publisher_link    | lien vers le PDF sur le site de l'éditeur                                    |                                              |
| oa_repo_link         | lien vers le PDF disponible en archive                                       |                                              |
| deposit_condition    | les conditions pour le dépôt en archive                                      | acceptedVersion ; cc-by-nc-nd ; 2021-01-01   |
| todo                 | action à réaliser manuellement                                               |                 |

<br />

### Outils

- Notebook scanr [récupérer les DOI de son établissement](https://github.com/MinistereSupRecherche/bso/blob/master/notebooks/OA_perimetre_specifique.ipynb)
- [Unpaywall](https://www.unpaywall.org/)
- [Persmissions](https://shareyourpaper.org/permissions)

<br />


### Statistiques

pour l'université de Paris avec les DOIs de 2021 venant de Scopus
```
nb de DOI a traiter                                     1063
mailto auteur pour appliquer LRN                        568
creer/retrouver notice                                  266
selon licence ajouter PDF editeur                       208
verifier identifiants notice                              5
recuperer pdf publisher et mailto auteur pour accord      5

```
Partagez les votre en issue dans github 