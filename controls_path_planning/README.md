# Risk Aware Planning

## Description
The algorithm used for this challenge is a modified version of the commonly used A* algorithm, which allows for risk aversion. For each node, it calculates the g and h values normally, but in its f value calculation it adds a weight based on if the node is in a high risk zone. Because the optimal risk weight may be different for each site, 25 different weights are tested, and the path with the lowest score value is chosen. Score is determined by  **risk** + **path_length**/3.