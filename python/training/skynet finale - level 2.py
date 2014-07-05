import sys

def print_status(agent_pos):
    print >> sys.stderr, "---------------------"
    print >> sys.stderr, "Agent is at %d" % agent_pos
    print >> sys.stderr, "Graph: %s " % str(link_graph)
    for gateway in filter(lambda x: len(link_graph[x])>1,gateways):
        print >> sys.stderr, "Gateway %d has %d links" % (gateway, len(link_graph[gateway]))

    for link in link_graph[agent_pos]:
        
    #for link in [item for item in link_graph if len(item>1)]:#filter(link_graph:
        gates = [val for val in link_graph[link] if val in gateways]
        if len(gates) >0 :
            print >> sys.stderr, "link %d has %s gates" % (link, str(gates))
    print >> sys.stderr, "---------------------"   

def get_link_graph(node_count, link_count):
    graph = {key:[] for key in range(node_count)}
    
    # get link data
    for link_index in range(link_count):
        l1, l2 = [int(i) for i in raw_input().split()]
        graph[l1].append(l2)
        graph[l2].append(l1)
    return graph

def is_node_next_to_an_exit(node):
    route_set = set(link_graph[node])
    gw_set = set(gateways)
    
    intersect = route_set & gw_set
    
    if len(intersect) > 0:
        print >> sys.stderr, "Node %d is linked to %s" % (node, str(list(intersect)))
        return list(intersect)
    else:
        return None


def are_nodes_neighbours_next_to_an_exit(node):
    print >> sys.stderr, "Agent is not linked to a gateway. Testing links to agent"
    final_link_to_sever = node
    prev_links=[]
    for link_to_sever in link_graph[node]:
        link2_to_sever = is_node_next_to_an_exit(link_to_sever)
        if link2_to_sever is not None and len(link2_to_sever) > 0 and len(link2_to_sever) >len(prev_links):
            final_link_to_sever = link_to_sever
            prev_links = link2_to_sever
    if len(prev_links) >0:
        return final_link_to_sever, prev_links
    else:
        return final_link_to_sever, None
    
def last_resort():
    print >> sys.stderr, "Guessing... Severing first gateway link I can find"
    for gateway in gateways:
        if len(link_graph[gateway]) > 0:
            return gateway, link_graph[gateway][0]
    return None, None

def perform_sever(link1, link2):
    print >> sys.stderr, "Severing link %d to %d" % (link1, link2)
    link_graph[link1].remove(link2)
    link_graph[link2].remove(link1)

    print link1, link2    

def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
            return path
    if not graph.has_key(start):
            return None
    shortest = None
    for node in graph[start]:
            if node not in path:
                    newpath = find_shortest_path(graph, node, end, path)
                    if newpath:
                            if not shortest or len(newpath) < len(shortest):
                                    shortest = newpath
    return shortest


# initialise variables
node_count, link_count, gateway_count = [int(i) for i in raw_input().split()]
link_graph = get_link_graph(node_count, link_count)
gateways = [int(raw_input()) for i in range(gateway_count)]


while 1:
    # Read information from standard input
    agent_pos = int(raw_input())

    print_status(agent_pos)
    
    link1_to_sever = agent_pos
    
    # is the agent next
    links_to_sever = is_node_next_to_an_exit(agent_pos)

    # try links to the agent
    if links_to_sever is None or len(links_to_sever)==0:
        link1_to_sever, links_to_sever = are_nodes_neighbours_next_to_an_exit(agent_pos)
    
    link2_to_sever = None
    if links_to_sever is not None:
        link2_to_sever = links_to_sever[0]

    if link2_to_sever is None:
        link1_to_sever, link2_to_sever = last_resort()

    perform_sever(link1_to_sever, link2_to_sever)
