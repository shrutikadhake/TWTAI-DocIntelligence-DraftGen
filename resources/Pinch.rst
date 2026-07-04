 Pinch Control
============

Overview
--------

This feature is aimed to:

- remove small features from the model

Specification
-------------

-  create pinch controls based on settings that you specify
-  manually designate the entities to be pinched, or allow the feature to automatically identify and pinch all features smaller than the specified size
- Should be placed under *Tree Outline*, right-click **Mesh** → select **Insert > Pinch Control**

UI Requirements
---------------

*Scoping Method*
~~~~~~~~~~~~~~~~

Scope the bodies having features that need to be suppressed.

- **Default Methods: Geometry Selection**
  - *Geometry Selection*: scope faces or edged from the geometry bodies
  - *Named Selection*: scope the faces or edges geometry bodies to be pinched in the named selection

*Type*
~~~~~~

Type of pinch control.

- **Types**
  - *Manual Pinch Control*: Selects the features that you want to pinch manually.
  - *Automatic Pinch Control*: Pinches all features smaller than the specified size automatically.  
    

*Source*
~~~~~~~~

Select the entities to be pinched.

- *Geometry*: Select the faces or edges from the geometry bodies
- *Mesh*: Select the faces or edges from the mesh bodies

**Automatic Pinch Control**

- *Minimum Size*: Specify the minimum size of the features to be pinched.
- *Maximum Size*: Specify the maximum size of the features to be pinched.
- *Step Size*: Specify the step size of the features to be pinched.

**Manual Pinch Control**

- *Features to Pinch*: Select the features that you want to pinch manually.


Limitation
----------

(TBD – limitations not specified in provided content)
