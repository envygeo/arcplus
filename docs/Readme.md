# Arcpy and ArcObjects "Data Type" reference

I'm tired of looking up data type definitions in hard to use PDF. So here are better renditions of Esri's [Geoprocessing_data_types.pdf][0] by way of the most excellent tool for liberating data from PDF: [Tabula][1].

View the result via **RawGit**: **[Geoprocessing_data_types.html][4]**

## Processing workflow

 1. pdf >> Tabula --> csv, json
    2. Excel (remove duplicate headers) --> csv
        2. csv >> [Mr. Data Converter][2] -->  python dict
        3. csv >> [ConvertCSV.com][3] --> html 
        4. html >> manually add `code` class styling
   

### ConvertCSV template:

    <tr>
      <td class="data_type">{f1}</td>
      <td class="description">{f2}</td>
      <td class="code">{f3}</td>
      <td>{f4}</td>
      <td>{f5}</td>
    </tr>

### Hand styling:

    <style type="text/css">
        table{border-collapse:collapse}
        tr { vertical-align: top; border-bottom:thin solid #ccc}
        .data_type {font-weight: bold;}
        .description {min-width: 18em;}
        .code {font-family: monospace;}
    </style>


 [0]:http://desktop.arcgis.com/en/arcmap/latest/tools/supplement/data-types-for-geoprocessing-tool-parameters.htm
 [1]:http://tabula.technology/
 [2]:https://shancarter.github.io/mr-data-converter/
 [3]:http://www.convertcsv.com/csv-to-html.htm
 [4]: https://cdn.rawgit.com/maphew/arcplus/59e89dde/docs/Geoprocessing_data_types.html
