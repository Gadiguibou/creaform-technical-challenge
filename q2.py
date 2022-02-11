from __future__ import annotations
from itertools import combinations
from math import sqrt
from typing import Optional, Tuple

# Threshold to determine equality of floats
# Chosen arbitrarily, but this could require further consideration
EPSILON = 0.00001


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def cross_product(self, other: Vector3) -> Vector3:
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector3(x, y, z)

    def dot_product(self, other: Vector3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __mul__(self, other: float) -> Vector3:
        return Vector3(
            self.x * other,
            self.y * other,
            self.z * other,
        )

    def magnitude(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


class Line:
    def __init__(self, point: Vector3, direction: Vector3):
        self.point1 = point
        self.direction = direction

    def __repr__(self):
        return f"Line({self.point1}, {self.direction})"

    def direction_vector(self):
        return self.direction


class Plane:
    # Initialize with 3 points on the plane
    def __init__(self, vertices: Tuple[Vector3, Vector3, Vector3]):
        self.vertices = vertices
        self.normal_v = (self.vertices[1] - self.vertices[0]).cross_product(
            self.vertices[2] - self.vertices[0]
        )

    def normal_vector(self) -> Vector3:
        return self.normal_v


class Pyramid:
    # Initialize with the 4 vertices of the pyramid
    def __init__(self, vertices: Tuple[Vector3, Vector3, Vector3, Vector3]):
        self.vertices = vertices

    def __repr__(self):
        return f"Polyhedron({self.vertices})"

    def faces(self) -> Tuple[Plane, Plane, Plane, Plane]:
        return tuple(Plane((f[0], f[1], f[2])) for f in combinations(self.vertices, 3))


def line_plane_intersection_point(line: Line, plane: Plane) -> Optional[Vector3]:
    # If line dot normal = 0 then the line is parallel to the plane
    if abs(line.direction_vector().dot_product(plane.normal_vector())) < EPSILON:
        return None

    # If (planePoint - linePoint) dot normal = 0 then the line is contained in the plane
    if (
        abs((plane.vertices[0] - line.point1).dot_product(plane.normal_vector()))
        < EPSILON
    ):
        return None

    # Otherwise, calculate the intersection point
    # Find the scalar d such that the intersection point p = linePoint + d * lineDirection
    d = (plane.vertices[0] - line.point1).dot_product(
        plane.normal_vector()
    ) / line.direction_vector().dot_product(plane.normal_vector())
    return line.point1 + line.direction_vector() * d


def point_in_triangle(point: Vector3, triangle: Plane) -> bool:
    # Checks whether the area of every triangle formed from a triangle edge and the point is
    # a fraction of the total triangle area (between 0 and 1) and whether the sum of the area of
    # those three triangles is 1.

    # If all of these conditions are met, the point is in the triangle.
    # Otherwise, it is not.
    triangle_area = (triangle.vertices[1] - triangle.vertices[0]).cross_product(
        triangle.vertices[2] - triangle.vertices[0]
    ).magnitude() / 2
    sub_triangle_1 = (point - triangle.vertices[1]).cross_product(
        point - triangle.vertices[2]
    ).magnitude() / (2 * triangle_area)
    sub_triangle_2 = (point - triangle.vertices[2]).cross_product(
        point - triangle.vertices[0]
    ).magnitude() / (2 * triangle_area)
    sub_triangle_3 = (point - triangle.vertices[0]).cross_product(
        point - triangle.vertices[1]
    ).magnitude() / (2 * triangle_area)

    return (
        all(0 <= area <= 1 for area in [sub_triangle_1, sub_triangle_2, sub_triangle_3])
        and sub_triangle_1 + sub_triangle_2 + sub_triangle_3 - 1 < EPSILON
    )


def line_intersection_with_pyramid(line: Line, pyramid: Pyramid) -> bool:
    # For each face look for the intersection point between the line and the face
    # If there is one, check whether that intersection point is within the face and the line
    for face in pyramid.faces():
        intersection_point = line_plane_intersection_point(line, face)
        if intersection_point is None:
            continue
        if point_in_triangle(intersection_point, face):
            return True
    return False


if __name__ == "__main__":
    # Test with a pyramid that should be crossed by the line
    line = Line(Vector3(0, 0, 0), Vector3(1, 1, 1))
    pyramid = Pyramid(
        (Vector3(0, 0, 0), Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(1, 1, 1))
    )
    # Should return True
    print("Should be True:", line_intersection_with_pyramid(line, pyramid))

    # Test with a pyramid that should not be crossed by the line
    pyramid2 = Pyramid(
        (Vector3(0, 0, 0), Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, -1))
    )
    # Should return False
    print("Should be False:", line_intersection_with_pyramid(line, pyramid2))
