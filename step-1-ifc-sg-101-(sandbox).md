IFC-SG 101

1

OBJECTIVE

 What is IFC & IFC-SG

 How IFC-SG captures local Regulatory Requirements

 How to map Regulatory requirements into IFC

 How to read the IFC-SG Excel

2

3

STANDARDISING INFORMATION TO SUPPORT CORENET X,
USING IFC AS THE COMMON REPRESENTATION

Software A

BIM in
format A

Software B

BIM in
format B

Software C

BIM in
format C

4

t
r
o
p
x
E

t
r
o
p
x
E

t
r
o
p
x
E

Common
language/
definition

Adopting IFC
- Open, neutral standard
-
- Customized tools and services could

Platform/solution independent

be developed

Visualization for
comments & checks

Rules for
auto-checks

Archival and version
mgmt

Extraction and filtering
of info

Other analyses &
applications…

*Industry Foundation Classes (IFC)
– international, open standard to
describe building information

CAPTURING REGULATORY REQUIREMENTS

IFC-SG captures the Regulatory
Requirements of Singapore Code of
Practices

▪ Development of IFC-SG is based on IFC4

(Reference View), with no amendments to the IFC

schema

▪ Localization includes addition of subtypes and

properties to address regulatory checks leveraging

on the information predefined in IFC Schema

5

IFC 4
Objects, Types  and properties
defined in IFC schema

IFC-SG
Localised information of
interest

Objects (Entity) : IfcWall

SubType
PARTITIONING

Properties
Combustible

Objects (Entity) : IfcRamp

SubType
RETAINING WALL

Properties
WaterTight

Properties
HandicapAccessible

Properties
BarrierFreeAccessibility

Information predefined in IFC’s
schema.
Localised information of interest (sub
types and properties) from regulatory
requirements.

FLOW OF INFORMATION FROM NATIVE BIM TO IFC

Information in IFC comes from information modelled in the Native BIM Model

Export to IFC

Configure components and
parameters in BIM authoring
software to map to the desired IFC
representation

Eventual IFC model with
components and
parameters captured

Components and
parameters of interest to
be modelled in BIM

6

WHAT IS IFC?

7

WHAT IS IFC?

Industry Foundation Classes
International Open Standard Representing The Built Environment

▪ A standardized digital description of the built environment.

▪ Developed by buildingSMART International to facilitate

interoperability in the architecture, engineering and

construction (AEC) industry

Design

Plan

▪ IFC is published as an official ISO standard – ISO16739

Operate

Build

8

VERSIONS OF IFC TO-DATE

1996

1997
IFC 1.0

1998
IFC 1.5

1999
IFC 2.0

2000
IFC 2x

2003
IFC 2x2

2006
IFC 2x3

2007
IFC 2x3 TC1

2013
IFC 4

2017
IFC 4 Add2

2017
IFC 4.1

2019
IFC 4.2

2020
IFC 4.3 RC1&2

2021
IFC 4.3 RC3

9

MODEL VIEW DEFINITION (MVD) AND IFC

The MVD defines a subset of the overall IFC
schema, to focus on a set of information for a use
case or workflow. It can be used to define
exchange requirements of a project.

 Software Vendors implement various MVDs to
help support industry’s needs. Some of the
notable MVD includes

o IFC2x3 Coordination View 2.0

o IFC4 Reference View

o IFC4 Design Transfer View

10

Credits: BIM Corner

11

buildingSmart International - IFC Documentation

KEY DATA STRUCTURES IN IFC TO DESCRIBE
BUILDING ELEMENTS

Entity

Sub-types

Property Set & Properties

12

KEY DATA STRUCTURES – ENTITY

An Entity is an object defined in the IFC data model

It can be used to define a physical element or a conceptual idea

A physical element - Wall / Window / Furniture / Slab / Beam / Column

A conceptual idea – Space / Spatial Zones / Site / Room / Area

Defined Object ➔

Entity ➔

Wall

IfcWall

The data item names for types, entities, rules and functions start with the prefix "Ifc" and continue
with the English words in PascalCase naming convention (no underscore, first letter in word in upper case)

IfcWindow IfcSlab

IfcSpace

13

KEY IFC DATA STRUCTURES – SUB-TYPES

Defines/describes the object defined (Entity) in the data model with sub-types.

It is the next level of detail to further describe the entity.

IfcEntity

IfcEntity

Sub-Types
PredefinedType

Users can tap on the predefined (IFC Standard)
list of wall types to indicate the type of wall
used in a building

Ifc Sub-Types
PredefinedType

An actual IFC Export of localized information on IfcWall

Sub-Types
PredefinedType

USERDEFINED

Object Type

14

IFC Feature:
Used for localization

KEY IFC DATA STRUCTURES – PROPERTY SET & PROPERTIES

Property Set

Properties

Value (Type)

Set/Group of Properties that describes the
function or feature of the Entity/Sub-Type

ENTITY

SUB-TYPE

PROPERTY SET

PROPERTIES:  VALUE (Boolean / Label)

IfcWall

PARAPET

Pset_Wallcommon

Combustible:  Yes / No (Boolean)

FireRating: 2Hr (Label)

15

WHAT IS IFC-SG?

IFC-SG is localized IFC data model that is developed based on the IFC standard to address local regulatory needs

16

KEY DATA STRUCTURES OF IFC–SG

Entity

Sub-types

Property Set & Properties

USERDEFINED Object Type

USERDEFINED Property Set & Properties

17

Information predefined in IFC’s schema.

Localised information of interest (object
types and properties) from Regulatory
Requirements.

KEY DATA STRUCTURES OF IFC–SG

USERDEFINED OBJECT TYPE

When no Predefined Type exists to describe the Entity. E.g RETAININGWALL

Users may use “USERDEFINED” as Subtype provided by IFC to capture the localized information

IfcEntity: IfcWall

Sub-Types
PredefinedType

PredefinedType: USERDEFINED

Object Type: RETAININGWALL

Ifc SubTypes
PredefinedType

An actual IFC Export of localized information on IfcWall

18

IfcEntity

IFC Feature:
Used for localization

KEY DATA STRUCTURES OF IFC–SG

USERDEFINED PROPERTY SETS & PROPERTIES

When no Property Sets or Properties exists to describe the Entity.  E.g.  A wall with a WaterTight feature

Users may use USERDEFINED feature provided by IFC to capture the localized information

ENTITY

SUB-TYPE

USERDEFINED PROPERTY SET

USERDEFINED PROPERTIES: VALUE

IfcWall

PARAPET

SGPset_Wall

WaterTight: Yes / No

For USERDEFINED Property Sets, the naming are
pre-fixed with “SG” to indicate that it captures
Singapore localized requirement

19

An actual IFC Export of localized information on IfcWall

SPACE REPRESENTATION IN IFC-SG

 Spaces were identified & checked by Agencies.

 As there is vast number of spaces definition, users can input the

name of the spaces in the properties of the object.
Users are to refer to the excel provided to assign Entities,
Subtypes, Property Sets & properties for space representations

ENTITY– IfcSpace

USERDEFINED PROPERTY SET

USERDEFINED PROPERTIES:  VALUE

SGPset_Space

SpaceName: Kitchen / Corridoor … etc
(Label)

20

URA excel which documents the space information

UNDERSTANDING
THE MAPPING

21

UNDERSTANDING THE MAPPING

IFC-SG MAPPING

Filter on / off

Agencies COP & Rules

LTA

Vehicle Parking Provision in
Development Proposals - 2019 Edition

Parking
Layout
Dimensions

The minimum length of a car parking lot for
parallel parking shall be 5.4m.

22

UNDERSTANDING THE MAPPING

IFC-SG MAPPING

Identified Objects & BIM Authoring Tools Representation

Filter on / off

Car Parking Lot

Length

Generic Models

Model Element

N.A

Object

23

UNDERSTANDING THE MAPPING

IFC-SG MAPPING

Proposed IFC Representation

Filter on / off

IfcBuildingElement

Proxy

SGPset_Building

*CARLOT

ElementProxy

Width

Length

mm

Dimension

* =  USERDEFINED
Subtype

24

AUTO POPULATING DIMENSIONS

Dimensions in Native BIM auto populates & information will be exported to IFC

Default dimensions in Native BIM will be exported under the Property Set SGPset_EntityDimension

E.g. IfcWall
Default dimensions
"Length" will be exported under SGPset_WallDimension with property "Length".

E.g. IfcDoor
Default dimensions
"Width" will be exported under SGPset_DoorDimension with property "Width".

25

CORENET X BCA WEBSITE

More information on IFC and recordings are available on the website: https://www1.bca.gov.sg/regulatory-
info/building-control/corenet-x

26

CHANGELOG

Date

Description

22 Nov 2022

Added description on auto populating dimensions

27

