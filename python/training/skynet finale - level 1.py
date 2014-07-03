import sys


links = {}
gateways = []

def init():
    # indexes of values to care about
    link_count = 1
    gateway_count = 2

    # get raw input as a list of ints
    init_counts = map(lambda x:int(x), raw_input().split())
    
    # get link data
    for link_index in range(init_counts[link_count]):
        node_indexes = map(lambda x:int(x), raw_input().split())
        
        if node_indexes[0] not in links:
            links[node_indexes[0]] = [node_indexes[1]]
        else:
            links[node_indexes[0]].append(node_indexes[1])
            
        if node_indexes[1] not in links:
            links[node_indexes[1]] = [node_indexes[0]]
        else:
            links[node_indexes[1]].append(node_indexes[0])

    # get gateways
    for gateway_index in range(init_counts[gateway_count]):
        gateway = raw_input()
        if gateway not in gateways:
            gateways.append(int(gateway))
    print >> sys.stderr, "---------------------"
    print >> sys.stderr, "Nodes : %s " % str(links)
    print >> sys.stderr, "Gateways : %s" % str(gateways)
    print >> sys.stderr, "---------------------"

def is_node_next_to_an_exit(node):
    routes = links[node]
    for gateway in gateways:
        if gateway in routes:
            print >> sys.stderr, "Node %d is linked to gateway %d!" % (node, gateway)
            return gateway
    return None

def are_nodes_neighbours_next_to_an_exit(node):
    print >> sys.stderr, "Agent is not linked to a gateway. Testing links to agent"
    
    for link_to_sever in links[node]:
        link2_to_sever = is_node_next_to_an_exit(link_to_sever)
        if link2_to_sever is not None:
            return link_to_sever, link2_to_sever

    return node, None
    
def last_resort():
    print >> sys.stderr, "Guessing... Severing first gateway link I can find"
    for gateway in gateways:
        if len(links[gateway]) > 0:
            return gateway, links[gateway][0]
    return None, None

def perform_sever(link1, link2):
    print >> sys.stderr, "Severing link %d to %d" % (link1, link2)
    links[link1].remove(link2)
    links[link2].remove(link1)

    print link1, link2    
    
init()

while 1:
    # Read information from standard input
    agent_pos = int(raw_input())
    
    print >> sys.stderr, "Agent is at %d" % agent_pos
    
    link1_to_sever = agent_pos
    
    # is the agent next
    link2_to_sever = is_node_next_to_an_exit(agent_pos)
    
    # try links to the agent
    if link2_to_sever is None:
        link1_to_sever, link2_to_sever = are_nodes_neighbours_next_to_an_exit(agent_pos)
    
    if link2_to_sever is None:
        link1_to_sever, link2_to_sever = last_resort()
        
    perform_sever(link1_to_sever, link2_to_sever)
