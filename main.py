import pygame
import sys
import pyautogui
import easygui
import Ndepth
#import FullSearch
from config import *


# Initialization
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("1. praktiskais darbs")

icon = pygame.image.load('img/games.png')
pygame.display.set_icon(icon)

# Fonts and texts in game

# NewGame texts
HeadFont = pygame.font.Font('fonts/Roboto/Roboto-Black.ttf', 20)
SmallFont = pygame.font.Font('fonts/Roboto/Roboto-Black.ttf', 17)
NewGameFont = pygame.font.Font('fonts/Roboto/Roboto-Medium.ttf', 50)

NewGame = NewGameFont.render('New game', False, "White", 'Red')
NewGameRect = NewGame.get_rect(topleft=((SCREEN_W - NewGame.get_width()) / 2, 300))

Header = NewGameFont.render('Game: Nims', False, "Yellow")
HeaderRect = Header.get_rect(topleft=((SCREEN_W - Header.get_width()) / 2, 50))

ValidText = HeadFont.render('Input error', False, "White")
ValidTextRect = ValidText.get_rect(topleft=((SCREEN_W - ValidText.get_width()) / 2, 400))

ValidGameText = HeadFont.render('Input error', False, "Black")
ValidGameTextRect = ValidText.get_rect(topleft=((SCREEN_W - ValidText.get_width()) / 2, 500))

AIStep = pygame.Surface((200, 100))
AIStep.fill('Red')
AIStepRect = AIStep.get_rect(topleft=((SCREEN_W / 2 - AIStep.get_width()), 400))
AIText = SmallFont.render('First step - AI', False, "Black")
AITextRect = AIText.get_rect(topleft=(AIStepRect.x + 40, AIStepRect.y + 40))

UserStep = pygame.Surface((200, 100))
UserStep.fill('Green')
UserStepRect = UserStep.get_rect(topleft=((SCREEN_W / 2), 400))
UserText = SmallFont.render('First step - User', False, "Black")
UserTextRect = UserText.get_rect(topleft=(UserStepRect.x + 40, UserStepRect.y + 40))

stick = pygame.image.load('img/billiard.png')
stick = pygame.transform.scale(stick, (50, 50))

# Print current game condition - N and count of stick taken by each player
def printres(N, cnt1, cnt2):
    Score = SmallFont.render('Current N: ' + str(N), False, "Black")
    ScoreRect = Score.get_rect(topleft=((SCREEN_W - Score.get_width()) / 2, 130))
    screen.blit(Score, ScoreRect)
    Score = SmallFont.render('Users taken sticks: ' + str(cnt1), False, "Black")
    ScoreRect = Score.get_rect(topleft=(50, 430))
    screen.blit(Score, ScoreRect)
    Score = SmallFont.render('AI taken sticks: ' + str(cnt2), False, "Black")
    ScoreRect = Score.get_rect(topleft=(50, 450))
    screen.blit(Score, ScoreRect)

# Logical variable for drawing

IsNewGame = True
ValidBlock = False

# Initialization values

UserScore = 0
AIScore = 0
color = 'Black'

N = -1
K = -1
AIFirst = False
ShowSteps = False
UserCount = 0
AICount = 0

while True:
    screen.fill(color)
    screen.blit(Header, HeaderRect)

    # New Game screen
    if IsNewGame:
        color = 'Black'
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        # Draw
        screen.blit(NewGame, NewGameRect)
        Score = SmallFont.render('User ' + str(UserScore) + ': ' + str(AIScore) + ' AI', False, 'White')
        ScoreRect = Score.get_rect(topleft=((SCREEN_W - Score.get_width()) / 2, 130))
        screen.blit(Score, ScoreRect)
        if ShowSteps:
            screen.blit(UserStep, UserStepRect)
            screen.blit(UserText, UserTextRect)
            screen.blit(AIStep, AIStepRect)
            screen.blit(AIText, AITextRect)
        if ValidBlock:
            screen.blit(ValidText, ValidTextRect)

        # User actions
        if NewGameRect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            ShowSteps = True
            ValidBlock = False

        if (UserStepRect.collidepoint(mouse) or AIStepRect.collidepoint(mouse)) and pygame.mouse.get_pressed()[0]:
            UserCount = 0
            AICount = 0
            ShowSteps = False

            if UserStepRect.collidepoint(mouse):
                AIFirst = False
            else:
                AIFirst = True
            try:
                N = int(easygui.enterbox("Enter N - the number of sticks at the beginning:"))
                K = int(easygui.enterbox("Enter K - the number of sticks can be taken per turn"))
                if N <= 0 or K <= 0:
                    raise Exception()

                IsNewGame = False
                color = 'White'
            except ValueError:
                ValidBlock = True
            except Exception:
                ValidBlock = True
    else:
        # Game Screen

        # End game condition
        if N <= 0:
            if AIFirst:
                UserScore += 1
                pyautogui.alert("User wins")
            else:
                AIScore += 1
                pyautogui.alert("AI wins")
            IsNewGame = True
            continue

        # Vizualization

        for i in range(0, int(N / 10) + 1):
            for j in range(0, min(N - i * 10, 10)):
                screen.blit(stick, ((SCREEN_W - (50 * min(N - i * 10, 10))) / 2 + j * 50, 200 + i * 75))
        printres(N, UserCount, AICount)
        pygame.display.flip()

        # Step logic
        if AIFirst:
            curK = Ndepth.getnewK(N, K)  # Algorithm "Pārlūkošana uz priekšu pār ngājieniem"
            #curK = FullSearch.getnewK(N, K) # Alhorithm "Minimaksa" with full detour of the graph
            AICount += curK
            N -= curK
        else:
            # User step - input "K" and decrease number of the sticks
            while True:
                try:
                    if ValidBlock:
                        screen.blit(ValidGameText, ValidGameTextRect)
                        pygame.display.flip()
                    curK = int(easygui.enterbox("Ievadiet skaitli, cik serkocinu janonem [1:" + str(min(N, K)) + "]"))
                    if curK <= 0 or curK > min(N, K):
                        raise Exception()
                    ValidBlock = False
                    break
                except ValueError:
                    ValidBlock = True
                except Exception:
                    ValidBlock = True
            UserCount += curK
            N -= curK

        AIFirst = not AIFirst

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(100)
