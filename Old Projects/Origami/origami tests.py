    def move(self, newCoords, stationary=None):
        #vertex.move
        if stationary:
            stationary=list(stationary)
        else:
            stationary=[]
        stationary+=list(fixedPoints)
        movers=[]
        self.findMovers(movers, stationary)
        self.sp.pos=self.coords=vector(newCoords)
        while movers:
            moversTemp=list(movers)
            for m in moversTemp:
                temp=[]
                for a in m.attached:
                    if a not in movers:
                        temp+=[a]
                for k in m.knex:
                    if k not in movers:
                        temp+=[k]
                if len(temp)<3:
                    continue
                points=[]
                radii=[]
                for i in range(3):
                    points+=[list(temp[i].coords)]
                    radii+=distP2P(m,temp[i])
                position=trilaterate(points, radii)
                if result==None:
                    continue
                m.sp.pos=m.coords=vector(position)
                movers.remove(m)

    def findMovers(self, movers, stationary):
        #for vertex.move
        for k in self.knex:
            if k not in movers and k not in stationary:
                movers+=[k]
                k.findMovers(movers, stationary)
