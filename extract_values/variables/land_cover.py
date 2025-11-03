from enum import Enum


class LandCoverGroup(Enum):
    FOREST = 'LC_Forest', ['50', '60', '70', '80', '90'], "Land cover: forest (%)"


    def get_lc(self):
        return

    def get_name(self, buffer:int = None):
        """Get the name of the variable used in further processing."""
        name = self.value[0]
        if buffer is not None:
            if buffer == 10000:
                name += '_buf_A'
            elif buffer == 30000:
                name += '_buf_B'
            elif buffer == 50000:
                name += '_buf_C'
            else:
                name = name

        return name
