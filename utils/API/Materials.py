import json
from pathlib import Path
from dataclasses import asdict
from DefineMaterialsCmd import __dir__
from DefineMaterialsCmd import Material

class Materials:
    def __init__(self, material: Material = None):
        self.material = material
        self.path_file = Path(__dir__, "data", "materials.json")

    def save(self):
        """ Add new material to materials file """
        # Prepare data to save
        dict_material = asdict(self.material)

        # Save within file
        def doesntexists():
            # define it
            dict_mat = { "materials": [dict_material] }

            # json it
            json_content = json.dumps(dict_mat)

            # save it
            file.write(json_content)

        # Operation on data file
        with self.path_file.open("r+") as file:
            
            if self.path_file.is_file(): # File exists
                # read it
                content = self.path_file.read_text()
                print(len(content))

                if len(content) > 0:
                    # decode it
                    json_decoder = json.JSONDecoder()
                    json_content = json_decoder.decode(content) # { "materials": [{ "materialName": "name", weight: 12 }] }

                    # Add to materials it
                    json_content["materials"].append(dict_material)

                    # save in file it
                    file.write(json.dumps(json_content))
                else:
                    doesntexists()
            else: # File doesn't exists
                doesntexists()

    def get_all(self):
        # read it
        content = self.path_file.read_text()

        # unjson it -> list[dict]
        json_dict = json.loads(content)["materials"]

        # To Material class each
        output = []
        for json_mat in json_dict:
            one = Material(**json_mat)
            output.append(one)

        return output
    
    def to_list(self):
        """ Transform materials class to list with materials rows only fields """
        all = self.get_all()

        results = []
        for row in all:
            results.append([row.materialName, row.weight])
        
        return results