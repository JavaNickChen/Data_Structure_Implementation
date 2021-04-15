 

# Title  
	Data_Structure_Implementation for Laboratory Works of CPO Course    
	
# Group Name and List of Group Menmber      
	Group Name: PZEZ  
	Group Member:   Chen Jinhua && Wang Maoyu       
	
# Laboratory Work Number    
	1    
	
# Variant Description   
	Dictionary based on hash-map (collision resolution: separate chaining)    
	
# Synopsis
As a team, Chen Jinhua and Wang Maoyu completed the tasks required by CPO Lab 1. We have finished a Dictionary based on hash-map (collision resolution: separate chaining) with mutable vertion and immutable vertion.Chen Jinhua is responsible for the development of the mutable version, and Wang Maoyu is responsible for the immutable version.         

In this laboratory work, We have completed various basic operations on the dictionary structure with python LIST.These operations include: add, remove, convert to list, convert from list, Find element, Filter data structure, Map structure, and reduce.We also create a iterator and implement mempty and mconcat funtion.    

Our code has been committed into the github https://github.com/JavaNickChen/Data_Structure_Implementation    

# Contribution Summary for Each Group Member
Chen, Jinhua has completed the mutable version of the dictionary structure. The code he has completed is under the file path 'SRC /Chen';     
 
Wang, Maoyu has implemented an immutable version of the dictionary structure, and the code he has completed is under the file path 'SRC /Wang'.    

# Explanation of Taken Design Decisions and Analysis   
Design Decision for mutable version:    

	-'hashTable' is the key variable and property in class Dictionary.
    -'hashTable' is built-in list of Python, and consists of 'HeadNode' (a class).
    -'HeadNode' refer to a Singly Linked List which consists of 'ChainNode' (a class).
    -A 'ChainNode' store a key and relevant values. And the dictionary supports the different values with the same key in a 'ChainNode'.
Design Decision for immutable version:    

	-In the immutable version, we use two different lists to store the key and value respectively, and ensure the consistency of access to the key list and the valve list index in the function. A new dictionary is returned in each operation. We use  nested lists to implementate separate chaining.


# Work Demonstration
Use 'cd' command-line to go to the file in the path of the local computer, and execute one of the following command-line statements to execute the corresponding test file.  
 
	python DictionaryTest.py  
	python testCPO.py

The file DictionaryTest.py is corresponding to testing the work done by Chen Jinhua;   
The file testCPO.py is corresponding to tesing the work done by Wang Maoyu.

# Conclusion   
According to the test results, the dictionary model we developed can effectively meet the needs of dictionary access, modification, deletion, iteration, etc., while ensuring the mutable/immutable data structure of the dictionary. Compared with the dictionary data structure that comes with python, our model still has some flaws for some unconventional inputs.
