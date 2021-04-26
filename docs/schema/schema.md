# Metadata Selection from NCBI Schema

The schema files are designed to act as a text 'menu' for users to select desired metadata to retrieve. Lines from the schema can be copy and pasted into the "TABLE_COLUMNS" section of a configuration file (config.yaml). Consult the comprehensive file example/config.yaml for a template.

The schema is of the following format:

```yaml
    - BioSampleOrganism: OrganismName
```

The left side (key) will be the name of the column in the final table and can be changed to whatever the user desires. However, please avoid putting spaces in your column names.  The right side is a keyword specific to the biopython API and should not be altered.

(Note: It is highly recommended to keep the default column names the author has provided. These ensure clarity of which database the information comes from. In addition, the default column names are all unique allowing for any combination of full-joins or partial-joins of tables)

The whitespace (number of spaces) before the dash is important to keep intact when copying and pasting to your configuration file. Please do not delete spaces before the dash, as the line must remain properly indented.

The following sections should only be read if you want to gain a deeper understanding of the XML parsing method, or if you want to experiment with adding new metadata fields from NCBI that have not been implemented yet by the author.

## 1) Retrieving a simple node value with biopython from the metadata xml.

User selects:

```yaml
    - AssemblyAccession : AssemblyAccession
```

XML from NCBI:

```xml
    <AssemblyAccession>GCA_003086155.1</AssemblyAccession>
```

Retrieves Accession Number "GCA_003086155.1" and stores it under column "AssemblyAccession".

## 2) Retrieving an attribute value (not a node value)

User selects:

```yaml
    - SRAExperimentAccession : Experiment, accession
```

XML from NCBI:

```xml
    <EXPERIMENT alias="EXT00317997" accession="SRX4321294">
```

Retrieves accession "SRX4321294" and stores it under "SRAExperimentAccession"
The value in this case, is a list of 2 elements:

```yaml
    : Experiment, accession
```

The first value ("Experiment"), is the name of the node.
The second value ("accession") is the attribute to target.

Note that the list of elements are values separated by a comma and a single space.
This is mandatory and used for parsing/splitting them into separate elements.

## 3) Retrieving a simple node value by specifying an attribute value.

User selects:

```yaml
    - BioSampleCollectionDate : Attribute, harmonized_name, collection_date
```

XML from NCBI:

```xml
    <Attribute display_name="collection date" harmonized_name="collection_date" attribute_name="collection date">2006</Attribute>
    <Attribute display_name="host taxonomy ID" harmonized_name="host_taxid" attribute_name="host taxid">10090</Attribute>
```

Retrieves collection date "2006 "and stores it under "BioSampleCollectionDate".
The host taxid line is not mistakenly processed instead.

The value in this case, is a list of 3 elements:

```yaml
    : Attribute, harmonized_name, collection_date
```

The first value ("Attribute"), is the name of the node.
The second value ("harmonized_name") is the attribute to match.
The third value ("collection_date") is the attribute's value to match.

## 4) Retrieving simple node values that don't have unique names or attributes.

User selects:

```yaml
    - AssemblyGenbankBioprojectAccession : GB_BioProjects, BioprojectAccn
```

XML from NCBI:
In the following example, note how the node "BioprojectAccn" is not a unique name, as there is both a GenBank and RefSeq Bioproject Accession.

```xml
    <GB_BioProjects>
      <Bioproj>
        <BioprojectAccn>PRJNA31257</BioprojectAccn>
        <BioprojectId>31257</BioprojectId>
      </Bioproj>
    </GB_BioProjects>


    <RS_BioProjects>
      <Bioproj>
        <BioprojectAccn>PRJNA168</BioprojectAccn>
        <BioprojectId>168</BioprojectId>
    </Bioproj>
    </RS_BioProjects>
```

Retrieves accession number "PRJNA31257" and stores it under "AssemblyGenbankBioprojectAccession".
The value in this case, is a list of 2 elements:

```yaml
    : GB_BioProjects, BioprojectAccn
```

This can be built from any number of elements, and provides a directional path to follow to find a node.
Note that it must be IN ORDER, but can skip intermediate values (ex. node \<Bioproj\> is missing from the list).

## 5) Advanced XPath Queries

Advanced users can pass an XPath query by specifying the first element in the comma separated list as "XPATH". Following that you can specify an actual XPath query to be executed.

User selects:

```yaml
    - BioProjectAccession: XPATH, //Links/Link[@target='bioproject']/@label
```

XML from NCBI:

```xml
    <Links>
      <Link type="url" label="GEO Sample GSM3995467">https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM3995467</Link>
      <Link type="entrez" target="bioproject" label="PRJNA558013">558013</Link>
    </Links>
```

Retrieves accession number "PRJNA558013" and stores it under "BioProjectAccession".

## 6) Customizing Schema

To puzzle out additional xml criteria for your search query, search for the line:

```python
    #print(etree.tostring(ID_root).decode())
```

And uncomment it (delete the \#  at the beginning).

When NCBImeta is run now, it will print out the xml for each record. It is recommended to redirect this output to a file, example:

```bash
NCBImeta --config example/config.yaml > config_xml_output.txt
```

Also please read through <https://www-ncbi-nlm-nih-gov.libaccess.lib.mcmaster.ca/biosample/docs/attributes/> for the BioSample database attributes.
