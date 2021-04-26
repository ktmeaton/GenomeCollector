# Configuration File Instructions

The configuration files contain all the options required to run the NCBImeta program.
They consist of 6 variables:

```yaml
OUTPUT_DIR
EMAIL
DATABASE
TABLES
SEARCH_TERMS
TABLE_COLUMNS
```

The names of these variables should not be altered in any way. Just their assigned value.

## 1) OUTPUT_DIR

```yaml
  OUTPUT_DIR : ../NCBImeta_ouput/
```

Can be a relative or absolute path. Note that when using a relative path, it will be relative from wherever you are EXECUTING the program (not necessarily from where the config file is located).

If the directory does not exist, it will be created.

## 2) EMAIL

```yaml
  EMAIL : myemailname@domain.com
```

This must be a valid email address for using biopython/NCBI's API.

## 3) API_KEY

```yaml
  API_KEY : a6526gs1h4l3t324th5htl234tlhlt234435
```

[OPTIONAL] This is a valid API key as issued to your account through NCBI. Providing an API key will allow you to fetch 10 records/sec. Otherwise leave blank as in the example config.yaml file.

## 4) FORCE_PAUSE_SECONDS:

```yaml
  FORCE_PAUSE_SECONDS : 0.5
```

The amount of time (in seconds) that the program should forcibly sleep (wait) in between record fetching.

## 5) DATABASE

```yaml
  DATABASE : my_organism_db.sqlite
```

This will be the name of your created database and should not be a path. By default, a "database" directory will be created in your output directory to store this file. If you choose the --flat option at runtime, the database directory will not be created, and it will simply be stored in your selected output directory.

It does not need to end in ".sqlite", but you may find that helpful as your computer will associate that with an appropriate viewer application.

## 6) TABLES

```yaml
  TABLES :
    - Assembly
    - BioSample
```

A line-separated list (beginning with dashes) containing the names of all tables you want to search in. Note that these must match exactly to SEARCH TERMS and TABLE COLUMNS.

## 7) SEARCH_TERMS

```yaml
  SEARCH_TERMS :
    - Assembly : Yersinia pestis[Orgn]
    - BioSample : Yersinia pestis[Orgn] and 2017[Publication Date]
```

This list contains the names of all tables and corresponding ENTREZ search queries.
Building an appropriate search query is sometimes the most difficult part.
Test your queries in the web browser first before committing  ([NCBI Web Portal](https://www.ncbi.nlm.nih.gov/)).

Note that the table names must match exactly to TABLES and TABLE COLUMNS.

\*Note that record retrieval is currently limited to 9999999 records per table. This can be changed locally in your program by searching for the first instance of "retmax" in the NCBImeta source file (ncbimeta/NCBImeta).

## 8) TABLE_COLUMNS

```yaml
  TABLE_COLUMNS :

    - Assembly :
      - AssemblyAccession : AssemblyAccession
      - AssemblyBioSampleAccession : BioSampleAccn
      - AssemblyOrganism : Organism

    - BioSample :
      - BioSampleAccession : Accession
      - BioSampleBioProjectAccession : Link, label
      - BioSampleSRAAccession: Id, SRA, db
      - BioSampleTitle: Title
```

This contains metadata elements selected from the schema files (schema/). They should be copy-pasted from the appropriate schema file if adding additional lines. The whitespace (number of spaces/indendentation) is very important in this file! When copying and pasting, don't delete spaces before the dash.

Note that the Table Names must match exactly to SEARCH TERMS and TABLES.
