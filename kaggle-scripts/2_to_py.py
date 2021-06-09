import subprocess
import pickle
from pathlib import Path
import os

class Session:
    def __init__(self, session_path):
        """
        The conversion process can last for days. We have to handle interruptions.
        Session has 3 attributes:
        session.index: int
        session.index_file_path: Path
        session.file_list: list
        """
        list_file_path = session_path / "session_file_list.pickle"
        if not list_file_path.exists():
            print(f"{list_file_path} not found, creating...")
            file_list = list(sample_path.glob("**/*.ipynb"))
            with open(list_file_path, mode="wb") as list_file:
                pickle.dump(file_list, list_file)

        index_file_path = session_path / "session_index.pickle"
        if not index_file_path.exists():
            print(f"{index_file_path} not found, creating...")
            index = 0
            with open(index_file_path, mode="wb") as index_file:
                pickle.dump(index, index_file)

        
        with open(list_file_path, mode="rb") as list_file:
            self.file_list: list = pickle.load(list_file)

        with open(index_file_path, mode="rb") as index_file:
            self.index: int = pickle.load(index_file)

        self.index_file_path = index_file_path

        print(f"starting from {self.index=}")

    def set_index(self, value:int):
        """
        Makes index updates persistent
        """

        self.index = value
        with open(self.index_file_path, mode = "wb") as f:
            pickle.dump(self.index, f)
            f.flush()
            os.fsync(f)
        print(f"wrote {self.index} to file")
        

def all_to_py(session: Session):
    """
    All files inside session.file_list will be converted from ipynb to py.
    Saves progress on every file
    """

    successful = 0
    total = 0
    while session.index < len(session.file_list):
        ipynb = session.file_list[session.index]
        process = subprocess.run(
            ["jupyter", "nbconvert", "--to", "script", ipynb.as_posix()],
            capture_output=True,
        )
        print(f"{process.stdout=}\n{process.stderr=}")
        successful = successful + 1 if process.returncode == 0 else successful
        total += 1
        session.set_index(session.index + 1)
    print(f"{total=}, {successful=}")

    return None


if __name__ == "__main__":

    sample_path = Path("G:/bachelor/bigsample")
    session = Session(Path("G:/bachelor"))
    
    all_to_py(session)
