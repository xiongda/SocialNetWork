#coding:utf-8
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
import os
# Create your models here.
class Net(models.Model):
    netName = models.CharField(max_length=50)
    netDescription = models.CharField(max_length=200)
    netNodeCounter = models.IntegerField(default=-1)
    netEdgeCounter = models.IntegerField(default=-1)
    netDirectedEdgeCounter = models.IntegerField(default=-1)
    netUndirectedEdgeCounter = models.IntegerField(default=-1)
    netSelfEdgeCounter = models.IntegerField(default=-1)
    netBiDirEdgeCounter =models.IntegerField(default=-1)
    netClosedTriangleCounter = models.IntegerField(default=-1)
    netOpenTriangleCounter = models.IntegerField(default=-1)
    netClusterCoefficient = models.FloatField(default=-1)
    netAverageDegree = models.FloatField(default=-1)
    netAveragePathLength = models.FloatField(default=-1)
    netFracOfClosedTriads = models.FloatField(default=-1)
    netConnectedComponentSize = models.FloatField(default=-1)
    netStrongConnCompSize = models.FloatField(default=-1)
    netApproxFullDiameter = models.FloatField(default=-1)
    net90EffectiveDiameter = models.FloatField(default=-1)
    netDegreeDistribution = models.ImageField(default=os.path.join(settings.BASE_DIR,'image','default.jpg'))
    netClusterCoefficientDistribution = models.ImageField(default=os.path.join(settings.BASE_DIR,'image','default.jpg'))
   
    @classmethod
    def create(cls, name):
        net = cls(netName=name)
        return net
    def __str__(self):
        return self.netName



class Node(models.Model):
    nodeName = models.CharField(max_length=50)
    nodeId = models.IntegerField(primary_key=True)
    net = models.ForeignKey(Net)
    node = models.ManyToManyField('self', related_name='neighbor',through='Edge',symmetrical=False)
    @classmethod
    def create(cls, nodeId, net):
        node = cls(nodeId=nodeId,net=net)
        return node
    def __str__(self):
        return str(self.nodeId)

    
class Edge(models.Model):
    nodeOut = models.ForeignKey(Node,related_name='outEdge')
    nodeIn = models.ForeignKey(Node,related_name='inEdge')
    weight = models.FloatField(default=1)
    directed = models.BooleanField(default=False)
    @classmethod
    def create(cls, nodeIn,nodeOut):
        edge = cls(nodeIn = nodeIn,nodeOut=nodeOut)
        return edge
    def __str__(self):
        if self.directed:
            return str(self.nodeOut) + str('->')+ str(self.nodeIn)
        else:
            return str(self.nodeOut) + str('--') + str(self.nodeIn)

def creatNet(snapNet):
    net = Net()
    
    # creat Net data base!

    return net
