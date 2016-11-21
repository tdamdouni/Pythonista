def bring_to_front(self, layer):
   """bring layer to the front, if it exists as a sublayer (otherwise nothing changes).  This assumes that sublayer[0] is the bottom layer, so sorts the list so layer is at the end."""
   self.root_layer.sublayers.sort( 
                    key=lambda x: x == layer,
                    reverse=False)

def send_to_back(self,layer):
   """send layer to the back, if it exists as a sublayer (otherwise nothing changes).  This assumes that sublayer[0] is the bottom layer, so sorts the list so layer is at the front"""
   self.root_layer.sublayers.sort( 
                    key=lambda x: x == layer,
                    reverse=True)
