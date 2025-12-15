#include <pybind11/pybind11.h>
#include <fstream>
#include <string>

namespace py = pybind11;

// Forward declarations for binding functions
void bind_geometry(py::module &m);
void bind_agent(py::module &m);
void bind_mission(py::module &m);

// Simple function to check if module is enabled (without JSON dependency)
bool is_module_enabled(const std::string &module_name) {
    // For now, enable core modules by default
    // You can extend this to read a simple text config file if needed
    return (module_name == "core" || module_name == "geometry");
}

PYBIND11_MODULE(orca_core, m) {
    m.doc() = "ORCA Algorithm Python Bindings - Multi-Agent Path Finding with Collision Avoidance";
    
    // Always include geometry as it's fundamental
    if (is_module_enabled("geometry")) {
        bind_geometry(m);
    }
    
    // Include core agent functionality
    if (is_module_enabled("core")) {
        bind_agent(m);
        bind_mission(m);
    }
    
    // Add version info
    m.attr("__version__") = "0.1.0";
    
    // Add module information
    m.def("get_enabled_modules", []() {
        std::vector<std::string> enabled_modules;
        std::vector<std::string> all_modules = {"core", "geometry", "experimental"};
        
        for (const auto &module : all_modules) {
            if (is_module_enabled(module)) {
                enabled_modules.push_back(module);
            }
        }
        return enabled_modules;
    }, "Get list of enabled modules");
}