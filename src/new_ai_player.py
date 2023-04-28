from src.player import Player


class AIPlayer(Player):
    

    def take_turn(self, node_buttons, built_roads):
        for node_button in node_buttons:
        
            for road in built_roads:
                start_node_x = road[0].x_pos
                end_node_x = road[1].x_pos
                
                if not node_button.x_pos == start_node_x and not node_button.x_pos == end_node_x:
                    return (True, node_button)
        return (False, None)
