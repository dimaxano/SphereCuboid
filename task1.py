import sys

import numpy as np
import h5py
import pyransac3d as pyrsc
# import open3d as o3d

# horizontal_fov_deg = 60.0
# vertical_fov_deg = 40.0

CHEAT_CONSTANT = -100 # x-axis division between the two object
height = 140
width = 200

cx, cy = width // 2 + 0.5, height // 2 + 0.5
focal = 1
K = np.array([[focal, 0, cx], [0, focal, cy], [0, 0, 1]])


def calculate_sphere_statisctics(radius):
    """
        Calculates surface area and volume of a sphere with given radius

        retunrs: surface area, volume
    """
    surface_area = 4 * np.pi * radius**2
    volume = 4/3 * np.pi * radius**3
    return surface_area, volume

if __name__ == "__main__":
    filename = "./cuboid-sphere.hdf5"

    with h5py.File(filename, "r") as f:
        depth = f.get('depth_map')[:]

    # depth to point cloud
    sphere_points = []
    cuboid_points = []
    for v in range(height):
        for u in range(width):
            if not np.isnan(depth[v, u]):
                z = depth[v, u]
                x = (u - cx) * z / focal
                y = (v - cy) * z / focal
                z = z * 100 # scale z 

                if x < CHEAT_CONSTANT:
                    sphere_points.append([x, y, z])
                else:
                    cuboid_points.append([x, y, z])

    # sphere stuff 
    sphere_points = np.array(sphere_points)

    sphere = pyrsc.Sphere()
    center, r, _ = sphere.fit(sphere_points, thresh=0.4)
    sphere_surface_area, sphere_volume = calculate_sphere_statisctics(r)

    print(f"Sphere center: {center}")
    print(f"Sphere surface area: {sphere_surface_area}")
    print(f"Sphere volume: {sphere_volume}")

    cuboid_points = np.array(cuboid_points)

    # cuboid_pcd = o3d.geometry.PointCloud()
    # cuboid_pcd.points = o3d.utility.Vector3dVector(cuboid_points)
    # box = cuboid_pcd.get_oriented_bounding_box(robust=True)
    # l, w, h = cuboid.extent 

    # print(f"Cuboid center: {box.center}")
    # print(f"Cuboid surface area: {2(l*w+w*h+l*h)}")
    # print(f"Cuboid volume: {l*w*h}")

    with h5py.File("cuboid-sphere-point-cloud.hdf5", "w") as f:
        f.create_dataset("point_cloud", data=cuboid_points)
        f.create_dataset("sphere_points", data=sphere_points)