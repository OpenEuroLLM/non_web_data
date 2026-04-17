# non_web_data

In this repository we will add the scripts and other indications used for the file extraction of non web data for the OELLM project.

Our task of gathering linguistic data consists of several steps:

`Locate data sources – Extract file URLs and create the metadata in Json format – Download files – Upload to the server`

<h2>1. Locate data sources</h2>

<h3>1.1 Basic information</h3>

The first step is to search websites containing files with relevant linguistic data in any format (pdf, docx, txt, mp3, mp4, etc.) with an explicit open license. We do not want the text present on the web page itself, like HTML or similar, but downloadable documents whose text is not visible using web navigators. This undesired data is supposed to be already gathered by other projects.

The languages of interest are:

|  |     |     |   |
| -------- | --------- | ---------- | ---------- |
| Albanian | Basque    | Bosnian    | Bulgarian  |
| Catalan  | Croatian  | Czech      | Danish     |
| Dutch    | Estonian  | Finnish    | Galician   |
| Georgian | Greek     | Hungarian  | Icelandic  |
| Irish    | Latvian   | Lithuanian | Macedonian |
| Maltese  | Norwegian Nynorsk and Bokmal | Polish     | Romanian   |
| Serbian  | Slovak    | Slovenian  | Swedish    |
| Turkish  | Ukrainian |       |            |

We think that every person/group should work with only one different language at a time to avoid duplications.

<h3>1.2 Add a row to the shared Google sheets</h3>

We shared a [Google sheets](https://docs.google.com/spreadsheets/d/1ERMeyCK1gKepeToE2TkwSuv_xYyQbggwaCYIIp3k-Y0/edit?gid=0#gid=0) document where we need to add every source of data and its relevant or helpful information. If no option in the dropdown lists fits a particular data source, it is possible to increase the options, but this should be done only after checking that there is no other preexistent suitable (or near suitable) tag.

There are also columns without a dropdown list that need a specific format:

- In DATE_OF_IDENTIFICATION it must be used the DD/MM/YYYY format.

- In the DOWNLOAD_SOURCE column, it is better to use the URLs where the data is placed, not only the home page. For example, I saved these URLs in this website: https://www.argia.eus/multimedia/podcastak and https://www.argia.eus/multimedia, instead of https://www.argia.eus/ . This will make the next step much easier. I used to save these multiple URLs separated by a line break in the same cell.

- In MIXED_LANGUAGES the languages must be separated by a comma (,), always written in the same form as in the LANGUAGE column, or as written before in any column if this language is not present in the LANGUAGE column.

<h3>1.3.	How I found relevant data in the Basque test</h3>

First, I searched government or regional official websites, institutions, ministries or publicly funded associations, looking for sections named “publications” or similar. These public websites used to cite other websites they fund or with which they collaborate. Then I looked for official state gazettes, civil/penal codes, constitutions and other public legal documents. After that, I searched annual reports of banks, big companies, NGOs, etc.
Moreover, I used the [CC](https://search.creativecommons.org/) search portal to find data. I used random words from different topics plus the format I wanted in quotes, for example, ‘gardening “pdf”’ or ‘sports “mp3”’. Then I looked for radios, televisions or podcasts in this CC searcher, because they used to archive their recorded programs.

<h2>2.	Extract file URLs</h2>
<h3>2.1.	Basic information</h3>

After gathering data sources, it is needed to extract all URLs where every single file is placed.

The first step in this process is to identify the structure of the data on the website. Then, for each document, it is necessary to assemble the JSON metadata format as in this example:

```
{
    "PATH": "eus/www.euskariana.euskadi.eus/euskadibib/es/media/group",
    "NAME": "1557223.do", 
    "LANGUAGE_CODE": "eus", 
    "MACRO_LANG": "eus", 
    "SCRIPT_LANG": "Latn", 
    "LANGUAGE": "Basque", 
    "VARIANT": "Batua (Standard Basque)", 
    "TOPIC": "Culture", 
    "DATA_TYPE": "pdf", 
    "SOURCE_ORGANIZATION": "Euskariana", 
    "LICENSE": "CC-BY-NC-SA-4.0", 
    "DOWNLOAD_SOURCE": "https://www.euskariana.euskadi.eus/euskadibib/es/media/group/1557223.do", 
    "MIXED_LANGUAGES": [“Spanish”, “French”], 
    "COMMENTARY": “”, 
    "DATASET_NAME_OR_DESCRIPTION": "Euskariana", "DATE_OF_IDENTIFICATION": "31/01/2026",
    "CONTACT”: "”
}
```

_PATH_ must be created as _LANGUAGE_CODE_ + url without the document name. The intention is to mirror the original location of the documents. In the OELLM database, files will be saved following the _PATH_ value. Regarding the ELDA team, metadata that it is supposed to be sent to the Prompsit team should be empty in the _PATH_ value. Prompsit team will fill this value using always the URL and the same logic present in [path.py](src/non_web_oellm/metadata/path.py).

_NAME_ corresponds to the file name with extension. The _NAME_ value and the file name must always be the same. This attribute will also be kept empty by the ELDA team and filled after the download by Prompsit, by far.

_DOWNLOAD_SOURCE_ is used to store the complete and final URL of the file. This must be a direct access or direct download link. If there is any relevant issue for the download step, this can be explained in the _COMMENTARY_ section. In the download step, if the file contains multiple files inside, like in a ZIP or RAR, the _DOWNLOAD_SOURCE_ value must be the URL of the compressed file. The file must be uncompressed, and every document inside must have its own JSON metadata.

The rest of the metadata should derive from the corresponding row of the Google sheets document.

![image](images/imagen1.png)

<h3>2.2.	How I extracted the final URLs</h3>

Generally, in the data I found, there are a few types of data structures:

<h4>2.2.1 All the desired links are easily collectable from a single webpage</h4>

In this cases, if there is not a long pagination, I used to only inspect the page manually and copy the element that contains the links:

![image](images/Imagen2.png)

Then I used a simple [Python tool](notebooks/all_files_from_copied_selection.ipynb) to extract URLs:

![image](images/Imagen3.png)

It is also possible to use a regex like `href="(.*?.pdf)"` or other tools, but for me this is the quicker option.

If, on the other hand, a long pagination is found, I used to scrap the box where the files of interest are placed and then extract automatically all file links. I used a different [Python tool](notebooks/all_files_in_box_with_pagination.ipynb). In this example case I used the numbers of the "<a>" tags to extract all pagination links:

![image](images/Imagen4.png)
![image](images/Imagen5.png)

There are multiple options even in this page. It is possible to explore URLs using the GET attribute "page":

- https://www.or[...]ault.aspx?page=1

In these cases you need to ensure that the number of pages is consistent, otherwise, if you try to access to some wrong URLs, it is possible that the server blocks your IP.

Another usefull way to visit all the needed pages is to extract always the ">" button, until it is not present. This would need some changes in the [script](notebooks/all_files_in_box_with_pagination.ipynb) mencioned before.

<h4>2.2.2 An Ad Hoc crawler/method is needed</h4>

Often it is impossible to only copy and extract links. Some websites need to be analyzed before choosing a valid method. In this part, I only can give you some different examples and how I resolved the problems I encountered:

- ARGIA

First, acceded to each podcast manually:

![image](images/Imagen6.png)

After that, I copied the HTML element where each chapter of the podcast is placed. In this moment, I saw that not all chapters where in the HTML. Chapters actually appear (are generated) when you scroll down the page, so I decided to scroll to the end every page and then I copied the HTML element.

![image](images/Imagen7.png)

In this step I took the oportunity to explore a bit each podcast to better fit the topic/domain of each podcast, rather than use the generic one I added to the Google Sheets ("Culture").

- Gipuzkoa Official Gazette

The Gipuzkoa Gazette is intended to be explored by date or by keyword:

![image](images/Imagen8.png)

The easiest way I found to extract all links were to search by year. The first year I found was 1996 and I saw that the URLs saved this information in the GET attribute in the URL (`_BoletinOficial_WAR_LEEboletinOficialportlet_anio=1996`):

- `https://egoitza.gipuzkoa.eus/eu/gao?p_p_id=BoletinOficial_WAR_LEEboletinOficialportlet&p_p_lifecycle=0&_BoletinOficial_WAR_LEEboletinOficialportlet_d-4021526-p=1&_BoletinOficial_WAR_LEEboletinOficialportlet_myaction=busqueda&_BoletinOficial_WAR_LEEboletinOficialportlet_isAvanzada=false&_BoletinOficial_WAR_LEEboletinOficialportlet_anio=1996`


![image](images/Imagen9.png)

Each year could be processed as a regular page with pagination. It is necessay, however, to do a two step page visit, becasuse the direct link is inside the first one.

![image](images/Imagen10.png)

When I need to work with a two or three steps link I like to scrap all the page, save the intermediate links in a file and then, at another time, extract the next step. For example, I saved all the links to the resources in a txt:

![image](images/Imagen11.png)

Then I visited all of them to extract the link behind the "PDF" button. I do not like to make all in the same time, because you can overload the server and it is more likely to be banned.
