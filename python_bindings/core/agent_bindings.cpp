#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include "../../include/agent.h"

namespace py = pybind11;

void bind_agent(py::module &m) {
    // AgentParam class binding
    py::class_<AgentParam>(m, "AgentParam")
        .def(py::init<>())
        .def_readwrite("sight_radius", &AgentParam::sightRadius)
        .def_readwrite("time_boundary", &AgentParam::timeBoundary)
        .def_readwrite("time_boundary_obst", &AgentParam::timeBoundaryObst)
        .def_readwrite("radius", &AgentParam::radius)
        .def_readwrite("r_eps", &AgentParam::rEps)
        .def_readwrite("max_speed", &AgentParam::maxSpeed)
        .def_readwrite("agents_max_num", &AgentParam::agentsMaxNum);

    // Abstract Agent class binding (simplified for now)
    py::class_<Agent>(m, "Agent")
        .def("set_position", &Agent::SetPosition, "Set agent position")
        .def("get_position", &Agent::GetPosition, "Get agent position")
        .def("get_velocity", &Agent::GetVelocity, "Get agent velocity")
        .def("get_radius", &Agent::GetRadius, "Get agent radius")
        .def("get_id", &Agent::GetID, "Get agent ID")
        .def("is_finished", &Agent::isFinished, "Check if agent reached goal")
        .def("init_path", &Agent::InitPath, "Initialize path planning")
        .def("get_collision", &Agent::GetCollision, "Get collision statistics")
        .def("add_neighbour", &Agent::AddNeighbour, "Add neighboring agent")
        .def("update_neighbour_obst", &Agent::UpdateNeighbourObst, "Update obstacle neighbors")
        .def(py::self == py::self)
        .def(py::self != py::self);
}