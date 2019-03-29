import pywavefront
from pywavefront import visualization
import numpy as np
import matplotlib.pyplot as plt

def genRandBaryCentricCoordinates(numOfPoints):
    randBarycentricCoords = np.random.randn(numOfPoints,3)
    randBarycentricCoords = np.abs(randBarycentricCoords)
    normalizer = np.sum(randBarycentricCoords,1)
    rBaryCoord = []
    for i in range(len(normalizer)):
        rBaryCoord.append(randBarycentricCoords[i] / normalizer[i])
    return np.asarray(rBaryCoord)

def genFaceVertexMap(verts , face):
    mappedVerts = []
    for vertIdx in face:
        mappedVerts.append(verts[vertIdx])
    return np.array(mappedVerts)
def genAffineTransform(vertex , weights):
    #Assume verts is form of [[x1 y1]
    #                         [x2 y2]
    #                         [x3 y3]] 
    
    
    #And weights are          [c11 c12 c13]
    #                         [c21 c22 c23]
    #                         [c21 c32 c33] 
    #                              ..     
    #                         [cN1 cN2 cN3]]
    v = vertex.transpose()
    w = weights.transpose()
    transPoints = np.matmul( v,w)
    return np.array(transPoints)

def loadObjFile(filename):
    scene = pywavefront.Wavefront(filename ,collect_faces=True)
    vertices = []
    faces = scene.parser.mesh.faces
    for vertex in scene.parser.wavefront.vertices:
        vertices.append(vertex)
    vertices = np.asarray(vertices)
    print(vertices)
    xs = vertices[:,0]
    ys = vertices[:,2]
    verts = np.array(list(zip(xs,ys)))
    return faces , verts

faces , verts = loadObjFile('./disk.obj')
#print(verts)
#Generate random face indexes
faceIdx = np.random.randint(len(faces),size=100)

mVert = []
for idx in faceIdx:
    mVert.append(genFaceVertexMap(verts,faces[idx]))
    #print("Faces: ", faces[idx])

#print("Vertex: " , mVert) 
# for face in faces :
#     print("Face: " , face)    

plt.triplot(verts[:,0],verts[:,1],faces)
rBaryCoord = genRandBaryCentricCoordinates(300)
points = []
for mv in mVert:
  points.append(genAffineTransform(mv ,rBaryCoord))
for point in points:
    plt.scatter(point[0],point[1])
plt.show()    
