# OpenEuroLLM Non-Web-Data Guide

This guide and repository compiles information and useful scripts about the acquisition of non-web-data for the OpenEuroLLM project.  

The task of gathering linguistic data different from web data content implies several steps such as:

1) Locating permissively licensed data sources (mainly sets of files)
2) Extracting file URLs
3) Downloading the files
4) Uploading the files to a server
5) Downloading the files to a cluster
6) Processing the files to extract text

This guide will be growing as we complete a first cycle through all the steps. 

<h2>1. Locating data sources</h2>

<h3>1.0 Basic information</h3>

We are looking for websites containing sets of files with relevant linguistic data in any format (pdf, docx, txt, mp3, mp4, etc.) with an explicit open license. 

We do not want the text present on the web page itself, like HTML or similar, but downloadable documents whose text is not visible using web browsers. The web content (HTML) is supposed to be already gathered in web datasets.

<h3>1.1 Picking a language</h3>
We will look for sources in particular languages. The languages of interest are defined in the following [file](https://github.com/OpenEuroLLM/training-data-catalogue/blob/main/languages).

Languages with less resources sould be prioritized. A hint for picking your next language could be the following ranking showing the biggest web dataset available for the languages of interest, leaving out English, Italian, French, German, Portuguese and Spanish: 

![image](images/oellm-languages-web-dataset.png)

Please log your team name in the following table once you pick a language and start working with it. These are all the priority languages with information about data availability and the team in charge for a particular cycle: 


|Language|Data availability| Team in charge (1st cycle)|
|--------|--------------|------------------|
|Albanian|low| | 
|Basque|very low| Prompsit |
|Bosnian|low|  |
|Bulgarian|mid-low|  |
|Catalan|low|  |
|Croatian|low|  |
|Czech|mid|  |
|Danish|mid-low|  |
|Dutch|mid|  |
|Estonian|low|  |
|Finnish|mid-low|  |
|Galician|very low|  |
|Georgian|very-low|  |
|Greek|mid-low|  |
|Hungarian|mid-low|  |
|Icelandic|very-low|  |
|Irish|very-low|  |
|Latvian|low|  |
|Lithuanian|low|  |
|Macedonian|very low|  |
|Maltese|very low|  |
|Norwegian Nynorsk|very low|  |
|Norwegian Bokmal|mid-low|  |
|Polish|mid|  |
|Romanian|mid-low| |
|Serbian|low|  |
|Slovak|mid-low|  |
|Slovenian|low|  |
|Swedish|mid-low|  |
|Turkish|low|  |
|Ukrainian|mid-low|  |

The tiers correspond to the following token availability ranges: very low (<10BT), low (>10-40BT), mid-low (>40-120BT), mid (>120BT).




<h3>1.2 Recording resources in the shared Google sheets</h3>

We share a [Google sheets](https://docs.google.com/spreadsheets/d/1ERMeyCK1gKepeToE2TkwSuv_xYyQbggwaCYIIp3k-Y0/edit?gid=0#gid=0) document where we need to add every data source and its relevant or helpful information. Some of the information has pre-defined dropdown lists. Increasing the options in these lists is possible, but please check carefully if no other preexistent suitable (or near suitable) option is available.

There are also columns without predefined options that need a specific format:

- In DATE_OF_IDENTIFICATION it must be used the DD/MM/YYYY format.

- In the DOWNLOAD_SOURCE column, it is better to use the URLs where the actual data is linked instead of the home page. For example, we would save the following URLs in this website: https://www.argia.eus/multimedia/podcastak and https://www.argia.eus/multimedia instead of just https://www.argia.eus/. This will make the next step much easier. Multiple URLs separated by a line break can be saved in the same cell.

- In MIXED_LANGUAGES, the languages must be separated by a comma (,), always written in the same form as in the LANGUAGE column, or as written before in any column if this language is not present in the LANGUAGE column.

<h3>1.3.    Tips on how to find relevant data </h3>

First, it is recommended to search for government or regional official websites, institutions, ministries or publicly funded associations, looking for sections named “publications” or similar. These public websites used to cite other websites they fund or with which they collaborate. 

Then, looking for official state gazettes, civil/penal codes, constitutions and other public legal documents can lead to good results. 

After that, is may be worth searching for annual reports of banks, big companies, NGOs, etc.

Besides this, the [CC](https://search.creativecommons.org/) search portal may be good to find other types of permissively licensed data. A good idea is to use random words from different topics plus the required format in quotes, for example, ‘gardening “pdf”’ or ‘sports “mp3”’. Looking for radios, televisions or podcasts in this CC searcher is also a good idea to find archived recorded programs.

<h2>2.	Extracting file URLs</h2>
<h3>2.0.	Basic information</h3>

After gathering data sources, it is needed to extract all URLs where every single file is placed.

The first step in this process is to identify the structure of the data on the website. Then, for each document, it is necessary to assemble a JSON file with metadata as in this example:

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

_PATH_ is a combintation of _LANGUAGE_CODE_ + url without the document name. The intention is to mirror the original location of the documents. To create the path the [path.py](src/non_web_oellm/metadata/path.py) script must be used. The "url" parameter correspond to the final URL where the file is downloaded, "base_path" should be the base path in the computer used to download the file + the language code.

_NAME_ corresponds to the file name with extension. The _NAME_ value and the file name must always be the same. This attribute will also be kept empty and filled after the download.

_DOWNLOAD_SOURCE_ is used to store the complete and final URL of the file. This must be a direct access or direct download link. If there is any relevant issue for the download step, this can be explained in the _COMMENTARY_ section. In the download step, if the file contains multiple files inside, like in a ZIP or RAR, the _DOWNLOAD_SOURCE_ value must be the URL of the compressed file. The file must be uncompressed, and every document inside must have its own JSON metadata.

The rest of the metadata is derived from the corresponding rows of the Google sheet document.

![image](images/imagen1.png)

<h3>2.1.	Extracting the final URLs</h3>

Generally, in the data sources found, there are a few types of data structures:

<h4>2.2.1 All the desired links are easily collectable from a single webpage</h4>

In this cases, if pagination is not very long, links can be collected by inspecting the page manually and copying the element that contains them:

![image](images/Imagen2.png)

Then, one can use a simple [Python tool](notebooks/all_files_from_copied_selection.ipynb) to extract URLs:

![image](images/Imagen3.png)

It is also possible to use a regex like `href="(.*?.pdf)"` or other tools but the former is a very quick option.

If, on the other hand, if pagination is very long, one can scrap the box where the files of interest are placed and then extract automatically all file links. In these cases, the [Python tool](notebooks/all_files_in_box_with_pagination.ipynb) can be used. In this example the numbers of the "<a>" tags were used to extract all pagination links:

![image](images/Imagen4.png)
![image](images/Imagen5.png)

There are multiple options even in this page. It is possible to explore URLs using the GET attribute "page":

- https://www.or[...]ault.aspx?page=1

In these cases you need to make sure that the number of pages is consistent, otherwise, if you try to access to some wrong URLs, it is possible that the server blocks your IP.

Another usefull way to visit all the needed pages is to extract always the ">" button, until it is not present. This would need some changes in the [script](notebooks/all_files_in_box_with_pagination.ipynb).

<h4>2.2.2 An ad hoc crawler/method is needed</h4>

Often, it is impossible to only copy and extract links. Some websites need to be analyzed before choosing a valid method. The different examples below show different problems already found and possible approaches to solve them:

- ARGIA: This news site has an interesting podcast section at https://www.argia.eus/.

![image](images/Imagen6.png)

First, access each podcast manually, e.g. https://www.argia.eus/multimedia/menda-bikoitza. Take a moment to explore a bit each podcast topic/domain to refine the info in the shared Google Sheets. 

![image](images/Imagen7.png)

Then, copy the HTML element where each chapter of the podcast is placed. Make sure that all podcasts are visible (e.g. scroll down the page to make the appear) before copying the HTML element.

- Gipuzkoa Official Gazette

The Gipuzkoa Gazette is intended to be explored by date or by keyword:

![image](images/Imagen8.png)

In this case, searching by year was the most sucessful strategy to get all the records. The year, e.g. 1996, was part of the URL in the GET attribute (`_BoletinOficial_WAR_LEEboletinOficialportlet_anio=1996`):

- `https://egoitza.gipuzkoa.eus/eu/gao?p_p_id=BoletinOficial_WAR_LEEboletinOficialportlet&p_p_lifecycle=0&_BoletinOficial_WAR_LEEboletinOficialportlet_d-4021526-p=1&_BoletinOficial_WAR_LEEboletinOficialportlet_myaction=busqueda&_BoletinOficial_WAR_LEEboletinOficialportlet_isAvanzada=false&_BoletinOficial_WAR_LEEboletinOficialportlet_anio=1996`


![image](images/Imagen9.png)

Each year could be processed as a regular page with pagination. In this case, however, it is necessay to do a two step page visit, becasuse the direct link of the final is inside the first one.

![image](images/Imagen10.png)

In similar cases, scraping the whole page and saving the intermediate links in a file can be useful to then, extract the final links in a subsequent step. For example, saving all the links in the above mentioned page in a txt results in:

![image](images/Imagen11.png)

Then, one can visit them to extract the links behind the "PDF" button. Be careful and avoid visiting them all at the same time, because you can overload the server and be banned.

<h2>3.	Downloading the files</h2>

TBC

<h2>4.	Uploading the files to the server</h2>

TBC

<h2>5. Downloading the files to a cluster</h2>
TBC
<h2>6. Processing the files</h2>

TBC
