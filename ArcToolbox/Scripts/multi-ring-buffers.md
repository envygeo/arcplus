# Multiple Ring Buffers With Attributes

Create multiple ring buffers, keeping the specified attributes of parent feature class.

### Parameters

**Features to buffer**:  input polygon feature class or shapefile

**Out workspace**: a folder, file geodatabase, or feature dataset. It must exist.

**Out feature class**: name of feature class to create. If workspace is a folder a shapefile will be created.

**Buffer widths**: comma separated list of numbers in map units (usually metres). No spaces.

**Attributes to keep**: list of field names to preserve in the output buffers.



### What it does

- create inside only buffer for each of the specified buffer widths
- store buffer width used as an attribute
- merge all buffers into a single feature class, ensuring largest width first so narrower ones are drawn on top



### Command line usage

​    multi-ring-buffers [feature class]  [workspace]  [output feature class]  [widths list]  [attributes to keep]

```
python multi-ring-buffers.py R:\data.gdb\Foobar_ply  X:\maps\buffers.gdb  Foobar_rings   50,-50,-100,-300,-600  NAME,TYPE
```

No spaces in buffer widths or attribute names.



Requires Arcgis 10, Arcinfo license level.

(c) 2021 Environment Yukon, matt.wilkie@yukon.ca
Licensed under the MIT license: http://www.opensource.org/licenses/MIT

*Also see http://gis.stackexchange.com/questions/19505/multiple-ring-buffer-with-attributes*