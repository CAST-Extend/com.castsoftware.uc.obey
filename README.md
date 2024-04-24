# Template SDK Extension

This project aims to give you a template from  which to create SDK extensions for CAST Imaging.

## Relevant documentation:

https://doc.castsoftware.com/display/EXTEND

http://cast-projects.github.io/Extension-SDK/doc/index.html

## How to use this template

### Obey

First, `Obey` needs to be replaced with the name of the language or framework you are creating support for. It appears in 4 places:
- In the folder name of `Configuration/Languages/Obey/`
- In the filename of `Configuration/Languages/Obey/ObeyMetaModel.xml`
- In the content of the file `Configuration/Languages/Obey/ObeyMetaModel.xml`
- In the content of the file `plugin.nuspec`

We also recommend you use this identifier when naming your methods in `analyzer_level.py` and/or `application_level.py`, although this is not required.

**Example**

If I am writing an extension for the Google framework Guice, I might choose `Guice` as my identifier. I need then to modify the project so that my structure becomes:
```
.
└── com.castsoftware.uc.guice/
    ├── Configuration/
    │   └── Languages/
    │       └── Guice/
    │           └── GuiceMetaModel.xml
    ├── analyzer_level.py
    ├── application_level.py
    ├── cast_upgrade_1_6_13.py
    ├── lib_cast_upgrade_1_6_13.zip
    └── plugin.nuspec
```

### YYY

Second, `YYY` needs to be replaced with the name of the custom object you are creating support for. It appears in 2 places:
- In the content of the file `Configuration/Languages/Obey/ObeyMetaModel.xml`
- In the content of the files `analyzer_level.py` and/or `application_level.py` depending on the step at which you create the object

**Example**

If I am writing an extension for the Google framework Guice, my object type might be `Annotation`. I need then to modify the files accordingly:
```
<type name="Guice_Annotation" rid="0">
    <description>Guice Annotation</description>
    <inheritedCategory name="UAObject"/>
</type>
```

### 252

Third, `252` needs to be replaced with the correct file_no you have reserved for your extension. For more info on this requirement, consult https://doc.castsoftware.com/display/EXTEND/Managing+ID+ranges+for+custom+extensions. It appears in 1 place:
- In the content of the file `Configuration/Languages/Obey/ObeyMetaModel.xml`

**Example**

If I am writing an extension for the Google framework Guice, I might have reserved the file_no 666. I need then to modify the file accordingly:
```
<metaModel file_level="client" file_no="666">
    <type name="Guice_Annotation" rid="0">
        <description>Guice Annotation</description>
        <inheritedCategory name="UAObject"/>
    </type>
</metaModel>
```