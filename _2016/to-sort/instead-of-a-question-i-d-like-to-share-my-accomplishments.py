# https://forum.omz-software.com/topic/3261/instead-of-a-question-i-d-like-to-share-my-accomplishments

# The following is all contained in my Map(object) class, which defines the grid.

# This method goes through EVERY tile and resets ALL relevant values to their initial state, to make sure that the pathfinding method can run. This is where I suspect I could be more efficient, but I haven't come up with a solution yet.
def reset_map(self):
        for y in range(self.numy):
            for x in range(self.numx):
                # self.map[y][x] is the coordinates for each tile, which are defined as their own Tile(object) class. Checksum is the value given to them which indicates distance from the start. It defaults to the size of the map in order to be error-proof later.
                self.map[y][x].checksum = (self.numx * self.numy)
                self.map[y][x].checked = False # Whether or not the algorithm has visited this tile.
                self.map[y][x].label.text = ""
                
                if self.map[y][x].type == 0: # Type 0 refers to "empty" tiles. This leaves "wall" tiles intact.
                    self.map[y][x].node.fill_color = 'white'
        # The start and finish tiles look different. More importantly, the start tile needs to be pre-initialized with checksum and checked values or else the algorithm gets angry.
        self.start.checksum = 0
        self.start.checked = True
        self.start.node.fill_color = 'green'
        self.finish.node.fill_color = 'red'


# This method is the one that does the bulk of the work.
    def pathfinding(self):

        # Calls the previous method to make sure all variables are ready.
        self.reset_map()
        
        # This is the list which will hold all tiles which make up the shortest path to the finish. It needs to be empty.
        del self.pathtofinish[:]
    
        # These two lists work in conjunction below to keep track of the next set of tiles to examine and give a checksum value to. Technically it could be done with one list I think? But this was the easiest solution for now.
        list = []
        list2 = []
        list2.append(self.start)
        # Simple status-checks
        foundfinish = False
        trapped = False
        
        # Basically... keep processing tiles until you find the finish or have nowhere else to go.
        while foundfinish == False and trapped == False:
            
            # 'list' always contains the latest tiles which were checked. Also known as the "frontier".
            for i in range(len(list)):
                
                # 'list' contains Tile instances, each of which has a method called 'neighbors'. This method identifies all neighboring tiles and failsafes against the boundaries of the grid.
                neighbors = list[i].neighbors
                
                # Loop through all neighbors for the current tile.
                for j in range(len(neighbors)):
                
                    # If it's not a wall (1) and it hasn't been checked and the finish hasn't been found yet, process the tile.
                    if not neighbors[j].type == 1 and neighbors[j].checked == False and foundfinish == False:

                        # Every tile gets a checksum value equal to that of its predecessor, then it's marked as checked and added to 'list2', which will contain all tiles which will form the next frontier.
                        neighbors[j].checksum = (list[i].checksum + 1)
                        neighbors[j].checked = True
                        list2.append(neighbors[j])

                        # Type 3 = the finish tile. After coloring it red, those variable adjustments are all meant to stop all of the current loops immediately instead of hanging.
                        if neighbors[j].type == 3:
                            neighbors[j].node.fill_color = 'red'
                            foundfinish = True
                            j = range(len(neighbors) - 1)
                            i = range(len(list) - 1)
            # This is where the lists get a little wonky... empty list, transfer list2 to list, then empty list2.
            del list[:]
            list = list2[:]
            del list2[:]

            # If the list is empty, then we must be trapped (because there's no tiles to check). This will exit the ground-level loop.
            if len(list) == 0:
                trapped = True
        # If we AREN'T trapped, then it's safe to generate a path!
        if trapped == False:
            self.generate_path()


# Pretty self-explanatory really....
    def generate_path(self):

        # We only need to look at one tile at a time, starting with the finish tile. Add it to the pathtofinish list.
        current = self.finish
        self.pathtofinish.append(self.finish)

        # We're going to run this process for as many steps as there are tiles in the shortest path.
        for i in range(self.finish.checksum):
            
            # Maybe not the best, but j is used as a "fake" loop, incremented at the end of the while loop.
            j = 0
            nextfound = False

            # Loop until the next tile in the path has been found. It will ALWAYS find a tile so it's safe.
            while nextfound == False:

                # We'll examine each neighboring tile one at a time.
                selected = current.neighbors[j]
                
                # If the selected tile has a lower value then the current one, then it's part of the shortest path.
                if selected.checksum < current.checksum:

                    # Append it to the pathtofinish list, make it the next current tile, rinse and repeat.
                    self.pathtofinish.append(selected)
                    current = selected
                    nextfound = True

                j += 1

        # Reverse the list for easier use later, then draw the path (pretty simple).
        self.pathtofinish.reverse()
        self.draw_path()
# --------------------
