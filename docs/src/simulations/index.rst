Simulations & Estimation Power  
==============================
.. _direct-simulations:

Prest |version| offers two ways in which the user can obtain information about the distribution of various variables of interest (axiom violations; model distance scores)
when a large number of artificial subjects are assumed to make **uniform-random choices** from menus that are derived
from a finite set of alternatives in a non-budgetary environment. From these distributions one can then identify human subjects whose choice behavior cannot 
be distinguished from random behavior for a given level of statistical significance.
This procedure can therefore provide a *power test* for the user's model-estimation and consistency-analysis computations on general datasets, 
as first suggested in [bronars87]_ for the case of budgetary datasets.


Choice *and* Dataset Simulations
--------------------------------

By clicking on *"Simulations -> Generate random subjects"* in the main menu, the user can first name 
the simulated dataset that will be created, specify the number and labels of the choice alternatives
(separated by commas), and choose the desired number of artificial subjects. Then, under *"Menu distribution options"*,
the user can choose from the following options:

  * **Exhaustive (each possible menu once):**  every subject's choices are from the `2^n-1` menus that are derived from the underlying set with `n` specified alternatives.
  
  * **Random sample with replacement:** every subject's choices are from a random selection of the `2^n-1` menus that are derived from the underlying set with `n` specified alternatives, where some menus may appear more than once.
  
  * **All binary menus:** every subject's choices are from the `{n}\choose{2}` binary menus that are derived from the underlying set with `n` specified alternatives. 
  
  * **Default alternative:** 

     * **None:** the dataset features no default alternatives.
     	 
     * **Uniformly random:** a random element of each menu is the default alternative in that menu.

The possible options under *"Choice mode"*, and their implications for the probability distribution used in the simulations, depend on what the user selected under *"Default alternative"*, as follows:

  * Under **Default alternative -> None**, the *"Observations without default alternatives"* menu is activated, featuring the following options:

         * **Forced choice**

           +---------------------------------------+-----------------------+----------------------------------+
           | Random menu with `k` alternatives     | Single-valued choice* | Multi-valued choice              |                   
           +=======================================+=======================+==================================+
           | Probability of each of the `k`        |      `\frac{1}{k}`    |   `\frac{1}{2}\frac{2^k}{2^k-1}` |                        
           | alternatives being chosen**           |                       |                                  |                 
           +---------------------------------------+-----------------------+----------------------------------+
           | Probability of each nonempty          |    Not defined        | `\frac{1}{2^k-1}`                |       
           | submenu being chosen                  |                       |                                  |      
           +---------------------------------------+-----------------------+----------------------------------+
    
         * **Non-forced choice**

           +------------------------------------------+-----------------------+-----------------------------------------------+
           |  Random menu with `k` alternatives       | Single-valued choice* | Multi-valued choice                           |                   
           +==========================================+=======================+===============================================+
           | Probability of each of the `k`           |   `\frac{1}{k+1}`     |   `\frac{1}{2}\frac{2^k}{2^k-1}\frac{k}{k+1}` |                        
           | alternatives being chosen                |                       |                                               |                 
           | (excl. deferral/outside option)**        |                       |                                               |                                 		 
           +------------------------------------------+-----------------------+-----------------------------------------------+
           | Probability of the                       |                       |                                               |  
           | deferral/outside option                  |    `\frac{1}{k+1}`    | `\frac{1}{k+1}`                               |       
           | being chosen                             |                       |                                               |      
           +------------------------------------------+-----------------------+-----------------------------------------------+
           | Probability of each nonempty             |    Not defined        | `\frac{k}{(k+1)(2^k-1)}`                      |       
           | submenu being chosen                     |                       |                                               |      
           +------------------------------------------+-----------------------+-----------------------------------------------+


  * Under **Default alternative -> Uniformly random**, the *"Observations with default alternatives"* menu is activated, featuring the following options:
     
         * **Unbiased**

           +------------------------------------------------+-----------------------+--------------------------------+
           |  Random menu with `k` alternatives             | Single-valued choice* | Multi-valued choice            |                   
           +================================================+=======================+================================+
           | Probability of each of the `k-1`               |  `\frac{1}{k}`        | `\frac{1}{2}\frac{2^k}{2^k-1}` |                        
           | non-default alternatives being chosen**        |                       |                                |                 
           +------------------------------------------------+-----------------------+--------------------------------+
           | Probability of the default                     |  `\frac{1}{k}`        | `\frac{1}{2}\frac{2^k}{2^k-1}` |       
           | alternative being chosen**                     |                       |                                |      
           +------------------------------------------------+-----------------------+--------------------------------+
           | Probability of each nonempty                   |    Not defined        | `\frac{1}{2^k-1}`              |       
           | submenu being chosen                           |                       |                                |
           +------------------------------------------------+-----------------------+--------------------------------+	 	 
    
         * **Default-biased*****

           +-------------------------------------------------+-----------------------+-----------------------------------------------------------------------------------------------+
           |  Random menu with `k` alternatives              | Single-valued choice* | Multi-valued choice                                                                           |                   
           +=================================================+=======================+===============================================================================================+
           | Probability of each  of the `k-1`               |   `\frac{1}{k+1}`     | `\frac{1}{2}\frac{2^k}{2^k-1}\frac{k}{k+1}`                                                   |               
           | non-default alternatives being chosen**         |                       |                                                                                               |                                       		 
           +-------------------------------------------------+-----------------------+-----------------------------------------------------------------------------------------------+
           | Probability of the                              |                       |                                                                                               |  
           | default alternative                             |    `\frac{2}{k+1}`    | `\frac{1}{k+1}+\frac{1}{2}\frac{2^k}{2^k-1}\frac{k}{k+1}=\frac{2^kk+2(2^k-1)}{2(2^k-1)(k+1)}` |       
           | being chosen**                                  |                       |                                                                                               |      
           +-------------------------------------------------+-----------------------+-----------------------------------------------------------------------------------------------+
           | Probability of each nonempty                    |    Not defined        | `\frac{k}{(k+1)(2^k-1)}`                                                                      |       
           | submenu being chosen                            |                       |                                                                                               |
           +-------------------------------------------------+-----------------------+-----------------------------------------------------------------------------------------------+	 	 

     `*`   *"Single-valued choice" here refers to the case where "Multi-valued choice" at the bottom of the dialog box is* not *selected, and results in up to one alternative being chosen from each menu.*    
	
     `**`   *The probability of an alternative being chosen under the "Multi-valued choice" mode is interpreted here as the probability that the given alternative belongs to the chosen submenu of the given menu. Assuming "Forced-choice" and considering an arbitrary menu* `A` *with* `k` *alternatives, every nonempty weak submenu of* `A` *is chosen with probability* `\frac{1}{2^k-1}`. *Since each of the* `k` *alternatives belongs to exactly* `\frac{2^k}{2}` *of these submenus, it follows that each of them is chosen with probability* `\frac{2^k}{2(2^k-1)}`. *If "Non-forced choice" is selected instead, then since some nonempty submenu of* `A` *is chosen with probability* `\frac{k}{k+1}` (*because the deferral/outside option is chosen with probability* `\frac{1}{k+1}`), *the corresponding choice probability for each of the* `k` *alternatives is adjusted accordingly.*
	
     `***`  *"Default-biased" simulations is an adaptation of "Non-forced choice" simulations in an environment where defaults are present, with the default option in every menu replacing the deferral/outside option. However, since the default option here is one of the* `k` *alternatives in the menu, this process leads to a choice probability distribution that is biased towards that option.*
			
The resulting random dataset will then appear in the workspace and the user can apply on it the consistency analysis and/or
model estimation operations that were described in the previous sections. The simulated subjects here
are named *"Random1, Random2, ..."*.


.. _similar-random-dataset:

Choice Simulations Based on an *Existing* Dataset
-------------------------------------------------

This allows users to generate choices of random-behaving subjects who faced *exactly* the same menus that subjects in an already existing
dataset were presented with. In this case, Prest reproduces subject-per-subject the menu structure of the original dataset.

This feature can be used by right-clicking on the dataset of interest in the workspace and 
select *"Analysis -> Generate similar random dataset"*. In the pop-up window, the "*Random subjects per subject*" option specifies how many simulated 
subjects will be generated in the way described above for each subject in the original dataset. The *"Subjects"* and *"Observations"* entries below that option
inform the user about the corresponding size dimensions of the simulated dataset that will be produced.

The options that were specified above are also available here under *"Choice mode"*. In addition, if the existing dataset contains some observations
with default alternatives and others without (see, for example, :ref:`the hybrid dataset  <dataset-examples>`), then the user can configure the simulation for each mode of analysis.

The resulting random dataset will again appear in the workspace and the user can apply on it the consistency analysis and/or
model estimation operations that were described in the previous sections. The simulated subjects here
are named *"Subject1Random1, ..., Subject1RandomN, SubjectKRandom1, ..., SubjectKRandomN"*, where *"Subject1, ..., SubjectK"* are 
assumed to be the subjects' names in the original dataset on which random behavior is generated and `N` is the number of simulated subjects selected by the user.
