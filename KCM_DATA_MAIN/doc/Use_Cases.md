## Use Cases

* __User: Academic Researchers__
	* Data visualization of KCM datasets to see if there are any relationships between when a battery module is replaced and operational time, where module is spatially located, bus route, features in dataset (voltage, current, power, temperature). 
	* _Component Design:_ 
		* Understanding datasets - what are the features? How is it organized right now?
		* Data cleaning - Transform into a usable dataframe.  How many individual modules? Identify repeats. Time between data collection. Segment by bus and then by module. Identify when model is taken out
		* Data visualization (numpy, matplotlib, seaborn, pandas) to observe relationships that may exist between modules and operational time, where module is spatially located, bus route, features in dataset

* __User: King County Metro (Predictive maintenance)__
	* Reduce sunk time and cost of unscheduled maintenance by predicting module current state of health and remaining usable life for predictive maintenance 
	* Data analysis - Is there enough data to train and test a model?
	* Train a model to predict replacement of battery module for hybrid bus fleet depending on factors such as voltage, temperature, bus route
	* _Component Design:_
		* Machine Learning to predict battery module end of life

* __User: Other Battery Systems Management Software Users__
	* Data visualization and predictive models for understanding battery operations better
