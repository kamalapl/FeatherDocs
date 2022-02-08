## TEXT-EDITOR
### **To run the server** 
1. Create a virtual environment
			
		$ cd Text-Editor
		$ virtualenv env
	    $ source env/bin/activate
2. Install the project’s dependencies inside an active virtual environment
		
		$ pip install -r requirements.txt
3. Run the server	    
	    
		$ uvicorn --reload server:app

<HR>

### **To run the client**

	npm start
