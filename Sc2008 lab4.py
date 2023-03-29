#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# # Load and Clean Data

# In[2]:


#Add header and clean up dataframe
df1 = pd.read_csv('SFlow_Data_lab4.csv', header = None)

df1.columns = ["Type", "sflow_agent_address", "inputPort", "outputPort", "src_MAC", "dst_MAC", "ethernet_type", 
              "in_vlan", "out_vlan", "src_IP", "dst_IP", "IP_protocol", "ip_tos", "ip_ttl",  
              "udp_src_port/tcp_src_port/icmp_type", "udp_dst_port/tcp_dst_port/icmp_code", "tcp_flags", "packet_size",
              "IP_size", "sampling_rate", "foo"]

df = df1.drop(labels = "foo", axis = 1)
df


# # Top 5 Talkers (ie Sender Nodes)

# In[3]:


#Top 5 Talkers

#uniqueTalkers = df["src_IP"].unique()
    
df["src_IP"].value_counts().head(5)


# # Top 5 Listeners (ie receiving nodes)
# 

# In[4]:


#Top 5 Listeners

df["dst_IP"].value_counts().head(5)


# # Proportion of TCP and UDP packets

# In[6]:


#% of tcp and udp protocol

total_traffic = df["IP_protocol"].count()

#df["IP_protocol"].value_counts()

df["IP_protocol"].value_counts(normalize = True).mul(100).round(1).astype(str) + '%'


# # Top 5 Application

# In[7]:


#Application Protocol

df["udp_dst_port/tcp_dst_port/icmp_code"].value_counts().head(5)


# # Total Traffic

# In[8]:


#Total traffic (TBC)

#convert form bits to MB and divide by sampling rate
df["IP_size"].sum() / (1024*1024*8) / (1/2048)


# # Top 5 Communication Pairs

# In[9]:


#Top 5 communication pairs

df_grouped = df.groupby(["src_IP", "dst_IP"]).size()

df_grouped.sort_values(ascending = False).head(5)


# # Visualizing Communication Between Different IP Hosts

# In[10]:


import networkx as nx
import matplotlib.pyplot as plt


# In[11]:



G = nx.from_pandas_edgelist(df, source='src_IP', target='dst_IP', edge_attr=True, create_using=nx.DiGraph())


# In[12]:


G.number_of_nodes()


# In[13]:


G.number_of_edges()


# In[14]:


G.degree()


# In[15]:


G.is_directed()


# In[16]:


nx.draw_networkx(G)


# In[17]:


# NetworkX sensible visualization threshold

viz_threshold = 500


# In[27]:


# Determine graph size
def set_size(df, n, sample_size):
    """Evaluates the count of records to determine graph size to adjust visualization styling"""
    if n > viz_threshold: # Maxim visualization threshold
        print("Records exceed visualization threshold, taking %s samples\n" % (sample_size))
        df = df.sample(n=sample_size) # take random sample
        n=len(df) # recalculate record count    
    if ((n <= 500) and (n > 250)):
        size = 'huge'
    elif ((n <= 250) and (n > 150)):
        size = 'large'
    elif ((n <= 150) and (n > 100)):
        size = 'medium'
    elif ((n <= 100) and (n > 50)):
        size = 'small'
    else:
        size = 'tiny'
    return(df, size)

# Print debug data for pandas DataFrame
def describe_pandas_data(df):
    """Prints out basic characteristics for a pandas dataframe"""
    print("\nPandas Data Description")
    print("\nFirst 5 Records\n")
    print(df.head(5))
    print("\nLast 5 Records\n")
    print(df.tail(5))
    print("\nData types\n")
    print(df.dtypes)
    print("\nCheck for NaN fields\n")
    print(df.isna().sum())
    print("\n")
    print("\nDescribe data\n")
    print(df.describe())
    print("\n")
    return

# Print debug data for networkx graph
def debug_graph_data(G):
    """Prints out additional debug data to troubleshoot graph data"""
    print("\nNodes in dataset\n")
    print(G.nodes())
    print("\nEdges in dataset\n")
    print(G.edges())
    print("\nEdges with data\n")
    print(G.edges.data())
    print("\nNodes and degrees\n")
    print(G.degree())
    print("\nIs the Graph directed?\n")
    print(G.is_directed())
    print("\nIs the Graph weighted?\n")
    print(nx.is_weighted(G))
    print("\n")
    return

def describe_graph(G):
    """Prints basic characteristics for a network graph"""
    print("\nGraph Description")
    print("Count of Records in data set")
    print(len(df))
    print("\nCount of nodes in dataset\n")
    print(G.order())
    print("\nCount of edges in dataset\n")
    print(G.number_of_edges())
    print("\n")
    return


# In[28]:


sample_size = 250

# Set variable for total count of records
n=len(df)

# Set plt.figure.figsize based on sample size
df, size = set_size(df, n, sample_size)
print("Graph Size: %s" % size)


# In[29]:


# create lists of edges and style attributes based on IP protocol

#TCP
# Create list to draw distinct edges for TCP connections
tcp_list = [
    (s, t) for s, t in G.edges
    if G.edges[s, t]['IP_protocol'] == 6]
# Set color for TCP edge line
tcp_color = '#11BB25'
# Set the style line (solid|dashed|dotted,dashdot)
tcp_line_style = 'solid'
# Set transparency for the TCP edge line
tcp_alpha = 1

# UDP
udp_list = [
    (s, t) for s, t in G.edges
    if G.edges[s, t]['IP_protocol'] == 17]
udp_color = '#258BE9'
udp_line_style = 'dashdot'
udp_alpha = 0.8

#ICMP
icmp_list = [
    (s, t) for s, t in G.edges
    if G.edges[s, t]['IP_protocol'] == 1]
icmp_color = '#E92B25'
icmp_line_style = 'dashed'
icmp_alpha = 0.8


# In[32]:


# Check what size our graph is, and assign stylings
if size == 'huge':
        fig_size = (50,50)
        font_size = 20
        lwidth = 3
        arrow_size = 20
        node_dot = 20
if size == 'large':
        fig_size = (100,100)
        font_size = 16
        lwidth = 1
        arrow_size = 10
        node_dot = 10
if size == 'medium':
        fig_size = (25,25)
        font_size = 12
        lwidth = 0.8
        arrow_size = 8
        node_dot = 8
if size == 'small':
        fig_size = (10,10)
        font_size = 8
        lwidth = 0.6
        arrow_size = 6
        node_dot = 6
if size == 'tiny':
        fig_size = (5,5)
        font_size = 6
        lwidth = 0.4
        arrow_size = 5
        node_dot = 5

# Colors for edges, labels and nodes
edge_font_color = '#000000'
label_font_color = '#000000'
nodes_color = "#ED805E"


# In[33]:


# get edge attributes to draw edge labels
edge_proto=nx.get_edge_attributes(G,'proto')

#Define our Graph Plot Layouts
layouts = (nx.spring_layout, nx.random_layout, nx.spiral_layout, nx.circular_layout)
title = ("Force-directed", "Random", "Spiral", "Circular")

## Create our Plots

# Create 4 subplots with the figure size based on graph size
_, plot = plt.subplots(4, 1, figsize=fig_size)
subplots = plot.reshape(1, 4)[0]
# Draw a plot for each layout
for plot, layout, title in zip(subplots, layouts, title):
    pos = layout(G)
    nx.draw_networkx_edges(G, pos, ax=plot, edgelist=tcp_list, width=lwidth, style=tcp_line_style, edge_color=tcp_color, alpha=tcp_alpha, arrows=True, arrowsize=arrow_size, arrowstyle="-|>")
    nx.draw_networkx_edges(G, pos, ax=plot, edgelist=udp_list, width=lwidth, style=udp_line_style, edge_color=udp_color, alpha=udp_alpha, arrows=True, arrowsize=arrow_size, arrowstyle="->")
    nx.draw_networkx_edges(G, pos, ax=plot, edgelist=icmp_list, width=lwidth, style=icmp_line_style, edge_color=icmp_color, alpha=icmp_alpha, arrows=True, arrowsize=arrow_size, arrowstyle="->")
    nx.draw_networkx_edge_labels(G, pos, ax=plot, font_color=edge_font_color, edge_labels= edge_proto, font_size=font_size)
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=plot, node_color=nodes_color, node_shape="D", nodelist=dict(G.degree).keys(), node_size=[d * node_dot for d in dict(G.degree).values()])
    # Draw labels
    nx.draw_networkx_labels(G, pos, ax=plot, font_color=label_font_color, font_size=font_size)
    plot.set_title(title)
# Draw with tight layout https://matplotlib.org/tutorials/intermediate/tight_layout_guide.html
plt.tight_layout()
plt.show(block=False)


# Double click to enlarge the image.
# 
# Green lines represent TCP, Blue lines represent UDP. 
# 
# Mostly green lines, which coincides with the data analysis above.

# In[ ]:




