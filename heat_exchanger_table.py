
class solution_matrix:
    def __init__(self, temperature_levels: list, streams: list):
        self.n = len(temperature_levels)           # Número de filas
        self.m = len(streams) + 1                  # Número de columnas (corrientes + 1 para T)
        self.matrix = [[0.0 for _ in range(self.m)] for _ in range(self.n)]

        # Llenar la primera columna con las tuplas (T_high, T_low)
        for i, level in enumerate(temperature_levels):
            self.matrix[i][0] = (level.T_high, level.T_low)

    def __str__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.matrix])
    
    def get_n(self):
        return self.n

    def get_m(self):
        return self.m



class stream:
    def __init__(self, name: str = "", service: bool = False, heat: bool = False, FCp: float = 0.0, Tin: float = 0.0, Tout: float = 0.0):
        self.name = name
        self.heat = heat
        self.FCp = FCp
        self.Tin = Tin
        self.Tout = Tout

    def __str__(self):
        tipo = "Heat" if self.heat else "Cold"
        return f"Steam {self.name} ({tipo}): FCp={self.FCp}, Tin={self.Tin}, Tout={self.Tout}"

class temperature_level:
    def __init__(self, T_high: float = 0.0, T_low: float = 0.0):
        self.T_high = T_high
        self.T_low = T_low

    def __str__(self):
        return f"{self.T_high} °C a {self.T_low} °C"
    
    def __repr__(self):
        return self.__str__()
    
    def remove_duplicate_levels(levels):
        "Remove duplicate levels based on T_high and T_low."
        seen = set()
        unique = []
        for lvl in levels:
            key = (lvl.T_high, lvl.T_low)
            if key not in seen:
                seen.add(key)
                unique.append(lvl)
        return unique

class HeatExchangerNetwork:
    def __init__(self):
        self.streams = []
        self.temp_levels = []

    def add_stream(self, name, heat, service, FCp, Tin, Tout):
        s = stream(name, service, heat, FCp, Tin, Tout)
        self.streams.append(s)

    def print_streams(self):
        for s in self.streams:
            print(s)

    def generate_temperature_levels(self, dif_level: float):
        
        temps = []
        levels = []

        for s in self.streams:
            temps.extend([s.Tin, s.Tout])

            if s.heat:
                T_high = s.Tin
                T_low = s.Tin - dif_level
                level = temperature_level( T_high=T_high, T_low=T_low)
            else:
                T_high = s.Tin + dif_level
                T_low = s.Tin
                level = temperature_level( T_high=T_high, T_low=T_low)
        
            levels.append(level)

        # print( max(temps), min(temps) )

        level = temperature_level( T_high=(max(temps) + dif_level), T_low=max(temps))
        levels.append(level)
        level = temperature_level( T_high=(min(temps) + dif_level) , T_low=min(temps))
        levels.append(level)

        levels = temperature_level.remove_duplicate_levels(levels)

        
        #it sorts the levels based on T_high in descending order
        levels.sort(key=lambda x: x.T_high, reverse=True)

        
        #Save the levels 
        self.temp_levels = levels


        



        # print(levels)





# -------------------
def sort_streams(matriz, hen):
    for j in range(1, matriz.get_m()):  # every stream (columns)
        stream = hen.streams[j-1]
        Tin, Tout, FCp = stream.Tin, stream.Tout, stream.FCp
        
        for i in range(1, matriz.get_n()):  # every level (rows)

            if stream.heat:                
                nivel = hen.temp_levels[i]  # every level represents an interval
                T_high = nivel.T_high
                T_low = nivel.T_low

                # nextThigh = hen.temp_levels[i + 1].T_high
                if T_high < Tout:
                    T_high = Tout
                    

                if Tin >= T_high:
                    matriz.matrix[i][j] = FCp * (Tin - T_high)
                    # print(f"Tint {Tin} >= T_high, y Thigh {T_high}")

                    Tin = Tin - (Tin - T_high)

                if Tin < Tout:
                    break
            else:
                nivel = hen.temp_levels[i]  #Evry level already represents an interval
                T_high = nivel.T_high
                T_low = nivel.T_low
                
                #I have this not debugged yet, but logically it should be correct
                if Tin > T_low:
                    T_low = Tin

                if Tout >= T_low:
                    matriz.matrix[i][j] = FCp * (Tout - T_low)
                    # print(f"Tout {Tout} >= T_low, y Tlow {T_low}")

                    Tout = Tout - (Tout - T_low)

                if Tout <= Tin:
                    break


    
    return matriz
                



            
    
    



#---------------------

#In the heat exchanger network, the streams are defined in order so the first you define is the first one in the matrix( cols )

hen = HeatExchangerNetwork()
hen.add_stream("H1", True, False, 2.5, 400, 320)
hen.add_stream("H2", True,False, 3.8, 370, 320)
hen.add_stream("C1", False,False, 2, 300, 420)
hen.add_stream("C2", False, False, 2, 300, 370)
hen.add_stream("QL", True,True, 1.5, 380, 400)

# hen.add_stream("H1", True,False, 1, 400, 120)
# hen.add_stream("H2", True,False, 2, 340, 120)
# hen.add_stream("C1", False,False, 1.5, 160, 400)
# hen.add_stream("C2", False,False, 1.3, 100, 250)


#The function below generate the temperature levels based on the streams defined above
hen.generate_temperature_levels(dif_level=10)



# for lvl in hen.temp_levels:
#     print(lvl)


#The function below generates the solution matrix based on the temperature levels and the streams defined above
matriz = solution_matrix(hen.temp_levels, hen.streams)


#This function below sorts the streams in the solution matrix based on the temperature levels and the streams defined above
#It is important to note that the first column of the matrix is reserved for the temperature levels
sort_streams(matriz, hen)

print(matriz)
