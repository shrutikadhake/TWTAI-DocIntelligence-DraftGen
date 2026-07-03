**Feature Name: Connect**

**Overview**
This feature is aimed to create conformal mesh between the selected entities.

**Specification**
-	Limited only to bodies scoped under Automatic Prime method
-	Ensure all bodies scoped under Weld are meshed together.
-	Should be placed under Tree Outline, right-click Mesh select Insert > Connect.
UI Requirements

- **Suppressed**: suppress the Connect control. 
     Default value: No.
     When Yes, the Active field displays the status of the Connect control. 
- **Multiple Connection Steps**: provide multiple values for connection tolerance.
      Default value : No.
- **Connection Tolerance**: provide the tolerance value for connection. 
	 Value: Yes, 
     Connection Tolerance List is available to provide multiple values for connection tolerance. You can specify any number of connection tolerance values separated by a space. The first value in Connection Tolerance List performs face to face intersections, short edge removal, thin face removal and so on. From the second tolerance value onwards only the unconnected (free) edges are considered for performing connections.
-	**Connection Size**: size with which you discretize the edges before connecting them.
	  Default: Element Size.
-	**Connection Option**: select the connect options. 
      The available connection options:
        -  All to All, 
        - Free to All,
        - Free to Free. 


**Limitation**
Files having partially saved mesh, the previously saved mesh gets cleared. You may have to regenerate mesh for the entire model.
