import numpy as np

class Azul_game():

    def __init__(self):

        self.p1_score = 0
        self.p2_score = 0

        self.player_turn = "P1"
        self.initial_player = "P1"
        #refattorizza nome
        self.new_first_player = True

        self.board_p1 = np.zeros((5, 5), dtype=int)
        self.board_p2 = np.zeros((5, 5), dtype=int)

        self.rows_p1 = self.initialize_rows()
        self.rows_p2 = self.initialize_rows()

        self.penalty_row_p1 = [0, 0, 0, 0, 0, 0, 0]
        self.penalty_row_p2 = [0, 0, 0, 0, 0, 0, 0]

        self.create_drawing_pit()

        self.gameover = False
        self.is_done_phase = False

    def initialize_rows(self):

        first_row = np.zeros(1, dtype=int)
        second_row = np.zeros(2, dtype=int)
        third_row = np.zeros(3, dtype=int)
        fourth_row = np.zeros(4, dtype=int)
        fifth_row = np.zeros(5, dtype=int)
        penalty_row = np.zeros(7, dtype=int)

        # return [first_row , second_row , third_row , fourth_row , fifth_row , penalty_row]
        return [[0], [0, 0], [0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0]]

    def create_drawing_pit(self):
        pit_collection = []

        #
        self.new_first_player = True
        self.player_turn = self.initial_player
        self.is_done_phase = False

        for i in range(5):
            pit = [0, 0, 0, 0, 0]

            for j in range(4):
                generated_tile_type = np.random.randint(0, 5)
                pit[generated_tile_type] = pit[generated_tile_type] + 1

            pit_collection.append(pit)

        discard_pit = [0, 0, 0, 0, 0]
        pit_collection.append(discard_pit)

        self.penalty_row_p1 = [0, 0, 0, 0, 0, 0, 0]
        self.penalty_row_p2 = [0, 0, 0, 0, 0, 0, 0]
        self.drawing_pit =  pit_collection

    def play_turn(self, player, pit_choice, tile_type, column_choice):

        #controlla se è una mossa valida
        if(self.valid_move(player, pit_choice, tile_type, column_choice)):
            drawed_tiles = self.take_tile_from_pit(pit_choice, tile_type,player)

            if(pit_choice == 5 and self.new_first_player):
                self.initial_player = player
                self.new_first_player = False
                #aggiunge 1 penalità
                self.insert_tiles_in_penalty_column(1, player)

            # inserisci tile nella colonna specificata del player

            if (column_choice != 5):
                    self.insert_tiles_in_column(tile_type, drawed_tiles, column_choice, player)
            else:
                # se 5 allora inserisci direttamente nella colonna penalità
                self.insert_tiles_in_penalty_column(drawed_tiles, player)

            if self.player_turn == "P1":
                self.player_turn = "P2"
            else:
                self.player_turn = "P1"

            return True

        return False

    def valid_move(self, player, pit_choice, tile_type, column_choice):

        drawed_tile = self.drawing_pit[pit_choice][tile_type]

        if(drawed_tile == 0):
            return False

        if (player == "P1"):
            rows = self.rows_p1
            scoreboard = self.board_p1
        else:
            rows = self.rows_p2
            scoreboard = self.board_p2
        if(column_choice != 5):
            position = ((tile_type + column_choice) % 5)
            if (scoreboard[column_choice][position] == 1):
                return False
            if (rows[column_choice][0] == 0 or rows[column_choice][0] == tile_type + 1):
                return True
            return False

        else: return True

    def take_tile_from_pit(self, pit_choice, tile_type, player):

        drawed_tiles = self.drawing_pit[pit_choice][tile_type]
        self.drawing_pit[pit_choice][tile_type] = 0

        if not self.new_first_player:
            self.new_first_player = False
            self.initial_player = player

        if (pit_choice != 5):
            for i in range(5):
                discarded_tile = self.drawing_pit[pit_choice][i]
                self.drawing_pit[pit_choice][i] = 0
                self.drawing_pit[5][i] = self.drawing_pit[5][i] + discarded_tile

        return drawed_tiles

    def insert_tiles_in_column(self, tile_type, drawed_tiles, column_choice, player):
        number_of_drawed_tile = drawed_tiles

        if (player == "P1"):
            rows = self.rows_p1
            scoreboard = self.board_p1
        else:
            rows = self.rows_p2
            scoreboard = self.board_p2

        if (column_choice == 5):
            self.insert_tiles_in_penalty_column(number_of_drawed_tile, player)
            return

        for i in range(column_choice + 1):

                if (rows[column_choice][i] == 0 and number_of_drawed_tile > 0):
                    rows[column_choice][i] = tile_type + 1
                    number_of_drawed_tile = number_of_drawed_tile - 1

                #mette le rimanenti nella penality column
                self.insert_tiles_in_penalty_column(number_of_drawed_tile, player)

    def insert_tiles_in_penalty_column(self, number_of_tiles, player):

        if (player == "P1"):
            penality_row = self.penalty_row_p1
        else:
            penality_row = self.penalty_row_p2

        #se si riempie la penality column allora vanno scartate le tessere
        for i in range(7):
            if (penality_row[i] == 0 and number_of_tiles > 0):
                penality_row[i] = 1
                number_of_tiles = number_of_tiles - 1

    def calculate_score(self, player):

        # calcolo dello score
        if (player == "P1"):
            rows = self.rows_p1

        else:
            rows = self.rows_p2

        index_row = 0
        for row in rows:
            first_elem = row[0]
            completed_row = True

            for elem in row:
                if (elem != first_elem or elem == 0):
                    completed_row = False
                    break

            if (completed_row):
                # manca metodo pulisci row
                self.clear_row(index_row, player)
                partial_score = self.add_tile_to_scoreboard(first_elem, player, index_row)
                self.update_score(player, partial_score)

            index_row = index_row + 1
        # calculate penality
        self.calculate_penality(player)

    def clear_row(self, index_row, player):

        if (player == "P1"):
            rows = self.rows_p1
        else:
            rows = self.rows_p2

        for i in range(index_row + 1):
            rows[index_row][i] = 0

    def add_tile_to_scoreboard(self, tile, player, index_row):

        if (player == "P1"):
            scoreboard = self.board_p1
        else:
            scoreboard = self.board_p2

        index_column = ((tile - 1 + index_row) % 5)
        scoreboard[index_row][index_column] = 1

        # cambia nome metodi in adiacent
        score_row = self.compute_row_point(index_row, index_column, player)
        score_column = self.compute_column_point(index_row, index_column, player)

        # 1 sta per l'inserimento della piastrella
        return 1 + score_row + score_column

    def compute_row_point(self, index_row, index_column, player):
        if (player == "P1"):
            scoreboard = self.board_p1
        else:
            scoreboard = self.board_p2
        score = 0
        i = 0
        for elem in scoreboard[index_row]:
            if (i < index_column):
                if (elem):
                    score = score + 1
                else:
                    score = 0
            else:
                if (elem):
                    score = score + 1
                else:
                    break
            i = i + 1
        return score - 1

    def compute_column_point(self, index_row, index_column, player):
        if (player == "P1"):
            scoreboard = self.board_p1
        else:
            scoreboard = self.board_p2
        point = 0
        i = 0
        for row in scoreboard:

            if (i < index_row):
                if (row[index_column]):
                    point = point + 1
                else:
                    point = 0
            else:
                if (row[index_column]):
                    point = point + 1
                else:
                    break

            i = i + 1
        return point - 1

    def calculate_penality(self, player):
        if (player == "P1"):
            penality_row = self.penalty_row_p1
        else:
            penality_row = self.penalty_row_p2
        penality = 0

        for i in range(7):
            if (penality_row[i]):
                if (i < 2):
                    penality = penality - 1
                elif (i < 5):
                    penality = penality - 2
                else:
                    penality = penality - 3

        self.update_score(player, penality)

    def update_score(self, player, points):

        if (player == "P1"):
            if (self.p1_score + points > 0):

                self.p1_score = self.p1_score + points
            else:
                self.p1_score = 0
        else:
            if (self.p2_score + points > 0):
                self.p2_score = self.p2_score + points
            else:
                self.p2_score = 0

    def valid_actions(self,player):
        valid_actions = []
        for i in range(6):
            for j in range(5):
                for k in range(6):
                    if(self.valid_move(player, i, j, k)):
                        valid_actions.append([i,j,k])
        return valid_actions

    def is_turn_done(self):
        for pit in self.drawing_pit:
            for tile_type in pit:
                if(tile_type != 0):
                    self.is_done_phase = False
                    return

        self.is_done_phase = True
        return

    def is_game_done(self):
        #controlla la board p1
        if self.is_turn_done():
            for row in self.board_p1:
                completed_tiles_in_a_row = 0
                for tile in row:
                    completed_tiles_in_a_row = completed_tiles_in_a_row + tile
                if(completed_tiles_in_a_row == 5):
                    self.gameover = True
                    return

            # controlla la board p2
            for row in self.board_p2:
                completed_tiles_in_a_row = 0
                for tile in row:
                    completed_tiles_in_a_row = completed_tiles_in_a_row + tile
                if (completed_tiles_in_a_row == 5):
                    self.gameover = True
                    return

            self.gameover = False
            return
        else : return False

    def final_points(self,player):
        def row_completed_score(scoreboard):
            row_completed = 0
            for row in scoreboard:
                n_tile_in_a_row = 0
                for tile in row:
                    if(tile == 1):
                        n_tile_in_a_row = n_tile_in_a_row +1
                if(n_tile_in_a_row == 5):
                    row_completed = row_completed + 1
            return row_completed * 2
        def column_completed_score(scoreboard):
            column_completed = 0
            cumulative = [0,0,0,0,0]

            for row in scoreboard:
                cumulative = cumulative + row
            for elem in cumulative:
                if(elem == 5):
                    column_completed = column_completed + 1
            return column_completed * 5

        def tile_completed_score(scoreboard):
            tile_completed = 0
            tile_array = [0,0,0,0,0]
            for i in range(5):
                for j in range(5):
                    if(scoreboard[i][j] == 1):
                        tile_array[(i+j) % 5] = tile_array[(i+j) % 5] + 1
            for elem in tile_array:
                if(elem == 5):
                    tile_completed = tile_completed + 1
            return tile_completed *7


        if(player == "P1"):
            scoreboard = self.board_p1
            self.p1_score = self.p1_score + row_completed_score(scoreboard) + column_completed_score(scoreboard) + tile_completed_score(scoreboard)
        else:
            scoreboard = self.board_p2
            self.p2_score = self.p2_score + row_completed_score(scoreboard) + column_completed_score(scoreboard) + tile_completed_score(scoreboard)

    def print_table(self):

        print(f"P1:{self.p1_score}")
        print(self.board_p1)
        print(f"row_p1:{self.rows_p1}")
        print(f"penality:{self.penalty_row_p1}")
        print("=" * 20)
        print(f"P2:{self.p2_score}")
        print(self.board_p2)
        print(f"row_p2:{self.rows_p2}")
        print(f"penality:{self.penalty_row_p2}")
        print("=" * 20)
        print(self.drawing_pit)
        print("=" * 20)

