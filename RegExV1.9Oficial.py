class BMHMatching:
    def __init__(self):
        self.query = ""
        self.text = ""
        self.APHABET_SIZE = 130
        self.tabla = []
        self.textm = ""
        self.banderag = False
        self.banderai = False

    def set_text(self, text):
        self.text = text

    def __Char_to_index(self, char):
        return ord(char)
    
    def __calculate_bad_match_table(self, pattern):
        M = len(pattern)
        self.tabla = [M]*self.APHABET_SIZE
        for i in range(M - 1):
            s = self.__Char_to_index(pattern[i])
            self.tabla[s - 1] = M - i - 1
        return self.tabla
    
    def search(self, patterns):
        if isinstance(patterns, str):
            patterns = [patterns]
        
        N = len(self.text)
        matches = []

        for patron in patterns:
            M = len(patron)
            bad_match_table = self.__calculate_bad_match_table(patron)

            text_index = M - 1

            while text_index < N:
                shared_substr = 0
                while shared_substr < M:
                    if self.text[text_index - shared_substr] == patron[M - shared_substr - 1]:
                        shared_substr += 1
                    else:
                        break

                if shared_substr == M:
                    matches.append(text_index - M + 1)

                text_index += bad_match_table[self.__Char_to_index(self.text[text_index]) - 1]

        # Ordenar los matches por posición en el texto
        ####TRATAR DE ORDENAR CON HEAP

        return matches
    
    def m_search(self, patron):
        N = len(self.textm)
        M = len(patron)
        matches = []
        bad_match_table = self.__calculate_bad_match_table(patron)

        text_index = M - 1

        while text_index < N:
            shared_substr = 0
            while shared_substr < M:
                if self.textm[text_index - shared_substr] == patron[M - shared_substr - 1]:
                    shared_substr += 1
                else:
                    break

            if shared_substr == M:
                matches.append(text_index - M + 1)

            text_index += bad_match_table[self.__Char_to_index(self.textm[text_index]) - 1]

        return matches
        


    def unique_search(self, patron):
        N = len(self.text)
        M = len(patron)
        matches = []
        bad_match_table = self.__calculate_bad_match_table(patron)

        text_index = M - 1

        while text_index < N:
            shared_substr = 0
            while shared_substr < M:
                if self.text[text_index - shared_substr] == patron[M - shared_substr - 1]:
                    shared_substr += 1
                else:
                    break

            if shared_substr == M:
                matches.append(text_index - M + 1)
                return matches

            text_index += bad_match_table[self.__Char_to_index(self.text[text_index]) - 1]

        return matches
    
    def m_unique_search(self, patron):
        N = len(self.textm)
        M = len(patron)
        matches = []
        bad_match_table = self.__calculate_bad_match_table(patron)

        text_index = M - 1

        while text_index < N:
            shared_substr = 0
            while shared_substr < M:
                if self.textm[text_index - shared_substr] == patron[M - shared_substr - 1]:
                    shared_substr += 1
                else:
                    break

            if shared_substr == M:
                matches.append(text_index - M + 1)
                return matches

            text_index += bad_match_table[self.__Char_to_index(self.textm[text_index]) - 1]

        return matches
    
    def replace(self, pattern_with_replacement):
        parts = pattern_with_replacement.split('|')
        if len(parts) != 2:
            return "El patrón de reemplazo debe estar en el formato 'buscar|reemplazar'."

        buscar, reemplazar = parts
        print(parts)

        if self.banderag == True:
            matches = self.search(buscar)
            text_copy = self.text  # Copia del texto original

            # Almacenar las posiciones iniciales en orden inverso
            positions = matches[::-1]

            # Realizar los reemplazos en orden inverso
            for match_start in positions:
                match_end = match_start + len(buscar)
                text_copy = text_copy[:match_start] + reemplazar + text_copy[match_end:]

        if self.banderag == False:
            matches = self.unique_search(buscar)
            text_copy = self.text  # Copia del texto original

            # Realizar los reemplazos en el texto copiado
            for match_start in matches:
                match_end = match_start + len(buscar)
                text_copy = text_copy[:match_start] + reemplazar + text_copy[match_end:]

        return matches, text_copy
    

    def replace_with_i_flag(self, pattern_with_replacement, pattern_with_replacement_original):
        parts = pattern_with_replacement.split('|')
        if len(parts) != 2:
            return "El patrón de reemplazo debe estar en el formato 'buscar|reemplazar'."

        buscar, reemplazar = parts
        print(parts)

        parts_original = pattern_with_replacement_original.split('|')
        buscar_original, reemplazar_original = parts_original
        print(parts_original)

        if self.banderag == True:
            matches = self.m_search(buscar)
            text_copy = self.text  # Copia del texto original

            # Almacenar las posiciones iniciales en orden inverso
            positions = matches[::-1]

            # Realizar los reemplazos en orden inverso
            for match_start in positions:
                match_end = match_start + len(buscar_original)
                text_copy = text_copy[:match_start] + reemplazar_original + text_copy[match_end:]

        if self.banderag == False:
            matches = self.m_unique_search(buscar)
            text_copy = self.text  # Copia del texto original

            # Realizar los reemplazos en el texto copiado
            for match_start in matches:
                match_end = match_start + len(buscar_original)
                text_copy = text_copy[:match_start] + reemplazar_original + text_copy[match_end:]

        return matches, text_copy

    #Esta funcion tiene que transformar el query dado, si es que tiene {} o [0-9] o todas las cosas que vienen
    #Por ejemplo, un f a{5}rbol, lo tiene que transformar a aaaaarbol y quitarle la f para que lo lea el bmh
    #En caso de multiples opciones, como [0-9] o [a-z]bc, tiene que crear un array o tabla con las posibilidades
    #que serian abc, bbc, cbc, dbc, ebc.... hasta zbc.
    
    def rango_corchetes(self, pattern):
        incidencias = []

        i = 0
        while i < len(pattern):
            if pattern[i] == '[':
                i += 1
                char_set = set()

            while i < len(pattern) and pattern[i] != ']':
                char_set.add(pattern[i])
                i += 1

            # Expandir el conjunto de letras
            expanded_set = char_set
            for char in char_set:
                if len(char) == 3 and char[1] == '-':
                    start, end = char[0], char[2]
                    expanded_set.update(chr(code) for code in range(ord(start), ord(end) + 1))

                # Agregar la expansión al patrón resultante
                incidencias.extend([''.join(expanded_set)])

            else:
                i += 1

        return incidencias

    def corchetes(self, pattern):
        expanded_p = ""
        i = 0
        while i < len(pattern):
            if pattern[i] == '[':
                i += 1
                char_set = set()

                while i < len(pattern) and pattern[i] != ']':
                    char_set.add(pattern[i])
                    i += 1

                expanded_set = char_set.copy()
                for char in char_set:
                    if len(char) == 3 and char[1] == '-':
                        start, end = char[0], char[2]
                        expanded_set.update(chr(code) for code in range(ord(start), ord(end) + 1))
                expanded_p += ''.join(expanded_set)
            else:
                expanded_p += pattern[i]
                i += 1
        return expanded_p
           

    def pregunta(self, pattern):
        parts = pattern.split('?')
        if len(parts) != 2:
            print("El numero maximo de ? por palabra es 1")
            return None
        parts2 = [parts[0], parts[0]+parts[1]]
        print(parts2)
        return parts2

    '''
    def or_logico(self, pattern):
        parts = pattern.split(' | ')
        if len(parts) != 2:
            print("El or logico debe estar en el formato 'parte1|parte2'.")
            return None
        print(parts)
        return parts
    
    '''
    def search_with_or(self, pattern):
        patron1, patron2 = pattern.split('|')
        buscar_p1 = self.search(patron1)        
        buscar_p2 = self.search(patron2)
        if buscar_p1 == -1:
            print(f"No se encontro el patron {patron1}")
        if buscar_p2 == -1:
            print(f"No se encontro el patron {patron2}")
        return buscar_p1 + buscar_p2
    
    def expand_rep(self, pattern):
        partes = pattern.split('{')
        letter = partes[0][-1]
        repetition = int(partes[1][0]) #Convierte en entero el numero entre corchete
        return (letter * repetition)
    
    
    def search_with_rep(self, pattern):
        partes = pattern.split('{')
        pattern_with_r = self.expand_rep(pattern)
        aux = (len(partes[0]) - 1)
        result = self.search(pattern_with_r) - aux
        return result

    def revision_operadores(self, pattern):
        if ('|') in pattern:
            pattern_array = self.search_with_or(pattern)
            if '[' in pattern_array[0] and ']' in pattern_array[0]:
                pattern0 = pattern_array[0]
                pattern1 = self.corchetes(pattern0)
            if '*' in pattern_array[0]:
                pattern0 = pattern_array[0]
                pattern1 = self.comodin(pattern0)
            if '?' in pattern_array[0]:
                pattern0 = pattern_array[0]
                pattern1 = self.pregunta(pattern0)
            if '{' in pattern_array[0] and '}' in pattern_array[0]:
                pattern0 = pattern_array[0]
                pattern1 = self.llaves(pattern0)
            if '[' not in pattern_array[0] and ']' not in pattern_array[0] and '{' not in pattern_array[0] and '}' not in pattern_array[0] and '*' not in pattern_array[0] and '?' not in pattern_array[0]:
                pattern1 = pattern_array[0]
            if '[' in pattern_array[1] and ']' in pattern_array[1]:
                pattern20 = pattern_array[1]
                pattern2 = self.corchetes(pattern20)
            if '*' in pattern_array[1]:
                pattern20 = pattern_array[1]
                pattern2 = self.comodin(pattern20)
            if '?' in pattern_array[1]:
                pattern20 = pattern_array[1]
                pattern2 = self.pregunta(pattern20)
            if '{' in pattern_array[1] and '}' in pattern_array[1]:
                pattern20 = pattern_array[1]
                pattern2 = self.llaves(pattern20)
            if '[' not in pattern_array[1] and ']' not in pattern_array[1] and '{' not in pattern_array[1] and '}' not in pattern_array[1] and '*' not in pattern_array[1] and '?' not in pattern_array[1]:
                pattern2 = pattern_array[1]
            return pattern1 + pattern2  
        else:
            if '[' and ']' in pattern:
                pattern1 = self.corchetes(pattern)
            if '*' in pattern:
                pattern1 = self.comodin(pattern)
            if '?' in pattern:
                pattern1 = self.pregunta(pattern)
            if '{' and '}' in pattern:
                pattern1 = self.llaves(pattern)
            if '[' not in pattern and ']' not in pattern and '{' not in pattern and '}' not in pattern and '*' not in pattern and '?' not in pattern:
                pattern1 = pattern
            return pattern1
            

            

    def revision_operadores_with_fr(self, pattern):
        if '[' and ']' in pattern:
            pattern1 = self.corchetes(pattern)
        if '*' in pattern:
            pattern1 = self.comodin(pattern)
        if '?' in pattern:
            pattern1 = self.pregunta(pattern)
        if '{' and '}' in pattern:
            pattern1 = self.llaves(pattern)
        return pattern1



    def revision_banderas(self, query):
        subcadenas = query.split()
        print(subcadenas)

        if subcadenas[-1] == "g" or subcadenas[-2] == "g":
            self.banderag = True

        if subcadenas[-1] == "i" or subcadenas[-2] == "i":
            self.banderai = True

        #Si no se especifica ni buscar ni buscar y reemplazar
        if subcadenas[0] != "f" and subcadenas[0] != "fr":
            print("Debes poner una f para buscar o una fr para buscar y reemplazar al principio")
            return None
        
        #Si se elige buscar y no hay ninguna bandera
        if subcadenas[0] == "f" and self.banderag == False and self.banderai == False:
            pattern1 = query
            pattern2 = pattern1[2:]
            print (pattern2)
            pattern3 = self.revision_operadores(pattern2)
            return self.unique_search(pattern3)
            
        #Return buscar con for
        #Primero revisa operadores
        #Esto regresara el patron que se debe buscar
        #Poner un if para saber si el patron es una tabla
        #En ese caso, ejecutar el buscar con for
        #ZEUS ESTE ESTA INCOMPLETO UN SALUDO

        #Si se elige buscar y se coloca la bandera g
        if subcadenas[0] == "f" and self.banderag == True and self.banderai == False:
            pattern = query
            pattern1 = pattern[2:]
            pattern2 = pattern1[:(len(pattern1) - 2)]
            print (pattern2)
            pattern3 = self.revision_operadores(pattern2)
            print (pattern3)
            return self.search(pattern3)  

        #Si se elige buscar y se coloca la bandera i
        if subcadenas[0] == "f" and self.banderai == True and self.banderag == False:
            pattern = query
            pattern1 = pattern.casefold()
            pattern2 = pattern1[2:]
            pattern3 = pattern2[:(len(pattern2) - 2)]
            self.textm = self.text.casefold()
            print (pattern3)
            return self.m_unique_search(pattern3)
        
        #Si se elige buscar y se colocan las 2 banderas
        if subcadenas[0] == "f" and self.banderag == True and self.banderai == True:
            pattern = query
            pattern1 = pattern.casefold()
            pattern2 = pattern1[2:]
            pattern3 = pattern2[:(len(pattern2) - 4)]
            self.textm = self.text.casefold()
            print (pattern3)
            return self.m_search(pattern3)
        
        #Si se elige buscar y reemplazar y no se colocan banderas
        if subcadenas[0] == "fr" and self.banderag == False and self.banderai == False:
            pattern1 = query
            pattern2 = pattern1[3:]
            print (pattern2)
            return self.replace(pattern2)

        #Si se elige buscar y reemplazar y se coloca la bandera g
        if subcadenas[0] == "fr" and self.banderag == True and self.banderai == False:
            pattern = query
            pattern1 = pattern[3:]
            pattern2 = pattern1[:(len(pattern1) - 2)]
            print (pattern2)
            return self.replace(pattern2)  

        #Si se elige buscar y reemplazar y se coloca la bandera i
        if subcadenas[0] == "fr" and self.banderai == True and self.banderag == False:
            pattern = query
            pattern1 = pattern[3:]
            pattern2 = pattern1[:(len(pattern1) - 2)]
            pattern3 = pattern2.casefold()
            self.textm = self.text.casefold()
            print(pattern2, pattern3)
            return self.replace_with_i_flag(pattern3, pattern2)

            """
            pattern = query
            pattern1 = pattern.casefold()
            pattern2 = pattern1[2:]
            pattern3 = pattern2[:(len(pattern2) - 2)]
            self.textm = self.text.casefold()
            print (pattern3)
            return self.m_unique_search(pattern3)
            """

        #Si se elige buscar y reemplazar y se colocan las 2 banderas
        if subcadenas[0] == "fr" and self.banderai == True and self.banderag == True:
            pattern = query
            pattern1 = pattern[3:]
            pattern2 = pattern1[:(len(pattern1) - 4)]
            pattern3 = pattern2.casefold()
            self.textm = self.text.casefold()
            print(pattern2, pattern3)
            return self.replace_with_i_flag(pattern3, pattern2)
        


        
    # Función de validación de query, revisar despues
    def es_query_valido(self, query):
        """""
        operadores = ['*', '?', '|', '{']
        num_operadores = sum(1 for operador in operadores if operador in query)
        if num_operadores > 1:
            return False

        if query.count('[') != query.count(']'):
            return False
        caracteres_alfanumericos = ''.join(filter(lambda c: c.isalnum() or c.isspace(), query))
        if caracteres_alfanumericos != query:
            return False
        """    

        return True

    # Función para obtener un query válido del usuario
    def obtener_query_valido(self):
        while True:
            query = input("Introduce un query: ")
            if self.es_query_valido(query):
                self.query = query
                return query
            else:
                print("El query no es válido. Asegúrate de cumplir las reglas establecidas.")
    


text = input("Introduce un texto: ")
#Esto es un texto prueba, por lo tanto debe ser un poco largo el texto

string = BMHMatching()
string.set_text(text)
# Obtener un query válido del usuario
query_valido = string.obtener_query_valido()
print(f"Query válido: {query_valido}")
if string.revision_banderas(string.query):
    print(f"Se encontró el patrón en las posiciones: {string.revision_banderas(string.query)}")
else:
    print("No se encontró el patrón en el texto.")
print(string.query)
'''
text = "abc|xyz"
obj = BMHMatching()
obj.set_text(text)
patron = "bc|oo"
resultados1  = obj.search_with_or(patron)
resultados2 = obj.search_with_or(patron)
if resultados1 or resultados2:
    print(f"El patron {patron} se encontro en las posiciones {resultados1 + resultados2}")
else:
    print(f"No se encontró el patron {patron}")

'''
    
bmh = BMHMatching()
pattern = "arbo[les]"
pattern = bmh.corchetes(pattern)
print(pattern)
matches = bmh.search(pattern)
print(matches)