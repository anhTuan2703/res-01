import random
import ChessEngine

pieceScore = {"K": 5000, "Q": 100, "R": 50, "B": 30, "N": 30, "p": 10}
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 1



# picks and returns a random move
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]




# help
def findBestMoveMinMax(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove



def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    # move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, - alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:  # pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


# a positive score is good for white, a negative score is good for black
def scoreBoard(gs):
    score = 0
    if gs.checkmate:
        if gs.whiteToMove:
            score = -CHECKMATE # black wins
        else:
            score = CHECKMATE  # white wins
    elif gs.stalemate:
        score = STALEMATE
 
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
                if gs.whiteToMove:
                    if gs.inCheck():
                        score -= 9
                        print("white check")
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
                if not gs.whiteToMove:
                    if gs.inCheck():
                        score += 9
                        print(" black check")
            
    return score

