# dump_wiki_harman


Récupération et parsing d'un ficher d'archive de wikipedia

Les tests réalisés ont été faits avec le ficher [latest-pages-articles1](https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-pages-articles1.xml-p3p275787.bz2) du site [https://dumps.wikimedia.org](https://dumps.wikimedia.org) a télécharger (pour des raisons d'espaces je ne le stock pas dans le git)


usage :
```c
python3 main.py "path/du/fichier" nombre_d_article_a_traiter
```
si le nombre est à -1 le programme traitera tous les articles du document

Le parser recupere les éléments article par article, en gardant le titre et le texte de l'article
Ensuite le texte est traité pour récupérer les éléments voulus
* Les catégories sont extraites
* la partie en dessus de "== Notes et références ==" est supprimée (peu utile pour de l'analyse de phrases)
* les blocs [[]] sont traités puis les blocs resemblant le plus a de la géo sont retaggés(commençant par une majuscule ou jardin, grottes, parc, chutes, col. Le parsing n'est pas tres efficace puisqu'il prends aussi les noms propres)
* les dates sont transformées
* et le reste des éléments ne faisan pas parti des articles sont supprimés (Article détaillé, Ref, ref)
* Le text est séparé en sous ensembles en fonction des chapites, et les ensembles sont splités en phrases.
* Les éléments sont ensuite réunis en format json et envoyés dans un dossier
