#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
import tkinter
from tkinter import messagebox
import math

class Nodo(object):
    def __init__(self, dato, prioridad, valAcumulado):
        self._dato = dato
        self._prioridad = prioridad
        self._valAcumulado = valAcumulado
        self._sig = None

class ColaPrioridad(object):
    def __init__(self):
        self.head = None

    def enqueue(self, dato, prioridad, valAcumulado):
        nuevoNodo = Nodo(dato, prioridad, valAcumulado)

        anterior = None
        aux_nodo = self.head

        if self.head is None:
            self.head = nuevoNodo
        else :
            if aux_nodo._prioridad > prioridad:
                nuevoNodo._sig  = self.head
                self.head = nuevoNodo
            else:
                while aux_nodo._sig != None and aux_nodo._sig._prioridad < prioridad:
                        aux_nodo = aux_nodo._sig

                nuevoNodo._sig = aux_nodo._sig
                aux_nodo._next = nuevoNodo

    #Retorna el primer elemento, el cual tiene el menor costo
    def dequeue(self):
        if self.isEmpty():
            raise TypeError('Priority queue empty')

        dato = self.head._dato
        self.head = self.head._sig
        return dato

    #Retorna el valor del costo acumulado
    def getValAcumu(self):
        return self.head._valAcumulado

    #Verifica si existen elementos dentro de la cola
    def isEmpty(self):
        return self.head is None

class LinkedEdge(object):

    def __init__(self, fromVertex, toVertex, weight = None):
        self._vertex1 = fromVertex
        self._vertex2 = toVertex
        self._weight = weight
        self._mark = False

    def clearMark(self):
        self._mark = False

    def __eq__(self, other):
        if self is other: return True
        if type(self) != type(other):
            return False
        return self._vertex1 == other._vertex1 and \
               self._vertex2 == other._vertex2

    def getOtherVertex(self,  thisVertex):
        if thisVertex == None or thisVertex == self._vertex2:
            return self._vertex1
        else:
            return self._vertex2

    def getToVertex(self):
        return self._vertex2

    def getWeight(self):
        return self._weight

    def isMarked(self):
        return self._mark

    def setMark(self):
        self._mark = True

    def setWeight(self, weight):
        self._weight = weight

    def __str__(self):
        return str(self._vertex1) + ">" + \
               str(self._vertex2)   + ":" + \
               str(self._weight)

class LinkedVertex(object):

    def __init__(self, label,x,y):
        self._label = label
        self._edgeList = []
        self._mark = False
        self._coordenadaX= x
        self._coordenadaY=y

    def clearMark(self):
        self._mark = False;

    def getCoordenada(self):
        return (self._coordenadaX,self._coordenadaY)

    def getLabel(self):
        return self._label

    def isMarked(self):
        return self._mark

    def setLabel(self, label, g):
        g._vertices.pop(self._label, None)
        g._vertices[label] = self
        self._label = label

    def setMark(self):
        self._ = True

    def __str__(self):
        return str(self._label)

    # Methods used by LinkedGraph
    def addEdgeTo(self, toVertex, weight):
        edge = LinkedEdge(self, toVertex, weight)
        self._edgeList.append(edge)

    def getEdgeTo(self, toVertex):
        edge = LinkedEdge(self, toVertex)
        try:
            return self._edgeList[self._edgeList.index(edge)]
        except:
            return None

    def incidentEdges(self):
        return iter(self._edgeList)

    def neighboringVertices(self):
        vertices = []
        for edge in self._edgeList:
            vertices.append(edge.getOtherVertex(self))
        return iter(vertices)

    def removeEdgeTo(self, toVertex):
        edge = LinkedEdge(self, toVertex)
        if edge in self._edgeList:
            self._edgeList.remove(edge)
            return True
        else:
            return False

class LinkedDirectedGraph(object):

    def __init__(self, collection = None):
        self._vertexCount = 0
        self._edgeCount = 0
        self._vertices = {}
        if collection != None:
            for label in collection:
                self.addVertex(label,coordenadaX,coordenadaY)

    # Methods for clearing, marks, sizes, string rep
    def clear(self):
        self._vertexCount = 0
        self._edgeCount = 0
        self._vertices = {}

    def clearEdgeMarks(self):
        for edge in self.edges():
            edge.clearMark()

    def clearVertexMarks(self):
        for vertex in self.vertices():
            vertex.clearMark()

    def isEmpty(self):
        return self._vertexCount == 0

    def sizeEdges(self):
        return self._edgeCount

    def sizeVertices(self):
        return self._vertexCount

    def __str__(self):
        result = str(self.sizeVertices()) + " Vertices: "
        for vertex in self._vertices:
            result += " " + str(vertex)
        result += " and "
        result += str(self.sizeEdges()) + " Edges: "
        for edge in self.edges():
            result += " " + str(edge)
        return result

    # Vertex related methods
    def addVertex(self, label,coorX,coorY):
        self._vertices[label] = LinkedVertex(label,coorX,coorY)
        self._vertexCount += 1

    def containsVertex (self, label):
        return label in self._vertices

    def getVertex(self, label):
        return self._vertices[label]

    def removeVertex(self,  label):
        removedVertex = self._vertices.pop(label, None)
        if removedVertex is None:
            return False

        # Examine all vertices
        edgesBelongVertex = len(removedVertex._edgeList)
        self._edgeCount -= edgesBelongVertex
        for vertex in self.vertices():
            if vertex.removeEdgeTo(removedVertex):
                self._edgeCount -= 1
        self._vertexCount -= 1
        return True

    # Methods related to edges

    def addEdge(self, fromLabel, toLabel, weight):
        fromVertex = self.getVertex(fromLabel)
        toVertex   = self.getVertex(toLabel)
        fromVertex.addEdgeTo(toVertex, weight)
        self._edgeCount += 1

    def containsEdge(self, fromLabel, toLabel):
        return self.getEdge(fromLabel, toLabel) != None

    def getEdge(self, fromLabel, toLabel):
        fromVertex = self._vertices[fromLabel]
        toVertex   = self._vertices[toLabel]
        return fromVertex.getEdgeTo(toVertex)

    def removeEdge (self, fromLabel, toLabel):
        fromVertex = self.getVertex(fromLabel)
        toVertex   = self.getVertex(toLabel)
        edgeRemovedFlg = fromVertex.removeEdgeTo(toVertex)
        if edgeRemovedFlg:
            self._edgeCount -= 1
        return edgeRemovedFlg

    # Iterators

    def edges(self):
        result = []
        for vertex in self.vertices():
            for edges in vertex.incidentEdges():
                result.append(edges)
        return iter(result)

    def vertices(self):
        return iter(self._vertices.values())

    def incidentEdges(self, label):
        return self._vertices[label].incidentEdges()

    def neighboringVertices(self, label):
        return self._vertices[label].neighboringVertices()

    def valorHeuristico(self,start,end):
        startVert =self.getVertex(start)
        endVert =self.getVertex(end)
        #Se utilizara la ecuacion euclidiana
        valEuclidiano = (math.sqrt((startVert._coordenadaX-endVert._coordenadaX)**2+(startVert._coordenadaY-endVert._coordenadaY)**2))*1000000000
        return valEuclidiano

    def astar(self,nodoInicio, nodoDestino):
        queue = ColaPrioridad() #Una cola de prioridad para obtener los mejores datos
        startVertex = self.getVertex(nodoInicio)
        valHeu = self.valorHeuristico(nodoInicio,nodoDestino)
        queue.enqueue(nodoInicio,valHeu, 0) #Se encola el valor desde el que se empezará
        cad_res=""
        #i=1
        while not queue.isEmpty(): #mientras la cola no esté vacia
            valorAcum = queue.getValAcumu()
            vert_actual = queue.dequeue() #Se desencola el valor más pequeño, ya que queremos el valor más pequeño
            #print(i,")",vert_actual)
            #i=i+1
            cad_res= cad_res + "->"+ vert_actual
            if str(vert_actual) == str(nodoDestino):
                break
            for vertSig in self.neighboringVertices(vert_actual): #saca una lista de nodos vecinos para evaluar el camino y encolarlos según su dato
                arista = self.getEdge(vert_actual, vertSig._label)
                peso = arista.getWeight() + valorAcum
                valHeu = self.valorHeuristico(vertSig._label,nodoDestino)
                queue.enqueue(vertSig._label, valHeu + peso, peso) #se encola el nodo vecino junto con su prioridad
        return cad_res

def implementacion():
    dato1=Ociudad.get()
    dato2=Dciudad.get()
    dato1=dato1.upper()
    dato2=dato2.upper()
    lista_ciudades=["LORETO","TUMBES","PIURA","LAMBAYEQUE","CAJAMARCA","AMAZONAS","SAN MARTIN","LIBERTAD","ANCASH","HUANUCO","PASCO","JUNIN","LIMA","HUANCAVELICA","UCAYALI","CALLAO","ICA","AREQUIPA","MOQUEGUA","TACNA","PUNO","CUZCO","MADRE DE DIOS","AYACUCHO","APURIMAC"]
    if dato1 in lista_ciudades and dato2 in lista_ciudades:
        cad = grafo.astar(dato1,dato2)
        #etiqueta4 = tkinter.Label(raiz, text = cad).place(x = 520, y = 600)
        msg = msg = messagebox.showinfo("Ruta",cad)
    elif dato1=="" or dato2=="":
        msg = msg = messagebox.showinfo("Atención","Llene completamente los datos de las ciudades de origen y destino")
    elif dato1 not in lista_ciudades or dato2 not in lista_ciudades:
        msg = msg = messagebox.showinfo("Atención","Una o dos de las ciudades ha insertado no existe dentro del mapa del Perú")

grafo = LinkedDirectedGraph()
v1=LinkedVertex("LORETO",40,80)
v2=LinkedVertex("TUMBES",5,80)
v3=LinkedVertex("PIURA",3,75)
v4=LinkedVertex("LAMBAYEQUE",10,70)
v5=LinkedVertex("CAJAMARCA",20,68)
v6=LinkedVertex("AMAZONAS",20,78)
v7=LinkedVertex("SAN MARTIN",25,69)
v8=LinkedVertex("LIBERTAD",23,65)
v9=LinkedVertex("ANCASH",15,50)
v10=LinkedVertex("HUANUCO",30,49)
v11=LinkedVertex("PASCO",35,45)
v12=LinkedVertex("JUNIN",33,40)
v13=LinkedVertex("LIMA",30.5,38)
v14=LinkedVertex("HUANCAVELICA",33,35)
v15=LinkedVertex("UCAYALI",60,48)
v16=LinkedVertex("CALLAO",30,38)
v17=LinkedVertex("ICA",32,30)
v18=LinkedVertex("AREQUIPA",50,23)
v19=LinkedVertex("MOQUEGUA",85,15)
v20=LinkedVertex("TACNA",83,8)
v21=LinkedVertex("PUNO",90,28)
v22=LinkedVertex("CUZCO",70,35)
v23=LinkedVertex("MADRE DE DIOS",80,40)
v24=LinkedVertex("AYACUCHO",45,28)
v25=LinkedVertex("APURIMAC",60,33)

grafo.addVertex(v1._label,v1._coordenadaX,v1._coordenadaY)
grafo.addVertex(v2._label,v2._coordenadaX,v2._coordenadaY)
grafo.addVertex(v3._label,v3._coordenadaX,v3._coordenadaY)
grafo.addVertex(v4._label,v4._coordenadaX,v4._coordenadaY)
grafo.addVertex(v5._label,v5._coordenadaX,v5._coordenadaY)
grafo.addVertex(v6._label,v6._coordenadaX,v6._coordenadaY)
grafo.addVertex(v7._label,v7._coordenadaX,v7._coordenadaY)
grafo.addVertex(v8._label,v8._coordenadaX,v8._coordenadaY)
grafo.addVertex(v9._label,v9._coordenadaX,v9._coordenadaY)
grafo.addVertex(v10._label,v10._coordenadaX,v10._coordenadaY)
grafo.addVertex(v11._label,v11._coordenadaX,v11._coordenadaY)
grafo.addVertex(v12._label,v12._coordenadaX,v12._coordenadaY)
grafo.addVertex(v13._label,v13._coordenadaX,v13._coordenadaY)
grafo.addVertex(v14._label,v14._coordenadaX,v14._coordenadaY)
grafo.addVertex(v15._label,v15._coordenadaX,v15._coordenadaY)
grafo.addVertex(v16._label,v16._coordenadaX,v16._coordenadaY)
grafo.addVertex(v17._label,v17._coordenadaX,v17._coordenadaY)
grafo.addVertex(v18._label,v18._coordenadaX,v18._coordenadaY)
grafo.addVertex(v19._label,v19._coordenadaX,v19._coordenadaY)
grafo.addVertex(v20._label,v20._coordenadaX,v20._coordenadaY)
grafo.addVertex(v21._label,v21._coordenadaX,v21._coordenadaY)
grafo.addVertex(v22._label,v22._coordenadaX,v22._coordenadaY)
grafo.addVertex(v23._label,v23._coordenadaX,v23._coordenadaY)
grafo.addVertex(v24._label,v24._coordenadaX,v24._coordenadaY)
grafo.addVertex(v25._label,v25._coordenadaX,v25._coordenadaY)


e1 = LinkedEdge(v1._label, v7._label, 18.601075)
e2 = LinkedEdge(v1._label, v6._label, 20.09975)
e3 = LinkedEdge(v1._label, v15._label, 37.735925)

e4 = LinkedEdge(v7._label, v1._label, 18.601075)
e5 = LinkedEdge(v6._label, v1._label, 20.09975)
e6 = LinkedEdge(v15._label, v1._label, 37.735925)

e7 = LinkedEdge(v3._label, v4._label, 8.602325267)
e8 = LinkedEdge(v3._label, v5._label, 18.38477631)

e9 = LinkedEdge(v4._label, v3._label, 8.602325267)
e10 = LinkedEdge(v5._label, v3._label, 18.38477631)

e11 = LinkedEdge(v2._label, v3._label, 5.385164807)
e12 = LinkedEdge(v3._label, v2._label, 5.385164807)

e13 = LinkedEdge(v15._label, v10._label, 30.01666204)
e14 = LinkedEdge(v15._label, v11._label, 25.17935662)
e15 = LinkedEdge(v15._label, v12._label, 28.16025568)
e16 = LinkedEdge(v15._label, v22._label, 16.40121947)
e17 = LinkedEdge(v15._label, v23._label,21.54065923)

e18 = LinkedEdge(v10._label, v15._label,  30.01666204)
e19 = LinkedEdge(v11._label, v15._label, 25.17935662)
e20 = LinkedEdge(v12._label, v15._label, 28.16025568)
e21 = LinkedEdge(v22._label, v15._label,16.40121947)
e22 = LinkedEdge(v23._label, v15._label, 21.54065923)

e23 = LinkedEdge(v12._label, v11._label, 5.385164807)
e24= LinkedEdge(v12._label, v13._label,3.201562119)
e25 = LinkedEdge(v12._label, v14._label, 5)

e26 = LinkedEdge(v11._label, v12._label, 5.385164807)
e27 = LinkedEdge(v13._label, v12._label,3.201562119)
e28 = LinkedEdge(v14._label, v12._label, 5)

e29 = LinkedEdge(v18._label, v19._label, 35.90264614)
e30 = LinkedEdge(v18._label, v21._label, 40.31128874)
e31 = LinkedEdge(v18._label, v17._label, 19.31320792)
e32 = LinkedEdge(v18._label, v24._label, 7.071067812)
e33 = LinkedEdge(v18._label, v25._label, 14.14213562)
e34 = LinkedEdge(v18._label, v22._label, 23.32380758)

e35 = LinkedEdge(v19._label, v18._label, 35.90264614)
e36 = LinkedEdge(v21._label, v18._label, 40.31128874)
e37 = LinkedEdge(v17._label, v18._label, 19.31320792)
e38 = LinkedEdge(v24._label, v18._label, 7.071067812)
e39 = LinkedEdge(v25._label, v18._label, 14.14213562)
e40 = LinkedEdge(v22._label, v18._label, 23.32380758)

e41 = LinkedEdge(v9._label, v8._label, 17)
e42 = LinkedEdge(v9._label, v10._label, 15.03329638)
e43 = LinkedEdge(v9._label, v13._label, 23.75394704)

e44 = LinkedEdge(v8._label, v9._label, 17)
e45 = LinkedEdge(v10._label, v9._label, 15.03329638)
e46 = LinkedEdge(v13._label, v9._label, 23.75394704)

e47 = LinkedEdge(v20._label, v19._label, 7.280109889)
e48 = LinkedEdge(v20._label, v21._label, 21.1896201)

e49 = LinkedEdge(v19._label, v20._label, 7.280109889)
e50 = LinkedEdge(v21._label, v20._label, 21.1896201)

e51 = LinkedEdge(v23._label, v22._label, 11.18033989)
e52 = LinkedEdge(v23._label, v21._label, 15.62049935)

e53 = LinkedEdge(v22._label, v23._label, 11.18033989)
e54 = LinkedEdge(v21._label, v23._label, 15.62049935)

e55 = LinkedEdge(v25._label, v24._label, 15.8113883)
e56 = LinkedEdge(v25._label, v22._label, 10.19803903)

e57 = LinkedEdge(v24._label, v25._label, 15.8113883)
e58 = LinkedEdge(v22._label, v25._label, 10.19803903)

e59 = LinkedEdge(v7._label, v8._label, 4.472135955)
e60 = LinkedEdge(v7._label, v10._label, 20.61552813)

e61 = LinkedEdge(v8._label, v7._label, 4.472135955)
e62 = LinkedEdge(v10._label, v7._label, 20.61552813)

e63 = LinkedEdge(v13._label, v17._label, 8.139410298)
e64 = LinkedEdge(v13._label, v14._label, 3.905124838)

e65 = LinkedEdge(v17._label, v13._label, 8.139410298)
e66 = LinkedEdge(v14._label, v13._label, 3.905124838)

e67 = LinkedEdge(v13._label, v16._label, 0.5)
e68 = LinkedEdge(v16._label, v13._label, 0.5)

e69 = LinkedEdge(v6._label, v5._label, 10)
e70 = LinkedEdge(v6._label, v7._label, 10.29563014)

e71 = LinkedEdge(v5._label, v6._label, 10)
e72 = LinkedEdge(v7._label, v6._label, 10.29563014)

e73 = LinkedEdge(v8._label, v4._label, 13.92838828)
e74 = LinkedEdge(v8._label, v5._label, 4.242640687)

e75 = LinkedEdge(v4._label, v8._label, 13.92838828)
e76 = LinkedEdge(v5._label, v8._label, 4.242640687)

e77 = LinkedEdge(v24._label, v17._label, 13.15294644)
e78 = LinkedEdge(v24._label, v14._label, 13.89244399)

e79 = LinkedEdge(v17._label, v24._label, 13.15294644)
e80 = LinkedEdge(v14._label, v24._label, 13.89244399)

e81 = LinkedEdge(v10._label, v11._label, 6.403124237)
e82 = LinkedEdge(v11._label, v10._label, 6.403124237)

grafo.addEdge(v1._label, v7._label, e1._weight)
grafo.addEdge(v1._label, v6._label, e2._weight)
grafo.addEdge(v1._label, v15._label, e3._weight)

grafo.addEdge(v7._label, v1._label, e4._weight)
grafo.addEdge(v6._label, v1._label, e5._weight)
grafo.addEdge(v15._label, v1._label, e6._weight)

grafo.addEdge(v3._label, v4._label, e7._weight)
grafo.addEdge(v3._label, v5._label, e8._weight)
grafo.addEdge(v4._label, v3._label, e9._weight)
grafo.addEdge(v5._label, v3._label, e10._weight)
grafo.addEdge(v2._label, v3._label, e11._weight)
grafo.addEdge(v3._label, v2._label, e12._weight)

grafo.addEdge(v15._label, v10._label, e13._weight)
grafo.addEdge(v15._label, v11._label, e14._weight)
grafo.addEdge(v15._label, v12._label, e15._weight)
grafo.addEdge(v15._label, v22._label, e16._weight)
grafo.addEdge(v15._label, v23._label, e17._weight)

grafo.addEdge(v10._label, v15._label, e18._weight)
grafo.addEdge(v11._label, v15._label, e19._weight)

grafo.addEdge(v12._label, v15._label, e20._weight)
grafo.addEdge(v22._label, v15._label, e21._weight)
grafo.addEdge(v23._label, v15._label, e22._weight)
grafo.addEdge(v12._label, v11._label, e23._weight)
grafo.addEdge(v12._label, v13._label, e24._weight)
grafo.addEdge(v12._label, v14._label, e25._weight)

grafo.addEdge(v11._label, v12._label, e26._weight)
grafo.addEdge(v13._label, v12._label, e27._weight)
grafo.addEdge(v14._label, v12._label, e28._weight)
grafo.addEdge(v18._label, v19._label, e29._weight)
grafo.addEdge(v18._label, v21._label, e30._weight)
grafo.addEdge(v18._label, v17._label, e31._weight)
grafo.addEdge(v18._label, v24._label, e32._weight)
grafo.addEdge(v18._label, v25._label, e33._weight)
grafo.addEdge(v18._label, v22._label, e34._weight)

grafo.addEdge(v19._label, v18._label, e35._weight)
grafo.addEdge(v21._label, v18._label, e36._weight)
grafo.addEdge(v17._label, v18._label, e37._weight)
grafo.addEdge(v24._label, v18._label, e38._weight)
grafo.addEdge(v25._label, v18._label, e39._weight)
grafo.addEdge(v22._label, v18._label, e40._weight)

grafo.addEdge(v9._label, v8._label, e41._weight)
grafo.addEdge(v9._label, v10._label, e42._weight)
grafo.addEdge(v9._label, v13._label, e43._weight)
grafo.addEdge(v8._label, v9._label, e44._weight)
grafo.addEdge(v10._label, v9._label, e45._weight)
grafo.addEdge(v13._label, v9._label, e46._weight)
grafo.addEdge(v20._label, v19._label, e47._weight)
grafo.addEdge(v20._label, v21._label, e48._weight)
grafo.addEdge(v19._label, v20._label, e49._weight)
grafo.addEdge(v21._label, v20._label, e50._weight)

grafo.addEdge(v23._label, v22._label, e51._weight)
grafo.addEdge(v23._label, v21._label, e52._weight)
grafo.addEdge(v22._label, v23._label, e53._weight)
grafo.addEdge(v21._label, v23._label, e54._weight)
grafo.addEdge(v25._label, v24._label, e55._weight)
grafo.addEdge(v25._label, v22._label, e56._weight)

grafo.addEdge(v24._label, v25._label, e57._weight)
grafo.addEdge(v22._label, v25._label, e58._weight)
grafo.addEdge(v7._label, v8._label, e59._weight)
grafo.addEdge(v7._label, v10._label, e60._weight)
grafo.addEdge(v8._label, v7._label, e61._weight)
grafo.addEdge(v10._label, v7._label, e62._weight)
grafo.addEdge(v13._label, v17._label, e63._weight)
grafo.addEdge(v13._label, v14._label, e64._weight)
grafo.addEdge(v17._label, v13._label, e65._weight)
grafo.addEdge(v14._label, v13._label, e66._weight)
grafo.addEdge(v13._label, v16._label, e67._weight)
grafo.addEdge(v16._label, v13._label, e68._weight)
grafo.addEdge(v6._label, v5._label, e69._weight)
grafo.addEdge(v6._label, v7._label, e70._weight)
grafo.addEdge(v5._label, v6._label, e71._weight)
grafo.addEdge(v7._label, v6._label, e72._weight)
grafo.addEdge(v8._label, v4._label, e73._weight)
grafo.addEdge(v8._label, v5._label, e74._weight)
grafo.addEdge(v4._label, v8._label, e75._weight)
grafo.addEdge(v5._label, v8._label, e76._weight)
grafo.addEdge(v24._label, v17._label, e77._weight)
grafo.addEdge(v24._label, v14._label, e78._weight)
grafo.addEdge(v17._label, v24._label, e79._weight)
grafo.addEdge(v14._label, v24._label, e80._weight)
grafo.addEdge(v10._label, v11._label, e81._weight)
grafo.addEdge(v11._label, v10._label, e81._weight)


raiz = tkinter.Tk()
raiz.geometry('1100x500')
raiz.title('Algoritmo A* - RUTAS PERÚ')
raiz.configure(bg='white')

Ociudad= StringVar()
Dciudad= StringVar()

canvas = tkinter.Canvas(width=420, height=520, bg='white')
canvas.pack()
gif1 = PhotoImage(file='mapa8.ppm')
canvas.create_image(10, 10, image=gif1, anchor=NW)

boton = tkinter.Button(raiz,text='Encontrar ruta mas corta:',width=25,command =implementacion,bg="white").place(x=500,y=630)
etiqueta1 = tkinter.Label(raiz, text = "Ciudad origen:",bg="white").place(x = 400, y = 530)
entrada1 = tkinter.Entry(raiz, textvariable = Ociudad, width = 30).place(x = 520, y = 530)

etiqueta2 = tkinter.Label(raiz, text = "Ciudad destino:",bg="white").place(x = 400, y = 560)
entrada2 = tkinter.Entry(raiz, textvariable = Dciudad, width = 30).place(x = 520, y = 560)
raiz.attributes('-zoomed', True)
raiz.mainloop()
