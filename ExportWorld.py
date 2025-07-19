class ExportWorld():
    @staticmethod
    def ExportToOBJ(objects, filepath="scene.obj"):
        """Exporting the world as a 3D model in obj format"""
        with open(filepath, "w") as f:
            f.write("# Exported OBJ\n")
            vertex_index = 1 #OBJ index start from 1
            all_vertices = []
            all_faces = []

            for obj in objects.values():
                #print(obj)
                position = obj["position"]
                local_vertex_map = {}

                for vid, v in obj["vertices"].items():
                    vx, vy, vz = v + position
                    all_vertices.append(f"v {vx: .4f} {vy: .4f} {vz: .4f}")
                    local_vertex_map[vid] = vertex_index
                    vertex_index += 1

                for tri in obj["triangles"].values():
                    if not isinstance(tri, dict):
                        continue
                    indices = [local_vertex_map[i] for i in tri if isinstance(i, int)]
                    if len(indices) == 3:
                        all_faces.append(f"f {indices[0]} {indices[1]} {indices[2]}")

            f.write("\n".join(all_vertices) + "\n")
            f.write("\n".join(all_faces) + "\n")
            f.close()
            print("Exported OBJ successfully")
