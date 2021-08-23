### Instruction

1. Lauch server. In root directory,
    1. Create a virtual environment and activate it.
    2. Install dependency according to 'requirements.txt'.
    3. In command line: `Python server.py`

2. [Important] A **preset.json** file with **measure plans** involved in it is need for the proper functioning. The server will load measure plans before running. Its structure should be like this( Just refer to the file for details):
```json
{
  "Workshop": {
    "Device001": {
      "measure_plan_id": "MP#00001",
      "batch_size": 5,
      "parameter_number": 4,
      "parameter_info": [
        {
          "usl": 3,
          "lsl": 1,
          "scale": 2
        },
        {
        }
       ],
     "Device002": {}
  },
  "Warehouse": {
    "Devices003": {}
  }
}
```

3. Use commands to perform certain functions. Here are some useful commands in **IPython Shell**:
     - `assign_task(sub_sys_name, perpetual=False)`: Launch simulator to generate measure data of all parameters. 'sub_sys_name' can be either 'Workshop' or 'Warehouse'. If 'perpetual' is set True, the data submission is continuous. Otherwise the simulator just submits one batch.
     - `clear_perpetual_simulation(sub_sys_name)`: Use it when you want to stop the perpetual data submission.
     - `pause_simulation()`: Pause the perpetual data submission of  **Workshop** for a while.

e.g. 
```Python
# In IPython shell
server.assign_task('Workshop')
server.assign_task('Workshop', True)

server.clear_perpetual_simulation('Workshop')

server.pause_simulation()
```