# Smart City Simulation Platform with Uncertainty

This repository provides the source code, configuration scripts, and setup instructions for the paper:

"A Smart City Simulation Platform with Uncertainty"
Shuyang Dong, Meiyi Ma, and Lu Feng
Proceedings of the ACM/IEEE 12th International Conference on Cyber-Physical Systems (ICCPS), 2021

## Overview

This platform simulates urban environments with integrated services in transportation, energy, and emissions, while explicitly modeling real-world uncertainty from events, sensors, and devices. It supports urban planners and researchers with customizable simulations and multi-domain data generation.

## Features

* Basic Structure Layers:

  * Road networks built from OpenStreetMap
  * Building layers with amenity tagging and energy profiles

* Event Layer:

  * Scheduled (planned) events
  * Probabilistic, randomized emergency events (e.g., traffic accidents)

* Service Layer:

  * Transportation: Built on SUMO for traffic flow simulation and signal control
  * Emission: Evaluate noise and air pollution from vehicles and buildings
  * Energy: Calculate and analyze building-level energy consumption

* Uncertainty Modeling:

  * Sensor Uncertainty: Introduce noise into sensed data (e.g., Gaussian bias)
  * Device Uncertainty: Simulate probabilistic malfunctions of sensors and lights
  * Event Uncertainty: Inject randomized emergency scenarios

## Quick Start

### 1. Environment Setup

Ensure the following are installed:

* SUMO (Simulation of Urban MObility)
* Python >= 3.6
* Python packages: traci, sumolib
* SUMO Python tools: randomTrips.py, netconvert, polyconvert

### 2. Generate Simulation Network

From OpenStreetMap data:

```
netconvert --osm-files your_map.osm -o your_map.net.xml \
  --geometry.remove --ramps.guess --junctions.join \
  --tls.guess-signals --tls.discard-simple --tls.join --tls.default-type actuated
```

Convert building polygons:

```
polyconvert --xml-validation never --net-file your_map.net.xml \
  --osm-files your_map.osm --type-file osmPolyconvert.typ.xml \
  -o your_map.poly.xml
```

### 3. Generate Traffic Flows

Using SUMO's OSM Web Wizard to define traffic demand:

* `Through Traffic Factor` controls the ratio of vehicles that start/end outside the map (border traffic).
* `Count` defines hourly traffic volume based on road length and lane number.

For example, with total car-accessible road length = 5 km, 2 lanes each, and count = 90:
Vehicles/hour = 5 \* 2 \* 90 = 900 → One car generated every 4 seconds (equivalent to `p=4` in `randomTrips.py`).

Using `randomTrips.py`:

```
python randomTrips.py -n your_map.net.xml -o Trips.trips.xml \
  -p 10 --route-file Routes.rou.xml --validate
```

Customize vehicle types and speeds:

```
--vehicle-class bus --trip-attributes "maxSpeed=\"27.8\""
```

### 4. Launch Simulation

Launch SUMO or SUMO-GUI:

```
sumo -c your_simulation.sumocfg --queue-output output/queue.xml --quit-on-end
```

```
sumo-gui -c your_simulation.sumocfg
```

To export coordinates with geo-reference:

```
netconvert --sumo-net-file your_map.net.xml --plain-output-prefix plain --proj.plain-geo
```

### 5. Access Junction and Signal Light Info

Using TraCI:

* Get traffic light data: ID list, control logic, phase index, controlled lanes
* Get junction data: position, shape, ID

References:

* [https://sumo.dlr.de/docs/TraCI/Change\_Traffic\_Lights\_State.html](https://sumo.dlr.de/docs/TraCI/Change_Traffic_Lights_State.html)
* [https://sumo.dlr.de/docs/TraCI/Junction\_Value\_Retrieval.html](https://sumo.dlr.de/docs/TraCI/Junction_Value_Retrieval.html)

## Demo Scenarios

### Case 1: Traffic Light Failure from Accident

A random accident is simulated at an intersection, which disables the traffic light. The simulator then initiates a repair event until it is fixed.

### Case 2: Sensing Bias Simulation

Traffic demand data is injected with Gaussian noise to mimic sensing uncertainty during data acquisition.

## Running the Full Simulation

To run the entire integrated simulation with uncertainty modeling, services, and event handling, execute the following entry script:

```
python SmartCitySimNY.py
```

This script will initialize the simulation environment, inject uncertainty into the scenario, and launch the SUMO backend to perform a full simulation run of the New York use case.

## Citation

If you use this codebase or build upon our work, please cite:

```
@inproceedings{dong2021smart,
  title={A smart city simulation platform with uncertainty},
  author={Dong, Shuyang and Ma, Meiyi and Feng, Lu},
  booktitle={Proceedings of the ACM/IEEE 12th International Conference on Cyber-Physical Systems},
  pages={229--230},
  year={2021}
}
```
