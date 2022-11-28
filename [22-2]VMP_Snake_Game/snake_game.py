# 20211060 ohseohyun

import pygame
import os
import sys
import random
from time import sleep

# 게임 스크린 전역변수
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 게임 화면 전역변수
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

# 방향 전역변수
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 색상 전역변수
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GRAY = (100, 100, 100)
          
# 뱀 객체
class Snake(object):
    def __init__(self): # 초기 함수
        self.create() #create() 실행
        self.hit = pygame.mixer.Sound('/Users/seohyunoh/Documents/python/VMP/4_Snake_Game/assets/hit.wav')
        self.hit.set_volume(0.5) # hit에 hit.wav를 저장하고 볼륨을 0,5로 조정
            

    # 뱀 생성
    def create(self):
        self.length = 2 # 뱀 길이는 2
        self.positions = [(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))] # 뱀의 위치는 스크린의 가운데
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT]) # 시작방향은 상하좌우 중 랜덤으로 하나 선택

    # 뱀 방향 조정
    def control(self, xy): 
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy

    # 뱀 이동
    def move(self):
        cur = self.positions[0] #뱀 머리
        x, y = self.direction # 방향
        new = (cur[0] + (x * GRID_SIZE)), (cur[1] + (y * GRID_SIZE)) # 그리드 사이즈 만큼 x,y 이동해주기

        # 뱀이 자기 몸통에 닿았을 경우 뱀 처음부터 다시 생성
        if new in self.positions[2:]:
            sleep(1) # 잠시 멈췄다가
            self.hit.play() # hit 효과음을 넣고
            self.create() # snake를 새로 만들어준다. 
        
        # 뱀이 게임화면을 넘어갈 경우 뱀 처음부터 다시 생성
        elif new[0] < 0 or new[0] >= SCREEN_WIDTH or \
                new[1] < 0 or new[1] >= SCREEN_HEIGHT:
            sleep(1)
            self.hit.play()
            self.create()
        
        # 뱀이 정상적으로 이동하는 경우
        else:
            self.positions.insert(0, new) # 앞으로 이동하는 느낌
            if len(self.positions) > self.length:
                self.positions.pop() # 뒤 꼬리 잘라주는 느낌

    # 뱀이 먹이를 먹을 때 호출
    def eat(self):
        self.length += 1

    # 뱀 그리기
    def draw(self, screen):
        red, green, blue = 150 / (self.length - 1), 150 / (self.length - 1), 150 # 초기 뱀 색을 150,150,150으로 지정하기
        for i, p in enumerate(self.positions): # position에 따라 R,G 값을 점점 줄여나갈 예정
            color = (red * i, green * i, blue)
            rect = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE)) #그리드 사이즈의 정사각형을 position에 그린다.
            pygame.draw.rect(screen, color, rect)


# 먹이 객체
class Feed(object):
    def __init__(self):
        self.position = (0, 0) #초기 위치 설정 
        self.color = RED # 먹이 색
        self.create() # 먹이 생성

    # 먹이 생성
    def create(self):
        x = random.randint(0, GRID_WIDTH - 1) # x를 그리드 위드-1사이의 랜덤 수 설정
        y = random.randint(0, GRID_HEIGHT - 1) # y를 그리드 위드-1사이의 랜덤 수 설정
        self.position = x * GRID_SIZE, y * GRID_SIZE # x,y를 그리드 사이즈만큼 곱한 것을 위치로 설정

    # 먹이 그리기
    def draw(self, screen):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect) # 위치에 그리드 사이즈 만큼의 정사각형 그리기

# 방해물 객체
class Obstacle(object):
    def __init__(self):
        self.position = (0, 0) #초기 위치 설정 
        self.color = GRAY # 먹이 색
        self.create() # 먹이 생성

    # 장애물 생성
    def create(self):
        x = random.randint(0, GRID_WIDTH - 1) # x를 그리드 위드-1사이의 랜덤 수 설정
        y = random.randint(0, GRID_HEIGHT - 1) # y를 그리드 위드-1사이의 랜덤 수 설정
        self.position = x * GRID_SIZE, y * GRID_SIZE  # x,y를 그리드 사이즈만큼 곱한 것을 위치로 설정

    # 장애물 그리기
    def draw(self, screen):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect) # 위치에 그리드 사이즈 만큼의 정사각형 그리기


# 게임 객체
class Game(object):
    def __init__(self):
        self.snake = Snake() #초기 snake
        self.feed = Feed() # 초기 feed
        self.obt = Obstacle() # 초기 obstacle
        self.speed = 20 # 초기 스피드
        self.pop = pygame.mixer.Sound('/Users/seohyunoh/Documents/python/VMP/4_Snake_Game/assets/pop.wav')
        self.pop.set_volume(0.5) # 먹이 먹을 떄 나는 효과음 pop에 저장, 볼륨 0.5로 조정
        # 효과음 
        

    # 게임 이벤트 처리 및 조작
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # x버튼 눌러서 끄기
                return True
            elif event.type == pygame.KEYDOWN: # 상하좌우 버튼에 따라 control 움직이기
                if event.key == pygame.K_UP:
                    self.snake.control(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.control(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.control(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.control(RIGHT)
        return False

    # 게임 로직 수행
    def run_logic(self):
        self.snake.move() # snake가 움직일때마다 
        self.check_eat(self.snake, self.feed) # 먹었는지,
        self.check_obt(self.snake, self.obt) # 장애물 닿았는지 체크
        self.speed = (20 + self.snake.length) / 4 # length에 20을 더하고 4로 나눈 값으로 스피드 조절

    # 뱀이 먹이를 먹었는지 체크
    def check_eat(self, snake, feed):
        if snake.positions[0] == feed.position: # 뱀 머리가 feed의 위치와 같으면
            snake.eat() # snake.eat 함수 실행
            feed.create() # feed.create 함수 실행 ( 먹이 재생성)
            self.obt.create() # obstacle.create 함수 실행 ( 장애물 재생성)
            self.pop.play() # 먹이 먹은 효과음

    def check_obt(self,snake,obt):
        if snake.positions[0] == obt.position: # 뱀 머리가 장애물의 위치와 같으면
            sleep(1) # 시간 잠시 지연
            snake.hit.play() # 죽었을 때 효과음
            snake.create() # 새로 뱀 만들기
            obt.create() # 장애물 만들기

    def resource_path(self, relative_path): # 상대경로
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # 게임 정보 출력
    def draw_info(self, length, speed, screen):
        if length < 10: # 총 4단계로 구분해서 길이가 10씩 올라갈떄마다 level을 올리고 배경화면을 바꿈
            bg = pygame.image.load('/Users/seohyunoh/Documents/python/VMP/4_Snake_Game/assets/grass_bg.jpg')
            level = 1
        elif length < 20: # 배경화면은 잔디 -> 돌바닥 -> 해수면 -> 모래바닥 순으로 이루어져있음
            bg = pygame.image.load('/Users/seohyunoh/Documents/python/VMP/4_Snake_Game/assets/rock.jpg')
            level = 2
        elif length < 30:
            bg = pygame.image.load('/Users/seohyunoh/Documents/python/VMP/4_Snake_Game/assets/water.jpg')
            level = 3
        else:
            bg = pygame.image.load('/Users/seohyunoh/Documents/python/VMP/4_Snake_Game/assets/sand.jpg')
            level = 4
        info = "Level : " + str(level)  + "    " + "Length: " + str(length) + "    " + "Speed: " + str(round(speed, 2))
        font_path = resource_path("assets/NanumGothicCoding-Bold.ttf")
        font = pygame.font.Font(font_path, 26)
        text_obj = font.render(info, 1, WHITE) # 흰색으로 변경 
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 10
        screen.blit(bg,(0,0)) # 배경 로드를 위한 코드
        screen.blit(text_obj, text_rect) # text 로드를 위한 코드

    # 게임 프레임 처리
    def display_frame(self, screen):
        self.draw_info(self.snake.length, self.speed, screen) #draw_info 실행하고 
        self.snake.draw(screen) # 뱀 그리기
        self.feed.draw(screen) # 먹이 그리기
        self.obt.draw(screen) # 방해물 그리기
        screen.blit(screen, (0, 0)) # 스크린 띄우기

# 리소스 경로 설정
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    # 게임 초기화 및 환경 설정
    pygame.init() # 파이게임 초기화
    pygame.mixer.init() # 믹서 초기화
    pygame.display.set_caption('Snake Game')
    pygame.mixer.music.load('/Users/seohyunoh/Documents/python/VMP/4_Snake_Game/assets/bgm.mp3')
    pygame.mixer.music.set_volume(0.7) # music을 이용해 bgm 깔아주기, 볼륨은 0.7
    pygame.mixer.music.play(-1) # loop 재생
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN) # 풀스크린으로 설정
    clock = pygame.time.Clock()
    game = Game()
    
    done = False
    while not done: # 게임 실행
        done = game.process_events() 
        game.run_logic()
        game.display_frame(screen)
        pygame.display.flip()
        clock.tick(game.speed)

    pygame.quit() # 종료


if __name__ == '__main__':
    main()
