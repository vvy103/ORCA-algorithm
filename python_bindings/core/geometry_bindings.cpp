#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include "../../include/geom.h"

namespace py = pybind11;

void bind_geometry(py::module &m) {
    // Point class binding
    py::class_<Point>(m, "Point")
        .def(py::init<>())
        .def(py::init<float, float>())
        .def(py::init<const Point&>())
        .def("x", &Point::X, "Get X coordinate")
        .def("y", &Point::Y, "Get Y coordinate")
        .def("get_pair", &Point::GetPair, "Get (x, y) as pair")
        .def("scalar_product", &Point::ScalarProduct, "Compute scalar product with another point")
        .def("euclidean_norm", &Point::EuclideanNorm, "Compute Euclidean norm")
        .def("squared_euclidean_norm", &Point::SquaredEuclideanNorm, "Compute squared Euclidean norm")
        .def("det", &Point::Det, "Compute determinant with another point")
        .def("to_string", &Point::ToString, "Convert to string representation")
        .def(py::self - py::self)
        .def(py::self + py::self)
        .def(py::self == py::self)
        .def(py::self * float())
        .def(py::self / float())
        .def(-py::self)
        .def("__repr__", [](const Point &p) {
            return "Point(" + std::to_string(p.X()) + ", " + std::to_string(p.Y()) + ")";
        });

    // Node class binding
    py::class_<Node>(m, "Node")
        .def(py::init<int, int, Node*, double, double, int, int>(),
             py::arg("i") = 0, py::arg("j") = 0, py::arg("parent") = nullptr,
             py::arg("g") = 0, py::arg("h") = 0, py::arg("depth") = 0, py::arg("conflicts") = 0)
        .def_readwrite("i", &Node::i)
        .def_readwrite("j", &Node::j)
        .def_readwrite("F", &Node::F)
        .def_readwrite("g", &Node::g)
        .def_readwrite("H", &Node::H)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self)
        .def("__repr__", [](const Node &n) {
            return "Node(" + std::to_string(n.i) + ", " + std::to_string(n.j) + ")";
        });

    // Vertex class binding
    py::class_<Vertex, Point>(m, "Vertex")
        .def(py::init<>())
        .def(py::init<float, float, bool>(), py::arg("x"), py::arg("y"), py::arg("convex") = false)
        .def(py::init<const Point&, bool>(), py::arg("point"), py::arg("convex") = false)
        .def("is_convex", &Vertex::IsConvex)
        .def("set_convex", &Vertex::SetConvex);

    // ObstacleSegment class binding
    py::class_<ObstacleSegment>(m, "ObstacleSegment")
        .def(py::init<>())
        .def(py::init<int, const Vertex&, const Vertex&>())
        .def_readwrite("id", &ObstacleSegment::id)
        .def_readwrite("left", &ObstacleSegment::left)
        .def_readwrite("right", &ObstacleSegment::right)
        .def_readwrite("dir", &ObstacleSegment::dir)
        .def(py::self == py::self);

    // Utility functions
    m.def("sq_point_seg_distance", &Utils::SqPointSegDistance,
          "Compute squared distance from point to line segment");
}