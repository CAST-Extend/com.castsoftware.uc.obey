# Obey

## Introduction

This extension provides support for Obey files in HP NonStop Cobol applications.

Obey files are similar to JCL Jobs in the mainframe world. They are used to define the flow of a Cobol application.
Analyzing them can help to understand the end to end flow of a Cobol application.

## In what situations should you install this extension?

Whenever you need to analyze applications using Obey files in HP NonStop Cobol 
applications, and you want to get transactions / data call graph and representation of the actual physical files used to store data on disk, 
rather than just Cobol File Links.

Use cases covered:

- Knowledge Discovery / Blueprinting
- Transaction / Data Call Graph
- Identification of physical files used to store data on disk

## CAST version compatibility

This extension leverages the CAST extension SDK, and as such is compatible with CAST AIP releases starting from 8.3.0.

It has been tested with CAST AIP 8.3.54 / 8.3.56.

## Configuration instructions

1. Install the extension manually, since the extension will not be automatically installed after a fast scan.
2. Obey files should be renamed with the .obey extension. 
This is required for the extension to work, as it uses the file extension to identify Obey files.
3. Create an analysis unit for the "Obey" extension.

## What results can you expect?

Additional objects and links will be created in the knowledge base and will be available in CAST Imaging.

### Objects

- **Obey Job**: Represents the call graph entrypoint of the application, similar to JCL Jobs in the mainframe world.
- **Mainframe Unknown Program** : Represents a Cobol program that is called from an Obey Job but is not recognized. Indicates that the program is not part of the scan scope.
- **Obey Physical File**: Represents the physical files used to store data on disk.

### Links

- **Obey Job -> Mainframe Unknown Program**: Represents the call from an Obey Job to a Cobol program that is not recognized.
![obey_job_to_mainframe_unknown_program_link](images/obey_job_to_mainframe_unknown_program_link.png)
- **Obey Job -> Obey Physical File**: Represents the dependency from an Obey Job to a physical file. This dependency exists when an Obey Job assigns a physical file to a Cobol File Link and then calls a Cobol Program using this Cobol File Link.
![obey_job_to_obey_physical_file_link](images/obey_job_to_obey_physical_file_link.png)
- **Obey Job -> Cobol Program**: Represents the call from an Obey Job to a Cobol Program.
![obey_job_to_cobol_program_link](images/obey_job_to_cobol_program_link.png)
- **Cobol File Link -> Obey Physical File**: Represents the dependency from a Cobol File Link to a physical file. This dependency exists when a Cobol Program is being called from an Obey Job and the Obey Job assigns a physical file to a Cobol File Link being used by this particular Cobol Program.
![cobol_file_link_to_obey_physical_file_link](images/cobol_file_link_to_obey_physical_file_link.png)


| Behavior without the extension                      | Behavior with the extension                            |
|-----------------------------------------------------|--------------------------------------------------------|
| ![objects with no links](basic-support-without.png) | ![same objects but with links](basic-support-with.png) |
| ![objects with no links](basic-imaging-without.png) | ![same objects but with links](basic-imaging-with.png) |

## Approach used to support Guice

![schematicdoc](images/schematicdoc.png)

1. Analyze .obey files to identify the Obey Physical files, Cobol File Links and Cobol Programs being referenced
2. Create one Obey Job is created for each .obey file
3. Create one Obey Physical File object for each physical file being referenced in the Obey Job
4. Find the list of existing Cobol programs within the scan, and create one link between the Obey Job and each Cobol Program being called by the Obey Job
5. If a Cobol program being called is not part of the list of existing Cobol programs, create a Mainframe Unknown Program object and link it to the Obey Job 
6. For each existing Cobol Program (3) being called by an Obey Job, find the list of Cobol File Links being used by this program
7. For each of those Cobol File Link (6), find the list of Obey Physical Files being assigned to it in the Obey Job, and create one link between the Cobol File Link and the Obey Physical File
8. For each of those Cobol File Link (6), find the list of Obey Physical Files being assigned to it in the Obey Job, and Create one link between the Obey Job and the Obey Physical File

If we summarize:
- If Obey Job A calls Cobol Program B using Cobol File Link C, and Obey Job A assigns Obey Physical File D to Cobol File Link C, then:
  - Creation of Obey Job A
  - One link between Obey Job A and Obey Physical File D
  - One link between Obey Job A and Cobol Program B (if B is recognized, if not, a Mainframe Unknown Program object is created and linked to Obey Job A and we stop here)
  - If the Cobol Program B is recognized:
    - If Cobol File Link C is recognized because used within Cobol Program B, then:
      - One link between Cobol File Link C and Obey Physical File D
      

## Known limitations

- Obey Physical Files may show up in a transaction while they actually should not, because of the way CAST Imaging builds transactions and because of the way we link Cobol File Links to Obey Physical Files. Those Obey Physical File are easy to recognize though, they will not show any link with the Obey Job object entrypoint of the transaction.
![transaction_unrelated_obey_physical_file_limitation](images/transaction_unrelated_obey_physical_file_limitation.png)
In this example, the Obey file "$STL02.P0249D6.F0249N4E" should not appear in the transaction, as it is not linked to the Obey Job object entrypoint of the transaction. But since it is linked to a Cobol File Link which is part of the transaction and is an endpoint, it is included in the transaction.
- **Mainframe Unknown Program -> Obey Physical File**: Represents the dependency from a Cobol program that is not recognized to a physical file. This dependency exists when a Cobol program that is not recognized assigns a physical file to a Cobol Data File Link.