## Data Breakdown

py_packages/vis_buses/bus_1/!3J0018_ProfileData_20170920082828.csv
    
    This is the first csv of bus 1, data from bus 1's first visit
    
    Each visit will have a data breakdown of the following:

#### <Battery Current (A)>
  
  Breaks down the amount of time (in seconds) that the battery was experiencing that value of current (in Amps). In bins of 10 Amps going from -350A to 350+A. This data was collected over 80985877 seconds which is 937.3 days worth of data. 

#### <Battery Voltage (V)>
  Breaks down the amount of time (in seconds) that the battery spent at a corresponding Voltage (in Volts) . In bins of 10 Volts going from 450V to 750+V. This data was collected over 80985877 seconds which is 937.3 days worth of data. 

#### <Power (kW)>
  Breaks down the amount of time (in seconds) that the battery spent at a corresponding Power (in kW) . In bins of 10 kW going from -200kW to 200+kW. This data was collected over 80985877 seconds which is 937.3 days worth of data. 

The data is then broken down into modules 1 through 16
Each module has 12 cells. 

#### <Cell Voltages (V)>
Breaks down the amount of time (in seconds) that each cell 1-12 of that module spent at a corresponding voltage (in Volts).  In bins of 10 kW going from 2V to 4+V. 


#### <Cell Balancer (on/off)>
Shows the amount of time (in seconds) that the cells of the module were turned on and off to maintain even usage of each cell in the module.

#### <Module Temperatures (deg C)>
Shows the time (in seconds) that the module spent at different temperatures (in degrees Celsius). In bins of 5C  going from -40C to 80+C. 

#### <Module Voltages (V)>
Breaks down the amount of time (in seconds) that the module spent at a corresponding Voltage (in Volts) . In bins of 2.4Volts going from 24V to 48+V.
 

