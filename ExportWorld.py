import numpy as np
from BiomesType import BiomesType
import os

class ExportWorld():
    @staticmethod
    def ExportToOBJ(objects, filepath="scene.obj"):
        """Exporting the world as a 3D model in obj format"""

        def PassCubes(objects, biome, vertices, faces, vertex_counter):
            for obj in objects.values():
                if obj["biome"] != biome:
                    continue
                position = np.array(obj["position"])
                local_to_global = {}

                for local_id, v in obj["vertices"].items():
                    wp = np.array(v) + position
                    vertices.append(f"v {wp[0]:.6f} {wp[1]:.6f} {wp[2]:.6f}")
                    local_to_global[local_id] = vertex_counter
                    vertex_counter += 1

                for face in obj["triangles"].values():
                    idx = [str(local_to_global[k]) for k in face.keys() if isinstance(k, int)]
                    if len(idx) in (3, 4):
                        faces.append(f"f {' '.join(idx)}")
            return vertex_counter

        #Prepare paths
        dirname = os.path.dirname(filepath)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

        mtl_filename = os.path.splitext(filepath)[0] + ".mtl"
        mtl_basename = os.path.basename(mtl_filename)

        #Write MTL file
        with open(mtl_filename, "w") as mtl_file:
            mtl_file.write("#MTL File\n")

            #Land material (green)
            mtl_file.write("newmtl land\n")
            mtl_file.write("Ns 250.000000\n")
            mtl_file.write("Ka 1.000000 1.000000 1.000000\n")
            mtl_file.write("Kd 0.000000 0.800000 0.002411\n")
            mtl_file.write("Ks 0.500000 0.500000 0.500000\n")
            mtl_file.write("Ke 0.000000 0.000000 0.000000\n")
            mtl_file.write("Ni 1.450000\n")
            mtl_file.write("d 1.000000\n")
            mtl_file.write("illum 2\n\n")

            #Sea material (blue)
            mtl_file.write("newmtl sea\n")
            mtl_file.write("Ns 250.000000\n")
            mtl_file.write("Ka 1.000000 1.000000 1.000000\n")
            mtl_file.write("Kd 0.048158 0.000000 0.800679\n")
            mtl_file.write("Ks 0.500000 0.500000 0.500000\n")
            mtl_file.write("Ke 0.000000 0.000000 0.000000\n")
            mtl_file.write("Ni 1.450000\n")
            mtl_file.write("d 1.000000\n")
            mtl_file.write("illum 2\n\n")

        #Data collection for all groups
        land_vertices = []
        land_faces = []
        sea_vertices = []
        sea_faces = []

        vertex_counter = 1 #OBJ indices start with 1

        #Pass 1: LAND

        vertex_counter = PassCubes(objects, BiomesType.land, land_vertices, land_faces, vertex_counter)

        # for obj in objects.values():
        #     if obj["biome"] != BiomesType.land:
        #         continue
        #     position = np.array(obj["position"])
        #     local_to_global = {}
        #
        #     for local_id, v in obj["vertices"].items():
        #         wp = np.array(v) + position
        #         land_vertices.append(f"v {wp[0]:.6f} {wp[1]:.6f} {wp[2]:.6f}")
        #         local_to_global[local_id] = vertex_counter
        #         vertex_counter += 1
        #
        #     for face in obj["triangles"].values():
        #         if isinstance(face, dict):
        #             idx = [str(local_to_global[k]) for k in face.keys() if isinstance(k, int)]
        #             if len(idx) in (3, 4):
        #                 land_faces.append(f"f {' '.join(idx)}")

        #PASS 2: SEA

        vertex_counter = PassCubes(objects, BiomesType.sea, sea_vertices, sea_faces, vertex_counter)

        # #Write OBJ file
        with open(filepath, "w") as f:
            f.write("OBJ\n")
            f.write(f"mtllib {mtl_basename}\n\n")

            if land_vertices:
                f.write("o Land\n")
                f.write("\n".join(land_vertices) + "\n")
                f.write("usemtl land\n")
                f.write("s 0\n")
                f.write("\n".join(land_faces) + "\n\n")

            if sea_vertices:
                f.write("o Sea\n")
                f.write("\n".join(sea_vertices) + "\n")
                f.write("usemtl sea\n")
                f.write("s 0\n")
                f.write("\n".join(sea_faces) + "\n")


        # #Write OBJ file
        # with open(filepath, "w") as f:
        #     f.write("OBJ\n")
        #     f.write(f"mtllib {mtl_basename}\n\n")
        #
        #     vertex_offset = 1
        #     for obj_name, obj in objects.items():
        #         f.write(f"o {obj_name}\n")
        #
        #         #Write verticex
        #         position = np.array(obj["position"])
        #         for v in obj["vertices"].values():
        #             vertex_pos = (np.array(v) + position).tolist()
        #             f.write(f"v {vertex_pos[0]:.6f} {vertex_pos[1]:.6f} {vertex_pos[2]:.6f}\n")
        #
        #         #Write faces with material
        #         biome_type = obj["biome"]
        #         material = "land" if biome_type == BiomesType.land else "sea"
        #         f.write(f"usemtl {material}\n")
        #         f.write("s 0\n") #Smoothing group
        #
        #         #Write quad faces (4 vertices each)
        #         for face in obj["triangles"].values():
        #             if isinstance(face, dict):
        #                 indices = [str(vertex_offset + int(k)) for k in face.keys() if isinstance(k, (int, float)) and k not in ("color", "uv")]
        #
        #                 if len(indices) == 4:
        #                     f.write(f"f {' '.join(indices)}\n")
        #                 elif len(indices) == 3:
        #                     f.write(f"f {' '.join(indices)}\n")
        #         vertex_offset += len(obj["vertices"])

        print(f"successfully exported to {filepath} and {mtl_basename}")

