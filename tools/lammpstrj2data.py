import MDAnalysis as mda
import argparse


def replace_coordinates_and_write(data_file_path, coords, output_file_path):
    """
    Read a LAMMPS data file and a trajectory file, replace the coordinates in the data file
    with the coordinates from the trajectory, and write the updated data file.

    Parameters:
    data_file_path (str): Path to the LAMMPS data file
    trajectory_file_path (str): Path to the LAMMPS trajectory file
    output_file_path (str): Path to the output file where the updated data file will be written
    """
    # Load the universe with the data file and trajectory file
    u = mda.Universe(data_file_path)

    u.atoms.positions = coords

    # Write the updated data file for each timestep
    # Note: This example assumes the LAMMPS data file writer is available in MDAnalysis
    # The exact method to write the data file may vary depending on the version of MDAnalysis
    u.atoms.write(output_file_path.format())


# Example usage
# replace_coordinates_and_write('path_to_data_file', 'path_to_trajectory_file', 'output_data_file_{}.lammps')


def read_lammps_trajectory(file_path):
    """
    Read a LAMMPS trajectory file and extract the atom positions for each timestep.

    Parameters:
    file_path (str): Path to the LAMMPS trajectory file

    Returns:
    dict: A dictionary with timestep as keys and atom position data as values
    """
    trajectory_data = {}
    with open(file_path, "r") as file:
        frame = 0
        while True:
            line = file.readline()
            if not line:
                break  # End of file

            if "ITEM: TIMESTEP" in line:
                timestep = int(file.readline().strip())
                trajectory_data[frame] = []

            if "ITEM: NUMBER OF ATOMS" in line:
                n_atoms = int(file.readline().strip())

            if "ITEM: ATOMS" in line:
                for i in range(n_atoms):
                    atom_line = file.readline().strip()
                    atom_data = atom_line.split()
                    trajectory_data[frame].append(atom_data[2:5])
                frame += 1

    return trajectory_data


def replace_molids_in_data_file(original_data_file, output_data_file, N):
    """
    Replace molid in a LAMMPS data file. Each group of N atoms will have a unique molid.

    Parameters:
    original_data_file (str): Path to the original LAMMPS data file
    output_data_file (str): Path to the output data file with updated molids
    N (int): Number of atoms per molecule
    """
    with open(original_data_file, "r") as file:
        lines = file.readlines()

    with open(output_data_file, "w") as file:
        atom_section = False
        atom_id = 1
        for line in lines:
            if "Atoms" in line:  # Start of atom section
                atom_section = True
                file.write(line)
                continue

            # End of atom section if the line is empty or another section begins
            if atom_section and (
                "Bonds" in line or "Angles" in line or "Velocities" in line
            ):
                atom_section = False

            if atom_section and line.strip() != "":
                line_parts = line.split()
                molid = (atom_id - 1) // N + 1  # Calculate new molid
                line_parts[1] = str(molid)  # Replace molid in the line
                updated_line = " ".join(line_parts) + "\n"
                file.write(updated_line)
                atom_id += 1
            else:
                file.write(line)


# Example usage
# replace_molids_in_data_file('original_data_file.lammps', 'output_data_file.lammps', 400)


if __name__ == "__main__":
    # Read the trajectory file and store the data
    parser = argparse.ArgumentParser(
        description="Convert lammpstrj files to data files"
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=str,
        help="Paths to the input files (lammpstrj).",
    )
    parser.add_argument(
        "-d", "--data", required=True, type=str, help="Refference data file."
    )
    parser.add_argument(
    "-s", "--sparse", type=str, default="1", help="Reference data file."
    )

    args = parser.parse_args()
    sparse = int(args.sparse)  # sparseを整数に変換
    trajectory = read_lammps_trajectory(args.input)
    # trajectoryのキー（フレーム番号）を取得して整数型に変換、ソート
    sorted_keys = sorted(trajectory.keys(), key=int)

    Natoms = 400

    j = 0
    for i in sorted_keys[::sparse]:
        output_path = str(j).zfill(2) + ".data"
        replace_coordinates_and_write(args.data, trajectory[i], output_path)
        replace_molids_in_data_file(output_path, output_path, Natoms)
        j += 1
