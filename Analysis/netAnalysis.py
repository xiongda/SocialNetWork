#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import snap
from models import Net,Node,Edge

def getBasicInfo(strPath, net):

    G = snap.LoadEdgeList(snap.PUNGraph,strPath,0,1)
    GraphInfo = {}
    GraphInfo['nodes'] = G.GetNodes()
    GraphInfo['edges'] = G.GetEdges()
    GraphInfo['zeroDegNodes'] = snap.CntDegNodes(G, 0)
    GraphInfo['zeroInDegNodes'] = snap.CntInDegNodes(G, 0)
    GraphInfo['zeroOutDegNodes'] = snap.CntOutDegNodes(G, 0)
    GraphInfo['nonZeroIn-OutDegNodes'] = snap.CntNonZNodes(G)
    GraphInfo['uniqueDirectedEdges'] = snap.CntUniqDirEdges(G)
    GraphInfo['uniqueUndirectedEdges'] = snap.CntUniqUndirEdges(G)
    GraphInfo['selfEdges'] = snap.CntSelfEdges(G)
    GraphInfo['biDirEdges'] = snap.CntUniqBiDirEdges(G)

    NTestNodes = 10
    IsDir = False
    GraphInfo['approxFullDiameter'] = snap.GetBfsEffDiam(G, NTestNodes, IsDir)
    GraphInfo['90effectiveDiameter'] = snap.GetAnfEffDiam(G)

    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(G, DegToCntV)
    sumofNode = G.GetNodes()
    L = [item.GetVal1()*item.GetVal2() for item in DegToCntV]
    GraphInfo['averageDegree'] = float(sum(L))/(sumofNode)

    (DegreeCountMax ,Degree, DegreeCount, CluDegree, Clu) = getGraphInfo(G)
    # creatNet(G,net)

    return GraphInfo,DegreeCountMax , Degree, DegreeCount, CluDegree, Clu

def getGraphInfo(G):
    
    Degree = []
    DegreeCount = []
    CluDegree = []
    Clu = []

    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(G, DegToCntV)
    DegreeCountMax = 0
    for item in DegToCntV:
        tempy = item.GetVal2()
        if tempy > DegreeCountMax:
            DegreeCountMax = tempy
        Degree.append(item.GetVal1())
        DegreeCount.append(tempy)


    CfVec = snap.TFltPrV()
    Cf = snap.GetClustCf(G, CfVec, -1)
    for pair in CfVec:
        CluDegree.append(pair.GetVal1())
        Clu.append(pair.GetVal2())

    return DegreeCountMax,Degree,DegreeCount,CluDegree,Clu
    
def creatNet(G,net):

    # G = snap.LoadEdgeList(snap.PUNGraph,"d:\\networkdata\\show\\facebook.txt",0,1)
    # for NI in G.Nodes():
    #   print "node: %d, out-degree %d, in-degree %d" % ( NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
    nodeIDs = set()
    nodes = []
    edges = []
    for EI in G.Edges():

        # print "edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
        id = EI.GetDstNId()
        if id not in nodeIDs:
            nodeIDs.append(id)
        inNode = Node(nodeId=id,net=net)
        nodes.append(inNode)
        id = EI.GetSrcNId()
        if id not in nodeIDs:
            nodeIDs.append(id)
        outNode = Node(nodeId=id,net=net)
        nodes.append(outNode)
        edge = Edge(nodeIn=inNode,nodeOut=outNode)
        edges.append(edge)
 
        # edge.save()
    # for NI in G.Nodes():
    #   for Id in NI.GetOutEdges():
    #       print "edge (%d %d)" % (NI.GetId(), Id)
    Node.objects.bulk_create(nodes)
    Edge.objects.bulk_create(edges)

def test():
    GraphInfo = GetBasicInfo()
    for d,x in GraphInfo.items():
        print "key:"+d+",value:"+str(x)
    DegDistrInfo,CluDistrInfo = GetGraphInfo()
    for item in CluDistrInfo:
        print item[0],item[1]

if __name__ == '__main__':
    from timeit import Timer
    t = Timer("test()", "from __main__ import test") #第一个参数是要测试的函数
    print t.timeit(10) #重复执行1000次，如果不指定默认值为1000000