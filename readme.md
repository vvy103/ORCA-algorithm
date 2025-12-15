**_Linux_**
```bash
cd ORCA-algorithm
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE={Release/Debug} -DFULL_OUTPUT_FLAG={ON/OFF} -DFULL_LOG_FLAG={ON/OFF} -DMAPF_LOG_FLAG={ON/OFF} ..
make
```

where optins:
- `CMAKE_BUILD_TYPE` — Standard CMake option that specifies the build type. For more information see [[CMake Documentation](https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html)]    
etc
  - `Release` uses to build with no debugging information. 
  - `Debug` usually uses to enable debugging information, disable optimization 
- `FULL_OUTPUT_FLAG` — Enables/disables full output to stdout about reading xml files.
- `FULL_LOG_FLAG` — Enables/disables logging to xml file agents state information
- `MAPF_LOG_FLAG` — Enables/disables logging to xml files information about MAPF instances in coordinated mode

## Launch
There are two options to test the algorithm: single test on one task and series of tasks.
Use the following command to launch single test:

```bash
./single_test {file_name num}
```
where 
- `file_name` — name of the XML file, which contain task;
- `num` — the number of agents with which tasks will run.

For example:
```bash
./single_test ../task_examples/empty_task.xml 10
```
  
Summary will be displayed after execution using standard output, full log (if such option in in CMake was chosen) 
will be saved in same directory as task file and will be named according to the following pattern:
```
*taskfilename*_*number_of_agents*_log.xml
```
For example:
```
empty_task_10_log.xml
```


Use the following command to launch series test:
```bash
./series_test {n_min n_step n_max n_tasks path}
```
where 
- `n_min` — the initial number of agents at which tasks will run;
- `n_step` — step of changing the number of agents when restarting tasks;
- `n_max` — the final number of agents at which tasks will run;
- `n_tasks` — the number of tasks in series;
- `path` — path to the folder, which contains task files; 

For example:
```bash
./series_test 5 5 10 2 ../task_examples
```

To run the series tests and get a result you need to pass a correct input XML-file(s). The task files must be named according to the following pattern:
```
*number*_task.xml
```
Moreover, the numbering of tasks should form a sequence of numbers from **_0_** to **_n_tasks-1_**.
For example:
```
0_task.xml
1_task.xml
```

If the number of agents in the task is less than the required value, it will be started with the number of agents specified in the task.

Summary will be written after execution of each task in file `path/result.txt`, full log (if such option was chosen) will be saved at _path_ and will be named according to the following pattern:
```
*taskfilename*_*numberofagents*_log.xml
```
For example:
```
0_task_15_log.xml
```


## Input and Output files and Other Options
### Input files
Input files are an XML files with a specific structure.  
Input file should contain:

* Mandatory tag `<agents>`. It describes the parameters of the agents.
    * `number` — mandatory attribute that define the number of agents;
    * `type` — attribute that define the type of agents. Possible values: 
      - `orca` — running the algorithm in standard mode without avoiding deadlocks
      - `orca-par` — running the algorithm with avoiding deadlocks using Push and Rotate algorithm to create common coordinated plan. For more detains see out paper "A Combination of Theta*, ORCA and Push and Rotate for Multi-agent Navigation".
      - `orca-par-ecbs` — running the algorithm with avoiding deadlocks using combination of Push and Rotate and ECBS algorithms to create common coordinated plan. For more detains see out paper "Distributed Multi-Agent Navigation Based on Reciprocal Collision Avoidance and Locally Confined Multi-Agent Path Finding".
      - `orca-return` — experimental mode in which random agents return to their previous waypoints in case of deadlocks.
    * `<default_parameters>` — mandatory tags that defines default parameters of agents and agent's perception.
      * `agentsmaxnum` — mandatory attribute that defines a number of neighbors, that the agent takes into account;
      * `movespeed` — mandatory attribute that defines maximum speed of agent;
      * `sightradius` — mandatory attribute that defines the radius in which the agent takes neighbors into account;
      * `size` — mandatory attribute that defines size of the agent (radius of the agent);
      * `timeboundary` — mandatory attribute that defines the time within which the algorithm ensures collision avoidance with other agents;
      * `timeboundaryobst` — mandatory attribute that defines the time within which the algorithm ensures collision avoidance with static obstacles.
    * `<agent>` — mandatory tags that defines parameters of each agent.
        * `id` — mandatory attribute that defines the identifier of agent;
        * `start.xr` — mandatory attribute that defines the coordinate of start position on the x-axis (hereinafter, excluding `map` tag, points (x,y) are in coordinate system, which has an origin (0,0) in lower left corner. More about coordinate systems in the illustration below);
        * `start.yr` — mandatory attribute that defines the coordinate of start position on the y-axis; 
        * `goal.xr` — mandatory attribute that defines the coordinate of finish position on the x-axis; 
        * `goal.yr` — mandatory attribute that defines the coordinate of finish position on the y-axis; 
        * `agentsmaxnum` — attribute that defines a number of neighbors, that the agent takes into account;
        * `movespeed` — attribute that defines maximum speed of agent;
        * `sightradius` — attribute that defines the radius in which the agent takes neighbors into account;
        * `size` — attribute that defines size of the agent (radius of the agent);
        * `timeboundary` — attribute that defines the time within which the algorithm ensures collision avoidance with other agents;
        * `timeboundaryobst` — attribute that define the time within which the algorithm ensures collision avoidance with static obstacles.
* Mandatory tag `<map>`. It describes the environment for global path planning.
  * `<height>` and `<width>` — mandatory tags that define size of the map. Origin is in the upper left corner. (0,0) - is upper left, (*width*-1, *height*-1) is lower right (more about coordinate systems in the illustration below). 
  * `<cellsize>` — optional tag that defines the size of one cell.
  * `<grid>` — mandatory tag that describes the square grid constituting the map. It consists of `<row>` tags. Each `<row>` contains a sequence of "0" and "1" separated by blanks. "0" stands for traversable cell, "1" — for untraversable (actually any other figure but "0" can be used instead of "1").

* Mandatory tag `<obstacles>`. It describes static obstacles for collision avoidance.
  * `number` — mandatory attribute that defines the number of obstacles;
  * `<obstacle>` — mandatory tags which defines each static obstacles for collision avoidance.
    * `<vertex>` — mandatory tags which defines vertex of static obstacle for collision avoidance. 
      *  `xr` — mandatory attribute that defines the coordinate of vertex on the x-axis; 
      *  `yr` — mandatory attribute that defines the coordinate of vertex on the y-axis.
  
* Mandatory tag `<algorithm>`. It describes the parameters of the algorithm.
  * `<delta>` — mandatory tag that defines the distance between the center of the agent and the finish, which is enough to reach the finish (ORCA parameter);
  * `<timestep>` — mandatory tag that defines the time step of simulation (ORCA parameter);
  * `<searchtype>` — tag that defines the type of planning. Possible values - "thetastar" (use Theta* for planning), "direct" (turn off global planning and always use direction to global goal). Default value is "thetastar" (global planning parameter);
  * `<breakingties>` — tag that defines the priority in OPEN list for nodes with equal f-values. Possible values - "0" (break ties in favor of the node with smaller g-value), "1" (break ties in favor of the node with greater g-value). Default value is "0" (Theta* parameter);
  * `<cutcorners>` — boolean tag that defines the possibility to make diagonal moves when one adjacent cell is untraversable. The tag is ignored if diagonal moves are not allowed. Default value is "false" (Theta* parameter);
  * `<allowsqueeze>` — boolean tag that defines the possibility to make diagonal moves when both adjacent cells are untraversable. The tag is ignored if cutting corners is not allowed. Default value is "false" (Theta* parameter);
  * `<hweight>` — defines the weight of the heuristic function. Should be real number greater or equal 1. Default value is "1" (Theta* parameter);
  * `<trigger>` — defines the switching to the coordinated mode trigger. Possible values:
    - `speed-buffer` — use average speed for deadlock detection. For more detains see out paper "Distributed Multi-Agent Navigation Based on Reciprocal Collision Avoidance and Locally Confined Multi-Agent Path Finding".
    - `common-point` — use information about movement to a common waypoint for deadlock detection. For more detains see out paper "A Combination of Theta*, ORCA and Push and Rotate for Multi-agent Navigation".
  * `<mapfnum>` — defines the minimum number of agents that should move towards a common waypoint (for `common-point` trigger)

![map_scheme](img/map.png)

Examples locates in directory `task_examples`.

### Other Options

The implementation also contains a number of options that affect the operation of algorithms and experiments, but are not included in the input files (Sorry for that).

In `include/const.h` file:
- `COMMON_SPEED_BUFF_SIZE` — the number of steps that are taken into account to calculate the average speed that is used as a criterion for stopping the execution of an instance.
- `MISSION_SMALL_SPEED` — the value, when the average speed decreases below which the execution of the instance stops.
- `SPEED_BUFF_SIZE` — the number of steps that are taken into account to calculate the average speed that is used as a criterion for deadlock detection (for `speed-buffer` trigger).
- `SMALL_SPEED` — the value, when the average speed decreases below which the agent assume that deadlock is occurred (for `speed-buffer` trigger).
- `ECBS_SUBOUT_FACTOR` — Sub-optimal factor for ECBS algorithm.

In `src/experiments/single_test.cpp` or `src/experiments/series_test.cpp`:
- `STEP_MAX` — the maximum number of simulation steps.
- `STOP_BY_SPEED` — enables/disables instance execution halting depending on the average speed of the agents.
- `IS_TIME_BOUNDED` — enables/disables instance execution halting depending on the runtime.
- `TIME_MAX` — the maximum runtime in ms.

### Output files
#### Summary 

Contains the main information about the execution of tasks in series test. 
There are 6 columns:

* `success_rate` — shows the percent of agents, which succeed their tasks; 
* `run_time` — shows the time of running of task;
* `flow_time` — shows the sum of steps of all agents;
* `makespan` — shows the maximum value of steps of among all agents;
* `collisions` — shows the number of collisions between agents while execution of task;
* `collisions_obs` — shows the number of collisions between agents and static obstacles while execution of task;
* `init_count` — shows the number of coordinated mode launches;
* `unite_count` — shows the number of mergers of two coordinated groups;
* `update_count` — shows the number of updates of the coordinated plan when one or more uncoordinated agents are added;
* `ecbs_count` — shows the number of ECBS algorithm launches (only for `orca-par-ecbs` type);
* `par_count` — shows the number of Push and Rotate algorithm launches (only for `orca-par-ecbs` type);
* `success_count` — shows the number of successful coordinated mode launches;
* `unsuccess_count` — shows the number of unsuccessful coordinated mode launches;
* `mapf_flowtime` — shows the sum of steps of all agents in coordinated mode;
* `mapf_runtime` — shows computational time of MAPF algorithms;

#### Full log

Contains the full information about the execution of each task. 
Includes same tags as input file, summary and information about steps of each agent.


Summary example:
```xml
<summary successrate="100" runtime="1.061" makespan="170.90001" flowtime="477.60001" collisions="0" collisionsobst="0"/>
```
Agent's path example:
```xml
<agent number="0">
    <path pathfound="true" steps="4">
        <step number="0" x="33.18066" y="9.1728058"/>
        <step number="1" x="33.36132" y="9.3456116"/>
        <step number="2" x="33.541981" y="9.5184174"/>
        <step number="3" x="33.722641" y="9.6912231"/>
    </path>
</agent>
```
Examples locates in directory `task_examples`.