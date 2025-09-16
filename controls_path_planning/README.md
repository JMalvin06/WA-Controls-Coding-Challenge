# Risk Aware Planning

## Description
The algorithm used for this challenge is a slightly modified version of the A* algorithm, which adds weights for risk aversion.  It calculates the g and h values for each node normally, but when calculating the f value it adds weight based on whether the node is in a high risk zone. Because the optimal risk weight may be different for each site, 25 different risk penalty weights are tested, and the path with the lowest score value, determined by **path_risk** + **path_length**/3, is chosen.