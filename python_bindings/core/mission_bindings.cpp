#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../../include/mission.h"
#include "../../include/summary.h"
#include "../../include/environment_options.h"
#include "../../include/map.h"

namespace py = pybind11;

void bind_mission(py::module &m) {
    // Mission class binding
    py::class_<Mission>(m, "Mission")
        .def(py::init<std::string, unsigned int, unsigned int, bool, size_t, bool>(),
             py::arg("file_name"), py::arg("agents_num"), py::arg("steps_threshold"),
             py::arg("time_bounded"), py::arg("time_threshold"), py::arg("speed_stop"))
        .def("read_task", &Mission::ReadTask, "Read task from XML file")
        .def("start_mission", &Mission::StartMission, "Start the simulation mission")
        .def("__repr__", [](const Mission &m) {
            return "Mission(simulation_instance)";
        });

    // Summary type binding
    py::class_<Summary>(m, "Summary")
        .def(py::init<>())
        .def("__getitem__", [](Summary &s, const std::string &key) {
            return s[key];
        })
        .def("__setitem__", [](Summary &s, const std::string &key, const std::string &value) {
            s[key] = value;
        })
        .def("get_full_summary", &Summary::getFullSummary, "Get all summary fields as dictionary")
        .def("__repr__", [](const Summary &s) {
            return "Summary(results_dict)";
        });

    // Convenience function for running simulations
    m.def("run_simulation", [](const std::string &config_file, unsigned int num_agents,
                              unsigned int max_steps, bool time_bounded, size_t time_limit,
                              bool stop_on_speed) -> Summary {
        Mission mission(config_file, num_agents, max_steps, time_bounded, time_limit, stop_on_speed);
        if (!mission.ReadTask()) {
            throw std::runtime_error("Failed to read task from file: " + config_file);
        }
        return mission.StartMission();
    }, "Run a complete ORCA simulation",
       py::arg("config_file"), py::arg("num_agents"), py::arg("max_steps") = 1000,
       py::arg("time_bounded") = false, py::arg("time_limit") = 60000,
       py::arg("stop_on_speed") = false);
}